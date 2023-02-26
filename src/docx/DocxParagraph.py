"""DOCX Paragraph module

The module allows you to download a docx file and convert the properties of paragraphs to a single view

This script requires that `lxml`, `typing` , `python-docx` to be installed within the Python
environment you are running this script in.

This file can also be imported as a module and contains the following public
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

from src.docx.helpers.EnumFill import EnumFill
from src.docx.temp.Paragraph import Paragraph


class DocxParagraph:
    """
    A class make styles for paragraph in one style with OTD and PDF

    Attributes:
        path_to_document: Path to document docx
        document : docx.Document()
        styles: document.styles

    Methods:
         get_all_paragraphs_in_standard: list Paragraph in standard
         get_standard_paragraph(self, paragraph): A method that return standard paragraph
         get_font_size(self, paragraph): int
         get_font_style_for_attr: list Find style.font attr_name  in any paren or child elements
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

    @property
    def get_all_paragraphs_in_standard(self):
        """
        Get all paragraph in standard format as list

        :return: list of standard_paragraph
        """
        list_paragraphs = list()
        for paragraph in self.document.paragraphs:
            list_paragraphs.append(self.get_standard_paragraph(paragraph))
        return list_paragraphs

    def get_standard_paragraph(self, paragraph: docx.text.paragraph.Paragraph):
        """
        Make paragraph in standard format

        :param paragraph: docx.Paragraph
        :return : Paragraph object
        """

        return Paragraph(
            text=paragraph.text,
            indent=self._get_paragraph_format_style_for_attr(paragraph, "first_line_indent"),
            lineSpacing=self._get_paragraph_format_style_for_attr(paragraph, "line_spacing"),
            fontName=self._get_font_style_for_attr(paragraph, "name"),
            textSize=self._get_font_size(paragraph),
            nochangeFontName=self._is_change_font_name(paragraph),
            nochangeTextSize=self._is_change_text_size(paragraph),
            alignment=DocxParagraph.get_alignment_enum(self._get_paragraph_format_in_hierarchy(paragraph, 'alignment')),
            mrgrg=round(self._get_paragraph_format_style_for_attr(paragraph, "right_indent", "cm"), 2),
            mrglf=round(self._get_paragraph_format_style_for_attr(paragraph, "left_indent", "cm"), 2),
            mrgtop=round(self._get_paragraph_format_style_for_attr(paragraph, "space_before", "cm"), 2),
            mrgbtm=round(self._get_paragraph_format_style_for_attr(paragraph, "space_after", "cm"), 2),
            bold=self._is_style_append_text(paragraph, "bold"),
            italics=self._is_style_append_text(paragraph, "italic"),
            underlining=self._is_style_append_text(paragraph, "underline"),
            subText=self._get_run_font_style_in_hierarchy(paragraph, "subscript"),
            superText=self._get_run_font_style_in_hierarchy(paragraph, "superscript"),
            colorText=self._get_font_style_color(paragraph),
            keepLinesTogether=paragraph.paragraph_format.keep_together,
            keepWithNext=paragraph.paragraph_format.keep_with_next,
            outlineLevel=paragraph.style.font.outline,
            # noSpaceBetweenParagraphsOfSameStyle = None,
            pageBreakBefore=self._get_paragraph_format_style_for_attr(paragraph, "page_break_before")
        )

    def _get_font_size(self, paragraph: docx.text.paragraph.Paragraph):
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

    @staticmethod
    def rgb_to_hex(rgb: tuple):
        """
        Function get RGB param as tuple

        :return: str Hex-code
        """
        r, g, b = rgb
        return '#{:02x}{:02x}{:02x}'.format(r, g, b)

    def _get_font_style_color(self, paragraph: docx.text.paragraph.Paragraph) -> dict:
        """
        Function get all colors of paragraph in hex

        :param paragraph: docx.Paragraph
        :return: dict of hex color with max value {'#000000': 19, '#00b050': 1, '#5b9bd5': 1, 'max': '#000000'}
        """

        values = list()
        for run in paragraph.runs:
            if run.font.color.rgb is not None:
                value = {"count": len(run.text), "color": DocxParagraph.rgb_to_hex(run.font.color.rgb)}
            else:
                style = self.styles[paragraph.style.name]
                if style.font.color.rgb is not None:
                    value = {"count": len(run.text), "color": DocxParagraph.rgb_to_hex(style.font.color.rgb)}
                else:
                    value = {"count": len(run.text), "color": "#000000"}
            values.append(value)
        sums_by_color = {}
        for item in values:
            if item['color'] in sums_by_color:
                sums_by_color[item['color']] += item['count']
            else:
                sums_by_color[item['color']] = item['count']
        max_color = max(sums_by_color, key=lambda k: sums_by_color[k])
        sums_by_color['max'] = max_color
        return sums_by_color

    def _get_font_style_for_attr(self, paragraph: docx.text.paragraph.Paragraph, attr_name: str) -> list:
        """
        Find style.font attr_name  in any paren or child elements

        :param attr_name: str name of style attr
        :param paragraph: docx.Paragraph
        :return: list Names of attr_name values
        """

        attrs_values = set()
        attr = getattr(paragraph.style.font, attr_name)
        for run in paragraph.runs:
            if getattr(run.font, attr_name) is not None:
                attrs_values.add(getattr(run.font, attr_name))
        if attr is not None:
            attrs_values.add(attr)
        else:
            style = self.styles[getattr(paragraph.style, attr_name)]
            # if font.name is None try find in parents
            while getattr(style.font, attr_name) is None:
                style = style.base_style
            attrs_values.add(getattr(style.font, attr_name))
        return list(attrs_values)

    def _get_paragraph_format_style_for_attr(self, paragraph: docx.text.paragraph.Paragraph, attr_name: str,
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


        :param attr_name: str name of paragraph_format attr
        :param paragraph: docx.Paragraph
        :param msg: str "pt" | "cm"
        :return: int | pt | float
        """

        attr = self._get_paragraph_format_in_hierarchy(paragraph, attr_name)
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
        while style.name is None:
            style = style.base_style
        return self.styles[style.name]

    def _get_run_font_style_in_hierarchy(self, paragraph: docx.text.paragraph.Paragraph, attr_name: str) -> list:
        """
        Find docx.text.run.Font attributes
        """
        values = list()
        for run in paragraph.runs:
            if getattr(run.font, attr_name) is True:
                values.append({"count": len(run.text), "type": attr_name})
        return values

    def _get_paragraph_format_in_hierarchy(self, paragraph: docx.text.paragraph.Paragraph, attr_name: str):
        """
        Find paragraph.paragraph_format attributes

        :return: value attribute
        """
        attr = getattr(paragraph.paragraph_format, attr_name)
        if attr is None:
            style = self.__get_style_in_hierarchy(paragraph)
            while style:
                if getattr(style.paragraph_format, attr_name) is not None:
                    return getattr(style.paragraph_format, attr_name)
                style = style.base_style
        return attr

    def _is_style_append_text(self, paragraph: docx.text.paragraph.Paragraph, style_name: str) -> EnumFill:
        """
        Checks if the text is bold | italic | underline
        This is a function that uses the `docx` package.
        This is a function that uses the `EnumFill` class.

        :param style_name: str "bold" | "italic" | "underline"
        :param paragraph: docx.Document.Paragraph
        :return : EnumFill
        """
        list_styles = []
        for run in paragraph.runs:
            list_styles.append(getattr(run.font, style_name))
        # Sometime we can get [None, None] or [True, True] for 1 paragraph
        list_styles = list(set(list_styles))

        # if all paragraph  in one style
        if len(list_styles) == 1:
            return EnumFill.APPLY_TO_ALL_ELEMENTS if list_styles[0] else EnumFill.NO_APPLY
        # if paragraph bold have mix of True|False|None
        elif {True, False}.issubset(list_styles) or {True, None}.issubset(list_styles) or {False, None}.issubset(
                list_styles):
            return EnumFill.APPLY_TO_SOME_ELEMENTS
        else:
            return EnumFill.IS_UNKNOWN

    def _is_change_font_name(self, paragraph: docx.text.paragraph.Paragraph) -> bool:
        """
        This is a function that uses the `docx` package.
        This is a function that uses the `lxml` package.
        This is a function that uses the `re` package.
        Checks if the font and style names has changed within the same paragraph

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

    def _is_change_text_size(self, paragraph: docx.text.paragraph.Paragraph) -> bool:
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

    @staticmethod
    def get_alignment_enum(alignment: int) -> Union[WD_PARAGRAPH_ALIGNMENT, None]:
        """
        Get alignment by kye

        :return ENUM
        """
        alignment_map = {
            0: WD_PARAGRAPH_ALIGNMENT.LEFT,
            1: WD_PARAGRAPH_ALIGNMENT.CENTER,
            2: WD_PARAGRAPH_ALIGNMENT.RIGHT,
            3: WD_PARAGRAPH_ALIGNMENT.JUSTIFY,
        }

        return alignment_map.get(alignment, None)
