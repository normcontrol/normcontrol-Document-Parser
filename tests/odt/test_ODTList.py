import unittest
from src.odt.ODTParser import ODTParser
from src.odt.elements.ODTDocument import ODTDocument
from src.classes.List import List

class TestODTList(unittest.TestCase):
    def setUp(self) -> None:
        self.doc_path = "documents/listsimages.odt"
        self.doc = ODTDocument(self.doc_path)
        self.odt_parser = ODTParser()

    def test_extract_table_objects(self):
        lists_styles = self.odt_parser.list_parser.get_lists_styles(self.doc)
        self.assertEqual(len(lists_styles), 56)
        self.assertEqual(lists_styles[1], List(_list_type='bulleted', _list_name='WW_CharLFO5LVL1', _list_level=None,
                                               _list_start_value=None, _list_style_char=None, _list_style_name=None,
                                               _list_style_data=None))

        lists_styles = self.odt_parser.list_parser.get_list_styles_from_automatic_styles(self.doc)
        self.assertEqual(len(lists_styles), 19)
        self.assertEqual(lists_styles[0], List(_list_type='numbered', _list_name='LFO1', _list_level='9',
                                               _list_start_value='2', _list_style_char=None, _list_style_name=None,
                                               _list_style_data=None))

    def test_extract_lists_parameters(self):
        ast = self.odt_parser.automatic_style_parser.get_automatic_style_object_by_name(self.doc, 'LFO2')
        self.assertEqual(self.odt_parser.list_parser.get_list_parameter(ast, 'num-letter-sync'), "true")

        ast = self.odt_parser.regular_style_parser.get_regular_style_object(self.doc, 'WW_CharLFO17LVL9')
        self.assertEqual(self.odt_parser.list_parser.get_list_parameter(ast, 'font-size'), "10pt")