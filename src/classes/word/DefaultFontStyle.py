class DefaultFontStyle:
    font_name: str
    font_size: float
    def __init__(self, font_name: str, font_size: float = None):
        self.font_name = font_name
        self.font_size = font_size