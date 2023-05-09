from dataclasses import dataclass
from src.classes.Paragraph import Paragraph


@dataclass
class List(Paragraph):
    """
    Description: List class for document.

    Attributes:
        _type - attribute specifies the type of list - bulleted/numbered or other,
        _name - attribute specifies the name of a list,
        _level - attribute specifies the level of an outline or number list style,
        _start_value - attribute specifies a value that restarts numbering at the current list level,
        _style_char - attribute specifies a char in sequence,
        _style_name - attribute specifies name of the family style
    """

    _type: str = None
    _name: str = None
    _level: str = None
    _start_value: str = None
    _style_char: str = None
    _style_name: str = None

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value):
        self._level = value

    @property
    def start_value(self):
        return self._start_value

    @start_value.setter
    def start_value(self, value):
        self._start_value = value

    @property
    def style_char(self):
        return self._style_char

    @style_char.setter
    def style_char(self, value):
        self._style_char = value

    @property
    def style_name(self):
        return self._style_name

    @style_name.setter
    def style_name(self, value):
        self._style_name = value