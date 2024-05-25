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
import logging
import zipfile
import traceback
import xml.etree.ElementTree as ET
from typing import Union, Any, Dict
from xml.etree.ElementTree import Element
import docx.text.paragraph
from docx import Document
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT, WD_LINE_SPACING
from docx.oxml import parse_xml
from docx.shared import Pt
from docx.text.paragraph import Paragraph as ParagraphType
from src.classes.Frame import Frame
from src.classes.Image import Image
from src.classes.List import List
from src.classes.Paragraph import Paragraph
from src.classes.Table import Table
from src.classes.TableCell import TableCell
from src.classes.UnifiedDocumentView import UnifiedDocumentView
from src.classes.superclass.Parser import DefaultParser
from src.classes.superclass.StructuralElement import StructuralElement
from src.classes.word.DefaultFontStyle import DefaultFontStyle
from src.classes.word.DefaultFormatStyle import DefaultFormatStyle
from src.classes.word.Numbering import NumLvlStyle, AbstractNum, NumberingStyle, NumeringStyles
from src.docx.exceptions import *
from src.helpers.colors import rgb_to_hex
from src.helpers.enums.AlignmentEnum import AlignmentEnum
from src.helpers.enums.TableAlignmentEnum import TableAlignmentEnum
from src.helpers.enums.StylePropertyCoverage import StylePropertyCoverage
from src.helpers.utils import check_for_key_and_return_value, check_for_none, get_line_spacing
from xml.etree.ElementTree import ElementTree


class DocxParagraphParser(DefaultParser):
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
        logging.basicConfig(level=logging.INFO)
        self.path_to_document = path
        self.origin_document = Document(path)
        self.ns = self.origin_document.element.nsmap
        self.get_default_font_style()
        self.get_default_format_style()
        self.get_base_numbering_styles()
        self.xml_paragraphs = self.__add_xml_attr_to_paragraph(self.origin_document.paragraphs, self.ns)
        self.styles = self.origin_document.styles
        self.tables = self.extract_tables()
        self.pictures = self.extract_pictures()
        self.paragraphs = self.extract_paragraphs()
        self.document = self.get_all_elements()

    def get_standart_paragraph(self, paragraph: ParagraphType):
        """
        Make paragraph in standard format

        :param paragraph: docx.ParagraphType
        :return : Paragraph object
        """
        PRECISION = 2

        common_attributes = {
            "_line_spacing": self._get_paragraph_format_style_for_attr(paragraph, "line_spacing"),
            "_text": paragraph.text,
            "_indent": self._get_paragraph_format_style_for_attr(paragraph, "first_line_indent", "cm"),
            "_font_name": self._get_font_style_for_attr(paragraph, "name"),
            "_text_size": [value.pt if value is not None else None for value in
                           self._get_font_style_for_attr(paragraph, 'size')],
            "_alignment": self._get_paragraph_justification_type(
                self._get_paragraph_format_in_hierarchy(paragraph, 'alignment')),
            "_mrgrg": round(self._get_paragraph_format_style_for_attr(paragraph, "right_indent", "cm"), PRECISION),
            "_mrglf": round(
                self._get_paragraph_format_style_for_attr(paragraph, "left_indent", "cm") +
                self._get_paragraph_format_style_for_attr(paragraph, "first_line_indent")
                if self._get_paragraph_format_style_for_attr(paragraph, "first_line_indent") < 0
                else self._get_paragraph_format_style_for_attr(paragraph, "left_indent", "cm")
                , PRECISION),
            "_mrgtop": round(self._get_paragraph_format_style_for_attr(paragraph, "space_before", "cm"), PRECISION),
            "_mrgbtm": round(self._get_paragraph_format_style_for_attr(paragraph, "space_after", "cm"), PRECISION),
            "_bold": self.check_property_coverage(self._get_font_style_for_attr(paragraph, "bold")),
            "_italics": self.check_property_coverage(self._get_font_style_for_attr(paragraph, "italic")),
            "_underlining": self.check_property_coverage(self._get_font_style_for_attr(paragraph, "underline")),
            "_sub_text": self._get_run_font_style_in_hierarchy(paragraph, "subscript"),
            "_super_text": self._get_run_font_style_in_hierarchy(paragraph, "superscript"),
            "_color_text": [rgb_to_hex(value) for value in self._get_font_style_color(paragraph)],
            "_page_breake_before": self._get_paragraph_format_style_for_attr(paragraph, "page_break_before", "bool"),
            "_keep_lines_together": self._get_paragraph_format_style_for_attr(paragraph, "keep_together", "bool"),
            "_keep_with_next": self._get_paragraph_format_style_for_attr(paragraph, "keep_with_next", "bool"),
            "_outline_level": paragraph.outline_level
        }
        if paragraph.list_level is not None:
            standart_paragraph = List(
                level=paragraph.list_level,
                **common_attributes
            )
        else:
            standart_paragraph = Paragraph(
                **common_attributes
            )
            standart_paragraph.no_change_fontname = self._is_change_font_name(standart_paragraph)
            standart_paragraph.no_change_text_size = self._is_change_text_size(standart_paragraph)
        if standart_paragraph.first_key == '':
            if paragraph.list_level is not None:
                standart_paragraph.first_key = 'listLevel1'
            if paragraph.outline_level == '0':
                standart_paragraph.first_key = 'TitleLevel1'
            if paragraph.outline_level in ['1', '2', '3', '4', '5']:
                standart_paragraph.first_key = 'TitleLevel23'
        return standart_paragraph

    @staticmethod
    def check_property_coverage(attr: list):
        if len(attr) > 1:
            return StylePropertyCoverage.PARTLY
        elif len(attr) == 0:
            return StylePropertyCoverage.UNKNOWN
        else:
            match attr[0]:
                case True:
                    return StylePropertyCoverage.FULL
                case False | None:
                    return StylePropertyCoverage.NO
        return StylePropertyCoverage.UNKNOWN

    @staticmethod
    def get_standart_table(table):
        """
        Make table in standard format

        :param table: docx.Table
        :return : classes.Table
        """
        return Table(_inner_text=[cell.text for row in table.rows for cell in row.cells],
                     _cells=[[TableCell(_text=cell.text) for cell in row.cells] for row in table.rows])

    @staticmethod
    def get_table_attributes(table: Element) -> Dict[str, Any]:
        ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

        # Probably need fix (I'm not sure about tags)
        indent = table.find('.//w:tblPr//w:tblInd', ns)
        line_spacing = table.find('.//w:tblPr//w:spacing', ns)
        alignment = table.find('.//w:tblPr//w:jc', ns)
        mrgrg = table.find('.//w:tblPr//w:tblCellMar//w:right', ns)
        mrglf = table.find('.//w:tblPr//w:tblCellMar//w:left', ns)
        mrgtop = table.find('.//w:tblPr//w:tblCellMar//w:top', ns)
        mrgbtm = table.find('.//w:tblPr//w:tblCellMar//w:bottom', ns)
        page_break_before = table.find('.//w:tr//w:tc//w:p//w:r//w:lastRenderedPageBreak', ns)
        keep_lines_together = table.find('.//w:tblPr//w:keepLines', ns)
        keep_with_next = table.find('.//w:tblPr//w:keepNext', ns)

        return {
            '_indent': 0 if indent is None else float(indent.get(f'{{{ns["w"]}}}w')),
            '_line_spacing': 0 if line_spacing is None else float(line_spacing.get(f'{{{ns["w"]}}}line')),
            '_alignment': TableAlignmentEnum.LEFT if alignment is None else TableAlignmentEnum[alignment.get(f'{{{ns["w"]}}}val')],
            '_mrgrg': 0 if mrgrg is None else float(mrgrg.get(f'{{{ns["w"]}}}w')),
            '_mrglf': 0 if mrglf is None else float(mrglf.get(f'{{{ns["w"]}}}w')),
            '_mrgtop': 0 if mrgtop is None else float(mrgtop.get(f'{{{ns["w"]}}}w')),
            '_mrgbtm': 0 if mrgbtm is None else float(mrgbtm.get(f'{{{ns["w"]}}}w')),
            '_page_breake_before': False if page_break_before is None else True,
            '_keep_lines_together': False if keep_lines_together is None else True,
            '_keep_with_next': False if keep_with_next is None else True
        }

    @staticmethod
    def get_standart_frame(image):
        """
        Make image in standard format

        :param image: docx.InlineShapes
        :return : classes.Frame
        """

        return Frame(_width=image.width, _height=image.height, _anchor_type=image.type, _image=Image())

    def _get_font_style_color(self, paragraph: ParagraphType) -> list[str]:
        """
        Function get all colors of paragraph in hex

        :param paragraph: docx.Paragraph
        :return: most use hex code color
        """
        attrs_values = set()
        attr = getattr(paragraph.style.font, 'color', None)
        if getattr(attr, 'rgb', None) is None:
            attr = self.get_attrib_from_base_style(paragraph.style, 'font', 'color')

        for run in paragraph.runs:
            run_attrs = getattr(run.font, 'color', None)
            if getattr(run_attrs, 'rgb', None) is None:
                run_attrs = self.get_attrib_from_base_style(run.font, 'font', 'color')
            if getattr(run_attrs, 'rgb', None) is not None:
                attrs_values.add(run_attrs.rgb)
            else:
                if getattr(attr, 'rgb', None) is not None:
                    attrs_values.add(attr.rgb)
                else:
                    attrs_values.add(getattr(self.origin_document.default_font_style, 'color', None))
        return list(attrs_values)

    def _get_font_style_for_attr(self, paragraph: docx.text.paragraph.Paragraph, style_attr_name: str) -> list:
        """
        Find style.font style_attr_name in any parent or child elements

        :param style_attr_name: str name of style attr
        :param paragraph: docx.Paragraph
        :return attrs_values: list of fonts
        """

        attrs_values = set()
        attr = getattr(paragraph.style.font, style_attr_name, None)
        if attr is None:
            attr = self.get_attrib_from_base_style(paragraph.style, 'font', style_attr_name)

        for run in paragraph.runs:
            run_attrs = getattr(run.font, style_attr_name, None)
            if run_attrs is None and style_attr_name == 'name':
                rPr = run.font.element.rPr
                if rPr is not None:
                    rFonts = rPr.rFonts
                    if rFonts is not None:
                        if f'{{{self.ns["w"]}}}asciiTheme' in rFonts.keys():
                            if 'minorHAnsi' in rFonts.values():
                                run_attrs = self.origin_document.default_font_style.minorHAnsi
                            if 'majorHAnsi' in rFonts.values():
                                run_attrs = self.origin_document.default_font_style.majorHAnsi
            if run_attrs is None:
                run_attrs = self.get_attrib_from_base_style(run.style, 'font', style_attr_name)
            if run_attrs is not None:
                attrs_values.add(run_attrs)
            else:
                if attr is not None:
                    attrs_values.add(attr)
                else:
                    attrs_values.add(getattr(self.origin_document.default_font_style, style_attr_name, None))

        return list(attrs_values)

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

    @staticmethod
    def _get_run_font_style_in_hierarchy(paragraph: docx.text.paragraph.Paragraph,
                                         style_attr_name: str) -> bool:
        """
        Find docx.text.run.Font attributes
        """
        for run in paragraph.runs:
            attr = getattr(run.font, style_attr_name)
            if attr is None:
                attr = DocxParagraphParser.get_attrib_from_base_style(run.style, 'font', style_attr_name)
            if attr:
                return attr
        return False

    def _get_paragraph_format_in_hierarchy(self, paragraph: docx.text.paragraph.Paragraph, attr_name: str):
        """
        Find paragraph.paragraph_format attributes

        :return: value attribute
        """
        try:
            attr = getattr(paragraph.paragraph_format, attr_name, None)
            number_attrs = ['first_line_indent', 'left_indent', 'right_indent']
            if attr is None:
                if paragraph.list_level is not None and paragraph.num_id is not None and attr_name in number_attrs:
                    num_style = self.origin_document.numbering_styles.num[int(paragraph.num_id)]
                    if int(paragraph.list_level) in num_style.override_numbering_styles.keys():
                        attr = getattr(num_style.override_numbering_styles[int(paragraph.list_level)], attr_name, None)
                    else:
                        attr = getattr(num_style.abstract_style.numbering_styles[int(paragraph.list_level)], attr_name, None)
                else:
                    attr = self.get_attrib_from_base_style(paragraph.style, 'paragraph_format', attr_name)
            if attr is None:
                attr = getattr(self.origin_document.default_format_style, attr_name, None)
            return attr
        except KeyError as ke:
            # traceback.print_exc()
            logging.warning(f'Стиля нумерации с таким id ({ke}) не существует')
        except Exception as e:
            # traceback.print_exc()
            print(e)
            return None

    @staticmethod
    def _is_change_font_name(paragraph: Paragraph) -> bool:
        """
        Checks if the font and style names has changed within the same paragraph

        This is a function that uses the `docx` package.
        This is a function that uses the `lxml` package.
        This is a function that uses the `re` package.

        :param paragraph:docx.Document.Paragraph
        :return: True | False
        """
        if len(paragraph.font_name) <= 1:
            return True
        else:
            return False

    @staticmethod
    def _is_change_text_size(paragraph: Paragraph) -> bool:
        """
        Checks if the font size has changed within the same paragraph

        :param paragraph:
        :return: True | False
        """
        if len(paragraph.text_size) <= 1:
            return True
        else:
            return False

    @staticmethod
    def _get_paragraph_justification_type(alignment: int) -> Union[AlignmentEnum, None]:
        """
        Get paragraph justification type by key

        :return WD_PARAGRAPH_ALIGNMENT | None
        """
        try:
            alignments = {
                0: AlignmentEnum.LEFT,
                1: AlignmentEnum.CENTER,
                2: AlignmentEnum.RIGHT,
                3: AlignmentEnum.JUSTIFY,
                4: AlignmentEnum.DISTRIBUTE,
                5: AlignmentEnum.JUSTIFY,
                7: AlignmentEnum.JUSTIFY,
                8: AlignmentEnum.JUSTIFY,
                9: AlignmentEnum.JUSTIFY
            }
            if alignment is None:
                return AlignmentEnum.LEFT
            return alignments[alignment]
        except Exception as e:
#             traceback.print_exc()
            print(e)
            raise e

    def extract_tables(self) -> list[Table]:
        """
        Extracts all table objects from the document and stores them as a class parameter

        :return list_of_tables: list[StructuralElement]
        """
        with zipfile.ZipFile(self.path_to_document, 'r') as zr:
            with zr.open('word/document.xml') as xml_doc:
                root = ET.parse(xml_doc).getroot()
                namespaces = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
                elem_tables = root.findall('.//w:tbl', namespaces)
                extracted_tables = []
                for elem in elem_tables:
                    table_data = []
                    rows = elem.findall('.//w:tr', namespaces)
                    for row in rows:
                        row_data = []
                        for cell in row.findall('.//w:tc', namespaces):
                            row_data.append(TableCell(
                                _text=''.join(cell.find('.//w:t', namespaces).itertext())
                            ))
                        table_data.append(row_data)
                    extracted_tables.append(Table(
                        _cells=table_data,
                        _inner_text=[cell.text for row in table_data for cell in row],
                        **self.get_table_attributes(elem)
                    ))
                return extracted_tables




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
        document = UnifiedDocumentView(self.origin_document.core_properties.author,
                                       str(self.origin_document.core_properties.created))
        list_of_consecutive_elements = self.__get_xml_consecutive_content()
        list_of_consecutive_elements = self.__get_all_xml_elements(list_of_consecutive_elements)
        for i, element in enumerate(list_of_consecutive_elements):
            document.add_content(i, element)
        return document

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
                list_of_element_with_attr.append(
                    self.get_standart_table(self.origin_document.tables[element['id'] - 1]))
        return list_of_element_with_attr

    def __get_xml_consecutive_content(self):
        """
        Selects a sequence of elements from xml

        :return list_of_consecutive_elements: dict[int,dict]
        """
        try:
            elements = self.origin_document.element.find('.//w:body', self.ns)
            list_of_consecutive_elements = {}
            i = 1
            table_id = 1
            para_id = 1
            for element in elements:
                if element.tag == f'{{{self.ns["w"]}}}p':
                    attrib = {'type': 'paragraph'}
                    for key, value in element.attrib.items():
                        if 'paraId' in key:
                            attrib['id'] = value
                            break
                    if 'id' not in attrib.keys():
                        attrib['id'] = para_id
                        para_id += 1
                if element.tag == f'{{{self.ns["w"]}}}tbl':
                    if len(list_of_consecutive_elements) == 0:
                        attrib = {'type': 'table', 'prev_id': table_id,
                                      'id': table_id}
                    else:
                        if list_of_consecutive_elements[i - 1]['type'] == 'paragraph':
                            attrib = {'type': 'table', 'prev_id': list_of_consecutive_elements[i - 1]['id'], 'id': table_id}
                        else:
                            attrib = {'type': 'table', 'prev_id': list_of_consecutive_elements[i - 1]['prev_id'],
                                      'id': table_id}
                    table_id = + 1
                list_of_consecutive_elements[i] = attrib
                i += 1
            return list_of_consecutive_elements
        except Exception as e:
            #  traceback.print_exc()
            print(e)

    @staticmethod
    def __add_xml_attr_to_paragraph(paragraphs, ns):
        def get_paragraph_id(paragraph):
            for key, value in paragraph.paragraph_format.element.attrib.items():
                if 'paraId' in key:
                    return value
            return None

        def get_ilvl(numprs, ns):
            ilvls = numprs.findall('.//w:ilvl', ns)[0]
            if ilvls > 0:
                for key, value in ilvls.attrib.items():
                    if 'val' in key:
                        return value
            return None

        def get_numId(numprs, ns):
            numIds = numprs.findall('.//w:ilvl', ns)[0]
            if numIds > 0:
                for key, value in numIds.attrib.items():
                    if 'val' in key:
                        return value
            return None

        def get_outline_lvl(outline):
            for key, value in outline.attrib.items():
                if 'val' in key:
                    return value
            return None

        def get_outline_lvl_in_style(paragraph, ns):
            try:
                outline = paragraph.paragraph_format.element.findall('.//w:outlineLvl', ns)
                if len(outline) > 0:
                    return get_outline_lvl(outline[0])
                else:
                    style = paragraph.style
                    outline = style.element.findall('.//w:outlineLvl', ns)
                    while len(outline) < 1:
                        if style.base_style is not None:
                            outline = style.base_style.element.findall('.//w:outlineLvl', ns)
                            style = style.base_style
                        else:
                            break
                    if len(outline) > 0:
                        return get_outline_lvl(outline[0])
                    else:
                        return None
            except Exception as e:
#                 traceback.print_exc()
                print(e)
                return None

        """
        Selects additional paragraph attributes from xml

        :return paragraphs: list[docx.Paragraph]
        """
        xml_paragraphs = []
        para_id = 1
        for num, paragraph in enumerate(paragraphs):
            paragraph.id = get_paragraph_id(paragraph)
            if paragraph.id is None:
                paragraph.id = para_id
                para_id += 1
            numprs = paragraph.paragraph_format.element.findall('.//w:numPr', ns)
            if len(numprs) > 0:
                list_level = getattr(numprs[0],'ilvl')
                paragraph.list_level = list_level.val if list_level is not None else None
                num_id = getattr(numprs[0],'numId')
                paragraph.num_id = num_id.val if num_id is not None else None
            else:
                paragraph.list_level = None
                paragraph.num_id = None
            paragraph.outline_level = get_outline_lvl_in_style(paragraph, ns)
            xml_paragraphs.append(paragraph)
        logging.info("Special attributes was added to paragraph")
        return xml_paragraphs

    def get_default_font_style(self):
        try:
            def get_theme_font_style(document_part):
                THEME_PATH = "/word/theme/"
                minorHAnsi = None
                majorHAnsi = None
                for part in document_part:
                    if part.partname.startswith(THEME_PATH):
                        theme = parse_xml(part.blob)
                        for minor_font in theme.xpath("//a:minorFont", namespaces=theme.nsmap):
                            for typeface in minor_font.xpath("./a:latin/@typeface", namespaces=theme.nsmap):
                                minorHAnsi = typeface

                        for major_font in theme.xpath("//a:majorFont", namespaces=theme.nsmap):
                            for typeface in major_font.xpath("./a:latin/@typeface", namespaces=theme.nsmap):
                                majorHAnsi = typeface
                        return minorHAnsi, majorHAnsi

            default_font_style = self.origin_document.styles.element.xpath("./w:docDefaults/w:rPrDefault/w:rPr")
            if default_font_style:
                default_font_style = default_font_style[0]
                self.origin_document.default_font_style = DefaultFontStyle(name=default_font_style.rFonts.ascii,
                                                                           size=getattr(default_font_style.sz, 'val',
                                                                                        None),
                                                                           color=getattr(default_font_style.color,
                                                                                         'rgb', (0, 0, 0)))
                minorHAnsi, majorHAnsi = get_theme_font_style(self.origin_document.part.package.parts)
                self.origin_document.default_font_style.minorHAnsi = minorHAnsi
                self.origin_document.default_font_style.majorHAnsi = majorHAnsi
                logging.info("Default font styles were extracted full")
            else:
                self.origin_document.default_font_style = DefaultFontStyle()
#                 traceback.print_exc()
                logging.info("Default font styles were extracted empty")
        except Exception as e:
#             traceback.print_exc()
            logging.error(f'Error occurred while getting default font style: {str(e)}')
            self.origin_document.default_font_style = DefaultFontStyle()

    def get_default_format_style(self):
        try:
            default_format_style = self.origin_document.styles.element.xpath("./w:docDefaults/w:pPrDefault/w:pPr")
            if default_format_style:
                d = default_format_style[0]
                self.origin_document.default_format_style = DefaultFormatStyle(
                    d.jc_val if d.jc_val is not None else WD_PARAGRAPH_ALIGNMENT.LEFT,
                    get_line_spacing(d.spacing_line,
                                     d.spacing_lineRule),
                    getattr(d.ind_left, 'cm', None),
                    getattr(d.ind_right, 'cm', None),
                    getattr(d.spacing_after, 'pt', None),
                    getattr(d.spacing_before, 'pt', None),
                    d.keepLines, d.keepNext,
                    d.pageBreakBefore,
                    getattr(d.first_line_indent, 'cm', None))
                logging.info("Default format styles were extracted")
            else:
                self.origin_document.default_format_style = DefaultFormatStyle()
                logging.info("Default format styles were extracted empty")
        except Exception as e:
#             traceback.print_exc()
            logging.error(e)

    @staticmethod
    def get_attrib_from_base_style(style, tag_name, attrib_name):
        try:
            p_font_attr = None
            while style is not None:
                tag = getattr(style, tag_name, None)
                if tag is None:
                    break
                if getattr(tag, attrib_name, None) is not None:
                    p_font_attr = getattr(tag, attrib_name, None)
                    break
                else:
                    if style.base_style is not None:
                        style = style.base_style
                    else:
                        break
            return p_font_attr
        except Exception as e:
            print(e)
#             traceback.print_exc()
            return None

    @staticmethod
    def get_numlvlstyle(num_lvl, ns):
        value_string = f'{{{ns["w"]}}}val'
        ilvl = int(num_lvl.attrib[f'{{{ns["w"]}}}ilvl'])
        start = check_for_key_and_return_value(value_string, num_lvl.xpath("w:start", namespaces=ns)[
            0].attrib) if len(
            num_lvl.xpath("w:start", namespaces=ns)) > 0 else None

        num_fmt = check_for_key_and_return_value(value_string, num_lvl.xpath("w:numFmt", namespaces=ns)[
            0].attrib) if len(
            num_lvl.xpath("w:numFmt", namespaces=ns)) > 0 else None
        lvl_text = check_for_key_and_return_value(value_string,
                                                  num_lvl.xpath("w:lvlText", namespaces=ns)[
                                                      0].attrib) if len(
            num_lvl.xpath("w:lvlText", namespaces=ns)) > 0 else None
        lvl_jc = check_for_key_and_return_value(value_string, num_lvl.xpath("w:lvlJc", namespaces=ns)[
            0].attrib) if len(
            num_lvl.xpath("w:lvlJc", namespaces=ns)) > 0 else None
        if len(num_lvl.xpath("w:pPr", namespaces=ns)) > 0:
            ppr = num_lvl.xpath("w:pPr", namespaces=ns)[0]
            try:
                left_mrg = ppr.ind_left
            except Exception as e:
#                 traceback.print_exc()
                print(e)
                left_mrg = None

            try:
                right_mrg = ppr.ind_right
            except Exception as e:
#                 traceback.print_exc()
                print(e)
                right_mrg = None
            try:
                indent = ppr.first_line_indent
            except Exception as e:
#                 traceback.print_exc()
                print(e)
                indent = None
        else:
            left_mrg = None
            right_mrg = None
            indent = None
        return NumLvlStyle(ilvl, left_mrg,
                           right_mrg, indent,
                           start, num_fmt,
                           lvl_text, lvl_jc)

    @staticmethod
    def get_abstract_num_by_id(document, id, ns):
        for abstract_num in document.part.numbering_part.element.xpath("/w:numbering/w:abstractNum"):
            abstract_num_id = check_for_key_and_return_value(f'{{{ns["w"]}}}abstractNumId',
                                                             abstract_num.attrib)
            if abstract_num_id is not None:
                if int(abstract_num_id) == id:
                    abstract_num_id = int(abstract_num_id)
                    num_level_list = abstract_num.xpath("w:lvl", namespaces=ns)
                    if len(num_level_list) > 0:
                        numbering_styles = []
                        for num_level in num_level_list:
                            if f'{{{ns["w"]}}}ilvl' in num_level.attrib.keys():
                                numbering_styles.append(DocxParagraphParser.get_numlvlstyle(num_level, ns))
                            else:
                                raise Exception('Ошибка в стиле уровня перечисления : не имеет ilvl значения')
                        return AbstractNum(abstract_num_id, numbering_styles)
                    else:
                        num_style_links = abstract_num.xpath("w:numStyleLink", namespaces=ns)
                        if len(num_style_links) > 0:
                            num_style_link = check_for_key_and_return_value(f'{{{ns["w"]}}}val',
                                                                            num_style_links[0].attrib)
                            for style in document.styles.element.style_lst:
                                if style.styleId == num_style_link:
                                    num_id_link = style.pPr.numPr.numId.val
                                    return DocxParagraphParser.get_abstract_style_by_num_id(
                                        document, num_id_link, ns)
            else:
                raise Exception('Ошибка в абстрактном стиле перечисление : не имеет id')
        return AbstractNum(None, None)

    @staticmethod
    def get_abstract_style_by_num_id(document, id, ns):
        for num_style in document.part.numbering_part.element.xpath("/w:numbering/w:num"):
            if num_style.numId == id:
                return DocxParagraphParser.get_abstract_num_by_id(document, num_style.abstractNumId.val, ns)
        return None

    def get_base_numbering_styles(self):

        def get_abstacts_nums():
            abstracts = {}
            for abstract_num in self.origin_document.part.numbering_part.element.xpath("/w:numbering/w:abstractNum"):
                abstract_num_id = check_for_key_and_return_value(f'{{{self.ns["w"]}}}abstractNumId',
                                                                 abstract_num.attrib)
                if abstract_num_id is not None:
                    abstract_num_id = int(abstract_num_id)
                else:
                    raise Exception('Ошибка в абстрактном стиле перечисление : не имеет id')

                num_level_list = abstract_num.xpath("w:lvl", namespaces=self.ns)
                if len(num_level_list) > 0:
                    numbering_styles = []
                    for num_level in num_level_list:
                        if f'{{{self.ns["w"]}}}ilvl' in num_level.attrib.keys():
                            numbering_styles.append(self.get_numlvlstyle(num_level, self.ns))
                        else:
                            raise Exception('Ошибка в стиле уровня перечисления : не имеет ilvl значения')
                        abstracts[abstract_num_id] = AbstractNum(abstract_num_id, numbering_styles)
                else:
                    num_style_links = abstract_num.xpath("w:numStyleLink", namespaces=self.ns)
                    if len(num_style_links) > 0:
                        num_style_link = check_for_key_and_return_value(f'{{{self.ns["w"]}}}val',
                                                                        num_style_links[0].attrib)
                        for style in self.origin_document.styles.element.style_lst:
                            if style.styleId == num_style_link:
                                num_id_link = style.pPr.numPr.numId.val
                                abstracts[abstract_num_id] = DocxParagraphParser.get_abstract_style_by_num_id(
                                    self.origin_document, num_id_link, self.ns)

            return abstracts

        def get_num_styles(abstracts: dict[int, AbstractNum]):
            nums = {}
            for num in self.origin_document.part.numbering_part.element.xpath("/w:numbering/w:num"):
                num_id = num.numId
                abstract_style = abstracts[num.abstractNumId.val]
                numbering_styles = {}
                for ovverride in num.lvlOverride_lst:
                    ilvl = ovverride.ilvl
                    for num_level in ovverride.xpath("w:lvl"):
                        if f'{{{self.ns["w"]}}}ilvl' in num_level.attrib.keys():
                            numbering_styles[ilvl] = self.get_numlvlstyle(num_level, self.ns)
                        else:
                            raise StyleException('Ошибка в стиле уровня перечисления : не имеет ilvl значения')
                nums[num_id] = NumberingStyle(num_id, abstract_style, numbering_styles)
            return nums

        try:
            abstracts = get_abstacts_nums()
            nums = get_num_styles(abstracts)
            numbering_styles = NumeringStyles(num=nums, abstract_num=abstracts)
        except NotImplementedError as ne:
#             traceback.print_exc()
            numbering_styles = NumeringStyles(None, None)
            print(ne)
        except Exception as e:
#             traceback.print_exc()
            print(e)
        self.origin_document.numbering_styles = numbering_styles
        logging.info("Numbering styles were extracted")
        return numbering_styles


@staticmethod
def get_paragraphs_split_outline(paragraphs: list[StructuralElement]):
    def get_tree(array):
        temp = {
            'children': []
        }
        out = min(level[0] for level in array)
        outs = []
        for outline in array:
            if outline[0] in [out, -1]:
                if 'main' in temp.keys():
                    if len(temp['children']) > 0:
                        temp['children'] = get_tree(temp['children'])
                    outs.append(temp)
                temp = {
                    'main': (outline[0], outline[1]),
                    'children': []
                }
                if outline[0] == -1:
                    out = 0
                    continue
            else:
                temp['children'].append((outline[0], outline[1]))
        if len(temp['children']) > 0:
            temp['children'] = get_tree(temp['children'])
        outs.append(temp)
        return outs

    list_of_outline_paragraph = []
    list_of_paragraph = []
    outline_lvl = None
    for paragraph in paragraphs:
        if paragraph.outline_level is not None:
            if len(list_of_paragraph) > 0:
                list_of_outline_paragraph.append(
                    (int(outline_lvl) if outline_lvl is not None else -1, list_of_paragraph))
            list_of_paragraph = []
            outline_lvl = paragraph.outline_level
        list_of_paragraph.append(paragraph)

    split_paragraphs = get_tree(list_of_outline_paragraph)
    return split_paragraphs


@staticmethod
def get_json_split_paragraphs(split_paragraphs: list) -> str:
    def get_main(sections):
        json_dict = {}
        level = 0
        for section in sections:
            section_main_temp = {}
            import dataclasses
            # para_lvl = 0
            try:
                paragraphs = []
                for paragraph in section['main'][1]:
                    para_temp = {}

                    # for attribute_name, value in dataclasses.asdict(paragraph).items():
                    # para_temp[attribute_name[1::]] = value
                    paragraphs.append(paragraph.text)
                section_main_temp['section_text'] = [paragraphs[0]]
                if len(paragraphs) > 1:
                    section_main_temp['main'] = paragraphs[1::]
                    # para_lvl += 1
                children = section['children']
                if len(children) > 0:
                    section_main_temp['children'] = get_main(children)
                else:
                    json_dict[level] = section_main_temp
                    level += 1
                    continue
                json_dict[level] = section_main_temp
                level += 1
            except Exception as e:
#                 traceback.print_exc()
                print(e)
        return json_dict

    json_dict = get_main(split_paragraphs)
    import json
    json_text = json.loads(json.dumps(json_dict))
    return json_text
