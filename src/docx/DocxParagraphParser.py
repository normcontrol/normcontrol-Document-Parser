"""DOCX Paragraph module

The module allows you to download a docx file and bring
the properties of paragraphs to a single view

This script requires that `lxml`, `typing` , `python-docx`
to be installed within the Python
environment you are running this script in.

This file can also be imported as a module and
contains the following public
functions:

    * get_standard_paragraph(self, paragraph): A method that return standard paragraph
    * load_data_source(self, path: str):
            The method initializes the reading of the source document
    * extract_tables(self) -> list[StructuralElement]:
            The method extracts and returns a list of all the tables in the document
    * extract_pictures(self) -> list[StructuralElement]:
            The method extracts and returns a list of all the image in the document
    * extract_formulas(self) -> list[StructuralElement]:
            The method extracts and returns a list of all the formulas in the document
    * get_all_elements(self) -> UnifiedDocumentView:
            The method extracts and returns a list of all the structural elements in the document
    * extract_paragraphs(self) -> list[StructuralElement]:
            The method extracts and returns a list of all the paragraphs in the document
    * extract_lists(self) -> list[StructuralElement]
            The method extracts and returns a list of all the list in the document:
"""
import re
from typing import Union
import docx.text.paragraph
from docx import Document
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.shared import Length
from docx.styles.style import BaseStyle
from docx.text.paragraph import Paragraph as ParagraphType
from lxml import etree
from src.classes.Frame import Frame
from src.classes.Image import Image
from src.classes.Paragraph import Paragraph
from src.classes.Table import Table
from src.classes.TableCell import TableCell
from src.classes.UnifiedDocumentView import UnifiedDocumentView
from src.classes.interfaces.InformalParserInterface import InformalParserInterface
from src.classes.superclass.Parser import DefaultParser
from src.classes.superclass.StructuralElement import StructuralElement
from src.classes.word.DefaultFontStyle import DefaultFontStyle
from src.classes.word.Numbering import NumLvlStyle, AbstractNum, NumberingStyle, NumeringStyles
from src.helpers.colors import rgb_to_hex
from src.helpers.enums.AlignmentEnum import AlignmentEnum
from src.helpers.enums.StylePropertyCoverage import StylePropertyCoverage


class DocxParagraphParser(InformalParserInterface, DefaultParser):
    """
    Class extract paragraph and attributes from DOCX files

    Parameters:
    ----------
        path_to_document: str
            Path to document docx

        origin_document : docx.Document()
            Origin parser of docx document

        styles: document.styles
            All elements styles in document

        ns: dict
            Supported docx data schemas

        xml_paragraphs
            Representation of a paragraph in xml format

        Inherited from DefaultParser:
            _document: UnifiedDocumentView

            _pictures: list[Frame]

            _tables: list[Table]

            _paragraphs: list[Paragraph]

            _lists: list[List]

            _formulas: list[Formula]


    Methods:
    ----------
        get_standard_paragraph(paragraph):
            A method that return standard paragraph src.classes.Paragraph

        _get_font_size(paragraph) -> int
            Size in pt of font

        _get_font_style_color(paragraph: ParagraphType) -> str
            HEX code of color

        _get_font_style_for_attr(paragraph: docx.text.paragraph.Paragraph, style_attr_name: str) -> str
            Find style.font style_attr_name in any parent or child elements

        _get_paragraph_format_style_for_attr(self, paragraph: docx.text.paragraph.Paragraph, style_attr_name: str,
                                             format_return: str = "pt") -> Union[int, float, bool]
            Return value of attribute if set format_return in "pt" or "cm". If set "bool" check has element this
            attribute or not

        __get_style_in_hierarchy(self, paragraph): BaseStyle
            Find style in hierarchy

        _get_run_font_style_in_hierarchy(self, paragraph: docx.text.paragraph.Paragraph,
                                         style_attr_name: str) -> bool
            Find docx.text.run.Font attributes

        _get_paragraph_format_in_hierarchy(self, paragraph: docx.text.paragraph.Paragraph, attr_name: str)
            Find paragraph.paragraph_format attributes

        _is_style_append(self, paragraph: ParagraphType, style_name: str) -> stylePropertyCoverage
            Checks if the text is bold | italic | underline

        _is_change_text_size(self, paragraph: ParagraphType) -> bool
            Checks if the font size has changed within the same paragraph

        _get_paragraph_justification_type(self, alignment: int) -> Union[WD_PARAGRAPH_ALIGNMENT, None]
            Get paragraph justification type by key

        __find_most_common_attribute(self, values: list, attr: str, count_field: str = "count") -> str
            Function is used in determining the name of the font or color, if there are several of them
            in one paragraph. Since the Paragraph class expects a single value, the font name or color
            that occurs most often in the paragraph is returned.

        load_data_source(self, path: str):
            The method initializes the reading of the source document

        extract_tables(self) -> list[StructuralElement]:
            The method extracts and returns a list of all the tables in the document

        extract_pictures(self) -> list[StructuralElement]:
            The method extracts and returns a list of all the image in the document

        extract_formulas(self) -> list[StructuralElement]:
            The method extracts and returns a list of all the formulas in the document

        get_all_elements(self) -> UnifiedDocumentView:
            The method extracts and returns a list of all the elements in the document

        extract_paragraphs(self) -> list[StructuralElement]:
            The method extracts and returns a list of all the paragraphs in the document

        extract_lists(self) -> list[StructuralElement]
            The method extracts and returns a list of all the list in the document:
    """

    def __init__(self, path):
        """

        :param path: Path to DOCX document
        """
        self.path_to_document = path
        self.origin_document = Document(path)
        self.ns = self.origin_document.element.nsmap
        self.get_default_font_style()
        self.get_base_numbering_style()
        self.xml_paragraphs = self.__add_xml_attr_to_paragraph()

        self.styles = self.origin_document.styles
        self.tables = self.extract_tables()
        self.pictures = self.extract_pictures()
        self.paragraphs = self.extract_paragraphs()
        self.document = UnifiedDocumentView(self.origin_document.core_properties.author,
                                                    str(self.origin_document.core_properties.created),
                                                    None)
        self.get_all_elements()


    def get_standart_paragraph(self, paragraph: ParagraphType):
        """
        Make paragraph in standard format

        :param paragraph: docx.Paragraph
        :return : Paragraph object
        """

        standart_paragraph = Paragraph(
            _line_spacing=self._get_paragraph_format_style_for_attr(paragraph, "line_spacing"),
            _text=paragraph.text,
            _indent=round(self._get_paragraph_format_style_for_attr(paragraph, "first_line_indent"), 2),
            _font_name=self._get_font_style_for_attr(paragraph, "name"),
            _text_size=self._get_font_size(paragraph),
            _alignment=self._get_paragraph_justification_type(
                self._get_paragraph_format_in_hierarchy(paragraph, 'alignment')) if self._get_paragraph_justification_type(
                self._get_paragraph_format_in_hierarchy(paragraph, 'alignment')) is not None else 'Unknown',
            _mrgrg=round(self._get_paragraph_format_style_for_attr(paragraph, "right_indent", "cm"), 2),
            _mrglf=round(
                self._get_paragraph_format_style_for_attr(paragraph, "left_indent", "cm") +
                self._get_paragraph_format_style_for_attr(paragraph, "first_line_indent")
                if self._get_paragraph_format_style_for_attr(paragraph, "first_line_indent") < 0
                else self._get_paragraph_format_style_for_attr(paragraph, "left_indent", "cm")
                , 2),
            _mrgtop=round(self._get_paragraph_format_style_for_attr(paragraph, "space_before", "cm"), 2),
            _mrgbtm=round(self._get_paragraph_format_style_for_attr(paragraph, "space_after", "cm"), 2),
            _bold=self._is_style_append(paragraph, "bold"),
            _italics=self._is_style_append(paragraph, "italic"),
            _underlining=self._is_style_append(paragraph, "underline"),
            _sub_text=self._get_run_font_style_in_hierarchy(paragraph, "subscript"),
            _super_text=self._get_run_font_style_in_hierarchy(paragraph, "superscript"),
            _color_text=self._get_font_style_color(paragraph),
            _page_breake_before=self._get_paragraph_format_style_for_attr(paragraph, "page_break_before", "bool"),
            _keep_lines_together=self._get_paragraph_format_style_for_attr(paragraph, "keep_together", "bool"),
            _keep_with_next=self._get_paragraph_format_style_for_attr(paragraph, "keep_with_next", "bool"),
            _no_change_fontname=self._is_change_font_name(paragraph),
            _no_change_text_size=self._is_change_text_size(paragraph),
            _outline_level=paragraph.outline_level
        )
        if standart_paragraph.first_key == '':
            if paragraph.list_level is not None:
                standart_paragraph.first_key = 'listLevel1'
            if paragraph.outline_level == '0':
                standart_paragraph.first_key = 'TitleLevel1'
            if paragraph.outline_level in ['1', '2', '3', '4', '5']:
                standart_paragraph.first_key = 'TitleLevel23'
        return standart_paragraph

    @staticmethod
    def get_standart_table(table):
        """
        Make table in standard format

        :param table: docx.Table
        :return : classes.Table
        """

        return Table(_inner_text=[cell.text for row in table.rows for cell in row.cells],
                     _cells=[TableCell(_text=cell.text) for row in table.rows for cell in row.cells])

    @staticmethod
    def get_standart_frame(image):
        """
        Make image in standard format

        :param image: docx.InlineShapes
        :return : classes.Frame
        """

        return Frame(_width=image.width, _height=image.height, _anchor_type=image.type, _image=Image())


    def _get_font_size(self, paragraph: ParagraphType):
        """
        Get font size from paragraph
        because sometime paragraph.style.font.size.pt in not correct

        :param paragraph: paragraph: docx.Paragraph
        :return fonts_sizes: list of font sizes
        """
        style = paragraph.style
        p_font_style = self.get_attrib_from_base_font_style(style, 'size')
        fonts_sizes = []
        for run in paragraph.runs:
            font_size = run.font.size
            if font_size is None:
                font_size = self.get_attrib_from_base_font_style(run.style, 'size')
            if font_size is not None:
                if font_size.pt not in fonts_sizes:
                    fonts_sizes.append(font_size.pt)
        if len(fonts_sizes) == 0 and p_font_style is not None:
            fonts_sizes = [p_font_style.pt]
        if len (fonts_sizes) == 0:
            fonts_sizes = [self.origin_document.default_font_style.font_size]
        return fonts_sizes

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
                value["color"] = rgb_to_hex(run.font.color.rgb)
            else:
                style = self.styles[paragraph.style.name]
                if style.font.color.rgb is not None:
                    value["color"] = rgb_to_hex(style.font.color.rgb)
            values.append(value)

        return self.__find_most_common_attribute(values, "color")

    def _get_font_style_for_attr(self, paragraph: docx.text.paragraph.Paragraph, style_attr_name: str) -> list[str]:
        """
        Find style.font style_attr_name in any parent or child elements

        :param style_attr_name: str name of style attr
        :param paragraph: docx.Paragraph
        :return attrs_values: list of fonts
        """

        attrs_values = []
        attr = getattr(paragraph.style.font, style_attr_name)
        for run in paragraph.runs:
            attr_value = getattr(run.font, style_attr_name)
            if attr_value is not None:
                if attr_value not in attrs_values:
                    attrs_values.append(attr_value)
        if attr is not None:
            if len(attrs_values) == 0:
                attrs_values.append(attr)
        else:
            style = self.styles[getattr(paragraph.style, style_attr_name)]
            # if font.name is None try find in parents
            if style.font is not None:
                while getattr(style.font, style_attr_name) is None:
                    if style.base_style is not None:
                        style = style.base_style
                    else:
                        if len(attrs_values) == 0:
                            attrs_values.append(self.origin_document.default_font_style.font_name)
                        return attrs_values
            else:
                if len(attrs_values) == 0:
                    attrs_values.append(self.origin_document.default_font_style.font_name)
                return attrs_values
            if getattr(style.font, style_attr_name) not in attrs_values:
                attrs_values.append(getattr(style.font, style_attr_name))
        return attrs_values

    def _get_paragraph_format_style_for_attr(self, paragraph: docx.text.paragraph.Paragraph, style_attr_name: str,
                                             format_return: str = "cm") -> Union[int, float, bool]:
        """
        Find paragraph_format attr value

        !!!! IMPORTANT !!!!!
        paragraph.paragraph_format. first_line_indent return 35.4
        paragraph.style.paragraph_format. first_line_indent return 35.45

        The first_line_indent property of a paragraph in Python's python-docx
        library represents the number of points that the first line of the paragraph is indented.
        In Word, the value of this property can be set to a value with up to two decimal places,
        but when this value is returned by the python-docx library, it is rounded to the nearest integer.

        :param style_attr_name: str name of paragraph_format attr
        :param paragraph: docx.Paragraph
        :param format_return: str "pt" | "cm" | "bool"
        :return: int | float | bool
        """

        attr = self._get_paragraph_format_in_hierarchy(paragraph, style_attr_name)
        if attr is None:
            return 0 if format_return != "bool" else False
        if format_return == "bool":
            return True
        return attr if isinstance(attr, float) else getattr(attr, format_return)

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

    @staticmethod
    def _get_run_font_style_in_hierarchy(paragraph: docx.text.paragraph.Paragraph,
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
            if paragraph.list_level is not None and paragraph.num_id is not None and attr_name in ['indent', 'left_mrg', 'right_mrg']:
                num_style = self.origin_document.numbering_styles.num[paragraph.num_id]
                if int(paragraph.list_level) in num_style.override_numbering_styles.keys():
                    attr = getattr(num_style.override_numbering_styles[paragraph.list_level], attr_name)
                else:
                    attr = getattr(num_style.abstract_style.numbering_styles[paragraph.list_level], attr_name)
            else:
                attr = self.get_attrib_from_base_font_style(paragraph.style, attr_name)
        return attr

    @staticmethod
    def _is_style_append(paragraph: ParagraphType, style_name: str) -> bool:
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
        style_property_coverage = None
        # style_property_coverage = StylePropertyCoverage.UNKNOWN
        undesired_subsets = [{True, False}, {True, None}, {False, None}]
        if len(styles) == 1:
            style_property_coverage = True if styles[0] else False
        elif any(subset.issubset(styles) for subset in undesired_subsets):
            # style_property_coverage = StylePropertyCoverage.PARTLY
            style_property_coverage = True
        return style_property_coverage

    @staticmethod
    def _is_change_font_name(paragraph: ParagraphType) -> bool:
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

    @staticmethod
    def _is_change_text_size(paragraph: ParagraphType) -> bool:
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
    def _get_paragraph_justification_type(alignment: int) -> Union[str, None]:
        """
        Get paragraph justification type by key

        :return WD_PARAGRAPH_ALIGNMENT | None
        """
        alignments = [
            AlignmentEnum.LEFT,
            AlignmentEnum.CENTER,
            AlignmentEnum.RIGHT,
            AlignmentEnum.JUSTIFY
        ]
        if alignment is None:
            return None
        return alignments[alignment].value if alignment < len(alignments) else None

    @staticmethod
    def __find_most_common_attribute(values: list, attr: str, count_field: str = "count") -> str:
        """
        This function is used in determining the name of the font or color,
        if there are several of them in one paragraph.
        Since the Paragraph class expects a single value,
        the font name or color that occurs most often in the paragraph is returned.

        @param values: [{"name_attr": "name", "count": 11}]
        @param attr: "name_attr" name
        @param count_field: "count" name
        @return: more used attr
        """
        sum_repeat = {}
        for item in values:
            if item[attr] in sum_repeat:
                sum_repeat[item[attr]] += item[count_field]
            else:
                sum_repeat[item[attr]] = item[count_field]
        if len(sum_repeat) < 1:
            return None
        sum_repeat['max'] = max(sum_repeat, key=lambda k: sum_repeat[k])
        return sum_repeat['max']

    def extract_tables(self) -> list[StructuralElement]:
        """
        Extracts all table objects from the document and stores them as a class parameter

        :return list_of_tables: list[StructuralElement]
        """

        list_of_tables = []
        for table in self.origin_document.tables:
            list_of_tables.append(self.get_standart_table(table))
        return list_of_tables

    def extract_pictures(self) -> list[StructuralElement]:
        """
        extracts all objects drawings from the document and saves them as a class parameter

        :return list_of_image: list[StructuralElement]
        """

        list_of_image = []
        for image in self.origin_document.inline_shapes:
            list_of_image.append(self.get_standart_frame(image))
        return list_of_image

    def extract_formulas(self) -> list[StructuralElement]:
        """
        Extracts all formula objects from the document and stores them as a class parameter
        """

        pass

    def get_all_elements(self) -> UnifiedDocumentView:
        """
        Extracts all structural elements from the document, preserving the correct sequence of their presentation, and
         stores them as a class parameter

        :return: document: UnifiedDocumentView
        """
        if len(self.document.content) != 0:
            return self.document
        list_of_consecutive_elements = self.__get_xml_consecutive_content()
        list_of_consecutive_elements = self.__get_all_xml_elements(list_of_consecutive_elements)
        for i, element in enumerate(list_of_consecutive_elements):
            self.document.add_content(i, element)
        return self.document

    def extract_paragraphs(self) -> list[StructuralElement]:
        """
        extracts all paragraph objects from the document and stores them as a class parameter
        """

        list_of_paragraphs = []
        for paragraph in self.xml_paragraphs:
            list_of_paragraphs.append(self.get_standart_paragraph(paragraph))
        return list_of_paragraphs

    def extract_lists(self) -> list[StructuralElement]:
        """
        extracts all enumeration objects from the document and stores them as a class parameter
        """

        pass

    def __get_all_xml_elements(self, list_of_consecutive_elements):
        """
        Builds all objects according to their sequence

        :param list_of_consecutive_elements: dict[]
        :return list_of_element_with_attr: list[StructuralElement]
        """

        list_of_element_with_attr = []
        for element in list_of_consecutive_elements.values():
            if element['type'] == 'paragraph':
                for paragraph in self.xml_paragraphs:
                    if element['id'] == paragraph.id:
                        list_of_element_with_attr.append(self.get_standart_paragraph(paragraph))
                        break
            if element['type'] == 'table':
                list_of_element_with_attr.append(self.get_standart_table(self.origin_document.tables[element['id']-1]))
        return list_of_element_with_attr

    def __get_xml_consecutive_content(self):
        """
        Selects a sequence of elements from xml

        :return list_of_consecutive_elements: dict[int,dict]
        """

        elements = self.origin_document.element.find('.//w:body', self.ns)
        list_of_consecutive_elements = {}
        i = 1
        table_id = 1
        for element in elements:
            if element.tag == f'{{{self.ns["w"]}}}p':
                attrib = {'type': 'paragraph'}
                for key, value in element.attrib.items():
                    if 'paraId' in key:
                        attrib['id'] = value
                list_of_consecutive_elements[i] = attrib
                i += 1
            if element.tag == f'{{{self.ns["w"]}}}tbl':
                if list_of_consecutive_elements[i - 1]['type'] == 'paragraph':
                    attrib = {'type': 'table', 'prev_id': list_of_consecutive_elements[i - 1]['id'], 'id': table_id}
                    table_id = + 1
                else:
                    attrib = {'type': 'table', 'prev_id': list_of_consecutive_elements[i - 1]['prev_id'],
                              'id': table_id}
                    table_id = + 1
                list_of_consecutive_elements[i] = attrib
                i += 1
        return list_of_consecutive_elements

    def __add_xml_attr_to_paragraph(self):
        """
        Selects additional paragraph attributes from xml

        :return paragraphs: list[docx.Paragraph]
        """

        paragraphs = []
        for paragraph in self.origin_document.paragraphs:
            style = paragraph.style
            numprs = paragraph.paragraph_format.element.findall('.//w:numPr', self.ns)
            if len(numprs) > 0:
                for key, value in numprs[0].findall('.//w:ilvl', self.ns)[0].attrib.items():
                    if 'val' in key:
                        paragraph.list_level = value
                        break
                for key, value in numprs[0].findall('.//w:numId', self.ns)[0].attrib.items():
                    if 'val' in key:
                        paragraph.num_id = value
                        break
            else:
                paragraph.list_level = None
                paragraph.num_id = None
            outline_level = paragraph.paragraph_format.element.findall('.//w:outlineLvl', self.ns)
            if len(outline_level) > 0:
                for key, value in outline_level[0].attrib.items():
                    if 'val' in key:
                        paragraph.outline_level = value
                        break
            else:
                outline_level = style.element.findall('.//w:outlineLvl', self.ns)
                while len(outline_level) < 1:
                    if style.base_style is not None:
                        outline_level = style.base_style.element.findall('.//w:outlineLvl', self.ns)
                    else:
                        break
                if len(outline_level) > 0:
                    for key, value in outline_level[0].attrib.items():
                        if 'val' in key:
                            paragraph.outline_level = value
                            break
                else:
                    paragraph.outline_level = None
            for key, value in paragraph.paragraph_format.element.attrib.items():
                if 'paraId' in key:
                    paragraph.id = value
            paragraphs.append(paragraph)
        return paragraphs

    def get_default_font_style(self):
        for fonts in self.origin_document.styles.element.xpath("./w:docDefaults/w:rPrDefault/w:rPr"):
            self.origin_document.default_font_style = DefaultFontStyle(fonts.rFonts.ascii, fonts.sz.val.pt if fonts.sz.val else None)

    @staticmethod
    def get_attrib_from_base_font_style(style, attrib_name):
        p_font_style = None
        while style is not None:
            if getattr(style.font, attrib_name, None) is not None:
                p_font_style = getattr(style.font, attrib_name, None)
                break
            else:
                if style.base_style is not None:
                    style = style.base_style
                else:
                    break
        return p_font_style

    def get_base_numbering_style(self):
        abstracts = {}
        for abstract_num in self.origin_document.part.numbering_part.element.xpath("/w:numbering/w:abstractNum"):
            if f'{{{self.ns["w"]}}}abstractNumId' in abstract_num.attrib.keys():
                abstract_num_id = int(abstract_num.attrib[f'{{{self.ns["w"]}}}abstractNumId'])
                numbering_styles = []
                for num_level in abstract_num.xpath("w:lvl", namespaces=self.ns):
                    if f'{{{self.ns["w"]}}}ilvl' in num_level.attrib.keys():
                        ilvl = int(num_level.attrib[f'{{{self.ns["w"]}}}ilvl'])

                        # Необходимо дополнить чтобы выделялись и остальные свойства

                        ppr = num_level.xpath("w:pPr", namespaces=self.ns)[0]
                        left_mrg = ppr.ind_left
                        right_mrg = ppr.ind_right
                        indent = ppr.first_line_indent
                        numbering_styles.append(NumLvlStyle(ilvl, left_mrg, right_mrg, indent))
                    else:
                        raise Exception('Ошибка в стиле уровня перечисления : не имеет ilvl значения')
                abstracts[abstract_num_id] = AbstractNum(abstract_num_id, numbering_styles)
            else:
                raise Exception('Ошибка в абстрактном стиле перечисление : не имеет id')

        nums = {}
        for num in self.origin_document.part.numbering_part.element.xpath("/w:numbering/w:num"):
            num_id = num.numId
            abstract_style = abstracts[num.abstractNumId.val]
            numbering_styles = {}
            for ovverride in num.xpath("w:lvlOverride/w:lvl"):
                ilvl = ovverride.attrib[f'{{{self.ns["w"]}}}ilvl']
                for num_level in num.xpath("w:lvl", namespaces=self.ns):
                    if f'{{{self.ns["w"]}}}ilvl' in num_level.attrib.keys():
                        lvl = num_level.attrib[f'{{{self.ns["w"]}}}ilvl']
                        # Необходимо дополнить чтобы выделялись и остальные свойства
                        ppr = num_level.xpath("w:pPr", namespaces=self.ns)[0]
                        left_mrg = ppr.ind_left
                        right_mrg = ppr.ind_right
                        indent = ppr.first_line_indent
                        numbering_styles[ilvl] = NumLvlStyle(lvl, left_mrg, right_mrg, indent)
                    else:
                        raise Exception('Ошибка в стиле уровня перечисления : не имеет ilvl значения')
            nums[num_id] = NumberingStyle(num_id,abstract_style, numbering_styles)

        self.origin_document.numbering_styles = NumeringStyles(num=nums, abstract_num=abstracts)


