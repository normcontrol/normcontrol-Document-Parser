import unittest

from src.pdf.PDFParser import PDFParser
from src.classes.Frame import Frame
from src.classes.Image import Image
from src.classes.Paragraph import Paragraph
from src.classes.Table import Table
from src.classes.TableCell import TableCell


class TestPDFParser(unittest.TestCase):
    path = 'documents\\Отчёт по практике для парсинга.pdf'
    pdf_parser = PDFParser(path=path)
    pdf_parser.get_all_elements(pdf_parser.lines, pdf_parser.line_spaces, pdf_parser.list_of_table, pdf_parser.pictures)

    def test_parse_content(self):
        self.assertEqual(len(self.pdf_parser.document.content), 211)
        self.assertEqual(self.pdf_parser.document.content[1],
                         Paragraph(_indent=7.88, _line_spacing=0.35, _alignment=None, _mrgrg=None, _mrglf=None,
                                   _mrgtop=None, _mrgbtm=None, _page_breake_before=None, _keep_lines_together=None,
                                   _keep_with_next=None, _outline_level=None, _font_name='TimesNewRomanPSMT',
                                   _text_size=14, _text='Введение ', _bold=None, _italics=None,
                                   _underlining=None, _sub_text=None, _super_text=None, _color_text=None,
                                   _no_change_fontname=True, _no_change_text_size=False))
        self.assertEqual(self.pdf_parser.document.content[23],
                         Paragraph(_indent=1.89, _line_spacing=0.37, _alignment=None, _mrgrg=None, _mrglf=None,
                                   _mrgtop=None, _mrgbtm=None, _page_breake_before=None, _keep_lines_together=None,
                                   _keep_with_next=None, _outline_level=None, _font_name='TimesNewRomanPSMT',
                                   _text_size=14, _text='− жесткий диск: HDD 40 Гб в RAID 1. ',
                                   _bold=None, _italics=None, _underlining=None, _sub_text=None, _super_text=None,
                                   _color_text=None, _no_change_fontname=False, _no_change_text_size=False))
        self.assertEqual(self.pdf_parser.document.content[38],
                         Frame(_indent=None, _line_spacing=None, _alignment=None, _mrgrg=None, _mrglf=None,
                               _mrgtop=None, _mrgbtm=None, _page_breake_before=None, _keep_lines_together=None,
                               _keep_with_next=None, _outline_level=None, _style_name=None, _anchor_type=None,
                               _bbox=(125.9, 484.07, 548.05, 736.92), _width=422.15, _height=422.15, _rel_width=None,
                               _rel_height=None, _image=Image(_href=None, _type='image', _show=None, _actuate=None),
                               _page_number=4))
        self.assertEqual(self.pdf_parser.document.content[62],
                         Table(_indent=None, _line_spacing=None, _alignment=None, _mrgrg=None, _mrglf=None,
                               _mrgtop=None, _mrgbtm=None, _page_breake_before=None, _keep_lines_together=None,
                               _keep_with_next=None, _outline_level=None,
                               _inner_text=[['Название признака', 'Тип', 'Свойство'], ['text', 'String', 'Текст'],
                                            ['PrevElementMark', 'String', 'Класс предыдущего элемента'],
                                            ['CurElementMark', 'String', 'Класс текущего элемента'],
                                            ['NextElementMark', 'String', 'Класс следующего элемента'],
                                            ['bold', 'Boolean', 'Жирный'], ['italics', 'Boolean', 'Курсив'],
                                            ['keep_together', 'Boolean', 'Не разрывать абзац'],
                                            ['keep_with_next', '', 'Не отрывать от следующего'],
                                            [None, 'Boolean', None], ['windows\\orphans', '', 'Висячие строки'],
                                            [None, 'Double', None]], _master_page_number=6, _family=None,
                               _width=467.49601999999993,
                               _bbox=(85.46399499999995, 496.86999999999995, 552.9600149999999, 725.283991),
                               _page_bbox=(0, 0, 595.32, 841.92), _cells=[
                                 TableCell(_name=None, _family=None, _border=None, _writing_mode=None,
                                           _padding_top=None, _padding_left=None, _padding_bottom=None,
                                           _padding_right=None, _text='Название признака'),
                                 TableCell(_name=None, _family=None, _border=None, _writing_mode=None,
                                           _padding_top=None, _padding_left=None, _padding_bottom=None,
                                           _padding_right=None, _text='Тип'),
                                 TableCell(_name=None, _family=None, _border=None, _writing_mode=None,
                                           _padding_top=None, _padding_left=None, _padding_bottom=None,
                                           _padding_right=None, _text='Свойство'),
                                 TableCell(_name=None, _family=None, _border=None, _writing_mode=None,
                                           _padding_top=None, _padding_left=None, _padding_bottom=None,
                                           _padding_right=None, _text='text'),
                                 TableCell(_name=None, _family=None, _border=None, _writing_mode=None,
                                           _padding_top=None, _padding_left=None, _padding_bottom=None,
                                           _padding_right=None, _text='String'),
                                 TableCell(_name=None, _family=None, _border=None, _writing_mode=None,
                                           _padding_top=None, _padding_left=None, _padding_bottom=None,
                                           _padding_right=None, _text='Текст'),
                                 TableCell(_name=None, _family=None, _border=None, _writing_mode=None,
                                           _padding_top=None, _padding_left=None, _padding_bottom=None,
                                           _padding_right=None, _text='PrevElementMark'),
                                 TableCell(_name=None, _family=None, _border=None, _writing_mode=None,
                                           _padding_top=None, _padding_left=None, _padding_bottom=None,
                                           _padding_right=None, _text='String'),
                                 TableCell(_name=None, _family=None, _border=None, _writing_mode=None,
                                           _padding_top=None, _padding_left=None, _padding_bottom=None,
                                           _padding_right=None, _text='Класс предыдущего элемента'),
                                 TableCell(_name=None, _family=None, _border=None, _writing_mode=None,
                                           _padding_top=None, _padding_left=None, _padding_bottom=None,
                                           _padding_right=None, _text='CurElementMark'),
                                 TableCell(_name=None, _family=None, _border=None, _writing_mode=None,
                                           _padding_top=None, _padding_left=None, _padding_bottom=None,
                                           _padding_right=None, _text='String'),
                                 TableCell(_name=None, _family=None, _border=None, _writing_mode=None,
                                           _padding_top=None, _padding_left=None, _padding_bottom=None,
                                           _padding_right=None, _text='Класс текущего элемента'),
                                 TableCell(_name=None, _family=None, _border=None, _writing_mode=None,
                                           _padding_top=None, _padding_left=None, _padding_bottom=None,
                                           _padding_right=None, _text='NextElementMark'),
                                 TableCell(_name=None, _family=None, _border=None, _writing_mode=None,
                                           _padding_top=None, _padding_left=None, _padding_bottom=None,
                                           _padding_right=None, _text='String'),
                                 TableCell(_name=None, _family=None, _border=None, _writing_mode=None,
                                           _padding_top=None, _padding_left=None, _padding_bottom=None,
                                           _padding_right=None, _text='Класс следующего элемента'),
                                 TableCell(_name=None, _family=None, _border=None, _writing_mode=None,
                                           _padding_top=None, _padding_left=None, _padding_bottom=None,
                                           _padding_right=None, _text='bold'),
                                 TableCell(_name=None, _family=None, _border=None, _writing_mode=None,
                                           _padding_top=None, _padding_left=None, _padding_bottom=None,
                                           _padding_right=None, _text='Boolean'),
                                 TableCell(_name=None, _family=None, _border=None, _writing_mode=None,
                                           _padding_top=None, _padding_left=None, _padding_bottom=None,
                                           _padding_right=None, _text='Жирный'),
                                 TableCell(_name=None, _family=None, _border=None, _writing_mode=None,
                                           _padding_top=None, _padding_left=None, _padding_bottom=None,
                                           _padding_right=None, _text='italics'),
                                 TableCell(_name=None, _family=None, _border=None, _writing_mode=None,
                                           _padding_top=None, _padding_left=None, _padding_bottom=None,
                                           _padding_right=None, _text='Boolean'),
                                 TableCell(_name=None, _family=None, _border=None, _writing_mode=None,
                                           _padding_top=None, _padding_left=None, _padding_bottom=None,
                                           _padding_right=None, _text='Курсив'),
                                 TableCell(_name=None, _family=None, _border=None, _writing_mode=None,
                                           _padding_top=None, _padding_left=None, _padding_bottom=None,
                                           _padding_right=None, _text='keep_together'),
                                 TableCell(_name=None, _family=None, _border=None, _writing_mode=None,
                                           _padding_top=None, _padding_left=None, _padding_bottom=None,
                                           _padding_right=None, _text='Boolean'),
                                 TableCell(_name=None, _family=None, _border=None, _writing_mode=None,
                                           _padding_top=None, _padding_left=None, _padding_bottom=None,
                                           _padding_right=None, _text='Не разрывать абзац'),
                                 TableCell(_name=None, _family=None, _border=None, _writing_mode=None,
                                           _padding_top=None, _padding_left=None, _padding_bottom=None,
                                           _padding_right=None, _text='keep_with_next'),
                                 TableCell(_name=None, _family=None, _border=None, _writing_mode=None,
                                           _padding_top=None, _padding_left=None, _padding_bottom=None,
                                           _padding_right=None, _text=''),
                                 TableCell(_name=None, _family=None, _border=None, _writing_mode=None,
                                           _padding_top=None, _padding_left=None, _padding_bottom=None,
                                           _padding_right=None, _text='Не отрывать от следующего'),
                                 TableCell(_name=None, _family=None, _border=None, _writing_mode=None,
                                           _padding_top=None, _padding_left=None, _padding_bottom=None,
                                           _padding_right=None, _text=None),
                                 TableCell(_name=None, _family=None, _border=None, _writing_mode=None,
                                           _padding_top=None, _padding_left=None, _padding_bottom=None,
                                           _padding_right=None, _text='Boolean'),
                                 TableCell(_name=None, _family=None, _border=None, _writing_mode=None,
                                           _padding_top=None, _padding_left=None, _padding_bottom=None,
                                           _padding_right=None, _text=None),
                                 TableCell(_name=None, _family=None, _border=None, _writing_mode=None,
                                           _padding_top=None, _padding_left=None, _padding_bottom=None,
                                           _padding_right=None, _text='windows\\orphans'),
                                 TableCell(_name=None, _family=None, _border=None, _writing_mode=None,
                                           _padding_top=None, _padding_left=None, _padding_bottom=None,
                                           _padding_right=None, _text='')], _rows=[]))
        self.assertEqual(self.pdf_parser.document.content[72],
                         Frame(_indent=None, _line_spacing=None, _alignment=None, _mrgrg=None, _mrglf=None,
                               _mrgtop=None, _mrgbtm=None, _page_breake_before=None, _keep_lines_together=None,
                               _keep_with_next=None, _outline_level=None, _style_name=None, _anchor_type=None,
                               _bbox=(90.45, 330.92, 558.2, 711.77), _width=467.75000000000006,
                               _height=467.75000000000006, _rel_width=None, _rel_height=None,
                               _image=Image(_href=None, _type='image', _show=None, _actuate=None), _page_number=8))

    def test_parse_pictures(self):
        self.assertEqual(len(self.pdf_parser.pictures), 12)
        self.assertEqual(self.pdf_parser.pictures[0],
                         Frame(_indent=None, _line_spacing=None, _alignment=None, _mrgrg=None, _mrglf=None,
                               _mrgtop=None, _mrgbtm=None,
                               _page_breake_before=None, _keep_lines_together=None, _keep_with_next=None,
                               _outline_level=None,
                               _style_name=None, _anchor_type=None, _bbox=(90.45, 465.39, 539.8000000000001, 736.92),
                               _width=449.3500000000001, _height=449.3500000000001, _rel_width=None, _rel_height=None,
                               _image=Image(_href=None, _type='image', _show=None, _actuate=None), _page_number=3))
        self.assertEqual(self.pdf_parser.pictures[5],
                         Frame(_indent=None, _line_spacing=None, _alignment=None, _mrgrg=None, _mrglf=None,
                               _mrgtop=None, _mrgbtm=None, _page_breake_before=None, _keep_lines_together=None,
                               _keep_with_next=None, _outline_level=None, _style_name=None, _anchor_type=None,
                               _bbox=(212.8, 171.76, 424.55, 785.23), _width=211.75, _height=211.75, _rel_width=None,
                               _rel_height=None, _image=Image(_href=None, _type='image', _show=None, _actuate=None),
                               _page_number=12))
        self.assertEqual(self.pdf_parser.pictures[10],
                         Frame(_indent=None, _line_spacing=None, _alignment=None, _mrgrg=None, _mrglf=None,
                               _mrgtop=None, _mrgbtm=None, _page_breake_before=None, _keep_lines_together=None,
                               _keep_with_next=None, _outline_level=None, _style_name=None, _anchor_type=None,
                               _bbox=(99.35, 300.37, 538.0, 562.86), _width=438.65, _height=438.65, _rel_width=None,
                               _rel_height=None, _image=Image(_href=None, _type='image', _show=None, _actuate=None),
                               _page_number=21))

    def test_parse_paragraphs(self):
        self.assertEqual(len(self.pdf_parser.paragraph_list), 195)
        self.assertEqual(self.pdf_parser.paragraph_list[4],
                         Paragraph(_indent=1.25, _line_spacing=0.37, _alignment=None, _mrgrg=None, _mrglf=None,
                                   _mrgtop=None, _mrgbtm=None, _page_breake_before=None, _keep_lines_together=None,
                                   _keep_with_next=None, _outline_level=None, _font_name='TimesNewRomanPSMT',
                                   _text_size=14,
                                   _text='− оптимизация работы процесса обмена информацией между клиентской частью и сервером; ',
                                   _bold=None, _italics=None, _underlining=None, _sub_text=None,
                                   _super_text=None, _color_text=None, _no_change_fontname=False,
                                   _no_change_text_size=False))
        self.assertEqual(self.pdf_parser.paragraph_list[52],
                         Paragraph(_indent=1.25, _line_spacing=0.41, _alignment=None, _mrgrg=None, _mrglf=None,
                                   _mrgtop=None, _mrgbtm=None, _page_breake_before=None, _keep_lines_together=None,
                                   _keep_with_next=None, _outline_level=None, _font_name='TimesNewRomanPSMT',
                                   _text_size=14, _text='Вся информация была разделена на следующие 3 категории: ',
                                   _bold=None, _italics=None, _underlining=None, _sub_text=None,
                                   _super_text=None, _color_text=None, _no_change_fontname=True,
                                   _no_change_text_size=False))
        self.assertEqual(self.pdf_parser.paragraph_list[92],
                         Paragraph(_indent=0.0, _line_spacing=0.4, _alignment=None, _mrgrg=None, _mrglf=None,
                                   _mrgtop=None, _mrgbtm=None, _page_breake_before=None, _keep_lines_together=None,
                                   _keep_with_next=None, _outline_level=None, _font_name='TimesNewRomanPSMT',
                                   _text_size=14,
                                   _text='посредством прохождения циклом по всем объектам списка параграфов; ',
                                   _bold=None, _italics=None, _underlining=None, _sub_text=None,
                                   _super_text=None, _color_text=None, _no_change_fontname=True,
                                   _no_change_text_size=False))

    def test_parse_tables(self):
        self.assertEqual(len(self.pdf_parser.list_of_table), 8)
        self.assertEqual(self.pdf_parser.list_of_table[0].bbox, (85.46399499999995, 496.86999999999995,
                                                                 552.9600149999999, 725.283991))
        self.assertEqual(self.pdf_parser.list_of_table[0].master_page_number, 6)
        self.assertEqual(self.pdf_parser.list_of_table[0].page_bbox, (0, 0, 595.32, 841.92))
        self.assertEqual(len(self.pdf_parser.list_of_table[0].table_cells), 32)

        self.assertEqual(self.pdf_parser.list_of_table[6].bbox,
                         (85.10400000000003, 597.5500099999999, 532.92002, 767.0160099999999))
        self.assertEqual(self.pdf_parser.list_of_table[6].master_page_number, 22)
        self.assertEqual(self.pdf_parser.list_of_table[6].page_bbox, (0, 0, 595.32, 841.92))
        self.assertEqual(len(self.pdf_parser.list_of_table[6].table_cells), 21)
