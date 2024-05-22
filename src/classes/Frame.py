from dataclasses import dataclass
from src.classes.Image import Image
from src.classes.superclass.StructuralElement import StructuralElement


@dataclass
class Frame(StructuralElement):
    """
    Description: Frame class for ODT document.

    Attributes:
    ----------
        _style_name: str
            attribute specifies the style of current frame,
        _anchor_type: str
            attribute specifies how a frame is bound to a text document,
        _width: float
            attribute specifies the width of the frame,
        _height: float
            attribute specifies the height of the frame,
        _rel_width: str
            attribute specifies height of a drawing object as a relative value within a frame,
        _rel_height: str
            attribute specifies the width of a drawing object as a relative value within a frame.
        _bbox: tuple
            attribute specifies x0, y0, x1, y1 position of frame in page
        _image: Image
            attribute specifies all image in frame
        _page_number: int
            attribute specifies number of page, witch contains this frame
    """

    _rId: str = None
    _style_name: str = None
    _anchor_type: str = None
    _width: float = None
    _height: float = None
    _rel_width: str = None
    _rel_height: str = None
    _image: Image = None
    _page_number: int = None
    _bbox: tuple[int | float, int | float, int | float, int | float] = None


    @property
    def rId(self):
        return self._rId

    @rId.setter
    def rId(self, value: str):
        self.rId = value

    @property
    def style_name(self):
        return self._style_name

    @style_name.setter
    def style_name(self, value):
        self._style_name = value


    @property
    def anchor_type(self):
        return self._anchor_type

    @anchor_type.setter
    def anchor_type(self, value):
        self._anchor_type = value

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value

    @property
    def rel_width(self):
        return self._rel_width

    @rel_width.setter
    def rel_width(self, value):
        self._rel_width = value

    @property
    def rel_height(self):
        return self._rel_height

    @rel_height.setter
    def rel_height(self, value):
        self._rel_height = value

    @property
    def bbox(self):
        return self._bbox

    @bbox.setter
    def bbox(self, value):
        self._bbox = value

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, value):
        self._image = value

    @property
    def page_number(self):
        return self._page_number

    @page_number.setter
    def page_number(self, value):
        self._page_number = value