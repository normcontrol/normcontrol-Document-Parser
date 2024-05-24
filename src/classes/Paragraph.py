import re
from dataclasses import dataclass, field
from .superclass.StructuralElement import StructuralElement


@dataclass(kw_only=True)
class Paragraph(StructuralElement):
    """
    Description: an inified class representing a text paragraph, its properties? styles and content

    Attributes:
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

    _paraId: str = None
    _text: str = None
    _count_of_sp_sbl: int = field(init=False)
    _count_sbl: int = field(init=False)
    _lowercase: bool = field(init=False)
    _uppercase: bool = field(init=False)
    _last_sbl: str = field(init=False)
    _first_key: str = field(init=False)
    _bold: bool = None
    _italics: bool = None
    _underlining: bool = None
    _sub_text: bool = None
    _super_text: bool = None
    _color_text: list[str] = None
    _no_change_fontname: bool = None
    _no_change_text_size: bool = None
    _font_name: list[str] = field(default_factory=list)
    _text_size: list[float] = field(default_factory=list)


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

        :param
            text: Paragraph text
        :return The number of special characters in the text, such as dots and commas

        """
        return len(re.findall("[,.!?;:\'\"«»~]", text))

    @classmethod
    def get_count_sbl(cls, text):
        """

        Counts and returns the number of all characters in a text

        :param
            text: Paragraph text

        :return The number of all characters in the text

        """
        return len(text)

    @classmethod
    def get_lowercase(cls, text):
        """

        Calculates whether the entire paragraph is lowercase

        :param
            text: Paragraph text

        :return True if all text is in lowercase

        """
        return bool(text.islower())

    @classmethod
    def get_uppercase(cls, text):
        """

        Calculates whether the entire paragraph is uppercase

        :param
            text: Paragraph text

        :return True if all text is in uppercase

        """
        return bool(text.isupper())

    @classmethod
    def get_last_sbl(cls, text: str):
        """

        Calculates the last character of a paragraph

        :param
            text: Paragraph text

        :return The last character of a paragraph

        """
        try:
            if len(text) > 1 and text[len(text) - 1] != '':
                if  re.match(r'[.,;:!?]', text[len(text) - 1]) is not None:
                    return text[len(text) - 1]
            if re.match(r'[.,;:!?]', text[len(text) - 2]) is not None:
                return text[len(text) - 2]
            return None
        except IndexError:
            return None
        except TypeError:
            print('TypeError, allowed type is str')
            return None

    @classmethod
    def get_first_key(cls, text):
        """

        Calculates the type of the first character of a paragraph

        :param text: Paragraph text
        :return: The type of the first character of a paragraph

        """
        first_key = text.split(' ')[0]
        if re.match(r'^(\d+\.)$|^(\d+\))$|^(-)$|^(–)$|^(−)|^(⎯)$|^([a-z]\))$', first_key):
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
    def paraId(self):
        return self._paraId

    @paraId.setter
    def paraId(self, value: str):
        self._paraId = value

    @property
    def font_name(self):
        return self._font_name

    @font_name.setter
    def font_name(self, font_name):
        self._font_name = font_name

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text

    @property
    def color_text(self):
        return self._color_text

    @color_text.setter
    def color_text(self, color_text):
        self._color_text = color_text

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

    @property
    def bbox(self):
        return self._bbox

    @bbox.setter
    def bbox(self, bbox):
        self._bbox = bbox

    @property
    def no_change_fontname(self):
        return self._no_change_fontname

    @no_change_fontname.setter
    def no_change_fontname(self, no_change_fontname):
        self._no_change_fontname = no_change_fontname

    @property
    def no_change_text_size(self):
        return self._no_change_text_size

    @no_change_text_size.setter
    def no_change_text_size(self, no_change_text_size):
        self._no_change_text_size = no_change_text_size
