from odf.opendocument import load
from odf.style import Style
from odf.table import Table
from guppy import hpy
import timing

from src.styles import Auto
from src.styles import Default
from src.styles import Style
from src import const

class TableParser():
    def __init__(self, file):
        self.filePath = file
        self.fileText = []

    # Получение текста таблицы
    def all_table_text(self):
        doc = load(self.filePath)
        for table in doc.getElementsByType(Table):
            self.fileText.append(table)
            print(table)

if __name__ == '__main__':
    h = hpy()
    h1 = h.heap()

    doc = TableParser('tabl1.odt')
    print("Получение текста и автоматических стилей:\n")
    print(Auto.get_styles(doc))
    print("-----------------------------------------\n")
    print("Получение стилей:\n")
    print(Default.get_styles(doc))
    print("--------------------1-----------------------")
    print(Style.get_styles_style(doc))
    print("--------------------2-----------------------")
    print(Style.get_styles_table(doc))
    print("--------------------3-----------------------")
    print(Auto.get_styles_automatic_styles_table(doc))
    print(Style.get_style(doc, 'TableColumn2'))
    print("----------------------table-------------------\n")
    print(Default.get_style_default(doc, 'table-column'))
    print(Default.get_style_default(doc, 'table-row'))
    print(Default.get_style_default(doc, 'table-cell'))
    print("-----------------------------------------\n")
    print(Auto.get_text_style_by_name(doc, 'TableCell599'))
    print("-------------------------------------------\n")
    print("Получение конкретных характеристик:")
    ast = Auto.get_style_by_name('tabl1.odt', 'TableCell395')
    print(Style.get_cellTable_param(ast, 'border'))

    ast = Auto.get_style_by_name('tabl1.odt', 'TableRow623')
    print(Style.get_rowTable_param(ast, 'use-optimal-row-height'))

    ast = Auto.get_style_by_name('tabl1.odt', 'TableColumn6')
    print(Style.get_columnTable_param(ast, 'column-width'))
    print("-------------------------------------------\n")

    h2 = h.heap()
    print(h2)
    print("\nMemory Usage After Creation Of Objects : ", h2.size - h1.size, " bytes")