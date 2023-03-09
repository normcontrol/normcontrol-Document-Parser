import re
import pdfplumber
from src.classes.DocumentClass import DocumentClass
from src.classes.Paragraph import Paragraph
from src.pdf.pdfclasses.Line import Line
from src.pdf.pdfclasses.PdfParagraph import PdfParagraph
from src.pdf.pdfclasses.Table import PDFTable


class PDFParser:
    """
    Description: The class is a parser that extracts structural elements of text documents in PDF format

    Parameters:
    ----------
        path - attribute specifies file path
        __pdf - attribute representing an object obtained by using the pdfplumber library that models a pdf file
                and its internal objects
        document - attribute representing a unified text document object containing structural elements and
                their properties
        lines - an attribute representing a list of all formed lines
        list_of_table - an attribute representing a list of all extracted tables

    Methods:
    ----------
        __get_tables(self):
            Extracts all pdf tables using the object of pdfplumber library.

        __get_lines(self):
            Extracts all text rows using the object of pdfplumber library.

        __get_space(lines):
            Based on the properties of the document lines, generates a line spacing for each line

        add_paragraph_in_document_with_attribute(self, pdf_paragraph, paragraph_id):
            Adds a paragraph object containing its properties and attributes to the list of structural elements
            of the document

        get_elements(self, lines, spaces, list_of_table):
            Forms structural elements of the document based on lines, line spacing, tables and pictures

        @staticmethod
        get_standart_paragraph(pdf_paragraph):
            Converts the resulting paragraph and its attributes into a unified view

        @classmethod
        delete_dublicates(cls, pdf_paragraph, removed_tables, list_of_table):
            Removes duplicate table text lines, forms their properties and adds them to the paragraph object

    """

    def __init__(self, path):
        self._path = path
        self.__pdf = pdfplumber.open(path)
        self.document = DocumentClass(owner=self.__pdf.metadata.get('Author'),
                                      time=self.__pdf.metadata.get('CreationDate'))
        self._pictures = self.__get_all_pictures()
        self._lines = self.__get_lines()
        self._list_of_table = self.__get_tables()

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value):
        self._path = value

    @property
    def pictures(self):
        return self._pictures

    @pictures.setter
    def pictures(self, value):
        self._pictures = value

    @property
    def document(self):
        return self._document

    @document.setter
    def document(self, document):
        self._document = document

    @property
    def lines(self):
        return self._lines

    @lines.setter
    def lines(self, lines):
        self._lines = lines

    @property
    def list_of_table(self):
        return self._list_of_table

    @list_of_table.setter
    def list_of_table(self, list_of_table):
        self._list_of_table = list_of_table

    def __get_tables(self):
        list_of_table = []
        for page in self.__pdf.pages:
            # Extracting tables and tabular text
            tables = page.find_tables()
            tables_text = page.extract_tables()
            for number_of_table, table in enumerate(tables):
                current_table = PDFTable(table)
                current_table.addText(tables_text[number_of_table])
                list_of_table.append(current_table)
        return list_of_table

    def __get_lines(self):

        """

        Counts and returns the number of special characters in a text

        :return
            lines: List of all document lines
            list_of_table: List of all document tables

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
    def get_space(lines):

        """

        Calculates the line spacing between two subsequent lines

        :param
            lines: list of document lines

        :return
            spaces: List of calculated line spacing

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

    def add_paragraph_in_document_with_attribute(self, pdf_paragraph, paragraph_id):

        """
        Calculates the properties and attributes of a paragraph and adds it to the list of structural elements
        of the document

        :param
            pdf_paragraph: An object representing a paragraph highlighted by the algorithm
            paragraph_id: Id of paragraph

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
        self.document.content[paragraph_id] = self.get_standart_paragraph(pdf_paragraph)

    def get_elements(self, lines, spaces, list_of_table, list_of_picture):
        """

        Generates paragraphs from a list of lines

        :param
            lines: List of all document lines
            spaces: List of calculated line spacing
            list_of_table: List of all document tables

        :return
            document: List of all structural elements in the document

        """

        i = 1
        paragraph_id = 1
        removed_tables = []
        removed_pictures = []

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
                    if paragraph.lines[0].number_of_page == picture.get("page_number") and paragraph.lines[0].y0 >\
                            picture.get("y0"):
                        self.document.add_content(paragraph_id, picture)
                        removed_pictures.append(picture)
                        list_of_picture.remove(picture)
                        paragraph_id += 1
                paragraph.line_spacing = mean
                element, removed_tables, list_of_table = PDFParser.delete_dublicates(paragraph, removed_tables,
                                                                                     list_of_table)
                if element is not None:
                    if type(element) == PDFTable:
                        self.document.add_content(paragraph_id, element)
                    else:
                        self.add_paragraph_in_document_with_attribute(element, paragraph_id)
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

    @staticmethod
    def get_standart_paragraph(pdf_paragraph):

        """

        Brings the resulting paragraph to the standard form

        :param
            pdf_paragraph: The original, obtained after executing the formation algorithm, paragraph

        :return
            paragraph: The resulting Standard paragraph

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
    def delete_dublicates(cls, pdf_paragraph, removed_tables, list_of_table):

        """

        Brings the resulting paragraph to the standard form

        :param
            pdf_paragraph: The original, obtained after executing the formation algorithm, paragraph
            removed_tables: The list of already added to the list of structural elements of tables
            list_of_table: The list of tables that have not yet been added has been added to the list of structural elements
        :return
            table: If a table is found, it returns the object representing it to add
            pdf_paragraph: If there are no duplicates of the table text, returns the paragraph passed as a parameter
            removed_tables: The list of already added to the list of structural elements of tables
            list_of_table: The list of tables that have not yet been added has been added to the list of structural elements

        """
        # Checking that this paragraph is tabular and this table has already been added
        for remove_table in removed_tables:
            if (remove_table.table.page.bbox[3] - remove_table.table.bbox[1]) > pdf_paragraph.lines[0].y0 > \
                    (remove_table.table.page.bbox[3] - remove_table.table.bbox[3]) and \
                    remove_table.table.page.page_number == pdf_paragraph.lines[0].number_of_page:
                return None, removed_tables, list_of_table
        # Checking that this paragraph is tabular and adding a table if it has not been completed yet
        for table in list_of_table:
            if (table.table.page.bbox[3] - table.table.bbox[1]) > pdf_paragraph.lines[0].y0 > (
                    table.table.page.bbox[3] - table.table.bbox[3]) and table.table.page.page_number == \
                    pdf_paragraph.lines[0].number_of_page:
                removed_tables.append(table)
                list_of_table.remove(table)
                return table, removed_tables, list_of_table
        return pdf_paragraph, removed_tables, list_of_table

    def __get_all_pictures(self):
        pictures = []
        for number_of_page, page in enumerate(self.__pdf.pages):
            for image in page.images:
                pictures.append(image)
        return pictures
