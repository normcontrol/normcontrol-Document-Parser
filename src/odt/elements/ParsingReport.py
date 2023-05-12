from src.classes.UnifiedDocumentView import UnifiedDocumentView
from src.helpers.odt import consts
from src.odt.elements.ODTDocument import ODTDocument
from src.odt.ODTParser import ODTParser
from src.odt.elements.StylesContainer import StylesContainer

class ParsingReport:
    def __init__(self, doc:ODTDocument):
        creator = doc._document.element_dict[('http://purl.org/dc/elements/1.1/', 'creator')][0].lastChild.data
        creation_date = doc._document.element_dict[('urn:oasis:names:tc:opendocument:xmlns:meta:1.0', 'creation-date')][0].lastChild.data
        page_count = doc._document.element_dict[('urn:oasis:names:tc:opendocument:xmlns:meta:1.0', 'document-statistic')][0].attributes[('urn:oasis:names:tc:opendocument:xmlns:meta:1.0', 'page-count')]
        self._unified_document = UnifiedDocumentView(owner=creator,
                                             time=creation_date,
                                             page_count=page_count)

    def create_odt_report(self, doc:ODTDocument):
        odt_parser = ODTParser()
        styles_container = StylesContainer(doc)

        styles_container.build_dict()
        all_doc_info = styles_container.get_nodes_with_style_full7(doc.document.text, consts.DEFAULT_PARAM)
        all_paragraphs = odt_parser.paragraph_parser.paragraphs_helper(styles_data=all_doc_info)
        all_frames = odt_parser.image_parser.get_frame_styles(doc)
        all_lists = odt_parser.list_parser.get_list_styles_from_automatic_styles(doc, all_doc_info)

        obj_id = 1
        for paragraph in all_paragraphs:
            self._unified_document.add_content(obj_id, paragraph)
            obj_id += 1
        for frame in all_frames:
            self._unified_document.add_content(obj_id, frame)
            obj_id += 1
        for list in all_lists:
            self._unified_document.add_content(obj_id, list)
            obj_id += 1
        return self._unified_document