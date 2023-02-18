from src.Class.DocumentClass import Class
from src.PDF.PDFParser import PDFParser
from os import walk

f = []
for dirpath, dirnames, filenames in walk('C:\\Users\\Slava\\Downloads\\Telegram Desktop\\MagiRemoved'):
#"Отчёт по практике для парсинга.pdf"
    for filename in filenames:
        pdfParser = PDFParser(path=dirpath+ '\\' + filename)
        lines, listOfTable = pdfParser.getLinesAndTables()
        spaces = pdfParser.getSpace(lines)
        document = pdfParser.getParagraph(lines,spaces,listOfTable)
        document.writeCSV(dirpath+ '\\' + filename + '.csv')
        # json = document.createJsonToClasifier()
        # Class.requestToClasify(json)
