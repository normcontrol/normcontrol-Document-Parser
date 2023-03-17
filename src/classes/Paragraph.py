import re
from dataclasses import dataclass, field

from src.helpers.enums import AlignmentEnum


@dataclass
class Paragraph:
    """
    Description: a inified class representing a text paragraph, its properties? styles and content

    Parameters:
    ----------
            _text: str
                The attribute specifies paragraph text
            _countn_of_sp_sbl: int
                The attribute specifies number of special characters in a paragraph
            _count_sbl: int
                The attribute specifies number of characters in a paragraph
            _lowercase: bool
                The attribute specifies lowercase text in the entire paragraph
            _uppercase: bool
                The attribute specifies uppercase text in the entire paragraph
            _last_sbl: str
                The attribute specifies last paragraph character
            _first_key: str
                The attribute specifies first paragraph character
            _alignment: AlignmentEnum
                The attribute specifies text alignment
            _indent: float
                The attribute specifies indent from the red line
            _mrgrg: float
                The attribute specifies indent from the right side of the page
            _mrglf: float
                The attribute specifies indent from the left side of the page
            _line_spacing: float
                The attribute specifies paragraph line spacing
            _mrgtop: float
                The attribute specifies attribute specifies indent from the top side of the page
            _mrgbtm: float
                The attribute specifies attribute specifies indent from the bottom side of the page
            _font_name: str
                The attribute specifies paragraph font
            _bold: bool
                The attribute specifies paragraph text boldness
            _italics: bool
                The attribute specifies paragraph text italics
            _underlining: bool
                The attribute specifies paragraph text underlining
            _sub_text: bool
                The attribute specifies sub position of text
            _super_text: bool
                The attribute specifies super position of text
            _text_size: float
                The attribute specifies text size
            _color_text: str
                The attribute specifies text color in HEX
            _page_breake_before: bool
                The attribute specifies start of a new page
            _keep_lines_together: bool
                The attribute specifies keeping the line style together
            _keep_with_next: bool
                The attribute specifies keeping paragraphs together
            _outline_level: str
                The attribute specifies paragraph type
            _no_change_fontname: bool
                The attribute specifies no change in text font inside a paragraph
            _no_change_text_size: bool
                The attribute specifies no change in text size inside a paragraph

    Methods:
    ----------
            get_countn_of_sp_sbl(cls, text)
                Counts and returns the number of special characters in a text

            get_count_sbl(cls, text)
                Counts and returns the number of all characters in a text

            get_lowercase(cls, text)
                Calculates whether the entire paragraph is lowercase

            get_uppercase(cls, text)
                Calculates whether the entire paragraph is uppercase

            get_last_sbl(cls, text)
                Calculates the last character of a paragraph

            get_first_key(cls, text)
                Calculates the type of the first character of a paragraph

    """
    _line_spacing: float
    _text: str
    _count_of_sp_sbl: int = field(init=False)
    _count_sbl: int = field(init=False)
    _lowercase: bool = field(init=False)
    _uppercase: bool = field(init=False)
    _last_sbl: str = field(init=False)
    _first_key: str = field(init=False)
    _indent: float
    _font_name: str
    _text_size: float

    _alignment: AlignmentEnum = None
    _mrgrg: float = None
    _mrglf: float = None
    _mrgtop: float = None
    _mrgbtm: float = None
    _bold: bool = None
    _italics: bool = None
    _underlining: bool = None
    _sub_text: bool = None
    _super_text: bool = None
    _color_text: str = None
    _page_breake_before: bool = None
    _keep_lines_together: bool = None
    _keep_with_next: bool = None
    _outline_level: str = None
    _no_change_fontname: bool = None
    _no_change_text_size: bool = None

    def __post_init__(self):
        self.count_of_sp_sbl = Paragraph.get_countn_of_sp_sbl(self.text)
        self.count_sbl = Paragraph.get_count_sbl(self.text)
        self.lowercase = Paragraph.get_lowercase(self.text)
        self.uppercase = Paragraph.get_uppercase(self.text)
        self.last_sbl = Paragraph.get_last_sbl(self.text)
        self.first_key = Paragraph.get_first_key(self.text)

    @classmethod
    def get_countn_of_sp_sbl(cls, text):
        """

        Counts and returns the number of special characters in a text

        :param text: Paragraph text
        :return: The number of special characters in the text, such as dots and commas

        """
        return len(re.findall("[,.!?;:\'\"«»~]", text))

    @classmethod
    def get_count_sbl(cls, text):
        """

        Counts and returns the number of all characters in a text

        :param text: Paragraph text
        :return: The number of all characters in the text

        """
        return len(text)

    @classmethod
    def get_lowercase(cls, text):
        """

        Calculates whether the entire paragraph is lowercase

        :param text: Paragraph text
        :return: True if all text is in lowercase

        """
        return bool(text.islower())

    @classmethod
    def get_uppercase(cls, text):
        """

        Calculates whether the entire paragraph is uppercase

        :param text: Paragraph text
        :return: True if all text is in uppercase

        """
        return bool(text.isupper())

    @classmethod
    def get_last_sbl(cls, text: str):
        """

        Calculates the last character of a paragraph

        :param text: Paragraph text
        :return: The last character of a paragraph

        """
        try:
            if re.match(r'[A-Za-zА-Яа-я0-9()]', text[len(text) - 2]) is None:
                return text[len(text) - 2]
            return None
        except IndexError:
            print("IndexError")
        except TypeError:
            print('Allowed type is str')
        finally:
            return None

    @classmethod
    def get_first_key(cls, text):
        """

        Calculates the type of the first character of a paragraph

        :param text: Paragraph text
        :return: The type of the first character of a paragraph

        """
        first_key = text.split(' ')[0]
        if re.match(r'^(\d+\.)$|^(\d+\))$|^(-)$|^(–)$', first_key):
            return 'listLevel1'
        if re.match(r'^\d+$', first_key):
            return 'TitleLevel1'
        if re.match(r'\d+(\.\d+)+', first_key):
            return 'TitleLevel23'
        if re.match(r'^Таблица$', first_key):
            return 'Таблица'
        if re.match(r'(Рисунок)|(Рис)|(Рис.)', first_key):
            return 'Рисунок'
        return ''

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text

    @property
    def keep_lines_together(self):
        return self._keep_lines_together

    @keep_lines_together.setter
    def keep_lines_together(self, keep_lines_together):
        self._keep_lines_together = keep_lines_together

    @property
    def outline_level(self):
        return self._outline_level

    @outline_level.setter
    def outline_level(self, outline_level):
        self._outline_level = outline_level

    @property
    def keep_with_next(self):
        return self._keep_with_next

    @keep_with_next.setter
    def keep_with_next(self, keep_with_next):
        self._keep_with_next = keep_with_next

    @property
    def indent(self):
        return self._indent

    @indent.setter
    def indent(self, indent):
        self._indent = indent

    @property
    def mrgrg(self):
        return self._mrgrg

    @mrgrg.setter
    def mrgrg(self, mrgrg):
        self._mrgrg = mrgrg

    @property
    def mrglf(self):
        return self._mrglf

    @mrglf.setter
    def mrglf(self, mrglf):
        self._mrglf = mrglf

    @property
    def mrgtop(self):
        return self._mrgtop

    @mrgtop.setter
    def mrgtop(self, mrgtop):
        self._mrgtop = mrgtop

    @property
    def mrgbtm(self):
        return self._mrgbtm

    @mrgbtm.setter
    def mrgbtm(self, mrgbtm):
        self._mrgbtm = mrgbtm

    @property
    def font_name(self):
        return self._font_name

    @font_name.setter
    def font_name(self, font_name):
        self._font_name = font_name

    @property
    def color_text(self):
        return self._color_text

    @color_text.setter
    def color_text(self, color_text):
        self._color_text = color_text

    @property
    def line_spacing(self):
        return self._line_spacing

    @line_spacing.setter
    def line_spacing(self, value):
        if value >= 0:
            self._line_spacing = value
        else:
            raise ValueError

    @property
    def bold(self):
        return self._bold

    @bold.setter
    def bold(self, bold):
        if isinstance(bold, bool):
            self._bold = bold
        else:
            raise ValueError

    @property
    def italics(self):
        return self._italics

    @italics.setter
    def italics(self, italics):
        if isinstance(italics, bool):
            self._italics = italics
        else:
            raise ValueError

    @property
    def underlining(self):
        return self._underlining

    @underlining.setter
    def underlining(self, underlining):
        if isinstance(underlining, bool):
            self._underlining = underlining
        else:
            raise ValueError

    @property
    def sub_text(self):
        return self._sub_text

    @sub_text.setter
    def sub_text(self, sub_text):
        if isinstance(sub_text, bool):
            self._sub_text = sub_text
        else:
            raise ValueError

    @property
    def super_text(self):
        return self._super_text

    @super_text.setter
    def super_text(self, super_text):
        if isinstance(super_text, bool):
            self._super_text = super_text
        else:
            raise ValueError

    @property
    def text_size(self):
        return self._text_size

    @text_size.setter
    def text_size(self, s):
        if s >= 8:
            self._text_size = s
        else:
            raise ValueError

    @property
    def count_of_sp_sbl(self):
        return self._count_of_sp_sbl

    @count_of_sp_sbl.setter
    def count_of_sp_sbl(self, count_of_sp_sbl):
        self._count_of_sp_sbl = count_of_sp_sbl

    @property
    def count_sbl(self):
        return self._count_sbl

    @count_sbl.setter
    def count_sbl(self, count_sbl):
        self._count_sbl = count_sbl

    @property
    def lowercase(self):
        return self._lowercase

    @lowercase.setter
    def lowercase(self, lowercase):
        self._lowercase = lowercase

    @property
    def uppercase(self):
        return self._uppercase

    @uppercase.setter
    def uppercase(self, uppercase):
        self._uppercase = uppercase

    @property
    def last_sbl(self):
        return self._last_sbl

    @last_sbl.setter
    def last_sbl(self, last_sbl):
        self._last_sbl = last_sbl

    @property
    def first_key(self):
        return self._first_key

    @first_key.setter
    def first_key(self, first_key):
        self._first_key = first_key
