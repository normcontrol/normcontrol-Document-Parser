import csv
import sys
import traceback
import xml
import zipfile
from datetime import time, datetime

from src.docx.DocxParagraphParser import DocxParagraphParser
import os

# documents_for_extract
for dir_path, dir_names, file_names in os.walk('.\\for_test'):

        length = len(file_names)
        for i, filename in enumerate(file_names):
            try:
                # path to file
                print(f'Обрабатывается {i+1} файл из {length}')
                path = dir_path + '\\' + filename
                # Load document
                docx = DocxParagraphParser(path)
                # list_of_paragraphs = docx.extract_paragraphs()
                # list_of_table = docx.extract_tables()
                unified_document_view = docx.get_all_elements()
                # unified_document_view.write_CSV()
                # json = unified_document_view.create_json()
                # split_paragraphs =docx.get_paragraphs_split_outline(list_of_paragraphs)
                # docx.get_json_split_paragraphs(split_paragraphs)
                print('')
            except Exception as e:
                # patherr = 'error.csv'
                # with open(patherr, 'a', newline='', encoding="utf-8") as csvfile:
                #     filewriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
                #     # *sys.exc_info()
                #     filewriter.writerow([datetime.now(), filename])
                #     filewriter.writerow([traceback.format_exc()])
                #     filewriter.writerow('')
                traceback.print_exc()
                print(file_names)


