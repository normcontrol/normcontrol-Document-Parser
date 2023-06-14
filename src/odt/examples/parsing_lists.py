from src.odt.elements.ODTDocument import ODTDocument
from src.odt.ODTParser import ODTParser
from src.helpers.odt import consts

if __name__ == '__main__':
    doc_path = "/Users/vladtereshch/PycharmProjects/normcontrol-Document-Parser/src/odt/documents/dipbac.odt"
    doc = ODTDocument(doc_path)
    odt_parser = ODTParser(doc)

    all_doc_info = odt_parser.get_document_nodes_with_higher_style_data(doc.document.text, consts.DEFAULT_PARAM)
    print(list)
    print(list["0"])

    print("Получение текста и автоматических стилей:\n")
    print(odt_parser.automatic_style_parser.get_automatic_styles(doc))
    print("-----------------------------------------\n")

    print("Получение стилей:\n")
    print(odt_parser.default_style_parser.get_default_styles(doc))

    print("--------------------1-----------------------")
    print(odt_parser.regular_style_parser.get_regular_styles(doc))

    print("--------------------2-----------------------")
    print(odt_parser.list_parser.get_lists_styles(doc), '\n')

    print("--------------------3-1---------------------")
    new_styles = odt_parser.list_parser.get_list_styles_from_automatic_styles(doc, all_doc_info)
    print((new_styles), '\n')

    print("--------------------3-2---------------------")
    print(odt_parser.automatic_style_parser.get_automatic_style_by_name(doc, 'WW_CharLFO5LVL1'))
    print(odt_parser.automatic_style_parser.get_automatic_style_by_name(doc, 'WW_CharLFO8LVL1'))
    print(odt_parser.automatic_style_parser.get_automatic_style_by_name(doc, 'WW_CharLFO17LVL8'))

    print("--------------------3-3---------------------")
    print(odt_parser.automatic_style_parser.get_automatic_style_by_name(doc, 'LFO2'))
    print(odt_parser.automatic_style_parser.get_automatic_style_by_name(doc, 'LFO5'))
    print(odt_parser.automatic_style_parser.get_automatic_style_by_name(doc, 'LFO16'))

    print("----------------------lists-------------------\n")
    print("Получение конкретных характеристик:")
    ast = odt_parser.automatic_style_parser.get_automatic_style_object_by_name(doc, 'LFO2')
    print(odt_parser.list_parser.get_list_parameter(ast, 'num-letter-sync'))

    ast = odt_parser.regular_style_parser.get_regular_style_object(doc, 'WW_CharLFO17LVL9')
    print("-------------------------------------------\n")

    auto_pars = odt_parser.paragraph_parser.paragraphs_helper(all_doc_info)
    print(auto_pars)