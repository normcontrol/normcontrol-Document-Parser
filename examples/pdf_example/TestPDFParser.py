from src.classes.UnifiedDocumentView import UnifiedDocumentView
from src.pdf.PDFParser import PDFParser
from os import walk
from requests.exceptions import ConnectionError

for dir_path, dir_names, file_names in walk('.\\documents'):
    for filename in file_names:
        '''
        Declare an object of the PDFParser class, in the initialization parameter,
        which will indicate the path to the pdf file
        '''
        pdf_parser = PDFParser(path=dir_path + '\\' + filename)
        lines = pdf_parser.lines
        spaces = pdf_parser.line_spaces
        tables = pdf_parser.list_of_table
        list_of_picture = pdf_parser.pictures
        '''
        Using the get_elements method, we get a file of the UnifiedDocumentView type, 
        which contains data about the entire text document and its structural elements
        '''
        document = pdf_parser.get_elements(lines, spaces, tables, list_of_picture)
        # To write information about structural elements, use the write_CSV method, specifying the save path
        document.write_CSV(dir_path + '\\' + filename + '.csv')
        '''
        To create a JSON string from data about structural elements, which will later be sent to the classifier,
        use the create_json_to_clasifier method, which takes a list of required fields as parameters
        '''
        json = document.create_json_to_clasifier()
        '''
        To send data to the classifier, use the request_to_clasify method, specifying the string in the json parameters
        '''
        try:
            UnifiedDocumentView.request_to_clasify(json)
        except ConnectionError:
            print("No connection with clasifier")