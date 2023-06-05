from dataclasses import dataclass


@dataclass
class Line:

    """
    Description: A class is a text string and its attributes

    Attributes:
    ----------
        _x0: float
            The attribute describes the upper horizontal position of the symbol
        _y0: float
            The attribute describes the upper vertical position of the symbol
        _x1: float
            The attribute describes the lower horizontal position of the symbol
        _y1: float
            The attribute describes the lower vertical position of the symbol
        _text: str
            The attribute describes line text
        _font_names: list
            The attribute describes line Fonts
        _sizes: list
            The attribute describes line sizes
        _no_change_font_name: bool
            The attribute describing that the font of the string has not changed
        _no_change_text_size: bool
            The attribute describing that the size of the string has not changed
        _number_of_page: int
            The attribute describes the number of page on which the line is located
        _chars: list
            The attribute list of characters that make up the string

    """

    _x0: float
    _x1: float
    _y0: float
    _y1: float
    _text: str
    _font_names: list
    _text_sizes: list
    _no_change_font_name: bool
    _no_change_text_size: bool
    _number_of_page: int
    _chars: list

    @property
    def x0(self):
        return self._x0

    @x0.setter
    def x0(self, value: float):
        self._x0 = value

    @property
    def x1(self):
        return self._x1

    @property
    def y0(self):
        return self._y0

    @property
    def y1(self):
        return self._y1

    @property
    def text(self):
        return self._text

    @property
    def font_names(self):
        return self._font_names

    @property
    def text_sizes(self):
        return self._text_sizes

    @property
    def no_change_font_name(self):
        return self._no_change_font_name

    @property
    def no_change_text_size(self):
        return self._no_change_text_size

    @property
    def number_of_page(self):
        return self._number_of_page

    @property
    def chars(self):
        return self._chars

    @x1.setter
    def x1(self, value: float):
        self._x1 = value

    @y0.setter
    def y0(self, value: float):
        self._y0 = value

    @y1.setter
    def y1(self, value: float):
        self._y1 = value

    @text.setter
    def text(self, value: str):
        self._text = value

    @font_names.setter
    def font_names(self, value: list):
        self._font_names = value

    @text_sizes.setter
    def text_sizes(self, value: list):
        self._text_sizes = value

    @no_change_font_name.setter
    def no_change_font_name(self, value: bool):
        self._no_change_font_name = value

    @no_change_text_size.setter
    def no_change_text_size(self, value: bool):
        self._no_change_text_size = value

    @number_of_page.setter
    def number_of_page(self, value: int):
        self._number_of_page = value

    @chars.setter
    def chars(self, value: list):
        self._chars = value
