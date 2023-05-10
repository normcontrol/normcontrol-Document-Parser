from src.odt.ODTParser import ODTParser
from src.odt.elements.ODTDocument import ODTDocument
from src.helpers.odt import consts

class StylesContainer:
    def __init__(self, doc: ODTDocument):
        odt_parser = ODTParser()
        self._all_automatic_styles = odt_parser.automatic_style_parser.automatic_style_dict(doc, consts.DEFAULT_PARAM)
        self._all_default_styles = odt_parser.default_style_parser.default_style_dict(doc, consts.DEFAULT_PARAM)
        self._all_regular_styles = odt_parser.regular_style_parser.regular_style_dict(doc, consts.DEFAULT_PARAM)

    @property
    def all_automatic_styles(self):
        return self._all_automatic_styles

    @all_automatic_styles.setter
    def all_automatic_styles(self, value):
        self._all_automatic_styles = value

    @property
    def all_default_styles(self):
        return self._all_default_styles

    @all_default_styles.setter
    def all_default_styles(self, value):
        self._all_default_styles = value

    @property
    def all_regular_styles(self):
        return self._all_regular_styles

    @all_regular_styles.setter
    def all_regular_styles(self, value):
        self._all_regular_styles = value