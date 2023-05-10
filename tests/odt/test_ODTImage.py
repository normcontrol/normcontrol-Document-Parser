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
        self.assertEqual(images_styles[0], Image(_href='media/image1.jpeg', _type='simple',
                                                 _show='embed', _actuate='onLoad'))

    def test_get_frame_styles(self):
        frames_styles = self.odt_parser.image_parser.get_frame_styles(self.doc)
        self.assertEqual(len(frames_styles), 8)
        self.assertEqual(frames_styles[0], Frame(_indent=None, _line_spacing=None, _alignment=None, _mrgrg=None,
                                                 _mrglf=None, _mrgtop=None, _mrgbtm=None, _page_breake_before=None,
                                                 _keep_lines_together=None, _keep_with_next=None, _outline_level=None,
                                                 _style_name='a0', _anchor_type='as-char',
                                                 _bbox=(0.0, 444.47861100000006, 742.4413350000001, 0.0),
                                                 _width=5.34515, _height=3.19999, _rel_width='scale',
                                                 _rel_height='scale', _image=Image(_href='media/image1.jpeg',
                                                 _type='simple', _show='embed', _actuate='onLoad'), _page_number=None))

    def test_get_image_parameter(self):
        self.assertEqual(self.odt_parser.image_parser.get_image_parameter(self.doc, 'image1', 'actuate'), 'onLoad')
        self.assertEqual(self.odt_parser.image_parser.get_image_parameter(self.doc, 'image1', 'type'), 'simple')

    def test_get_frame_parameter(self):
        self.assertEqual(self.odt_parser.image_parser.get_frame_parameter(self.doc, 'Рисунок_20_13', 'width'),
                         '5.34515in')
        self.assertEqual(self.odt_parser.image_parser.get_frame_parameter(self.doc, 'Рисунок_20_13', 'height'),
                         '3.19999in')