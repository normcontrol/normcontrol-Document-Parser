from src.odt.elements.ODTDocument import ODTDocument
from src.odt.ODTParser import ODTParser

if __name__ == '__main__':
    doc_path = "documents/tabl1.odt"
    doc = ODTDocument(doc_path)
    odt_parser = ODTParser()

    print("Получение текста и автоматических стилей:\n")
    print(odt_parser.automatic_style_parser.get_automatic_styles(doc))
    print("-----------------------------------------\n")

    print("Получение стилей:\n")
    print(odt_parser.default_style_parser.get_default_styles(doc))

    print("--------------------1-----------------------")
    print(odt_parser.regular_style_parser.get_regular_styles(doc))

    print("--------------------2-----------------------")
    print(odt_parser.table_parser.get_table_styles(doc))

    print("--------------------3-----------------------")
    print(odt_parser.table_parser.get_automatic_table_styles(doc))
    print(odt_parser.regular_style_parser.get_regular_style(doc, 'TableColumn2'))

    print("----------------------tables-------------------\n")
    print(odt_parser.default_style_parser.get_default_style_by_family(doc, 'table-column'))
    print(odt_parser.default_style_parser.get_default_style_by_family(doc, 'table-row'))
    print(odt_parser.default_style_parser.get_default_style_by_family(doc, 'table-cell'))
    print("-----------------------------------------\n")

    print(odt_parser.automatic_style_parser.get_text_style_by_name(doc, 'TableCell599'))
    print("-------------------------------------------\n")

    print("Получение конкретных характеристик:")
    ast = odt_parser.automatic_style_parser.get_automatic_style_object_by_name(doc, 'TableCell395')
    print(odt_parser.table_parser.get_table_cell_parameter(ast, 'border'))

    ast = odt_parser.automatic_style_parser.get_automatic_style_object_by_name(doc, 'TableRow623')
    print(odt_parser.table_parser.get_table_row_parameter(ast, 'use-optimal-row-height'))

    ast = odt_parser.automatic_style_parser.get_automatic_style_object_by_name(doc, 'TableColumn6')
    print(odt_parser.table_parser.get_table_column_parameter(ast, 'column-width'))
    print("-------------------------------------------\n")