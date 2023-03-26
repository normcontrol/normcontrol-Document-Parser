from dataclasses import dataclass

@dataclass
class NumberList:
    """
    Description: Number list class for ODT document.

    Attributes:
        _list_name - attribute specifies the name of a list,
        _list_style_bull_level - attribute specifies the level of an outline or number list style,
        _list_style_bull_style_name - attribute specifies name of the family style,
        _list_style_bull_char - attribute specifies a char in sequence,
        _list_style_data - attribute specifies the style data.
    """

    _list_name: str
    _list_style_bull_level: str
    _list_style_bull_style_name: str
    _list_style_bull_char: str
    _list_style_data: str

    @property
    def list_name(self):
        return self._list_name

    @list_name.setter
    def list_name(self, value):
        self._list_name = value

    @property
    def list_style_bull_level(self):
        return self._list_style_bull_level

    @list_style_bull_level.setter
    def list_style_bull_level(self, value):
        self._list_style_bull_level = value

    @property
    def list_style_bull_style_name(self):
        return self._list_style_bull_style_name

    @list_style_bull_style_name.setter
    def list_style_bull_style_name(self, value):
        self._list_style_bull_style_name = value

    @property
    def list_style_bull_char(self):
        return self._list_style_bull_char

    @list_style_bull_char.setter
    def list_style_bull_char(self, value):
        self._list_style_bull_char = value

    @property
    def list_style_data(self):
        return self._list_style_data

    @list_style_data.setter
    def list_style_data(self, value):
        self._list_style_data = value