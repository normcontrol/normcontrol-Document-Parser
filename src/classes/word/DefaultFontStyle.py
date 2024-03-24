from docx.shared import Pt


class DefaultFontStyle:
    name: str
    size: Pt
    color: tuple
    minorHAnsi: str
    majorHAnsi: str

    def __init__(self, name: str, size: Pt = None, color: tuple = (0, 0, 0), minorHAnsi: str = None,
                 majorHAnsi: str = None):
        self.name = name
        self.size = size
        self.color = color
        self.minorHAnsi = minorHAnsi
        self.majorHAnsi = majorHAnsi
