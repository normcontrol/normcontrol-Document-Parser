from src.helpers.odt import consts
from src.odt.elements.ODTDocument import ODTDocument
from src.odt.ODTParser import ODTParser
from src.odt.elements.StylesContainer import StylesContainer

if __name__ == '__main__':
    doc_path = "documents/dipbac.odt"
    doc = ODTDocument(doc_path)
    odt_parser = ODTParser()
    styles_container = StylesContainer(doc)

    styles_container.build_dict()
    list = styles_container.get_nodes_with_style_full7(doc.document.text, consts.DEFAULT_PARAM)
    print(list)
