from src.classes.DocumentClass import DocumentClass
from src.pdf.PDFParser import PDFParser
from os import walk

f = []
for dir_path, dir_names, file_names in walk('C:\\Users\\Slava\\PycharmProjects\\normcontrol-Document-Parser\\src\\pdf\\testpdfparser\\documents'):
    for filename in file_names:
        pdf_parser = PDFParser(path=dir_path+ '\\' + filename)
        lines = pdf_parser.lines
        spaces = pdf_parser.get_space(lines)
        tables = pdf_parser.list_of_table.copy()
        list_of_picture = pdf_parser.pictures
        document = pdf_parser.get_elements(lines, spaces, tables, list_of_picture)
        document.write_CSV(dir_path+ '\\' + filename + '.csv')
        json = document.create_json_to_clasifier()
        DocumentClass.request_to_clasify(json)