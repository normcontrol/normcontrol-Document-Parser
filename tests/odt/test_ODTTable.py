import unittest
from src.odt.ODTParser import ODTParser
from src.odt.elements.ODTDocument import ODTDocument
from src.classes.Table import Table
from src.classes.TableRow import TableRow
from src.classes.TableCell import TableCell

class TestODTTable(unittest.TestCase):
    def setUp(self) -> None:
        self.doc_path = "/Users/vladtereshch/PycharmProjects/normcontrol-Document-Parser/src/odt/documents/tabl1.odt"
        self.doc = ODTDocument(self.doc_path)
        self.odt_parser = ODTParser(self.doc)

    def test_get_table_styles(self):
        tables_styles = self.odt_parser.table_parser.get_table_styles(self.doc)
        self.assertEqual(len(tables_styles), 3)
        self.assertEqual(tables_styles[0], Table(_indent=None, _line_spacing=None, _alignment=None, _mrgrg=None,
                                                 _mrglf=None, _mrgtop=None, _mrgbtm=None, _page_breake_before=None,
                                                 _keep_lines_together=None, _keep_with_next=None, _outline_level=None,
                                                 _bbox=None, _inner_text=None, _master_page_number=None, _family=None,
                                                 _width=None, _page_bbox=None, _cells=[], _rows=[]))

    def test_get_automatic_table_styles(self):
        tables_styles = self.odt_parser.table_parser.get_automatic_table_styles(self.doc)
        self.assertEqual(len(tables_styles), 117)
        self.assertEqual(tables_styles[5], Table(_indent=None, _line_spacing=None, _alignment=None, _mrgrg=None,
                                                 _mrglf=None, _mrgtop=None, _mrgbtm=None, _page_breake_before=None,
                                                 _keep_lines_together=None, _keep_with_next=None, _outline_level=None,
                                                 _bbox=None, _inner_text=None, _master_page_number=None, _family=None,
                                                 _width=None, _page_bbox=None, _cells=[], _rows=[]))
        self.assertEqual(tables_styles[6], TableRow(_name=None, _family=None, _properties_min_height=None))
        self.assertEqual(tables_styles[7], TableCell(_name=None, _family=None, _border=None, _writing_mode=None,
                                                     _padding_top=None, _padding_left=None, _padding_bottom=None,
                                                     _padding_right=None, _text=None))

    def test_get_table_parameter(self):
        ast = self.odt_parser.automatic_style_parser.get_automatic_style_object_by_name(self.doc, 'Table1')
        self.assertEqual(self.odt_parser.table_parser.get_table_parameter(ast, 'width'), '6.8437in')
        self.assertEqual(self.odt_parser.table_parser.get_table_parameter(ast, 'align'), 'right')

    def test_get_table_cell_parameter(self):
        ast = self.odt_parser.automatic_style_parser.get_automatic_style_object_by_name(self.doc, 'TableCell395')
        self.assertEqual(self.odt_parser.table_parser.get_table_cell_parameter(ast, 'border'), '0.0069in solid #000000')
        self.assertEqual(self.odt_parser.table_parser.get_table_cell_parameter(ast, 'padding-top'), '0in')

    def test_get_table_row_parameter(self):
        ast = self.odt_parser.automatic_style_parser.get_automatic_style_object_by_name(self.doc, 'TableRow623')
        self.assertEqual(self.odt_parser.table_parser.get_table_row_parameter(ast, 'min-row-height'), '0.3361in')
        self.assertEqual(self.odt_parser.table_parser.get_table_row_parameter(ast, 'use-optimal-row-height'), 'false')

    def test_get_table_column_parameter(self):
        ast = self.odt_parser.automatic_style_parser.get_automatic_style_object_by_name(self.doc, 'TableColumn6')
        self.assertEqual(self.odt_parser.table_parser.get_table_column_parameter(ast, 'column-width'), '1.1368in')
        self.assertEqual(self.odt_parser.table_parser.get_table_column_parameter(ast, 'use-optimal-column-width'),
                         'false')