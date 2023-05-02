import unittest
from src.odt.ODTParser import ODTParser
from src.odt.elements.ODTDocument import ODTDocument
from src.classes.Table import Table
from src.classes.TableColumn import TableColumn
from src.classes.TableRow import TableRow
from src.classes.TableCell import TableCell

class TestODTTable(unittest.TestCase):
    def setUp(self) -> None:
        self.doc_path = "documents/tabl1.odt"
        self.doc = ODTDocument(self.doc_path)
        self.odt_parser = ODTParser()

    def test_extract_table_objects(self):
        tables_styles = self.odt_parser.table_parser.get_table_styles(self.doc)
        self.assertEqual(len(tables_styles), 3)
        self.assertEqual(tables_styles[0], Table(_table_name='Обычный', _table_family=None,
                                          _table_master_page_name=None, _table_properties_width=None,
                                          _table_properties_margin_left=None, _table_properties_align=None,
                                          _table_cells=[], _table_columns=[], _table_rows=[]))

        tables_styles = self.odt_parser.table_parser.get_automatic_table_styles(self.doc)
        self.assertEqual(len(tables_styles), 117)
        self.assertEqual(tables_styles[0], TableColumn(_column_name='TableColumn2', _column_family='table-column',
                                                       _column_properties_column_width=1.277,
                                                       _column_properties_use_optimal_column_width=False))
        self.assertEqual(tables_styles[6], TableRow(_row_name='TableRow7', _row_family='table-row',
                                                    _row_properties_min_row_height=0.6729,
                                                    _row_properties_use_optimal_row_height=False))
        self.assertEqual(tables_styles[7], TableCell(_cell_name='TableCell8', _cell_family='table-cell',
                                                     _cell_properties_border=0.0069,
                                                     _cell_properties_writing_mode='lr-tb',
                                                     _cell_properties_padding_top=0.0,
                                                     _cell_properties_padding_left=0.0,
                                                     _cell_properties_padding_bottom=0.0,
                                                     _cell_properties_padding_right=0.0))

    def test_extract_table_parameters(self):
        ast = self.odt_parser.automatic_style_parser.get_automatic_style_object_by_name(self.doc, 'TableCell395')
        self.assertEqual(self.odt_parser.table_parser.get_table_cell_parameter(ast, 'border'), "0.0069in solid #000000")

        ast = self.odt_parser.automatic_style_parser.get_automatic_style_object_by_name(self.doc, 'TableRow623')
        self.assertEqual(self.odt_parser.table_parser.get_table_row_parameter(ast, 'use-optimal-row-height'), "false")

        ast = self.odt_parser.automatic_style_parser.get_automatic_style_object_by_name(self.doc, 'TableColumn6')
        self.assertEqual(self.odt_parser.table_parser.get_table_column_parameter(ast, 'column-width'), "1.1368in")