import re
import pdfplumber
from src.Class.DocumentClass import Class
from src.Class.Paragraph import Paragraph
from src.PDF.Line import Line
from src.PDF.ParagraphLine import Pdfparagraph
from src.PDF.Table import PDFTable


class PDFParser:
    """
    Description: The class is a parser that extracts structural elements of text documents in PDF format
    ----------

    Parameters:
        __path - attribute specifies file path
        __pdf - attribute representing an object obtained by using the pdfplumber library that models a pdf file
                and its internal objects
        __document - attribute representing a unified text document object containing structural elements and
                their properties
        __lines - an attribute representing a list of all formed lines
        __list_of_table - an attribute representing a list of all extracted tables

    Methods
    ----------

        getLineAndTables(self):
            Extracts all pdf document objects using the pdfplumber library and forms rows and tables based on them

        getSpace(lines):
            Based on the properties of the document lines, generates a line spacing for each line

        addParagraphInDocumentWithAttribute(self, paragraph_line, paragraph_id):
            Adds a paragraph object containing its properties and attributes to the list of structural elements of the document

        getParagraph(self, lines, spaces, list_of_table):
            Forms paragraphs of the document based on lines, line spacing and tables

        getStandartParagraph(paragraph_line):
            Converts the resulting paragraph and its attributes into a unified view

        deleteDublicatesAndAddParagraph(self, paragraph_line, mean, removed_tables, i, paragraph_id, lines, spaces, list_of_table):
            Removes duplicate table text lines, forms their properties and adds them to the paragraph object

    """

    def __init__(self, path):
        self.__path = path
        self.__pdf = pdfplumber.open(path)
        self.__document = Class(owner=self.pdf.metadata.get('Author'), time=self.pdf.metadata.get('CreationDate'))
        self.__lines = []
        self.__list_of_table = []

    @property
    def path(self):
        return self.__path

    @path.setter
    def prevEl(self, path):
        self.__path = path


    @property
    def pdf(self):
        return self.__pdf

    @pdf.setter
    def pdf(self, pdf):
        self.__pdf = pdf

    @property
    def document(self):
        return self.__document

    @document.setter
    def document(self, document):
        self.__document = document

    @property
    def lines(self):
        return self.__lines

    @lines.setter
    def lines(self, lines):
        self.__lines = lines

    @property
    def list_of_table(self):
        return self.__list_of_table

    @list_of_table.setter
    def list_of_table(self, list_of_table):
        self.__list_of_table = list_of_table

    def getLinesAndTables(self):

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
        fontname = []
        size = []
        chars = []
        no_change_font_name = True
        no_change_size = True

        for number_of_page, page in enumerate(self.pdf.pages):
            #Extracting tables and tabular text
            tables = page.find_tables()
            tables_text = page.extract_tables()
            for number_of_table, table in enumerate(tables):
                current_table = PDFTable(table)
                current_table.addText(tables_text[number_of_table])
                self.list_of_table.append(current_table)

            #Selecting text strings
            text = ""
            for i, char in enumerate(page.chars):
                if y0 is not None:
                    y0 = round(y0)
                #Condition for adding a character to a string
                if (round(char.get('y0')) == y0) or (int(char.get('y0')) == y0) \
                        or text == '−' or text == '–' or text == "•":
                    chars.append(char)
                    text = text + char.get('text')
                    x1 = char.get('x1')
                    if i != 0:
                        #Font and line size selection
                        if char.get('fontname') not in fontname:
                            no_change_font_name = False
                            fontname.append(char.get('fontname'))
                        if char.get('size') not in size:
                            no_change_size = False
                            size.append(char.get('size'))
                        y1 = char.get('y1')
                    else:
                        fontname.append(char.get('fontname'))
                        size.append(char.get('size'))
                        y1 = char.get('y1')
                else:
                    if i != 0:
                        #Deleting headers and footers
                        if re.search(r'^\d+ $', text) is None and y0 > 60 and text != '':
                            if len(chars) != 0:
                                x0 = chars[0].get('x0')
                            else:
                                x0 = 0
                            self.lines.append(
                                Line(x0, y0, x1, y1, text, fontname, size, no_change_font_name, no_change_size,
                                     number_of_page + 1, chars))
                    chars = []
                    text = ""
                    y0 = char.get('y0')
                    fontname = []
                    size = []
                    no_change_font_name = True
                    no_change_size = True
                    #Deleting empty lines
                    if text == "" and char.get('text') == ' ':
                        continue
                    chars.append(char)
                    text = text + char.get('text')
            if len(chars) != 0:
                x0 = chars[0].get('x0')
            else:
                x0 = 0
            self.lines.append(
                Line(x0, y0, x1, y1, text, fontname, size, no_change_font_name, no_change_size, number_of_page + 1,
                     chars))
        return self.lines, self.list_of_table

    @staticmethod
    def getSpace(lines):

        """

        Calculates the line spacing between two subsequent lines

        :param lines: list of document lines

        :return
            spaces: List of calculated line spacing

        """

        spaces = []
        i = 0
        while i < len(lines):
            #If the line is the last one on the page, it is assigned a value equal to zero
            if i != len(lines) - 1 and (lines[i].y0 - lines[i + 1].y1 > 0):
                spaces.append(lines[i].y0 - lines[i + 1].y1)
            else:
                spaces.append(0)
            i = i + 1
        return spaces

    def addParagraphInDocumentWithAttribute(self, pdfparagraph, paragraph_id):

        """
        Calculates the properties and attributes of a paragraph and adds it to the list of structural elements of the document

        :param
            pdfparagraph: An object representing a paragraph highlighted by the algorithm
            paragraph_id: Id of paragraph
        :return

        """
        #Highlighting string attributes
        no_change_font_name = pdfparagraph.lines[0].nochangeFontName
        no_change_text_size = pdfparagraph.lines[0].nochangeSize
        for line in pdfparagraph.lines:
            if len(line.fontname) > 1 or line.nochangeFontName is False:
                no_change_font_name = False
            if len(line.size) > 1 or line.nochangeSize is False:
                no_change_text_size = False
        if len(pdfparagraph.lines[0].size) != 0:
            pdfparagraph.text_size = pdfparagraph.lines[0].size[0]
        if len(pdfparagraph.lines[0].fontname) != 0:
            pdfparagraph.fontname = pdfparagraph.lines[0].fontname[0]
        pdfparagraph.no_change_font_name = no_change_font_name
        pdfparagraph.no_change_text_size = no_change_text_size
        pdfparagraph.indent = pdfparagraph.lines[0].x0
        self.document.content[paragraph_id] = self.getStandartParagraph(pdfparagraph)

    def getParagraph(self, lines, spaces, list_of_table):
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
        paragraph = Pdfparagraph()
        paragraph.lines.append(lines[0])
        paragraph.spaces.append(spaces[0])
        paragraph_id = 1
        removed_tables = []
        while i < len(lines):
            mean = 0
            j = 0
            while j < len(paragraph.lines) - 1:
                mean = mean + paragraph.spaces[j]
                j = j + 1
            #Calculating the average value of the line spacing
            if len(paragraph.lines) - 1 > 1:
                mean = mean / (len(paragraph.lines) - 1)
            if mean == 0:
                mean = spaces[i - 1]
            if spaces[i - 1] == 0:
                spaces[i - 1] = mean
            #Condition for paragraph selection
            if (lines[i - 1].x0 < lines[i].x0 or lines[i - 1].x1 <= 520 or abs(spaces[i - 1] - mean) > 2 or (
                    len(paragraph.lines) == 1 and paragraph.lines[0].x0 == lines[i].x0)):
                paragraph.line_spacing = mean
                paragraph_id, removed_tables, list_of_table  = self.deleteDublicatesAndAddParagraph(paragraph, removed_tables, paragraph_id, list_of_table)
                paragraph = Pdfparagraph()
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
    def getStandartParagraph(pdfparagraph):

        """

        Brings the resulting paragraph to the standard form

        :param
            pdfparagraph: The original, obtained after executing the formation algorithm, paragraph

        :return
            paragraph: The resulting Standard paragraph

        """

        text = ""
        for line in pdfparagraph.lines:
            text = text + line.text
        paragraph = Paragraph(text=text, indent=round(Class.ptToSm(pdfparagraph.indent) - 3, 2),
                              lineSpacing=round(Class.ptToSm(pdfparagraph.line_spacing), 2),
                              fontName=pdfparagraph.fontname, textSize=round(pdfparagraph.text_size),
                              nochangeTextSize=pdfparagraph.no_change_text_size,
                              nochangeFontName=pdfparagraph.no_change_font_name)
        return paragraph

    def deleteDublicatesAndAddParagraph(self, pdfparagraph, removed_tables, paragraph_id, list_of_table):

        """

        Brings the resulting paragraph to the standard form

        :param
            pdfparagraph: The original, obtained after executing the formation algorithm, paragraph
            removed_tables: The list of already added to the list of structural elements of tables
            paragraph_id: The number of the paragraph to be added
            list_of_table: The list of tables that have not yet been added has been added to the list of structural elements
        :return
            paragraph_id: The number of the next paragraph
            removed_tables: The list of already added to the list of structural elements of tables
            list_of_table: The list of tables that have not yet been added has been added to the list of structural elements

        """
        insertTable = False
        #Checking that this paragraph is tabular and this table has already been added
        for remove_table in removed_tables:
            if (remove_table.table.page.bbox[3] - remove_table.table.bbox[1]) > pdfparagraph.lines[0].y0 > \
                    (remove_table.table.page.bbox[3] - remove_table.table.bbox[3]) and \
                    remove_table.table.page.page_number == pdfparagraph.lines[0].page:
                insertTable = True
        #Checking that this paragraph is tabular and adding a table if it has not been completed yet
        for table in list_of_table:
            if (table.table.page.bbox[3] - table.table.bbox[1]) > pdfparagraph.lines[0].y0 > (
                    table.table.page.bbox[3] - table.table.bbox[3]) and table.table.page.page_number == \
                    pdfparagraph.lines[0].page:
                self.document.content[paragraph_id] = table
                removed_tables.append(table)
                list_of_table.remove(table)
                insertTable = True
        if insertTable:
            return paragraph_id, removed_tables, list_of_table
        self.addParagraphInDocumentWithAttribute(pdfparagraph, paragraph_id)
        paragraph_id = paragraph_id + 1
        return paragraph_id, removed_tables, list_of_table
