from src.odt.elements.ODTDocument import ODTDocument
from src.odt.ODTParser import ODTParser
from src.odt.elements.StylesContainer import StylesContainer

if __name__ == '__main__':
    doc_path = "documents/listsimages.odt"
    doc = ODTDocument(doc_path)
    odt_parser = ODTParser()

    print("Получение текста и автоматических стилей:\n")
    print(odt_parser.automatic_style_parser.get_automatic_styles(doc))
    print("-----------------------------------------\n")

    print("Получение стилей по умолчанию:\n")
    print(odt_parser.default_style_parser.get_default_styles(doc))

    print("Получение обычных стилей:\n")
    print(odt_parser.regular_style_parser.get_regular_styles(doc))

    print("Получение автоматических стилей по имени:\n")
    print(odt_parser.automatic_style_parser.get_automatic_style_by_name(doc, 'WW_CharLFO5LVL1'))
    print(odt_parser.automatic_style_parser.get_automatic_style_by_name(doc, 'WW_CharLFO8LVL1'))
    print(odt_parser.automatic_style_parser.get_automatic_style_by_name(doc, 'WW_CharLFO17LVL8'))

    print("Получение автоматических стилей списка по имени:\n")
    print(odt_parser.automatic_style_parser.get_automatic_style_by_name(doc, 'LFO2'))
    print(odt_parser.automatic_style_parser.get_automatic_style_by_name(doc, 'LFO5'))
    print(odt_parser.automatic_style_parser.get_automatic_style_by_name(doc, 'LFO16'))

    print("Получение конкретных характеристик списка с использованием автоматических стилей:\n")
    ast = odt_parser.automatic_style_parser.get_automatic_style_object_by_name(doc, 'LFO2')
    print(odt_parser.list_parser.get_list_parameter(ast, 'num-letter-sync'))

    ast = odt_parser.regular_style_parser.get_regular_style_object(doc, 'WW_CharLFO17LVL9')
    print(odt_parser.list_parser.get_list_parameter(ast, 'font-size'))
    print("-------------------------------------------\n")

    print("Печать всех узлов документа:")
    print(odt_parser.node_parser.print_all_document_nodes_with_style_data(doc.document.text, "", doc))
    print("-------------------------------------------\n")

    print("Печать всех стилей документа:")
    styles_container = StylesContainer(doc)
    print(styles_container.all_automatic_styles)
    print(styles_container.all_default_styles)
    print(styles_container.all_regular_styles)