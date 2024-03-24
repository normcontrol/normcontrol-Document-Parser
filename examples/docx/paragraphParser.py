from src.docx.DocxParagraphParser import DocxParagraphParser
import os


for dir_path, dir_names, file_names in os.walk('.\\documents'):
    try:
        for filename in file_names:
            # path to file
            path = dir_path + '\\' + filename
            # Load document
            docx = DocxParagraphParser(path)
            list_of_paragraphs = docx.extract_paragraphs()
            list_of_table = docx.extract_tables()
            unified_document_view = docx.get_all_elements()
            # unified_document_view.write_CSV()
            # json = unified_document_view.create_json()
            # split_paragraphs =docx.get_paragraphs_split_outline(list_of_paragraphs)
            # docx.get_json_split_paragraphs(split_paragraphs)
            print('')
    except Exception as e:
        print(e)
        raise e

