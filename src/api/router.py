from bestconfig import Config
from fastapi import APIRouter, Response, HTTPException
from starlette.requests import Request
from src.api.schemas import DocumentData
from src.classes.UnifiedDocumentView import UnifiedDocumentView
from src.helpers.errors.errors import NotAllowedFormatFileException
from src.PDF.PDFParser import PDFParser
from src.odt.elements.ODTDocument import ODTDocument
from src.odt.elements.ParsingReport import ParsingReport

parser_router = APIRouter(prefix="", tags=["parser"])


def allowed_file(filename):
    __config = Config('settings.ini').to_dict()
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in __config['Api']['ALLOWED_EXTENSIONS']


@parser_router.post('/parse_document')
async def parse_document(
    request: Request,
    document_data: DocumentData
):
    def parse_pdf():
        """
        Declare an object of the PDFParser class, in the initialization parameter,
        which will indicate the path to the pdf file
        """
        pdf_parser = PDFParser(document_data.path)
        lines = pdf_parser.lines
        spaces = pdf_parser.line_spaces
        tables = pdf_parser.list_of_table
        list_of_picture = pdf_parser.pictures
        '''
        Using the get_elements method, we get a file of the UnifiedDocumentView type, 
        which contains data about the entire text document and its structural elements
        '''
        document = pdf_parser.get_all_elements(lines, spaces, tables, list_of_picture)
        '''
        To create a JSON string from data about structural elements, which will later be sent to the classifier,
        use the create_json_to_clasifier method, which takes a list of required fields as parameters
        '''
        return document.create_json()

    def parse_odt():
        doc = ODTDocument(document_data.path)
        parsing_report = ParsingReport(doc)
        document = parsing_report.create_odt_report(doc)
        return document.create_json()

    if request.method == 'POST':
        if document_data.path == '':
            raise HTTPException(status_code=404, detail="Path not found")
        try:
            with open(document_data.path, "r") as file:
                filename = file.name
                file.close()
        except (FileNotFoundError, FileExistsError) as e:
            return e
        try:
            if filename and allowed_file(filename):
                if document_data.document_type == 'pdf':
                    return parse_pdf()
                if document_data.document_type == 'odt':
                    return parse_odt()
                if document_data.document_type == 'docx':
                    pass
            else:
                raise NotAllowedFormatFileException
        except NotAllowedFormatFileException as e:
            return e
    return "Only POST request is supported"


@parser_router.post('/parse_paragraph')
async def parse_paragraph(
    request: Request,
    document_data: DocumentData
):
    if request.method == 'POST':
        if document_data.path == '':
            raise HTTPException(status_code=404, detail="Path not found")
        try:
            with open(document_data.path, "r") as file:
                filename = file.name
                file.close()
        except (FileNotFoundError, FileExistsError) as e:
            return e
        try:
            if filename and allowed_file(filename):
                if document_data.document_type == 'pdf':
                    return PDFParser(document_data.path).paragraph_list
                if document_data.document_type == 'odt':
                    pass
                if document_data.document_type == 'docx':
                    pass
            else:
                raise NotAllowedFormatFileException
        except NotAllowedFormatFileException as e:
            return e
    return "Only POST request is supported"


@parser_router.post('/parse_images')
async def parse_images(
    request: Request,
    document_data: DocumentData
):
    if request.method == 'POST':
        if document_data.path == '':
            raise HTTPException(status_code=404, detail="Path not found")
        try:
            with open(document_data.path, "r") as file:
                filename = file.name
                file.close()
        except (FileNotFoundError, FileExistsError) as e:
            return e
        try:
            if filename and allowed_file(filename):
                if document_data.document_type == 'pdf':
                    return PDFParser(document_data.path).pictures
                if document_data.document_type == 'odt':
                    pass
                if document_data.document_type == 'docx':
                    pass
            else:
                raise NotAllowedFormatFileException
        except NotAllowedFormatFileException as e:
            return e
    return "Only POST request is supported"


@parser_router.post('/parse_table')
async def parse_table(
    request: Request,
    document_data: DocumentData
):
    if request.method == 'POST':
        if document_data.path == '':
            raise HTTPException(status_code=404, detail="Path not found")
        try:
            with open(document_data.path, "r") as file:
                filename = file.name
                file.close()
        except (FileNotFoundError, FileExistsError) as e:
            return e
        try:
            if filename and allowed_file(filename):
                if document_data.document_type == 'pdf':
                    return PDFParser(document_data.path).list_of_table
                if document_data.document_type == 'odt':
                    pass
                if document_data.document_type == 'docx':
                    pass
            else:
                raise NotAllowedFormatFileException
        except NotAllowedFormatFileException as e:
            return e
    return "Only POST request is supported"


@parser_router.post('/parse_list')
async def parse_list(
    request: Request,
    document_data: DocumentData
):
    if request.method == 'POST':
        if document_data.path == '':
            raise HTTPException(status_code=404, detail="Path not found")
        try:
            with open(document_data.path, "r") as file:
                filename = file.name
                file.close()
        except (FileNotFoundError, FileExistsError) as e:
            return e
        try:
            if filename and allowed_file(filename):
                if document_data.document_type == 'pdf':
                    return 'In progress'
                if document_data.document_type == 'odt':
                    pass
                if document_data.document_type == 'docx':
                    pass
            else:
                raise NotAllowedFormatFileException
        except NotAllowedFormatFileException as e:
            return e
    return "Only POST request is supported"
