from dataclasses import dataclass
from src.classes.Paragraph import Paragraph


@dataclass
class List(Paragraph):
    """
    Description: The class is an abstraction of an enumeration object that is contained in text documents

    Attributes
    ----------
        _type: str
            attribute specifies the type of list - bulleted/numbered or other,
        _name: str
            attribute specifies the name of a list,
        _level:str
            attribute specifies the level of an outline or number list style,
        _start_value:str
            attribute specifies a value that restarts numbering at the current list level,
        _style_char:str
            attribute specifies a char in sequence,
        _style_name:str
            attribute specifies name of the family style
    """

    _type: str = None
    _name: str = None
    _level: str = None
    _start_value: str = None
    _style_char: str = None
    _style_name: str = None

    def __init__(self, level, **kwargs):
        super().__init__(**kwargs)
        self.level = level


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