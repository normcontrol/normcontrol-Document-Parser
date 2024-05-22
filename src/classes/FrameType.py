from dataclasses import dataclass
from src.classes.Image import Image
from src.classes.superclass.StructuralElement import StructuralElement


@dataclass
class FrameType(StructuralElement):
    _rId: str = None
    _width: float = None
    _height: float = None
    _anchorId: str = None
    _image: Image = None

    @property
    def rId(self):
        return self._rId

    @rId.setter
    def rId(self, value: str):
        self.rId = value

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
    def anchorId(self):
        return self._anchorId

    @anchorId.setter
    def anchorId(self, value: str):
        self._anchorId = value

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, value: Image):
        self._image = value
