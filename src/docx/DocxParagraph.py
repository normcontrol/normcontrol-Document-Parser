import re

from docx import Document
from lxml import etree

from src.docx._temp.Paragraph import Paragraph
from src.docx.helpers.EnumFill import EnumFill


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
         get_paragraph_format_style_for_attr: int | float Find paragraph_format.* attr, like first_line_indent, line_spacing  in parent Styles if None
         is_style_append_text(cls, paragraph, style_name: str): A method  check text is bold | italic | underline
         is_change_font_name(cls, paragraph): A method that chek changed font style in each paragraph
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

    def get_standard_paragraph(self, paragraph):
        """
        This is a function that uses the `docx` package.
        This is a function that uses the `Paragraph` package.
        Make paragraph in standard format

        :param paragraph: docx.Paragraph
        :return : Paragraph object
        """

        return Paragraph(
            text=paragraph.text,
            indent=self.get_paragraph_format_style_for_attr(paragraph, "first_line_indent"),
            lineSpacing=self.get_paragraph_format_style_for_attr(paragraph, "line_spacing"),
            fontName=self.get_font_style_for_attr(paragraph, "name"),
            textSize=self.get_font_size(paragraph),
            nochangeFontName=self.is_change_font_name(paragraph),
            nochangeTextSize=self.is_change_text_size(paragraph),
            alignment=paragraph.alignment,
            mrgrg=paragraph.paragraph_format.right_indent,
            mrglf=paragraph.paragraph_format.left_indent,
            bold=self.is_style_append_text(paragraph, "bold"),
            italics=self.is_style_append_text(paragraph, "italic"),
            underlining=self.is_style_append_text(paragraph, "underline"),
            keepLinesTogether=paragraph.paragraph_format.keep_together,
            keepWithNext=paragraph.paragraph_format.keep_with_next,
            outlineLevel=paragraph.style.font.outline
        )

    def get_font_size(self, paragraph):
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
        else:
            return round(sum(fonts_sizes) / len(fonts_sizes))

    def get_font_style_for_attr(self, paragraph, attr_name: str):
        """
        Find style.font attr_name  in any paren or child elements

        :param attr_name: str name of style attr
        :param paragraph: docx.Paragraph
        :return: list Names of attr_name values
        """
        fonts = set()
        attr = getattr(paragraph.style.font, attr_name)
        for run in paragraph.runs:
            if getattr(run.font, attr_name) is not None:
                fonts.add(getattr(run.font, attr_name))
        if attr is not None:
            fonts.add(attr)
        else:
            style = self.styles[getattr(paragraph.style, attr_name)]
            # if font.name is None try find in parents
            while getattr(style.font, attr_name) is None:
                style = style.base_style
            fonts.add(getattr(style.font, attr_name))
        return list(fonts)

    @classmethod
    def get_paragraph_format_style_for_attr(cls, paragraph, attr_name: str):
        """
        Find  | first_line_indent | line_spacing | in parent Styles if None

        !!!! IMPORTANT !!!!!
        paragraph.paragraph_format. first_line_indent return 35.4
        paragraph..style.paragraph_format. first_line_indent return 35.45

        The first_line_indent property of a paragraph in Python's python-docx
        library represents the number of points that the first line of the paragraph is indented.
        In Word, the value of this property can be set to a value with up to two decimal places,
        but when this value is returned by the python-docx library, it is rounded to the nearest integer.


        :param attr_name: str name of paragraph_format attr
        :param paragraph: docx.Paragraph
        :return: int  in pt | float
        """
        attr_paragraph = getattr(paragraph.paragraph_format, attr_name)
        if attr_paragraph is not None:
            return attr_paragraph if type(attr_paragraph) is float else attr_paragraph.pt
        attr = getattr(paragraph.style.paragraph_format, attr_name)
        if attr is None:
            current = paragraph.style
            while getattr(current.paragraph_format, attr_name) is None:
                current = current.base_style
            attr = getattr(current.paragraph_format, attr_name)
        return attr if type(attr) is float else attr.pt

    @classmethod
    def is_style_append_text(cls, paragraph, style_name: str):
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
            return EnumFill.NO_APPLY if list_styles[0] is None else EnumFill.APPLY_TO_ALL_ELEMENTS
        # if paragraph bold have mix of True|False|None
        elif {True, False}.issubset(list_styles) or {True, None}.issubset(list_styles) or {False, None}.issubset(
                list_styles):
            return EnumFill.APPLY_TO_SOME_ELEMENTS
        else:
            return EnumFill.IS_UNKNOWN

    @classmethod
    def is_change_font_name(cls, paragraph):
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

        return False if len(fonts) == 1 and len(styles) == 1 else True

    @classmethod
    def is_change_text_size(cls, paragraph):
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
