import unittest
from src.odt.ODTParser import ODTParser
from src.odt.elements.ODTDocument import ODTDocument

class TestODTDefaultStyle(unittest.TestCase):
    def setUp(self) -> None:
        self.doc_path = "/Users/vladtereshch/PycharmProjects/normcontrol-Document-Parser/src/odt/documents/dipbac.odt"
        self.doc = ODTDocument(self.doc_path)
        self.odt_parser = ODTParser(self.doc)

    def test_get_default_styles(self):
        regular_styles = self.odt_parser.default_style_parser.get_default_styles(self.doc)
        list_of_styles = list(regular_styles)
        self.assertEqual(len(regular_styles), 6)
        self.assertEqual(regular_styles[list_of_styles[0]], {'family': 'table', 'table-properties/align': 'left',
                                                             'table-properties/border-model': 'collapsing',
                                                             'table-properties/margin-left': '0in',
                                                             'table-properties/writing-mode': 'lr-tb'})
        self.assertEqual(regular_styles[list_of_styles[5]], {'family': 'graphic', 'graphic-properties/fill': 'solid',
                                                             'graphic-properties/fill-color': '#4f81bd',
                                                             'graphic-properties/opacity': '100%',
                                                             'graphic-properties/stroke': 'solid',
                                                             'graphic-properties/stroke-width': '0.02778in',
                                                             'graphic-properties/stroke-color': '#385d8a',
                                                             'graphic-properties/stroke-opacity': '100%',
                                                             'graphic-properties/stroke-linecap': 'butt'})

    def test_get_default_style_by_family(self):
        regular_styles = self.odt_parser.default_style_parser.get_default_style_by_family(self.doc, 'graphic')
        self.assertEqual(regular_styles, {'family': 'graphic', 'graphic-properties/fill': 'solid',
                                          'graphic-properties/fill-color': '#4f81bd',
                                          'graphic-properties/opacity': '100%', 'graphic-properties/stroke': 'solid',
                                          'graphic-properties/stroke-width': '0.02778in',
                                          'graphic-properties/stroke-color': '#385d8a',
                                          'graphic-properties/stroke-opacity': '100%',
                                          'graphic-properties/stroke-linecap': 'butt'})

    def test_get_default_style_object_by_family(self):
        regular_styles = self.odt_parser.default_style_parser.get_default_style_object_by_family(self.doc, 'graphic')
        self.assertEqual(len(regular_styles.allowed_children), 11)

    def test_get_default_style_parameters(self):
        ast = self.odt_parser.default_style_parser.get_default_style_object_by_family(self.doc, 'graphic')
        regular_style_parameter = self.odt_parser.default_style_parser.get_default_style_parameters(ast,
                                                                                        'graphic-properties', 'fill')
        self.assertEqual(regular_style_parameter, None)