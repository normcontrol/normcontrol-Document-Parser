import re
from abc import ABC

import pdfplumber

from src.classes.Table import Table
from src.classes.UnifiedDocumentView import UnifiedDocumentView
from src.classes.Paragraph import Paragraph
from src.classes.interfaces.InformalParserInterface import InformalParserInterface
from src.classes.superclass.StructuralElement import StructuralElement
from src.helpers.errors.errors import EmptyPathException
from src.PDF.pdfclasses.Line import Line
from src.PDF.pdfclasses.PdfParagraph import PdfParagraph
from src.PDF.pdfclasses.PDFTable import PDFTable


class PDFParser(InformalParserInterface, ABC):
    """
    Description: The class is a parser that extracts structural elements of text documents in PDF format

    Attributes:
    ----------
        _path:str
            Attribute specifies file path

        __pdf: pdfplumber.pdf
            Attribute representing an object obtained by using the pdfplumber library that models a pdf file
            and its internal objects

        _document: UnifiedDocumentView
            Attribute representing a unified text document object containing structural elements and
            their properties

        _lines: list
            An attribute representing a list of all formed lines

        _list_of_table: list
            An attribute representing a list of all extracted tables

        _line_spaces: list
            An attribute representing a list of spaces between lines

        _pictures:list
            An attribute representing a list of all pictures in file

        _paragraph_list:
             An attribute representing a list of all paragraphs in file

    Methods:
    ----------
        get_tables(self):
            Extracts all pdf tables using the object of pdfplumber library.

        get_lines(self):
            Extracts all text rows using the object of pdfplumber library.

        get_pictures(self):
            Extracts all images from a pdf document

        get_formules(self):
            Extracts all formules from a pdf document

        get_lists(self):
            Extracts all lists from a pdf document

        @staticmethod
        add_special_paragraph_attribute(pdf_paragraph: PdfParagraph):
            Calculates and adds special attributes to a paragraph

        get_all_elements(self, lines, spaces, list_of_table):
            Forms structural elements of the document based on lines, line spacing, tables and pictures

        get_paragraphs(self, lines, spaces, list_of_table):
            Forms paragraphs of the document based on lines, line spacing and tables

        @classmethod
        get_space(lines):
            Based on the properties of the document lines, generates a line spacing for each line

        @staticmethod
        get_standart_paragraph(pdf_paragraph):
            Converts the resulting paragraph and its attributes into a unified view

        @classmethod
        delete_dublicates(cls, pdf_paragraph, removed_tables, list_of_table):
            Removes duplicate table text lines, forms their properties and adds them to the paragraph object

    """

    def __init__(self, path):
        try:
            if len(path) == 0:
                raise EmptyPathException('Path is empty')
            self._path = path
            self.__pdf = pdfplumber.open(path)
            self._document = UnifiedDocumentView(owner=self.__pdf.metadata.get('Author'),
                                                 time=self.__pdf.metadata.get('CreationDate'))
            self._pictures = self.get_pictures()
            self._lines = self.get_lines()
            self._line_spaces = self.get_space(self._lines)
            self._list_of_table = self.get_tables()
            self._paragraph_list = self.get_paragraphs(self.lines, self.line_spaces, self.list_of_table)
        except EmptyPathException as e:
            print(e)


    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value: str):
        self._path = value

    @property
    def line_spaces(self):
        return self._line_spaces

    @line_spaces.setter
    def line_spaces(self, value: list):
        self._line_spaces = value

    @property
    def pictures(self):
        return self._pictures

    @pictures.setter
    def pictures(self, value: list):
        self._pictures = value

    @property
    def document(self):
        return self._document

    @document.setter
    def document(self, document: UnifiedDocumentView):
        self._document = document

    @property
    def lines(self):
        return self._lines

    @lines.setter
    def lines(self, lines: list):
        self._lines = lines

    @property
    def list_of_table(self):
        return self._list_of_table

    @list_of_table.setter
    def list_of_table(self, list_of_table: list):
        self._list_of_table = list_of_table

    @property
    def paragraph_list(self):
        return self._paragraph_list

    @paragraph_list.setter
    def paragraph_list(self, value: str):
        self._paragraph_list = value

    def get_tables(self) -> list[StructuralElement]:
        """

        Extracts all table from a pdf document

        :return
            list_of_table: list
                The list of tables in PDF file

        """

        list_of_table = []
        for page in self.__pdf.pages:
            # Extracting tables and tabular text
            tables = page.find_tables()
            tables_text = page.extract_tables()
            for number_of_table, table in enumerate(tables):
                list_of_table.append(Table(_inner_text=tables_text[number_of_table],
                                           _master_page=table.page,
                                           _master_page_number=table.page.page_number,
                                           _width=table.bbox[2]-table.bbox[0],
                                           _bbox=table.bbox))
        return list_of_table

    def get_lines(self) -> list:

        """

        Generates lines from a list of chars

        :return
            lines: list
                List of all document lines

        """
        # Initial initializations of variables
        y0 = -1
        x1 = 0
        y1 = 0
        font_names = []
        text_sizes = []
        chars = []
        no_change_font_name = True
        no_change_text_size = True
        lines = []
        for number_of_page, page in enumerate(self.__pdf.pages):
            # Selecting text strings
            text = ""
            for i, char in enumerate(page.chars):
                if y0 is not None:
                    y0 = round(y0)
                # Condition for adding a character to a string
                if (round(char.get('y0')) == y0) or (int(char.get('y0')) == y0) \
                        or text == '−' or text == '–' or text == "•":
                    chars.append(char)
                    text = text + char.get('text')
                    x1 = char.get('x1')
                    if i != 0:
                        # Font and line size selection
                        if char.get('fontname') not in font_names:
                            no_change_font_name = False
                            font_names.append(char.get('fontname'))
                        if char.get('size') not in text_sizes:
                            no_change_text_size = False
                            text_sizes.append(char.get('size'))
                        y1 = char.get('y1')
                    else:
                        font_names.append(char.get('fontname'))
                        text_sizes.append(char.get('size'))
                        y1 = char.get('y1')
                else:
                    if i != 0:
                        # Deleting headers and footers
                        if re.search(r'^\d+ $', text) is None and y0 > 60 and text != '':
                            if len(chars) != 0:
                                x0 = chars[0].get('x0')
                            else:
                                x0 = 0
                            lines.append(
                                Line(_x0=x0, _y0=y0, _x1=x1, _y1=y1, _text=text, _font_names=font_names,
                                     _text_sizes=text_sizes, _no_change_font_name=no_change_font_name,
                                     _no_change_text_size=no_change_text_size, _number_of_page=number_of_page + 1,
                                     _chars=chars))
                    chars = []
                    text = ""
                    y0 = char.get('y0')
                    font_names = []
                    text_sizes = []
                    no_change_font_name = True
                    no_change_text_size = True
                    # Deleting empty lines
                    if text == "" and char.get('text') == ' ':
                        continue
                    chars.append(char)
                    text = text + char.get('text')
            if len(chars) != 0:
                x0 = chars[0].get('x0')
            else:
                x0 = 0
            lines.append(
                Line(_x0=x0, _y0=y0, _x1=x1, _y1=y1, _text=text, _font_names=font_names, _text_sizes=text_sizes,
                     _no_change_font_name=no_change_font_name, _no_change_text_size=no_change_text_size,
                     _number_of_page=number_of_page + 1, _chars=chars))
        return lines

    @staticmethod
    def get_space(lines: list):

        """

        Calculates the line spacing between two subsequent lines

        :param
            lines: list
                list of document lines

        :return
            spaces: list
                List of calculated line spacing

        """

        spaces = []
        i = 0
        while i < len(lines):
            # If the line is the last one on the page, it is assigned a value equal to zero
            if i != len(lines) - 1 and (lines[i].y0 - lines[i + 1].y1 > 0):
                spaces.append(lines[i].y0 - lines[i + 1].y1)
            else:
                spaces.append(0)
            i = i + 1
        return spaces

    @staticmethod
    def add_special_paragraph_attribute(pdf_paragraph: PdfParagraph):

        """

        Calculates the properties and attributes of a paragraph and adds it to the list of structural elements
        of the document
        :param
            pdf_paragraph: PdfParagraph
                An object representing a paragraph highlighted by the algorithm

        :return pdf_paragraph: PdfParagraph

        """
        # Highlighting string attributes
        no_change_font_name = pdf_paragraph.lines[0].no_change_font_name
        no_change_text_size = pdf_paragraph.lines[0].no_change_text_size
        for line in pdf_paragraph.lines:
            if len(line.font_names) > 1 or line.no_change_font_name is False:
                no_change_font_name = False
            if len(line.text_sizes) > 1 or line.no_change_text_size is False:
                no_change_text_size = False
        if len(pdf_paragraph.lines[0].text_sizes) != 0:
            pdf_paragraph.text_size = pdf_paragraph.lines[0].text_sizes[0]
        if len(pdf_paragraph.lines[0].font_names) != 0:
            pdf_paragraph.font_name = pdf_paragraph.lines[0].font_names[0]
        pdf_paragraph.no_change_font_name = no_change_font_name
        pdf_paragraph.no_change_text_size = no_change_text_size
        pdf_paragraph.indent = pdf_paragraph.lines[0].x0
        return pdf_paragraph

    def get_all_elements(self, lines: list, spaces: list, list_of_table: list,
                         list_of_picture: list) -> UnifiedDocumentView:
        """

        Generates paragraphs from a list of lines
        :param
            lines: list
                List of all document lines

            spaces: list
                List of calculated line spacing

            list_of_table: list
                List of all document tables

            list_of_picture: list
                List of all document pictures

        :return
            document: UnifiedDocumentView
                List of all structural elements in the document

        """

        i = 1
        paragraph_id = 1
        removed_tables = []
        removed_pictures = []
        list_of_table = list_of_table.copy()

        paragraph = PdfParagraph()
        paragraph.lines.append(lines[0])
        paragraph.spaces.append(spaces[0])

        while i < len(lines):
            mean = 0
            j = 0
            while j < len(paragraph.lines) - 1:
                mean = mean + paragraph.spaces[j]
                j = j + 1
            # Calculating the average value of the line spacing
            if len(paragraph.lines) - 1 > 1:
                mean = mean / (len(paragraph.lines) - 1)
            if mean == 0:
                mean = spaces[i - 1]
            if spaces[i - 1] == 0:
                spaces[i - 1] = mean
            # Condition for paragraph selection
            if (lines[i - 1].x0 < lines[i].x0 or lines[i - 1].x1 <= 520 or abs(spaces[i - 1] - mean) > 2 or (
                    len(paragraph.lines) == 1 and paragraph.lines[0].x0 == lines[i].x0)):
                for picture in list_of_picture:
                    if paragraph.lines[0].number_of_page == picture.get("page_number") and paragraph.lines[0].y0 > \
                            picture.get("y0"):
                        self.document.add_content(paragraph_id, picture)
                        removed_pictures.append(picture)
                        list_of_picture.remove(picture)
                        paragraph_id += 1
                paragraph.line_spacing = mean
                element, removed_tables, list_of_table = PDFParser.delete_dublicates(paragraph, removed_tables,
                                                                                     list_of_table)
                if element is not None:
                    if isinstance(element, Table):
                        self.document.add_content(paragraph_id, element)
                    else:
                        element = self.add_special_paragraph_attribute(element)
                        self.document.content[paragraph_id] = self.get_standart_paragraph(element)
                    paragraph_id += 1
                paragraph = PdfParagraph()
                paragraph.lines.append(lines[i])
                paragraph.spaces.append(spaces[i])
            else:
                paragraph.lines.append(lines[i])
                if spaces[i] == 0:
                    spaces[i] = mean
                paragraph.spaces.append(spaces[i])
            i = i + 1
        return self.document

    def get_paragraphs(self, lines: list, spaces: list, list_of_table: list) -> list[StructuralElement]:
        """

        Generates paragraphs from a list of lines
        :param
            lines: list
                List of all document lines

            spaces: list
                List of calculated line spacing

            list_of_table: list
                List of all document tables

        :return
            paragraph_list: list
                List of all paragraphs in the document

        """

        i = 1
        removed_tables = []
        list_of_table = list_of_table.copy()
        paragraph_list = []

        paragraph = PdfParagraph()
        paragraph.lines.append(lines[0])
        paragraph.spaces.append(spaces[0])

        while i < len(lines):
            mean = 0
            j = 0
            while j < len(paragraph.lines) - 1:
                mean = mean + paragraph.spaces[j]
                j = j + 1
            # Calculating the average value of the line spacing
            if len(paragraph.lines) - 1 > 1:
                mean = mean / (len(paragraph.lines) - 1)
            if mean == 0:
                mean = spaces[i - 1]
            if spaces[i - 1] == 0:
                spaces[i - 1] = mean
            # Condition for paragraph selection
            if (lines[i - 1].x0 < lines[i].x0 or lines[i - 1].x1 <= 520 or abs(spaces[i - 1] - mean) > 2 or (
                    len(paragraph.lines) == 1 and paragraph.lines[0].x0 == lines[i].x0)):
                paragraph.line_spacing = mean
                element, removed_tables, list_of_table = PDFParser.delete_dublicates(paragraph, removed_tables,
                                                                                     list_of_table)
                if element is not None and isinstance(element, PdfParagraph):
                    paragraph_list.append(self.get_standart_paragraph(self.add_special_paragraph_attribute(element)))
                paragraph = PdfParagraph()
                paragraph.lines.append(lines[i])
                paragraph.spaces.append(spaces[i])
            else:
                paragraph.lines.append(lines[i])
                if spaces[i] == 0:
                    spaces[i] = mean
                paragraph.spaces.append(spaces[i])
            i = i + 1
        return paragraph_list

    @staticmethod
    def get_standart_paragraph(pdf_paragraph: PdfParagraph):
        """

        Brings the resulting paragraph to the standard form
        :param
            pdf_paragraph: PdfParagraph
                The original, obtained after executing the formation algorithm, paragraph
        :return
            paragraph: Paragraph
                The resulting Standard paragraph

        """
        from src.helpers.measurement import pt_to_sm

        text = ""
        for line in pdf_paragraph.lines:
            text = text + line.text
        paragraph = Paragraph(_text=text, _indent=round(pt_to_sm(pdf_paragraph.indent) - 3, 2),
                              _font_name=pdf_paragraph.font_name,
                              _text_size=round(pdf_paragraph.text_size)
                              if isinstance(pdf_paragraph.text_size, float) else None,
                              _line_spacing=round(pt_to_sm(pdf_paragraph.line_spacing), 2),
                              _no_change_text_size=pdf_paragraph.no_change_text_size,
                              _no_change_fontname=pdf_paragraph.no_change_font_name)
        return paragraph

    @classmethod
    def delete_dublicates(cls, pdf_paragraph: PdfParagraph, removed_tables: list, list_of_table: list):

        """

        Brings the resulting paragraph to the standard form
        :param
            pdf_paragraph: PdfParagraph
                The original, obtained after executing the formation algorithm, paragraph

            removed_tables: list
                The list of already added to the list of structural elements of tables

            list_of_table: list
                The list of tables that have not yet been added has been added to the list of structural elements

        :return
            table: PDFTable
                If a table is found, it returns the object representing it to add

            pdf_paragraph: PdfParagraph
                If there are no duplicates of the table text, returns the paragraph passed as a parameter

            removed_tables: list
                The list of already added to the list of structural elements of tables

            list_of_table: list
                The list of tables that have not yet been added has been added to the list of structural elements

        """
        # Checking that this paragraph is tabular and this table has already been added
        for remove_table in removed_tables:
            if (remove_table.master_page.bbox[3] - remove_table.bbox[1]) > pdf_paragraph.lines[0].y0 > \
                    (remove_table.master_page.bbox[3] - remove_table.bbox[3]) and \
                    remove_table.master_page_number == pdf_paragraph.lines[0].number_of_page:
                return None, removed_tables, list_of_table
        # Checking that this paragraph is tabular and adding a table if it has not been completed yet
        for table in list_of_table:
            if (table.master_page.bbox[3] - table.bbox[1]) > pdf_paragraph.lines[0].y0 > (
                    table.master_page.bbox[3] - table.bbox[3]) and table.master_page_number == \
                    pdf_paragraph.lines[0].number_of_page:
                removed_tables.append(table)
                list_of_table.remove(table)
                return table, removed_tables, list_of_table
        return pdf_paragraph, removed_tables, list_of_table

    def get_pictures(self) -> list:
        """

        Extracts all images from a pdf document
        :return
            pictures: list
                The list of pictures in PDF file

        """

        pictures = []
        for page in self.__pdf.pages:
            for image in page.images:
                pictures.append(image)
        return pictures

    def get_formulas(self):
        """

        Extracts all formulas from a pdf document
        :return
            formulas: list
                The list of formulas in PDF file

        """

        print("In progress")
        pass

    def get_lists(self):
        """

        Extracts all formulas from a pdf document
        :return
            lists: list
                The list of lists in PDF file

        """

        print("In progress")
        pass
