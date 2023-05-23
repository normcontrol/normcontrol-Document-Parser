from dataclasses import dataclass


@dataclass
class Image:
    """
    Description: Image class for ODT document.

    Attributes:
        _href - attribute specifies the location of an embedded object,
        _type - attribute always has the value simple in OpenDocument document instances,
        _show - attribute is used to communicate the desired presentation of the ending resource on traversal
            from the starting resource,
        _actuate - attribute is used to communicate the desired timing of traversal from the starting resource
            to the ending resource,
    """

    _href: str = None
    _type: str = None
    _show: str = None
    _actuate: str = None

    @property
    def href(self):
        return self._href

    @href.setter
    def href(self, value):
        self._href = value

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = value

    @property
    def show(self):
        return self._show

    @show.setter
    def show(self, value):
        self._show = value

    @property
    def actuate(self):
        return self._actuate

    @actuate.setter
    def actuate(self, value):
        self._actuate = value