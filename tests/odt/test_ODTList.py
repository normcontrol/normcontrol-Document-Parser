import unittest

from src.helpers.odt import consts
from src.odt.ODTParser import ODTParser
from src.odt.elements.ODTDocument import ODTDocument
from src.classes.List import List

class TestODTList(unittest.TestCase):
    def setUp(self) -> None:
        self.doc_path = "/Users/vladtereshch/PycharmProjects/normcontrol-Document-Parser/src/odt/documents/listsimages.odt"
        self.doc = ODTDocument(self.doc_path)
        self.odt_parser = ODTParser(self.doc)
        self.all_doc_info = self.odt_parser.get_document_nodes_with_higher_style_data(self.doc.document.text,
                                                                                 consts.DEFAULT_PARAM)

    def test_get_lists_styles(self):
        lists_styles = self.odt_parser.list_parser.get_lists_styles(self.doc, self.all_doc_info)
        self.assertEqual(len(lists_styles), 0)

    def test_get_list_styles_from_automatic_styles(self):
        lists_styles = self.odt_parser.list_parser.get_list_styles_from_automatic_styles(self.doc, self.all_doc_info)
        self.assertEqual(len(lists_styles), 10)
        self.assertEqual(lists_styles[0], List(_indent=0.0, _line_spacing=1.0, _alignment=None, _mrgrg=0.0,
                                               _mrglf=0.0, _mrgtop=0.0, _mrgbtm=0.0, _page_breake_before=None,
                                               _keep_lines_together=False, _keep_with_next=False, _outline_level=None,
                                               _bbox=None, _text='Система должна эмулировать потенциальные складские'
                                                                 ' помещения.Тест подсписка первого вложенияТест 2'
                                                                 ' подсписка первого вложенияТест подсписка второго'
                                                                 ' вложенияТест подсписка третьего вложенияТест 2'
                                                                 ' подсписка третьего вложенияТест подсписка четвертого'
                                                                 ' вложенияНеобходимо реализовать среду, в которой'
                                                                 ' происходят все наблюдения и с которой взаимодействует'
                                                                 ' агент.Требуется изучить существующие алгоритмы'
                                                                 ' обучения с подкреплением, реализовать их и сравнить'
                                                                 ' полученные результаты.', _bold=False, _italics=False,
                                               _underlining=False, _sub_text=False, _super_text=False,
                                               _color_text='#000000', _no_change_fontname=None,
                                               _no_change_text_size=None, _font_name=['Calibry'], _text_size=[11.0],
                                               _type=None, _name='LFO1', _level='9', _start_value='label-alignment',
                                               _style_char=None, _style_name=None))

    def test_get_list_parameter_from_automatic_styles(self):
        ast = self.odt_parser.automatic_style_parser.get_automatic_style_object_by_name(self.doc, 'LFO2')
        self.assertEqual(self.odt_parser.list_parser.get_list_parameter(ast, 'num-letter-sync'), 'true')
        self.assertEqual(self.odt_parser.list_parser.get_list_parameter(ast, 'num-suffix'), '.')

    def test_get_list_parameter_from_regular_styles(self):
        ast = self.odt_parser.regular_style_parser.get_regular_style_object(self.doc, 'WW_CharLFO17LVL9')
        self.assertEqual(self.odt_parser.list_parser.get_list_parameter(ast, 'font-size'), '10pt')
        self.assertEqual(self.odt_parser.list_parser.get_list_parameter(ast, 'font-name'), 'Wingdings')