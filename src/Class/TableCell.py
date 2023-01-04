# Table cell class for ODT document

class TableCell:
    def __init__(self, cell_name, cell_family, cell_properties_border, cell_properties_writing_mode,
                 cell_properties_padding_top, cell_properties_padding_left,
                 cell_properties_padding_bottom, cell_properties_padding_right):
        self.cell_name = cell_name
        self.cell_family = cell_family
        self.cell_properties_border = cell_properties_border
        self.cell_properties_writing_mode = cell_properties_writing_mode
        self.cell_properties_padding_top = cell_properties_padding_top
        self.cell_properties_padding_left = cell_properties_padding_left
        self.cell_properties_padding_bottom = cell_properties_padding_bottom
        self.cell_properties_padding_right = cell_properties_padding_right

    @property
    def cell_name(self):
        return self.cell_name

    @cell_name.setter
    def cell_name(self, value):
        self._cell_name = value

    @property
    def cell_family(self):
        return self.cell_family

    @cell_family.setter
    def cell_family(self, value):
        self._cell_family = value

    @property
    def cell_properties_border(self):
        return self.cell_properties_border

    @cell_properties_border.setter
    def cell_properties_border(self, value):
        self._cell_properties_border = value

    @property
    def cell_properties_writing_mode(self):
        return self.cell_properties_writing_mode

    @cell_properties_writing_mode.setter
    def cell_properties_writing_mode(self, value):
        self._cell_properties_writing_mode = value

    @property
    def cell_properties_padding_top(self):
        return self.cell_properties_padding_top

    @cell_properties_padding_top.setter
    def cell_properties_padding_top(self, value):
        self._cell_properties_padding_top = value

    @property
    def cell_properties_padding_left(self):
        return self.cell_properties_padding_left

    @cell_properties_padding_left.setter
    def cell_properties_padding_left(self, value):
        self._cell_properties_padding_left = value

    @property
    def cell_properties_padding_bottom(self):
        return self.cell_properties_padding_bottom

    @cell_properties_padding_bottom.setter
    def cell_properties_padding_bottom(self, value):
        self._cell_properties_padding_bottom = value

    @property
    def cell_properties_padding_right(self):
        return self.cell_properties_padding_right

    @cell_properties_padding_right.setter
    def cell_properties_padding_right(self, value):
        self._cell_properties_padding_right = value