import pdfplumber
from src.Class.DocumentClass import Class
from src.Class.Paragraph import Paragraph
from src.PDF.Line import Line
from src.PDF.ParagraphLine import ParagraphLine
from src.PDF.Table import PDFTable


class PDFParser:

    def getLine(self, path="test.pdf"):
        with pdfplumber.open(path) as pdf:
            self.document = Class(owner=pdf.metadata.get('Author'), time=pdf.metadata.get('CreationDate'))
            lines = []
            listOfTable = []
            for numberofpage, pages in enumerate(pdf.pages):
                tables = pages.find_tables()
                tablestext = pages.extract_tables()
                for numberOfTable, table in enumerate(tables):
                    currentTable = PDFTable(table)
                    currentTable.addText(tablestext[numberOfTable])
                    listOfTable.append(currentTable)
                y0 = None
                text = ""
                for i, char in enumerate(pages.chars):
                    if (char.get('y0') == y0):
                        text = text + char.get('text')
                        x1 = char.get('x1')
                        if i != 0:
                            if fontname != char.get('fontname'):
                                nochangeFontName = False
                                fontname = char.get('fontname')
                            if size != char.get('size'):
                                nochangeSize = False
                                size = char.get('size')
                            y1 = char.get('y1')
                        else:
                            fontname = char.get('fontname')
                            size = char.get('size')
                            y1 = char.get('y1')
                    else:
                        if i != 0:
                            # tableText = False
                            # for table in tables:
                            #     if y0 < (table.page.bbox[3] - table.bbox[1]) and y0 > (table.page.bbox[3] - table.bbox[3]):
                            #         tableText = True
                            lines.append(Line(x0, y0, x1, y1, text, fontname, size, nochangeFontName, nochangeSize,
                                              numberofpage + 1))
                        text = ""
                        text = text + char.get('text')
                        y0 = char.get('y0')
                        x0 = char.get('x0')
                        fontname = char.get('fontname')
                        size = char.get('size')
                        nochangeFontName = True
                        nochangeSize = True
                lines.append(
                    Line(x0, y0, x1, y1, text, fontname, size, nochangeFontName, nochangeSize, numberofpage + 1))
        print(lines)
        return lines, listOfTable

    def getSpace(self, lines):
        i = 0
        space = []
        while i < len(lines):
            if i != len(lines) - 1 and (lines[i].y0 - lines[i + 1].y1>0):
                space.append(lines[i].y0 - lines[i + 1].y1)
            else:
                space.append(9.12)
            i = i + 1
        return space
    def addParagraphInDocumentWithAttribute(self, paragraphline,id):
        fontname = paragraphline.lines[0].fontname
        size = paragraphline.lines[0].size
        nochangeFontName = paragraphline.lines[0].nochangeFontName
        nochangeSize = paragraphline.lines[0].nochangeSize
        for line in paragraphline.lines:
            if fontname != line.fontname or line.nochangeFontName == False:
                nochangeFontName = False
            if size != line.size or line.nochangeSize == False:
                nochangeSize = False
        paragraphline.textSize = size
        paragraphline.fontName = fontname
        paragraphline.nochangeFontName = nochangeFontName
        paragraphline.nochangeSize = nochangeSize
        paragraphline.indent = paragraphline.lines[0].x0
        self.document.content[id] = self.getStandartParagraph(paragraphline)


    def getParagraph(self, lines, spaces, listOfTable):
        i = 1
        paragraphline = ParagraphLine()
        paragraphline.lines.append(lines[0])
        paragraphline.spaces.append(spaces[0])
        id = 1
        mean = 0
        removedTables = []
        while i < len(lines):
            if i != len(lines) - 1:
                j = 0
                while j < len(paragraphline.lines):
                    mean = mean + spaces[j]
                    j = j + 1
                if len(paragraphline.lines) > 1:
                    mean = mean / len(paragraphline.lines)
                if lines[i-1].x0 < lines[i].x0 or lines[i-1].x1 <= 520 or abs(spaces[i] - mean) > 1:
                    if mean == 0:
                        mean = spaces[i]
                    paragraphline.lineSpacing = mean
                    insertTable = False
                    for removeTable in removedTables:
                        if paragraphline.lines[0].y0 < (removeTable.table.page.bbox[3] - removeTable.table.bbox[1]) and paragraphline.lines[0].y0 > (removeTable.table.page.bbox[3] - removeTable.table.bbox[3]) and removeTable.table.page.page_number == paragraphline.lines[0].page:
                            paragraphline = ParagraphLine()
                            paragraphline.lines.append(lines[i])
                            paragraphline.spaces.append(spaces[i])
                            insertTable = True
                    for numberOfTable, table in enumerate(listOfTable):
                        if paragraphline.lines[0].y0 < (table.table.page.bbox[3] - table.table.bbox[1]) and paragraphline.lines[0].y0 > (table.table.page.bbox[3] - table.table.bbox[3]) and table.table.page.page_number == paragraphline.lines[0].page:
                            self.document.content[id] = table
                            removedTables.append(table)
                            listOfTable.remove(table)
                            paragraphline = ParagraphLine()
                            id = id + 1
                            paragraphline.lines.append(lines[i])
                            paragraphline.spaces.append(spaces[i])
                            insertTable = True
                    if insertTable == True:
                        i = i + 1
                        continue
                    self.addParagraphInDocumentWithAttribute(paragraphline,id)
                    paragraphline = ParagraphLine()
                    id = id + 1
                    paragraphline.lines.append(lines[i])
                    paragraphline.spaces.append(spaces[i])
                else:
                    paragraphline.lines.append(lines[i])
                    paragraphline.spaces.append(spaces[i])
            else:
                paragraphline.lines.append(lines[i])
                paragraphline.spaces.append(spaces[i])
                if mean == 0:
                    mean = spaces[i]
                paragraphline.lineSpacing = mean
                self.addParagraphInDocumentWithAttribute(paragraphline,id)
                paragraphline = ParagraphLine()
                id = id + 1
            i = i + 1
            mean = 0
        print(self.document)

    def getStandartParagraph(self, paragraphLine):
        text = ""
        for line in paragraphLine.lines:
            text = text + line.text
        paragraph = Paragraph(text=text, indent=paragraphLine.indent, lineSpacing=paragraphLine.lineSpacing,
                              fontName=paragraphLine.fontName, textSize=paragraphLine.textSize,
                              nochangeTextSize=paragraphLine.nochangeTextSize,
                              nochangeFontName=paragraphLine.nochangeFontName)
        return paragraph
