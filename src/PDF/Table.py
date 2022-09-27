from pdfplumber.table import TableFinder


class PDFTable():
    def __init__(self, table):
        self.table = table
        self.text = []
    def addText(self, text):
        self.text.append(text)