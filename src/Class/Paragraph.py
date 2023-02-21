import re
class Paragraph:
    """

    Parameters:

    ----------
            _text  - attribute specifies paragraph text
            _countn_of_sp_sbl  - attribute specifies number of special characters in a paragraph
            _count_sbl - attribute specifies number of characters in a paragraph
            _lowercase - attribute specifies lowercase text in the entire paragraph
            _uppercase - attribute specifies uppercase text in the entire paragraph
            _last_sbl - attribute specifies last paragraph character
            _firstkey - attribute specifies first paragraph character
            _prev_el - attribute specifies the class of the previous structural element
            _cur_el - attribute specifies the class of the current structural element
            _next_el - attribute specifies the class of the next structural element
            _alignment - attribute specifies text alignment
            _indent - attribute specifies indent from the red line
            _mrgrg - attribute specifies indent from the right side of the page
            _mrglf - attribute specifies indent from the left side of the page
            _line_spasing - attribute specifies paragraph line spacing
            _mrgtop - attribute specifies attribute specifies indent from the top side of the page
            _mrgbtm - attribute specifies attribute specifies indent from the bottom side of the page
            _font_name - attribute specifies paragraph font
            _bold - attribute specifies paragraph text boldness
            _italics - attribute specifies paragraph text italics
            _underlining - attribute specifies paragraph text underlining
            _sub_text - attribute specifies
            _super_text - attribute specifies
            _text_size - attribute specifies text size
            _color_text - attribute specifies text color
            _page_breake_before - attribute specifies start of a new page
            _keep_lines_together - attribute specifies keeping the line style together
            _keep_with_next - attribute specifies keeping paragraphs together
            _outline_level - attribute specifies paragraph type
            _no_space_between_paragraphs_of_same_style - attribute specifies no extra space between paragraphs of the same style
            _no_change_fontname - attribute specifies no change in text font inside a paragraph
            _no_change_text_size - attribute specifies no change in text size inside a paragraph

    Methods

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

            get_firstkey(cls, text)
                Calculates the type of the first character of a paragraph

    """
    def __init__(self, text, indent, line_spasing, font_name, text_size, no_change_fontname, no_change_text_size,
                 alignment=None, mrgrg=None, mrglf=None, mrgtop=None, mrgbtm=None, bold=None, italics=None,
                 underlining=None, sub_text=None, super_text=None, color_text="White",
                 keep_lines_together=None, keep_with_next=None, outline_level=None,
                 no_space_between_paragraphs_of_same_style=None, page_breake_before=None):
        self._text = text
        self._countn_of_sp_sbl = Paragraph.get_countn_of_sp_sbl(text)
        self._count_sbl = Paragraph.get_count_sbl(text)
        self._lowercase = Paragraph.get_lowercase(text)
        self._uppercase = Paragraph.get_uppercase(text)
        self._last_sbl = Paragraph.get_last_sbl(text)
        self._firstkey = Paragraph.get_firstkey(text)
        self._prev_el = None
        self._cur_el = None
        self._next_el = None
        self._alignment = alignment
        self._indent = indent
        self._mrgrg = mrgrg
        self._mrglf = mrglf
        self._line_spasing = line_spasing
        self._mrgtop = mrgtop
        self._mrgbtm = mrgbtm
        self._font_name = font_name
        self._bold = bold
        self._italics = italics
        self._underlining = underlining
        self._sub_text = sub_text
        self._super_text = super_text
        self._text_size = text_size
        self._color_text = color_text
        self._page_breake_before = page_breake_before
        self._keep_lines_together = keep_lines_together
        self._keep_with_next = keep_with_next
        self._outline_level = outline_level
        self._no_space_between_paragraphs_of_same_style = no_space_between_paragraphs_of_same_style
        self._no_change_fontname = no_change_fontname
        self._no_change_text_size = no_change_text_size

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
        return True if text.islower() else False

    @classmethod
    def get_uppercase(cls, text):
        """

        Calculates whether the entire paragraph is uppercase

        :param text: Paragraph text
        :return: True if all text is in uppercase

        """
        return True if text.isupper() else False

    @classmethod
    def get_last_sbl(cls, text):
        """

        Calculates the last character of a paragraph

        :param text: Paragraph text
        :return: The last character of a paragraph

        """
        try:
            if re.match(r'[A-Za-zА-Яа-я0-9()]', text[len(text) - 2]) is None:
                return text[len(text) - 2]
            else:
                return None
        except:
            return None

    @classmethod
    def get_firstkey(cls, text):
        """

        Calculates the type of the first character of a paragraph

        :param text: Paragraph text
        :return: The type of the first character of a paragraph

        """
        import re
        first_key = text.split(' ')[0]
        if re.match(r'^(\d+\.)$|^(\d+\))$|^(-)$|^(–)$', first_key):
            return 'listLevel1'
        else:
            if re.match(r'^\d+$', first_key):
                return 'TitleLevel1'
            else:
                if re.match(r'\d+(\.\d+)+', first_key):
                    return 'TitleLevel23'
                else:
                    if re.match(r'^Таблица$', first_key):
                        return 'Таблица'
                    else:
                        if re.match(r'(Рисунок)|(Рис)|(Рис.)', first_key):
                            return 'Рисунок'
                        else:
                            return ''

    @property
    def prev_el(self):
        return self._prev_el

    @prev_el.setter
    def prev_el(self, prev_el):
        self._prev_el = prev_el
    @property
    def cur_el(self):
        return self._cur_el

    @cur_el.setter
    def cur_el(self, cur_el):
        self._cur_el = cur_el
    @property
    def nextEl(self):
        return self._nextEl

    @nextEl.setter
    def font_name(self, nextEl):
        self._nextEl = nextEl
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
    def no_space_between_paragraphs_of_same_style(self):
        return self._no_space_between_paragraphs_of_same_style

    @no_space_between_paragraphs_of_same_style.setter
    def no_space_between_paragraphs_of_same_style(self, no_space_between_paragraphs_of_same_style):
        self._no_space_between_paragraphs_of_same_style = no_space_between_paragraphs_of_same_style
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
            self._font_name= font_name

    @property
    def color_text(self):
        return self._color_text

    @color_text.setter
    def color_text(self, color_text):
            self._color_text= color_text

    @property
    def line_spasing(self):
        return self._line_spasing

    @line_spasing.setter
    def line_spasing(self, value):
        if value >= 0:
            self._line_spasing = value
        else:
            raise ValueError

    @property
    def bold(self):
        return self._bold

    @bold.setter
    def bold(self, b):
        if b is True or b is False:
            self._bold = b
        else:
            raise ValueError

    @property
    def italics(self):
        return self._italics

    @italics.setter
    def italics(self, i):
        if i is True or i is False:
            self._italics = i
        else:
            raise ValueError

    @property
    def underlining(self):
        return self._underlining

    @underlining.setter
    def underlining(self, underlining):
        if underlining is True or underlining is False:
            self._underlining = underlining
        else:
            raise ValueError

    @property
    def sub_text(self):
        return self._sub_text

    @sub_text.setter
    def sub_text(self, s):
        if s is True or s is False:
            self._sub_text = s
        else:
            raise ValueError

    @property
    def super_text(self):
        return self._super_text

    @super_text.setter
    def super_text(self, s):
        if s is True or s is False:
            self._super_text = s
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
    def countn_of_sp_sbl(self):
        return self._countn_of_sp_sbl

    @countn_of_sp_sbl.setter
    def countn_of_sp_sbl(self, countn_of_sp_sbl):
        self._countn_of_sp_sbl = countn_of_sp_sbl

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
    def firstkey(self):
        return self._firstkey

    @firstkey.setter
    def firstkey(self, firstkey):
        self._firstkey = firstkey
    @property
    def prev_el(self):
        return self._prev_el

    @prev_el.setter
    def prev_el(self, prev_el):
        self._prev_el = prev_el
    @property
    def cur_el(self):
        return self._cur_el

    @cur_el.setter
    def cur_el(self, cur_el):
        self._cur_el = cur_el
    @property
    def next_el(self):
        return self._next_el

    @next_el.setter
    def next_el(self, next_el):
        self._next_el = next_el