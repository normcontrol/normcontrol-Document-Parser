from dataclasses import dataclass
from src.classes.Paragraph import Paragraph
@dataclass
class List(Paragraph):
    """
    Description: List class for document.

    Attributes:
        _list_type - attribute specifies the type of list - bulleted/numbered or other,
        _list_name - attribute specifies the name of a list,
        _list_level - attribute specifies the level of an outline or number list style,
        _list_start_value - attribute specifies a value that restarts numbering at the current list level,
        _list_style_char - attribute specifies a char in sequence,
        _list_style_name - attribute specifies name of the family style,
        _list_style_data - attribute specifies the style data.
    """

    _list_type: str = None
    _list_name: str = None
    _list_level: str = None
    _list_start_value: str = None
    _list_style_char: str = None
    _list_style_name: str = None
    _list_style_data: str = None

    @property
    def list_type(self):
        return self._list_type

    @list_type.setter
    def list_type(self, value):
        self._list_type = value

    @property
    def list_name(self):
        return self._list_name

    @list_name.setter
    def list_name(self, value):
        self._list_name = value

    @property
    def list_level(self):
        return self._list_level

    @list_level.setter
    def list_level(self, value):
        self._list_level = value

    @property
    def list_start_value(self):
        return self._list_start_value

    @list_start_value.setter
    def list_start_value(self, value):
        self._list_start_value = value

    @property
    def list_style_char(self):
        return self._list_style_char

    @list_style_char.setter
    def list_style_char(self, value):
        self._list_style_char = value

    @property
    def list_style_name(self):
        return self._list_style_name

    @list_style_name.setter
    def list_style_name(self, value):
        self._list_style_name = value

    @property
    def list_style_data(self):
        return self._list_style_data

    @list_style_data.setter
    def list_style_data(self, value):
        self._list_style_data = value