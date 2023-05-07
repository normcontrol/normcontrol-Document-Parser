import unittest
from src.odt.ODTParser import ODTParser
from src.odt.elements.ODTDocument import ODTDocument

class TestODTAutomaticStyle(unittest.TestCase):
    def setUp(self) -> None:
        self.doc_path = "documents/dipbac.odt"
        self.doc = ODTDocument(self.doc_path)
        self.odt_parser = ODTParser()

    def test_get_automatic_styles(self):
        automatic_styles = self.odt_parser.automatic_style_parser.get_automatic_styles(self.doc)
        list_of_styles = list(automatic_styles)
        self.assertEqual(len(automatic_styles), 922)
        self.assertEqual(automatic_styles[list_of_styles[0]], {'list-level-style-number/display-levels': '9',
                                               'list-level-style-number/level': '9',
                                               'list-level-style-number/num-format': '1',
                                               'list-level-style-number/num-suffix': '.',
                                               'list-level-style-number/start-value': '2', 'name': 'LFO1'})
        self.assertEqual(automatic_styles[list_of_styles[3]], {'list-level-style-number/level': '9',
                                                                     'list-level-style-number/num-format': 'i',
                                                                     'list-level-style-number/num-letter-sync': 'true',
                                                                     'list-level-style-number/num-suffix': '.',
                                                                     'name': 'LFO4'})

    def test_get_text_styles_from_automatic_styles(self):
        text_styles = self.odt_parser.automatic_style_parser.get_text_styles_from_automatic_styles(self.doc)
        list_of_styles = list(text_styles)
        self.assertEqual(len(text_styles), 922)
        self.assertEqual(text_styles[list_of_styles[22]], {'text-properties/font-weight': 'bold',
                                                           'text-properties/font-weight-asian': 'bold',
                                                           'text-properties/font-weight-complex': 'bold'})
        self.assertEqual(text_styles[list_of_styles[24]], {'text-properties/font-size': '16pt',
                                                           'text-properties/font-size-asian': '16pt',
                                                           'text-properties/font-size-complex': '16pt',
                                                           'text-properties/font-weight': 'bold',
                                                           'text-properties/font-weight-asian': 'bold'})

    def test_get_automatic_style_by_name(self):
        automatic_style = self.odt_parser.automatic_style_parser.get_automatic_style_by_name(self.doc, 'LFO2')
        self.assertEqual(automatic_style, {'list-level-style-number/level': '9',
                                           'list-level-style-number/num-format': 'i',
                                           'list-level-style-number/num-letter-sync': 'true',
                                           'list-level-style-number/num-suffix': '.', 'name': 'LFO2'})

    def test_get_automatic_style_object_by_name(self):
        ast = self.odt_parser.automatic_style_parser.get_automatic_style_object_by_name(self.doc, 'LFO2')
        parameter = self.odt_parser.list_parser.get_list_parameter(ast, 'num-letter-sync')
        self.assertEqual(parameter, "true")