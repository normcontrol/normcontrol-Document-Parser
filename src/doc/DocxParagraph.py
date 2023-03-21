"""DOCX Paragraph module

The module allows you to download a docx file and bring
the properties of paragraphs to a single view

This script requires that `lxml`, `typing` , `python-docx`
to be installed within the Python
environment you are running this script in.

This file can also be imported as a module and
contains the following public
functions:

    * get_all_paragraphs_in_standard: list Paragraph in standard
    * get_standard_paragraph(self, paragraph): A method that return standard paragraph
"""
import re
from typing import Union

from lxml import etree

import docx.text.paragraph
from docx import Document
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.styles.style import BaseStyle
from docx.text.paragraph import Paragraph as ParagraphType

from src.helpers.enums.StylePropertyCoverage import StylePropertyCoverage
from src.classes.Paragraph import Paragraph


class DocxParagraph:
    """
    Class allows to take advantage of a file with the docx extension paragraph structure in a standard form

    Parameters:
    ----------
    path_to_document: Path to document docx
        document : docx.Document()
        styles: document.styles

    Methods:
    ----------
         get_standard_paragraph(self, paragraph): A method that return standard paragraph
         get_font_size(self, paragraph): int
         get_font_style_for_attr: list Find style.font style_attr_name  in any paren or child elements
         get_paragraph_format_style_for_attr: int | float
            Find paragraph_format.* attr, like first_line_indent, line_spacing
            in parent Styles if None
         _is_style_append_text(cls, paragraph, style_name: str):
            A method  check text is bold | italic | underline
         _is_change_font_name(cls, paragraph): A method chek changed font style in each paragraph
         get_all_paragraphs_in_standard(cls): Get all paragraph in standard format as list
    """

    def __init__(self, path):
        """

        :param path: Path to DOCX document
        """
        self.path_to_document = path
        self.document = Document(path)
        self.styles = self.document.styles

    def get_standard_paragraph(self, paragraph: ParagraphType):
        """
        Make paragraph in standard format

        :param paragraph: docx.Paragraph
        :return : Paragraph object
        """

        return Paragraph(
            _line_spacing=self._get_paragraph_format_style_for_attr(paragraph, "line_spacing"),
            _text=paragraph.text,
            _indent=self._get_paragraph_format_style_for_attr(paragraph, "first_line_indent"),
            _font_name=self._get_font_style_for_attr(paragraph, "name"),
            _text_size=self._get_font_size(paragraph),
            _alignment=self.get_paragraph_justification_type(
                self._get_paragraph_format_in_hierarchy(paragraph, 'alignment')),
            _mrgrg=round(self._get_paragraph_format_style_for_attr(paragraph, "right_indent", "cm"), 2),
            _mrglf=round(self._get_paragraph_format_style_for_attr(paragraph, "left_indent", "cm"), 2),
            _mrgtop=round(self._get_paragraph_format_style_for_attr(paragraph, "space_before", "cm"), 2),
            _mrgbtm=round(self._get_paragraph_format_style_for_attr(paragraph, "space_after", "cm"), 2),
            _bold=self._is_style_append(paragraph, "bold"),
            _italics=self._is_style_append(paragraph, "italic"),
            _underlining=self._is_style_append(paragraph, "underline"),
            _sub_text=self._get_run_font_style_in_hierarchy(paragraph, "subscript"),
            _super_text=self._get_run_font_style_in_hierarchy(paragraph, "superscript"),
            _color_text=self._get_font_style_color(paragraph),
            _page_breake_before=self._get_paragraph_format_style_for_attr(paragraph, "page_break_before"),
            _keep_lines_together=paragraph.paragraph_format.keep_together,
            _keep_with_next=paragraph.paragraph_format.keep_with_next,
            _outline_level=paragraph.style.font.outline,
            _no_change_fontname=self._is_change_font_name(paragraph),
            _no_change_text_size=self._is_change_text_size(paragraph),
        )

    def _get_font_size(self, paragraph: ParagraphType):
        """
        Get font size from paragraph
        because sometime paragraph.style.font.size.pt in not correct

        :param paragraph: paragraph: docx.Paragraph
        :return: int
        """
        p_font_style = paragraph.style.font.size.pt
        fonts_sizes = []
        for run in paragraph.runs:
            font_size = run.font.size
            if font_size is not None:
                fonts_sizes.append(font_size.pt)
        if len(fonts_sizes) == 0 and p_font_style is not None:
            return p_font_style
        return round(sum(fonts_sizes) / len(fonts_sizes))

    def rgb_to_hex(self, rgb: tuple):
        """
        Function to convert rgb to hex

        :return: str Hex-code
        """
        r, g, b = rgb
        return '#{:02x}{:02x}{:02x}'.format(r, g, b)

    def _get_font_style_color(self, paragraph: ParagraphType) -> str:
        """
        Function get all colors of paragraph in hex

        :param paragraph: docx.Paragraph
        :return: most use hex code color
        """

        values = []
        for run in paragraph.runs:
            value = {"count": len(run.text), "color": "#000"}
            if run.font.color.rgb is not None:
                value["color"] = self.rgb_to_hex(run.font.color.rgb)
            else:
                style = self.styles[paragraph.style.name]
                if style.font.color.rgb is not None:
                    value["color"] = self.rgb_to_hex(style.font.color.rgb)
            values.append(value)

        return self.__find_sum_by_attr(values, "color")

    def _get_font_style_for_attr(self, paragraph: docx.text.paragraph.Paragraph, style_attr_name: str) -> str:
        """
        Find style.font style_attr_name  in any paren or child elements

        :param style_attr_name: str name of style attr
        :param paragraph: docx.Paragraph
        :return: str more used font
        """

        attrs_values = []
        attr = getattr(paragraph.style.font, style_attr_name)
        for run in paragraph.runs:
            attr_value = getattr(run.font, style_attr_name)
            if attr_value is not None:
                attrs_values.append({"count": len(run.text), "font": attr_value})
        if attr is not None:
            attrs_values.append({"count": len(paragraph.text), "font": attr})
        else:
            style = self.styles[getattr(paragraph.style, style_attr_name)]
            # if font.name is None try find in parents
            while getattr(style.font, style_attr_name) is None:
                style = style.base_style
            attrs_values.append({"count": len(paragraph.text), "font": getattr(style.font, style_attr_name)})
        return self.__find_sum_by_attr(attrs_values, "font")

    def _get_paragraph_format_style_for_attr(self, paragraph: docx.text.paragraph.Paragraph, style_attr_name: str,
                                             msg: str = "pt") -> Union[int, float]:
        """
        Find paragraph_format attr value

        !!!! IMPORTANT !!!!!
        paragraph.paragraph_format. first_line_indent return 35.4
        paragraph..style.paragraph_format. first_line_indent return 35.45

        The first_line_indent property of a paragraph in Python's python-docx
        library represents the number of points that the first line of the paragraph is indented.
        In Word, the value of this property can be set to a value with up to two decimal places,
        but when this value is returned by the python-docx library, it is rounded to the nearest integer.


        :param style_attr_name: str name of paragraph_format attr
        :param paragraph: docx.Paragraph
        :param msg: str "pt" | "cm"
        :return: int | pt | float
        """

        attr = self._get_paragraph_format_in_hierarchy(paragraph, style_attr_name)
        if attr is None:
            return 0
        return attr if isinstance(attr, float) else getattr(attr, msg)

    def __get_style_in_hierarchy(self, paragraph) -> BaseStyle:
        """
        Find style in hierarchy

        :param paragraph: docx.Paragraph
        :return: BaseStyle
        """
        style = paragraph.style
        while (style_name := style.name) is None:
            style = style.base_style
        return self.styles[style_name]

    def _get_run_font_style_in_hierarchy(self, paragraph: docx.text.paragraph.Paragraph,
                                         style_attr_name: str) -> bool:
        """
        Find docx.text.run.Font attributes
        """
        for run in paragraph.runs:
            if getattr(run.font, style_attr_name) is True:
                return True
        return False

    def _get_paragraph_format_in_hierarchy(self, paragraph: docx.text.paragraph.Paragraph, attr_name: str):
        """
        Find paragraph.paragraph_format attributes

        :return: value attribute
        """
        attr = getattr(paragraph.paragraph_format, attr_name)
        if attr is None:
            style = self.__get_style_in_hierarchy(paragraph)
            while style:
                p_format_attr = getattr(style.paragraph_format, attr_name)
                if p_format_attr is not None:
                    return p_format_attr
                style = style.base_style
        return attr

    def _is_style_append(self, paragraph: ParagraphType, style_name: str) -> StylePropertyCoverage:
        """
        Checks if the text is bold | italic | underline
        This is a function that uses the `docx` package.
        This is a function that uses the `StylePropertyCoverage` class.

        :param style_name: str "bold" | "italic" | "underline"
        :param paragraph: docx.Document.Paragraph
        :return : StylePropertyCoverage
        """
        styles = set()
        for run in paragraph.runs:
            styles.add(getattr(run.font, style_name))

        styles = list(styles)
        style_property_coverage = StylePropertyCoverage.UNKNOWN
        undesired_subsets = [{True, False}, {True, None}, {False, None}]
        if len(styles) == 1:
            style_property_coverage = StylePropertyCoverage.FULL if styles[0] else StylePropertyCoverage.NO
        elif any(subset.issubset(styles) for subset in undesired_subsets):
            style_property_coverage = StylePropertyCoverage.PARTLY
        return style_property_coverage

    def _is_change_font_name(self, paragraph: ParagraphType) -> bool:
        """
        Checks if the font and style names has changed within the same paragraph

        This is a function that uses the `docx` package.
        This is a function that uses the `lxml` package.
        This is a function that uses the `re` package.

        :param paragraph:docx.Document.Paragraph
        :return: True | False
        """
        fonts = set()
        styles = set()

        for run in paragraph.runs:
            # find font name and style name in element
            # because sometime we can't get attr in style.font.name in run object
            string_xml = etree.tostring(run.element).decode('utf-8')
            cs_match = re.search(r'cs="([^"]+)"', string_xml)
            ascii_theme = re.search(r'w:asciiTheme="([^"]+)"', string_xml)
            if cs_match:
                cs_value = cs_match.group(1)
            # if style:font empty get asciiTheme like nameFont
            elif ascii_theme:
                cs_value = ascii_theme.group(1)
            else:
                cs_value = paragraph.style.font.name
            fonts.add(cs_value)
            if run.style.name:
                styles.add(run.style.name)

        return len(fonts) != 1 or len(styles) != 1

    def _is_change_text_size(self, paragraph: ParagraphType) -> bool:
        """
        Checks if the font size has changed within the same paragraph

        :param paragraph:
        :return: True | False
        """
        paragraph_font_size = paragraph.style.font.size
        is_changed = False
        for run in paragraph.runs:
            if run.font.name != paragraph_font_size and run.font.size is not None:
                is_changed = True
                break
        return is_changed

    def get_paragraph_justification_type(self, alignment: int) -> Union[WD_PARAGRAPH_ALIGNMENT, None]:
        """
        Get paragraph justification type by key

        :return WD_PARAGRAPH_ALIGNMENT | None
        """
        alignments = [
            WD_PARAGRAPH_ALIGNMENT.LEFT,
            WD_PARAGRAPH_ALIGNMENT.CENTER,
            WD_PARAGRAPH_ALIGNMENT.RIGHT,
            WD_PARAGRAPH_ALIGNMENT.JUSTIFY
        ]

        return alignments[alignment] if alignment < len(alignments) else None

    def __find_sum_by_attr(self, values: list, attr: str, count_field: str = "count") -> str:
        """

        @param values: [{"name_attr": "name", "count": 11}]
        @param attr: "name_attr" name
        @param count_field: "count" name
        @return: more used attr
        """
        sum = {}
        for item in values:
            if item[attr] in sum:
                sum[item[attr]] += item[count_field]
            else:
                sum[item[attr]] = item[count_field]
        sum['max'] = max(sum, key=lambda k: sum[k])

        return sum['max']
