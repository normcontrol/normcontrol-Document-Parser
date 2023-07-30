from bestconfig import Config
from fastapi import APIRouter, HTTPException
from starlette.requests import Request
from src.api.schemas import DocumentData
from src.classes.UnifiedDocumentView import UnifiedDocumentView
from src.docx.DocxParagraphParser import DocxParagraphParser
from src.helpers.errors.errors import NotAllowedFormatFileException
from src.pdf.PDFParser import PDFParser
from src.odt.ODTParser import ODTParser
from src.odt.elements.ODTDocument import ODTDocument

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
        tables = pdf_parser.tables
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
        odt_parser = ODTParser(doc)
        return odt_parser.get_all_elements().create_json()

    def parse_docx():
        docx = DocxParagraphParser(document_data.path)
        unified_document_view = docx.get_all_elements()
        return unified_document_view.create_json()

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
                    return parse_docx()
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
                    return PDFParser(document_data.path).paragraphs
                if document_data.document_type == 'odt':
                    pass
                if document_data.document_type == 'docx':
                    return DocxParagraphParser(document_data.path).paragraphs
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
                    return DocxParagraphParser(document_data.path).pictures
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
                    return PDFParser(document_data.path).tables
                if document_data.document_type == 'odt':
                    pass
                if document_data.document_type == 'docx':
                    return DocxParagraphParser(document_data.path).tables
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
                    return 'In progress'
                if document_data.document_type == 'docx':
                    return 'In progress'
            else:
                raise NotAllowedFormatFileException
        except NotAllowedFormatFileException as e:
            return e
    return "Only POST request is supported"
