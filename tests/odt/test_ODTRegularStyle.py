import unittest
from src.odt.ODTParser import ODTParser
from src.odt.elements.ODTDocument import ODTDocument

class TestODTRegularStyle(unittest.TestCase):
    def setUp(self) -> None:
        self.doc_path = "/Users/vladtereshch/PycharmProjects/normcontrol-Document-Parser/src/odt/documents/dipbac.odt"
        self.doc = ODTDocument(self.doc_path)
        self.odt_parser = ODTParser(self.doc)

    def test_get_regular_styles(self):
        regular_styles = self.odt_parser.regular_style_parser.get_regular_styles(self.doc)
        list_of_styles = list(regular_styles)
        self.assertEqual(len(regular_styles), 84)
        self.assertEqual(regular_styles[list_of_styles[0]], {'name': 'Заголовок1', 'display-name': 'Заголовок 1',
                                                             'family': 'paragraph', 'parent-style-name': 'Обычный',
                                                             'next-style-name': 'Обычный', 'auto-update': 'true',
                                                             'default-outline-level': '1',
                                                             'paragraph-properties/keep-with-next': 'always',
                                                             'paragraph-properties/line-height': '150%',
                                                             'paragraph-properties/margin-left': '0.0006in',
                                                             'paragraph-properties/text-indent': '-0.002in',
                                                             'text-properties/font-weight': 'bold',
                                                             'text-properties/font-weight-asian': 'bold',
                                                             'text-properties/font-weight-complex': 'bold',
                                                             'text-properties/font-size': '16pt',
                                                             'text-properties/font-size-asian': '16pt',
                                                             'text-properties/font-size-complex': '16pt',
                                                             'text-properties/hyphenate': 'false'})
        self.assertEqual(regular_styles[list_of_styles[2]], {'name': 'Обычный', 'display-name': 'Обычный',
                                                             'family': 'paragraph', 'auto-update': 'true',
                                                             'default-outline-level': '1',
                                                             'paragraph-properties/vertical-align': 'top',
                                                             'paragraph-properties/margin-bottom': '0in',
                                                             'paragraph-properties/line-height-at-least': '0.0006in',
                                                             'paragraph-properties/margin-left': '-0.0006in',
                                                             'paragraph-properties/text-indent': '-0.0006in',
                                                             'text-properties/font-name': 'Times New Roman',
                                                             'text-properties/font-name-asian': 'Times New Roman',
                                                             'text-properties/font-name-complex': 'Times New Roman',
                                                             'text-properties/text-position': '-4.1% 100%',
                                                             'text-properties/font-size': '12pt',
                                                             'text-properties/font-size-asian': '12pt',
                                                             'text-properties/font-size-complex': '12pt',
                                                             'text-properties/language-asian': 'ar',
                                                             'text-properties/country-asian': 'SA',
                                                             'text-properties/hyphenate': 'false'})

    def test_get_text_styles_from_regular_styles(self):
        regular_styles = self.odt_parser.regular_style_parser.get_text_styles_from_regular_styles(self.doc)
        list_of_styles = list(regular_styles)
        self.assertEqual(len(regular_styles), 84)
        self.assertEqual(regular_styles[list_of_styles[1]], {'text-properties/font-name': 'Cambria',
                                                             'text-properties/font-name-asian': 'Times New Roman',
                                                             'text-properties/font-name-complex': 'Times New Roman',
                                                             'text-properties/font-weight': 'bold',
                                                             'text-properties/font-weight-asian': 'bold',
                                                             'text-properties/font-weight-complex': 'bold',
                                                             'text-properties/color': '#4F81BD',
                                                             'text-properties/font-size': '13pt',
                                                             'text-properties/font-size-asian': '13pt',
                                                             'text-properties/font-size-complex': '13pt',
                                                             'text-properties/hyphenate': 'false'})
        self.assertEqual(regular_styles[list_of_styles[2]], {'text-properties/font-name': 'Times New Roman',
                                                            'text-properties/font-name-asian': 'Times New Roman',
                                                            'text-properties/font-name-complex': 'Times New Roman',
                                                            'text-properties/text-position': '-4.1% 100%',
                                                            'text-properties/font-size': '12pt',
                                                            'text-properties/font-size-asian': '12pt',
                                                            'text-properties/font-size-complex': '12pt',
                                                            'text-properties/language-asian': 'ar',
                                                            'text-properties/country-asian': 'SA',
                                                            'text-properties/hyphenate': 'false'})

    def test_get_regular_style(self):
        regular_styles = self.odt_parser.regular_style_parser.get_regular_style(self.doc, 'Обычный')
        self.assertEqual(regular_styles, {'name': 'Обычный', 'display-name': 'Обычный', 'family': 'paragraph',
                                          'auto-update': 'true', 'default-outline-level': '1',
                                          'paragraph-properties/vertical-align': 'top',
                                          'paragraph-properties/margin-bottom': '0in',
                                          'paragraph-properties/line-height-at-least': '0.0006in',
                                          'paragraph-properties/margin-left': '-0.0006in',
                                          'paragraph-properties/text-indent': '-0.0006in',
                                          'text-properties/font-name': 'Times New Roman',
                                          'text-properties/font-name-asian': 'Times New Roman',
                                          'text-properties/font-name-complex': 'Times New Roman',
                                          'text-properties/text-position': '-4.1% 100%',
                                          'text-properties/font-size': '12pt',
                                          'text-properties/font-size-asian': '12pt',
                                          'text-properties/font-size-complex': '12pt',
                                          'text-properties/language-asian': 'ar', 'text-properties/country-asian': 'SA',
                                          'text-properties/hyphenate': 'false'})

    def test_get_regular_style_object(self):
        regular_style_parameter = self.odt_parser.regular_style_parser.get_regular_style_object(self.doc,
                                                                                                'WW_CharLFO17LVL9')
        self.assertEqual(self.odt_parser.list_parser.get_list_parameter(regular_style_parameter, 'font-size'), '10pt')

    def test_get_paragraph_alignment(self):
        regular_style_alignment = self.odt_parser.regular_style_parser.get_paragraph_alignment(self.doc, 'Обычный')
        self.assertEqual(regular_style_alignment, None)
