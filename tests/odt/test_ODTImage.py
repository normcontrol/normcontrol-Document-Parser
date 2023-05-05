import unittest
from src.odt.ODTParser import ODTParser
from src.odt.elements.ODTDocument import ODTDocument
from src.classes.Image import Image
from src.classes.Frame import Frame

class TestODTImage(unittest.TestCase):
    def setUp(self) -> None:
        self.doc_path = "documents/listsimages.odt"
        self.doc = ODTDocument(self.doc_path)
        self.odt_parser = ODTParser()

    def test_get_image_styles(self):
        images_styles = self.odt_parser.image_parser.get_image_styles(self.doc)
        self.assertEqual(len(images_styles), 8)
        self.assertEqual(images_styles[0], Image(_image_href='media/image1.jpeg', _image_type='simple',
                                                 _image_show='embed', _image_actuate='onLoad'))

    def test_get_frame_styles(self):
        frames_styles = self.odt_parser.image_parser.get_frame_styles(self.doc)
        self.assertEqual(len(frames_styles), 8)
        self.assertEqual(frames_styles[0], Frame(_frame_style_name='a0', _frame_name='Рисунок_20_13',
                                                 _frame_anchor_type='as-char', _frame_x='0in', _frame_y='0in',
                                                 _frame_width='5.34515in', _frame_height='3.19999in',
                                                 _frame_rel_width='scale', _frame_rel_height='scale'))

    def test_get_image_parameter(self):
        self.assertEqual(self.odt_parser.image_parser.get_image_parameter(self.doc, 'image1', 'actuate'), 'onLoad')
        self.assertEqual(self.odt_parser.image_parser.get_image_parameter(self.doc, 'image1', 'type'), 'simple')

    def test_get_frame_parameter(self):
        self.assertEqual(self.odt_parser.image_parser.get_frame_parameter(self.doc, 'Рисунок_20_13', 'width'),
                         '5.34515in')
        self.assertEqual(self.odt_parser.image_parser.get_frame_parameter(self.doc, 'Рисунок_20_13', 'height'),
                         '3.19999in')