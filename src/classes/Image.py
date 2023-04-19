from dataclasses import dataclass
from src.classes.Frame import Frame

@dataclass
class Image:
    """
    Description: Image class for ODT document.

    Attributes:
        _image_href - attribute specifies the location of an embedded object,
        _image_type - attribute always has the value simple in OpenDocument document instances,
        _image_show - attribute is used to communicate the desired presentation of the ending resource on traversal
            from the starting resource,
        _image_actuate - attribute is used to communicate the desired timing of traversal from the starting resource
            to the ending resource,
        _image_frame - attribute storing the image frame.
    """

    _image_href: str
    _image_type: str
    _image_show: str
    _image_actuate: str

    @property
    def image_href(self):
        return self._image_href

    @image_href.setter
    def image_href(self, value):
        self._image_href = value

    @property
    def image_type(self):
        return self._image_type

    @image_type.setter
    def image_type(self, value):
        self._image_type = value

    @property
    def image_show(self):
        return self._image_show

    @image_show.setter
    def image_show(self, value):
        self._image_show = value

    @property
    def image_actuate(self):
        return self._image_actuate

    @image_actuate.setter
    def image_actuate(self, value):
        self._image_actuate = value