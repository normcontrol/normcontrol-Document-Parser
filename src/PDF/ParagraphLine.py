class Pdfparagraph:
    def __init__(self):
        self.lines = []
        self.indent = 0
        self.spaces = []
        self.line_spacing = 0
        self.fontname = None
        self.text_size = 0
        self.no_change_font_name = True
        self.no_change_text_size = True