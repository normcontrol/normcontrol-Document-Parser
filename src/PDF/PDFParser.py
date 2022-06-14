import pdfplumber

from src.Class.DocumentClass import Class
from src.Class.Paragraph import Paragraph
from src.PDF.Line import Line
from src.PDF.ParagraphLine import ParagraphLine


class PDFParser:

    def getLine(self, path = "test.pdf"):
        with pdfplumber.open(path) as pdf:
            self.document = Class(owner=pdf.metadata.get('Author'), time=pdf.metadata.get('CreationDate'))
            for numberofpage,pages in enumerate(pdf.pages):
                y0 = None
                text = ""
                lines = []
                for i,char in enumerate(pages.chars):
                    if (char.get('y0') == y0) :
                        text = text + char.get('text')
                        y1 = char.get('y1')
                        x1 = char.get('x1')
                        if i != 0:
                            if fontname != char.get('fontname'):
                                nochangeFontName = False
                                fontname = char.get('fontname')
                            if size != char.get('size'):
                                nochangeSize = False
                                size = char.get('size')
                        else:
                            fontname = char.get('fontname')
                            size = char.get('size')
                    else:
                        if i != 0:
                            lines.append(Line(x0,y0,x1,y1,text,fontname,size,nochangeFontName,nochangeSize,numberofpage+1))
                        text = ""
                        text = text + char.get('text')
                        y0 = char.get('y0')
                        x0 = char.get('x0')
                        fontname = char.get('fontname')
                        size = char.get('size')
                        nochangeFontName = True
                        nochangeSize = True
                lines.append(Line(x0, y0, x1, y1, text,fontname,size,nochangeFontName,nochangeSize,numberofpage+1))
        print(lines)
        return lines


    def getSpace(self,lines):
        i=0
        space = []
        while i < len(lines):
            if i != len(lines) - 1:
                space.append(lines[i].y0 - lines[i + 1].y1)
            else:
                space.append(1.5)
            i = i+1
        return space

    def getParagraph(self,lines,spaces):
        i = 1
        paragraphline = ParagraphLine()
        paragraphline.lines.append(lines[0])
        paragraphline.spaces.append(spaces[0])
        id = 1
        mean = 0
        while i < len(lines):
            if i != len(lines) - 1:
                j = 0
                while j < len(paragraphline.lines):
                    if j !=0:
                        mean = mean + spaces[j]
                    else:
                        mean = spaces[j]
                    j= j+1
                if len(paragraphline.lines)>1:
                    mean = mean/len(paragraphline.lines)
                if lines[i-1].x0 >= lines[i].x0 and ((abs(spaces[i]-1 - mean < 1 or mean == 0)) or lines[i-1].page != lines[i].page):
                    paragraphline.lines.append(lines[i])
                    paragraphline.spaces.append(spaces[i])
                else:
                    paragraphline.lines.append(lines[i])
                    paragraphline.spaces.append(spaces[i])
                    if mean == 0:
                        mean = spaces[i]
                    paragraphline.lineSpacing = mean
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
                    self.document.d[id] = self.getStandartParagraph(paragraphline)
                    paragraphline = ParagraphLine()
                    id = id+1
            else:
                    paragraphline.lines.append(lines[i])
                    paragraphline.spaces.append(spaces[i])
                    if mean == 0:
                        mean = spaces[i]
                    paragraphline.lineSpacing = mean
                    fontname = paragraphline.lines[0].fontname
                    size = paragraphline.lines[0].size
                    nochangeFontName = paragraphline.lines[0].nochangeFontName
                    nochangeSize = paragraphline.lines[0].nochangeSize
                    for line in paragraphline.lines:
                        if fontname != line.fontname:
                            nochangeFontName = False
                        if size != line.size:
                            nochangeSize = False
                    paragraphline.textSize = size
                    paragraphline.fontName = fontname
                    paragraphline.nochangeFontName = nochangeFontName
                    paragraphline.nochangeSize = nochangeSize
                    paragraphline.indent = paragraphline.lines[0].x0
                    self.document.d[id] = self.getStandartParagraph(paragraphline)
                    paragraphline = ParagraphLine()
                    id = id+1
            i=i+1
            mean=0
        print(self.document)

    def getStandartParagraph(self,paragraphLine):
        text = ""
        for line in paragraphLine.lines:
            text = text + line.text
        paragraph = Paragraph(text = text,indent=paragraphLine.indent,lineSpacing=paragraphLine.lineSpacing,fontName=paragraphLine.fontName,textSize = paragraphLine.textSize,
                              nochangeTextSize= paragraphLine.nochangeTextSize,nochangeFontName=paragraphLine.nochangeFontName)
        return paragraph



