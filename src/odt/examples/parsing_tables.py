from src.odt.elements.ODTDocument import ODTDocument
from src.odt.elements.AutomaticStylesParser import AutomaticStylesParser
from src.odt.elements.DefaultStylesParser import DefaultStylesParser
from src.odt.elements.RegularStylesParser import RegularStylesParser
from src.odt.elements.TablesParser import TablesParser

if __name__ == '__main__':
    doc_path = "documents/tabl1.odt"
    doc = ODTDocument(doc_path)
    auto_styles_parser = AutomaticStylesParser()
    default_styles_parser = DefaultStylesParser()
    regular_styles_parser = RegularStylesParser()
    tables_parser = TablesParser()

    print("Получение текста и автоматических стилей:\n")
    print(auto_styles_parser.get_automatic_styles(doc))
    print("-----------------------------------------\n")

    print("Получение стилей:\n")
    print(default_styles_parser.get_default_styles(doc))

    print("--------------------1-----------------------")
    print(regular_styles_parser.get_regular_styles(doc))

    print("--------------------2-----------------------")
    print(tables_parser.get_table_styles(doc))

    print("--------------------3-----------------------")
    print(tables_parser.get_automatic_table_styles(doc))
    print(regular_styles_parser.get_regular_style(doc, 'TableColumn2'))

    print("----------------------tables-------------------\n")
    print(default_styles_parser.get_default_style_by_family(doc, 'table-column'))
    print(default_styles_parser.get_default_style_by_family(doc, 'table-row'))
    print(default_styles_parser.get_default_style_by_family(doc, 'table-cell'))
    print("-----------------------------------------\n")

    print(auto_styles_parser.get_text_style_by_name(doc, 'TableCell599'))
    print("-------------------------------------------\n")

    print("Получение конкретных характеристик:")
    ast = auto_styles_parser.get_automatic_style_object_by_name(doc, 'TableCell395')
    print(tables_parser.get_table_cell_parameter(ast, 'border'))

    ast = auto_styles_parser.get_automatic_style_object_by_name(doc, 'TableRow623')
    print(tables_parser.get_table_row_parameter(ast, 'use-optimal-row-height'))

    ast = auto_styles_parser.get_automatic_style_object_by_name(doc, 'TableColumn6')
    print(tables_parser.get_table_column_parameter(ast, 'column-width'))
    print("-------------------------------------------\n")