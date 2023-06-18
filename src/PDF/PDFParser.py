import re
import pdfplumber
from pdfplumber import PDF
from tabula.io import read_pdf

from src.classes.Formula import Formula
from src.classes.Frame import Frame
from src.classes.Image import Image
from src.classes.List import List
from src.classes.Table import Table
from src.classes.TableCell import TableCell
from src.classes.UnifiedDocumentView import UnifiedDocumentView
from src.classes.Paragraph import Paragraph
from src.classes.interfaces.InformalParserInterface import InformalParserInterface
from src.classes.superclass.Parser import DefaultParser
from src.helpers.errors.errors import EmptyPathException
from src.pdf.pdfclasses.Line import Line
from src.pdf.pdfclasses.PdfParagraph import PdfParagraph


class PDFParser(InformalParserInterface, DefaultParser):
    """
    Description: The class is a parser that extracts structural elements of text documents in PDF format

    Attributes:
    ----------
        _path:str
            The attribute specifies file path

        __pdf: pdfplumber.pdf
            The attribute represents an object obtained by using the pdfplumber library that models a pdf file
                and its internal objects

        _document: UnifiedDocumentView
            The attribute represents a unified text document object containing structural elements and
                their properties

        _lines: list
            The attribute represents a list of all formed lines

        _list_of_table: list
            The attribute represents a list of all extracted tables

        _line_spaces: list
            The attribute represents a list of spaces between lines

        _pictures:list
            The attribute represents a list of all pictures in file

        _paragraph_list:
            The attribute represents a list of all paragraphs in file

    Methods:
    ----------
        load_data_source(self, path: str) -> PDF:
            Loads raw data from a document

        extract_tables(self) -> list[Table]:
            Extracts all pdf tables using the object of pdfplumber library.

        extract_lines(self) -> list[Line]:
            Extracts all text rows using the object of pdfplumber library.

        extract_pictures(self) -> list[Frame]:
            Extracts all images from a pdf document

        extract_formulas(self) -> list[Formula]:
            Extracts all formules from a pdf document

        extract_lists(self) -> list[List]:
            Extracts all lists from a pdf document

        extract_paragraphs(self, lines, spaces, list_of_table) -> list[Paragraph]:
            Forms paragraphs of the document based on lines, line spacing and tables

        get_all_elements(self, lines, spaces, list_of_table) -> UnifiedDocumentView:
            Forms structural elements of the document based on lines, line spacing, tables and pictures

        add_special_paragraph_attribute(pdf_paragraph: PdfParagraph) -> PdfParagraph:
            Calculates and adds special attributes to a paragraph

        extract_spaces(lines) -> list[float]:
            Based on the properties of the document lines, generates a line spacing for each line

        get_standart_paragraph(pdf_paragraph) -> Paragraph:
            Converts the resulting paragraph and its attributes into a unified view

        delete_dublicates(cls, pdf_paragraph, removed_tables, list_of_table):
            Removes duplicate table text lines, forms their properties and adds them to the paragraph object

    """

    def __init__(self, path):
        try:
            if len(path) == 0:
                raise EmptyPathException('Path is empty')
            self._path = path
            self.__pdf = self.load_data_source(path)
            self.document = UnifiedDocumentView(owner=self.__pdf.metadata.get('Author'),
                                                time=self.__pdf.metadata.get('CreationDate'),
                                                page_count=len(self.__pdf.pages))
            self.pictures = self.extract_pictures()
            self.lines = self.extract_lines()
            self.line_spaces = self.extract_spaces(self._lines)
            self.tables = self.extract_tables()
            self.paragraphs = self.extract_paragraphs(self.lines, self.line_spaces, self.tables)

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
    def lines(self):
        return self._lines

    @lines.setter
    def lines(self, lines: list[Line]):
        self._lines = lines

    def load_data_source(self, path: str) -> PDF:
        """
        Loads raw data from a document
        :param
            path:str
                Path to source file
        :return
            pdf: PDF
                A variable representing an object that stores the primary extracted data from the document,
                for example: symbols, rectangles, pictures

        """
        return pdfplumber.open(path)

    def extract_tables(self) -> list[Table]:
        """

        Extracts all table from a pdf document

        :return
            list_of_table: list
                The list of tables in PDF file

        """

        list_of_table = []
        for page in self.__pdf.pages:
            # Extracting tables and tabular text in document
            tables = page.find_tables()
            tables_text = page.extract_tables()
            for number_of_table, table in enumerate(tables):
                if len([cell for row in table.rows for cell in row.cells]) == len(
                        [item for sublist in tables_text[number_of_table] for item in sublist]):
                    list_of_table.append(Table(_inner_text=tables_text[number_of_table],
                                               _master_page_number=table.page.page_number,
                                               _width=table.bbox[2] - table.bbox[0],
                                               _bbox=table.bbox, _page_bbox=table.page.bbox,
                                               _cells=[
                                                   TableCell(_text=[item for sublist in tables_text[number_of_table]
                                                                    for item in sublist][i]) for i in
                                                   range(len([cell for row in table.rows for cell in row.cells]))]
                                               ))
        return list_of_table

    def extract_lines(self) -> list[Line]:

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
        chars = list()
        lines = []
        for page in self.__pdf.pages:
            # Selecting text strings
            text = ""
            font_names = [page.chars[0]['fontname']]
            text_sizes = [page.chars[0]['size']]
            no_change_font_name = True
            no_change_text_size = True

            for i, char in enumerate(page.chars):
                if y0 is not None:
                    y0 = round(y0)
                # Condition for adding a character to a string
                if (round(char['y0']) == y0) or (int(char['y0']) == y0) or not re.match(r'^[−–•]$', text) is None:
                    chars.append(char)
                    text += char['text']
                    x1 = char['x1']
                    y1 = char['y1']
                    # Font and line size selection
                    if not char['fontname'] in font_names:
                        no_change_font_name = False
                        font_names.append(char['fontname'])
                    if not char['size'] in text_sizes:
                        no_change_text_size = False
                        text_sizes.append(char['size'])
                else:
                    if i != 0:
                        # Deleting headers and footers
                        if re.search(r'^\d+ $', text) is None and y0 > 60 and text != '':
                            if len(chars) != 0:
                                x0 = chars[0]['x0']
                            else:
                                x0 = 0
                            lines.append(
                                Line(_x0=x0, _y0=y0, _x1=x1, _y1=y1, _text=text, _font_names=font_names,
                                     _text_sizes=text_sizes, _no_change_font_name=no_change_font_name,
                                     _no_change_text_size=no_change_text_size, _number_of_page=page.page_number,
                                     _chars=chars))

                    y0 = char['y0']
                    font_names = [char['fontname']]
                    text_sizes = [char['size']]
                    no_change_font_name = True
                    no_change_text_size = True
                    chars = [char]
                    text = char['text']
            if len(chars) != 0:
                x0 = chars[0]['x0']
            else:
                x0 = 0
            lines.append(
                Line(_x0=x0, _y0=y0, _x1=x1, _y1=y1, _text=text, _font_names=font_names, _text_sizes=text_sizes,
                     _no_change_font_name=no_change_font_name, _no_change_text_size=no_change_text_size,
                     _number_of_page=page.page_number, _chars=chars))
        return lines

    @staticmethod
    def extract_spaces(lines: list) -> list[float]:

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
    def add_special_paragraph_attribute(pdf_paragraph: PdfParagraph) -> PdfParagraph:

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
        text_size = set()
        font_name = set()
        for line in pdf_paragraph.lines:
            for size in line.text_sizes:
                text_size.add(round(size))
            for font in line.font_names:
                font_name.add(font)
            no_change_font_name = False if len(font_name) > 1 or line.no_change_font_name is False else True
            no_change_text_size = False if len(text_size) > 1 or line.no_change_text_size is False else True

        pdf_paragraph.font_name = list(font_name)
        pdf_paragraph.text_size = list(text_size)

        if len(pdf_paragraph.font_name) > 1:
            pdf_paragraph.full_bold = False
            pdf_paragraph.full_italics = False
        else:
            for font in pdf_paragraph.font_name:
                pdf_paragraph.full_italics = True if 'Italics' in font else False
                pdf_paragraph.full_bold = True if 'Bold' in font else False
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
        if len(self.document.content) != 0:
            return self.document.content
        i = 1
        paragraph_id = 1
        removed_tables = []
        removed_pictures = []
        list_of_table = list_of_table.copy()
        list_of_picture = list_of_picture.copy()
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
            if (lines[i - 1].x0 < lines[i].x0 or lines[i - 1].x1 <= 500 or abs(spaces[i - 1] - mean) > 2 or (
                    len(paragraph.lines) == 1 and paragraph.lines[0].x0 == lines[i].x0)):
                for picture in list_of_picture:
                    if paragraph.lines[0].number_of_page == picture.page_number and paragraph.lines[0].y0 > \
                            picture.bbox[1]:
                        self.document.add_content(paragraph_id, picture)
                        removed_pictures.append(picture)
                        list_of_picture.remove(picture)
                        paragraph_id += 1
                paragraph.line_spacing = mean
                element, removed_tables, list_of_table = PDFParser.delete_dublicates(paragraph, removed_tables,
                                                                                     list_of_table)
                if element is not None:
                    if not isinstance(element, PdfParagraph):
                        self.document.add_content(paragraph_id, element)
                        paragraph_id += 1
                    else:
                        check_text = ' '.join(line.text for line in element.lines)
                        if check_text != '' and check_text != ' ':
                            self.document.add_content(paragraph_id, self.get_standart_paragraph(
                                self.add_special_paragraph_attribute(element)))
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

    def extract_paragraphs(self, lines: list, spaces: list, list_of_table: list) -> list[Paragraph]:
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
            for j in range(len(paragraph.lines)):
                mean += paragraph.spaces[j]
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
                    check_text = ' '.join(line.text for line in element.lines)
                    if check_text != '' and check_text != ' ':
                        paragraph_list.append(
                            self.get_standart_paragraph(self.add_special_paragraph_attribute(element)))
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
    def get_standart_paragraph(pdf_paragraph: PdfParagraph) -> Paragraph:
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
        bbox = {

        }
        if len(pdf_paragraph.lines) == 1:
            bbox[pdf_paragraph.lines[0].number_of_page] = (pdf_paragraph.lines[0].x0, pdf_paragraph.lines[0].y1,
                                                           pdf_paragraph.lines[0].x1,
                                                           pdf_paragraph.lines[0].y0)
        else:
            for i in range(len(pdf_paragraph.lines)):
                if pdf_paragraph.lines[i].number_of_page != pdf_paragraph.lines[0].number_of_page and \
                        len(pdf_paragraph.lines) != 1:
                    bbox[pdf_paragraph.lines[i].number_of_page] = (pdf_paragraph.lines[i].x0, pdf_paragraph.lines[i].y1,
                                                                   pdf_paragraph.lines[0].x1,
                                                                   pdf_paragraph.lines[len(pdf_paragraph.lines) - 1].y0)
                    bbox[pdf_paragraph.lines[0].number_of_page] = (pdf_paragraph.lines[1].x0, pdf_paragraph.lines[0].y1,
                                                                   pdf_paragraph.lines[0].x1,
                                                                   pdf_paragraph.lines[i - 1].y0)
                    break
        if len(bbox.keys()) == 0:
            bbox[pdf_paragraph.lines[0].number_of_page] = (pdf_paragraph.lines[1].x0, pdf_paragraph.lines[0].y1,
                                                           pdf_paragraph.lines[0].x1,
                                                           pdf_paragraph.lines[len(pdf_paragraph.lines) - 1].y0)

        paragraph = Paragraph(_text=text, _indent=round(pt_to_sm(pdf_paragraph.indent) - 3, 2),
                              _font_name=pdf_paragraph.font_name, _text_size=pdf_paragraph.text_size,
                              _bold=pdf_paragraph.full_bold, _italics=pdf_paragraph.full_italics,
                              _line_spacing=round(pt_to_sm(pdf_paragraph.line_spacing), 2),
                              _no_change_text_size=pdf_paragraph.no_change_text_size,
                              _no_change_fontname=pdf_paragraph.no_change_font_name,
                              _bbox=bbox)
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
            if (remove_table.page_bbox[3] - remove_table.bbox[1]) > pdf_paragraph.lines[0].y0 > \
                    (remove_table.page_bbox[3] - remove_table.bbox[3]) and \
                    remove_table.master_page_number == pdf_paragraph.lines[0].number_of_page:
                return None, removed_tables, list_of_table
        # Checking that this paragraph is tabular and adding a table if it has not been completed yet
        for table in list_of_table:
            if (table.page_bbox[3] - table.bbox[1]) > pdf_paragraph.lines[0].y0 > (
                    table.page_bbox[3] - table.bbox[3]) and table.master_page_number == \
                    pdf_paragraph.lines[0].number_of_page:
                removed_tables.append(table)
                list_of_table.remove(table)
                return table, removed_tables, list_of_table
        return pdf_paragraph, removed_tables, list_of_table

    def extract_pictures(self) -> list[Frame]:
        """

        Extracts all images from a pdf document
        :return
            pictures: list
                The list of pictures in PDF file

        """

        pictures = []
        for page in self.__pdf.pages:
            for image in page.images:
                pictures.append(Frame(_bbox=(image['x0'], image['y0'], image['x1'], image['y1']),
                                      _width=image['width'], _height=image['width'], _page_number=image['page_number'],
                                      _image=Image(_type=image['object_type'])))
        return pictures

    def extract_formulas(self) -> list[Formula]:
        """

        Extracts all formulas from a pdf document
        :return
            formulas: list
                The list of formulas in PDF file

        """

        print("In progress")
        pass

    def extract_lists(self) -> list[List]:
        """

        Extracts all formulas from a pdf document
        :return
            lists: list
                The list of lists in PDF file

        """

        print("In progress")
        pass
