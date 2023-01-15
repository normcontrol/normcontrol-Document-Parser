from guppy import hpy
from src.odt.styles import Style, Auto, Default
import os

def create_path(abs_path, rel_path):
    script_dir = str.split(abs_path, '/')
    path = ''
    ind = 0
    while ind < len(script_dir) - 2:
        path += script_dir[ind]
        path += '/'
        ind += 1
    return path + rel_path

class ListParser:
    def __init__(self, file):
        self.filePath = file
        self.fileText = []

if __name__ == '__main__':
    h = hpy()
    h1 = h.heap()

    script_path = os.path.abspath(__file__)
    rel_path = "documents/listsimages.odt"
    doc = ListParser(create_path(script_path, rel_path))
    print("Получение текста и автоматических стилей:\n")
    print(Auto.get_styles(doc))
    print("-----------------------------------------\n")
    print("Получение стилей:\n")
    print(Default.get_styles(doc))
    print("--------------------1-----------------------")
    print(Style.get_styles_style(doc))
    print("--------------------2-----------------------")
    print(Style.get_styles_list(doc))
    print("--------------------3-----------------------")
    print(Style.get_styles_listText(doc), '\n')
    print("--------------------3-1---------------------")
    print(Auto.get_styles_automatic_styles_list(doc), '\n')
    print("--------------------3-2---------------------")
    print(Auto.get_styles_automatic_listsText(doc), '\n')
    print(Auto.get_style_automatic_by_name(doc, 'WW_CharLFO5LVL1'))
    print(Auto.get_style_automatic_by_name(doc, 'WW_CharLFO8LVL1'))
    print(Auto.get_style_automatic_by_name(doc, 'WW_CharLFO17LVL8'))
    print("--------------------3-3---------------------")
    print(Auto.get_style_automatic_by_name(doc, 'LFO2'))
    print(Auto.get_style_automatic_by_name(doc, 'LFO5'))
    print(Auto.get_style_automatic_by_name(doc, 'LFO16'))
    print("----------------------lists-------------------\n")
    print("Получение конкретных характеристик:")
    ast = Auto.get_style_by_name('/Users/vladtereshch/PycharmProjects/normcontrol-Document-Parser/src/odt/'
                                 'documents/listsimages.odt', 'LFO2')
    print(Style.get_list_param(ast, 'num-letter-sync'))

    ast = Style.get_style_new('/Users/vladtereshch/PycharmProjects/normcontrol-Document-Parser/src/odt/'
                              'documents/listsimages.odt', 'WW_CharLFO17LVL9')
    print(Style.get_list_param(ast, 'font-size'))
    print("-------------------------------------------\n")

    h2 = h.heap()
    print(h2)
    print("\nMemory Usage After Creation Of Objects : ", h2.size - h1.size, " bytes")