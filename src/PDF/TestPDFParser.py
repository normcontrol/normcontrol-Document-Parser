from src.PDF.PDFParser import PDFParser

pdfParser = PDFParser()
lines = pdfParser.getLine()
space = pdfParser.getSpace(lines)
listofParagraph = pdfParser.getParagraph(lines,space)