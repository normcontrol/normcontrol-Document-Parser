class Pdfparagraph:

    """
    Description: A class is a pdf paragraph and its attributes
    ----------

    Parameters:
        lines: The attribute describes list of all paragraph lines
        indent: The attribute describes indent from the red line of the paragraph
        spaces: The attribute describes list of line spacing of all paragraph lines
        line_spacing: The attribute describes line spacing in a paragraph
        fontname: The attribute describes paragraph Font
        text_size: The attribute describes paragraph size
        nochangeFontName: Attribute describing that the font of the paragraph has not changed
        nochangeSize: Attribute describing that the size of the paragraph has not changed

    """
    def __init__(self):
        self.lines = []
        self.indent = 0
        self.spaces = []
        self.line_spacing = 0
        self.fontname = None
        self.text_size = 0
        self.no_change_font_name = True
        self.no_change_text_size = True

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
    def fontname(self):
        return self._fontname

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
    def lines(self, value):
        self._lines = value

    @indent.setter
    def indent(self, value):
        self._indent = value

    @spaces.setter
    def spaces(self, value):
        self._spaces = value

    @line_spacing.setter
    def line_spacing(self, value):
        self._line_spacing = value

    @fontname.setter
    def fontname(self, value):
        self._fontname = value

    @text_size.setter
    def text_size(self, value):
        self._text_size = value

    @no_change_font_name.setter
    def no_change_font_name(self, value):
        self._no_change_font_name = value

    @no_change_text_size.setter
    def no_change_text_size(self, value):
        self._no_change_text_size = value
