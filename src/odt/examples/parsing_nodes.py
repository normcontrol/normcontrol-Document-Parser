from src.helpers.odt import consts
from src.odt.elements.ODTDocument import ODTDocument
from src.odt.ODTParser import ODTParser

if __name__ == '__main__':
    doc_path = "/Users/vladtereshch/PycharmProjects/normcontrol-Document-Parser/src/odt/documents/tabl1.odt"
    doc = ODTDocument(doc_path)
    odt_parser = ODTParser(doc)

    list = odt_parser.get_document_nodes_with_higher_style_data(doc.document.text, consts.DEFAULT_PARAM)
    print(list)
    print(list["0"])