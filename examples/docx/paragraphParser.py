from src.docx.DocxParagraphParser import DocxParagraphParser
import os


for dir_path, dir_names, file_names in os.walk('.\\documents'):
    for filename in file_names:
        # path to file
        path = dir_path + '\\' + filename
        # Load document
        docx = DocxParagraphParser(path)
        list_of_paragraphs = docx.extract_paragraphs()
        list_of_table = docx.extract_tables()
        unified_document_view = docx.get_all_elements()
        json = unified_document_view.create_json()
