from src.odt.elements.ODTDocument import ODTDocument
from src.odt.elements.AutomaticStylesParser import AutomaticStylesParser
from src.odt.elements.DefaultStylesParser import DefaultStylesParser
from src.odt.elements.RegularStylesParser import RegularStylesParser
from src.odt.elements.ListsParser import ListsParser

if __name__ == '__main__':
    doc_path = "documents/listsimages.odt"
    doc = ODTDocument(doc_path)
    auto_styles_parser = AutomaticStylesParser()
    default_styles_parser = DefaultStylesParser()
    regular_styles_parser = RegularStylesParser()
    lists_parser = ListsParser()

    print("Получение текста и автоматических стилей:\n")
    print(auto_styles_parser.get_automatic_styles(doc))
    print("-----------------------------------------\n")

    print("Получение стилей:\n")
    print(default_styles_parser.get_default_styles(doc))

    print("--------------------1-----------------------")
    print(regular_styles_parser.get_regular_styles(doc))

    print("--------------------2-----------------------")
    print(lists_parser.get_list_styles(doc))

    print("--------------------3-----------------------")
    print(lists_parser.get_lists_text_styles(doc), '\n')

    print("--------------------3-1---------------------")
    print(lists_parser.get_list_styles_from_automatic_styles(doc), '\n')

    print("--------------------3-2---------------------")
    print(auto_styles_parser.get_automatic_style_by_name(doc, 'WW_CharLFO5LVL1'))
    print(auto_styles_parser.get_automatic_style_by_name(doc, 'WW_CharLFO8LVL1'))
    print(auto_styles_parser.get_automatic_style_by_name(doc, 'WW_CharLFO17LVL8'))

    print("--------------------3-3---------------------")
    print(auto_styles_parser.get_automatic_style_by_name(doc, 'LFO2'))
    print(auto_styles_parser.get_automatic_style_by_name(doc, 'LFO5'))
    print(auto_styles_parser.get_automatic_style_by_name(doc, 'LFO16'))

    print("----------------------lists-------------------\n")
    print("Получение конкретных характеристик:")
    ast = auto_styles_parser.get_automatic_style_object_by_name(doc, 'LFO2')
    print(lists_parser.get_list_parameter(ast, 'num-letter-sync'))

    ast = regular_styles_parser.get_regular_style_object(doc, 'WW_CharLFO17LVL9')
    print(lists_parser.get_list_parameter(ast, 'font-size'))
    print("-------------------------------------------\n")