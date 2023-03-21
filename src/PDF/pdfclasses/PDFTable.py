class PDFTable:
    """
    Description: The class is a pdf table and its text

    Attributes:
    ----------
        _table -  attribute represents the table itself and its attributes
        _text - attribute representing tabular text

    """

    def __init__(self, table):
        self._table = table
        self._text = []

    def addText(self, text: list):
        self.text.append(text)

    @property
    def table(self):
        return self._table

    @table.setter
    def table(self, table):
        self._table = table

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text: str):
        self._text = text
