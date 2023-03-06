from pdfplumber.table import TableFinder


class PDFTable():

    """
    Description: The class is a pdf table and its text

    Parameters:
    ----------
        _table -  attribute represents the table itself and its attributes
        _text - attribute representing tabular text

    """

    def __init__(self, table):
        self._table = table
        self._text = []
    def addText(self, text):
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
    def text(self, text):
        self._text = text

