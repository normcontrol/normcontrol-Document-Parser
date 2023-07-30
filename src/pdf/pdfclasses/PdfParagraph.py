from dataclasses import dataclass, field
from src.pdf.pdfclasses.Line import Line


@dataclass()
class PdfParagraph:

    """
    Description: A class is a pdf paragraph and its attributes

    Attributes:
    ----------
        _lines: list
            The attribute describes list of all paragraph lines
        _indent: float
            The attribute describes indent from the red line of the paragraph
        _spaces: list
            The attribute describes list of line spacing of all paragraph lines
        _line_spacing: float
            The attribute describes line spacing in a paragraph
        _font_name: str
            The attribute describes paragraph Font
        _text_size: float
            The attribute describes paragraph size
        _no_change_font_name: bool
            Attribute describing that the font of the paragraph has not changed
        _no_change_text_size: bool
            Attribute describing that the size of the paragraph has not changed
        _full_bold: bool
            The attribute specifies paragraph text boldness
        _full_italics: bool
            The attribute specifies paragraph text italics
    """

    _indent: float = None
    _line_spacing: float = None
    _font_name: list = field(default_factory=list)
    _text_size: list = field(default_factory=list)
    _no_change_font_name: bool = None
    _no_change_text_size: bool = None
    _spaces: list = field(default_factory=list)
    _lines: list[Line] = field(default_factory=list)
    _full_italics: bool = None
    _full_bold: bool = None

    @property
    def lines(self):
        return self._lines

    @property
    def indent(self):
        return self._indent

    @property
    def spaces(self):
        return self._spaces

    @property
    def line_spacing(self):
        return self._line_spacing

    @property
    def font_name(self):
        return self._font_name

    @property
    def text_size(self):
        return self._text_size

    @property
    def no_change_font_name(self):
        return self._no_change_font_name

    @property
    def no_change_text_size(self):
        return self._no_change_text_size

    @lines.setter
    def lines(self, value: list):
        self._lines = value

    @indent.setter
    def indent(self, value: float):
        self._indent = value

    @spaces.setter
    def spaces(self, value: list):
        self._spaces = value

    @line_spacing.setter
    def line_spacing(self, value: float):
        self._line_spacing = value

    @font_name.setter
    def font_name(self, value: str):
        self._font_name = value

    @text_size.setter
    def text_size(self, value: float):
        self._text_size = value

    @no_change_font_name.setter
    def no_change_font_name(self, value: bool):
        self._no_change_font_name = value

    @no_change_text_size.setter
    def no_change_text_size(self, value: bool):
        self._no_change_text_size = value

    @property
    def full_bold(self):
        return self._full_bold

    @full_bold.setter
    def full_bold(self, value: bool):
        self._full_bold = value

    @property
    def full_italics(self):
        return self._full_italics

    @full_italics.setter
    def full_italics(self, value: bool):
        self._full_italics = value
