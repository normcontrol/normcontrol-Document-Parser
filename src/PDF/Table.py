from pdfplumber.table import TableFinder


class PDFTable():

    """
    Description: The class is a pdf table and its text
    ----------

    Parameters:
        __table -  attribute represents the table itself and its attributes
        __text - attribute representing tabular text

    """

    def __init__(self, table):
        self.__table = table
        self.__text = []
    def addText(self, text):
        self.text.append(text)

    @property
    def table(self):
        return self.__table

    @table.setter
    def table(self, table):
        self.__table = table

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, text):
        self.__text = text

