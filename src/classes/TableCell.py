from dataclasses import dataclass

@dataclass
class TableCell:
    """
    Description: Table cell class for ODT document.

    Attributes:
        _cell_name - attribute specifies the name of a cell,
        _cell_family - attribute specifies the family of a style (style:family),
        _cell_properties_border - attribute specifies the property for setting the same width, color, and style for
            all four borders, top, bottom, left, and right, of a box (style:table-cell-properties),
        _cell_properties_writing_mode - the property applies only to formatting objects that set up a reference-area.
            Each value of writing-mode sets all three of the direction traits indicated in each of the value
            descriptions above on the reference-area,
        _cell_properties_padding_top - specifies the width of the padding on the top-edge of a block-area
            or inline-area,
        _cell_properties_padding_left - Specifies the width of the padding on the left-edge of a block-area
            or inline-area,
        _cell_properties_padding_bottom - specifies the width of the padding on the bottom-edge of a block-area
            or inline-area,
        _cell_properties_padding_right - specifies the width of the padding on the right-edge of a block-area
            or inline-area.
    """

    _cell_name: str
    _cell_family: str
    _cell_properties_border: float
    _cell_properties_writing_mode: str
    _cell_properties_padding_top: float
    _cell_properties_padding_left: float
    _cell_properties_padding_bottom: float
    _cell_properties_padding_right: float

    @property
    def cell_name(self):
        return self._cell_name

    @cell_name.setter
    def cell_name(self, value):
        self._cell_name = value

    @property
    def cell_family(self):
        return self._cell_family

    @cell_family.setter
    def cell_family(self, value):
        self._cell_family = value

    @property
    def cell_properties_border(self):
        return self._cell_properties_border

    @cell_properties_border.setter
    def cell_properties_border(self, value):
        self._cell_properties_border = value

    @property
    def cell_properties_writing_mode(self):
        return self._cell_properties_writing_mode

    @cell_properties_writing_mode.setter
    def cell_properties_writing_mode(self, value):
        self._cell_properties_writing_mode = value

    @property
    def cell_properties_padding_top(self):
        return self._cell_properties_padding_top

    @cell_properties_padding_top.setter
    def cell_properties_padding_top(self, value):
        self._cell_properties_padding_top = value

    @property
    def cell_properties_padding_left(self):
        return self._cell_properties_padding_left

    @cell_properties_padding_left.setter
    def cell_properties_padding_left(self, value):
        self._cell_properties_padding_left = value

    @property
    def cell_properties_padding_bottom(self):
        return self._cell_properties_padding_bottom

    @cell_properties_padding_bottom.setter
    def cell_properties_padding_bottom(self, value):
        self._cell_properties_padding_bottom = value

    @property
    def cell_properties_padding_right(self):
        return self._cell_properties_padding_right

    @cell_properties_padding_right.setter
    def cell_properties_padding_right(self, value):
        self._cell_properties_padding_right = value
