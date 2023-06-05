from dataclasses import dataclass

@dataclass
class TableCell:
    """
    Description: Table cell class for ODT document.

    Attributes:
        _name: str
            The attribute specifies the name of a cell,
        _family: str
            The attribute specifies the family of a style (style:family),
        _border: float
            The attribute specifies the property for setting the same width, color, and style for
            all four borders, top, bottom, left, and right, of a box (style:table-cell-properties),
        _writing_mode: str
            The property applies only to formatting objects that set up a reference-area.
            Each value of writing-mode sets all three of the direction traits indicated in each of the value
            descriptions above on the reference-area,
        _padding_top: float
            The attribute specifies the width of the padding on the top-edge of a block-area or inline-area,
        _padding_left: float
            The attribute specifies the width of the padding on the left-edge of a block-area or inline-area,
        _padding_bottom: float
            The attribute specifies the width of the padding on the bottom-edge of a block-area or inline-area,
        _padding_right: float
            The attribute specifies the width of the padding on the right-edge of a block-area or inline-area.
        _text: str
            The attribute specifies the text in cell.
    """

    _name: str = None
    _family: str = None
    _border: float = None
    _writing_mode: str = None
    _padding_top: float = None
    _padding_left: float = None
    _padding_bottom: float = None
    _padding_right: float = None
    _text: str = None

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def family(self):
        return self._family

    @family.setter
    def family(self, value):
        self._family = value

    @property
    def border(self):
        return self._border

    @border.setter
    def border(self, value):
        self._border = value

    @property
    def writing_mode(self):
        return self._writing_mode

    @writing_mode.setter
    def writing_mode(self, value):
        self._writing_mode = value

    @property
    def padding_top(self):
        return self._padding_top

    @padding_top.setter
    def padding_top(self, value):
        self._padding_top = value

    @property
    def padding_left(self):
        return self._padding_left

    @padding_left.setter
    def padding_left(self, value):
        self._padding_left = value

    @property
    def padding_bottom(self):
        return self._padding_bottom

    @padding_bottom.setter
    def padding_bottom(self, value):
        self._padding_bottom = value

    @property
    def padding_right(self):
        return self._padding_right

    @padding_right.setter
    def padding_right(self, value):
        self._padding_right = value

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value
