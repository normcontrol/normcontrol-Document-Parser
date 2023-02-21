from src.Class.DocumentClass import Class
from src.PDF.PDFParser import PDFParser
from os import walk

f = []
for dir_path, dir_names, file_names in walk('C:\\Users\\Slava\\Downloads\\Telegram Desktop\\MagiRemoved'):
    for filename in file_names:
        pdf_parser = PDFParser(path=dir_path+ '\\' + filename)
        lines, list_of_table = pdf_parser.get_lines_and_tables()
        spaces = pdf_parser.get_space(lines)
        document = pdf_parser.get_paragraph(lines,spaces,list_of_table)
        document.write_CSV(dir_path+ '\\' + filename + '.csv')
        json = document.createJsonToClasifier()
        Class.requestToClasify(json)
