from dataclasses import dataclass

@dataclass
class BulletList:
    """
    Description: Bullet list class for ODT document.

    Attributes:
        _list_name - attribute specifies the name of a list,
        _list_style_num_level - attribute specifies the level of an outline or number list style,
        _list_style_num_suffix - attribute specifies what to display after the number,
        _list_style_num_format - attribute specifies a numbering sequence,
        _list_style_num_start_value - attribute specifies a value that restarts numbering at the current list level,
        _list_style_data - attribute specifies the style data.
    """

    _list_name: str
    _list_style_num_level: float
    _list_style_num_suffix: str
    _list_style_num_format: str
    _list_style_num_start_value: str
    _list_style_data: str

    @property
    def list_name(self):
        return self._list_name

    @list_name.setter
    def list_name(self, value):
        self._list_name = value

    @property
    def list_style_num_level(self):
        return self._list_style_num_level

    @list_style_num_level.setter
    def list_style_num_level(self, value):
        self._list_style_num_level = value

    @property
    def list_style_num_suffix(self):
        return self._list_style_num_suffix

    @list_style_num_suffix.setter
    def list_style_num_suffix(self, value):
        self._list_style_num_suffix = value

    @property
    def list_style_num_format(self):
        return self._list_style_num_format

    @list_style_num_format.setter
    def list_style_num_format(self, value):
        self._list_style_num_format = value

    @property
    def list_style_num_start_value(self):
        return self._list_style_num_start_value

    @list_style_num_start_value.setter
    def list_style_num_start_value(self, value):
        self._list_style_num_start_value = value

    @property
    def list_style_data(self):
        return self._list_style_data

    @list_style_data.setter
    def list_style_data(self, value):
        self._list_style_data = value