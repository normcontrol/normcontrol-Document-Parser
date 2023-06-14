from src.classes.Formula import Formula
from src.classes.Frame import Frame
from src.classes.List import List
from src.classes.Paragraph import Paragraph
from src.classes.Table import Table
from src.classes.UnifiedDocumentView import UnifiedDocumentView


class DefaultParser:
    """
    Description: Super class of all document parsers

    Attributes:
    ----------
        _document: UnifiedDocumentView
            The attribute represents a unified document view that contains all structural elements
                and their attributes
        _pictures: list[Frame]
            The attribute represents list of image that contains in document
        _tables: list[Table]
            The attribute represents list of table that contains in document
        _paragraphs: list[Paragraph]
            The attribute represents list of paragraphs that contains in document
        _lists: list[List]
            The attribute represents list of enumeration that contains in document
        _formulas: list[Formula]
            The attribute represents list of formulas that contains in document
    """

    _document: UnifiedDocumentView
    _pictures: list[Frame]
    _tables: list[Table]
    _paragraphs: list[Paragraph]
    _lists: list[List]
    _formulas: list[Formula]

    @property
    def pictures(self):
        return self._pictures

    @pictures.setter
    def pictures(self, value: list[Frame]):
        self._pictures = value

    @property
    def document(self):
        return self._document

    @document.setter
    def document(self, document: UnifiedDocumentView):
        self._document = document

    @property
    def tables(self):
        return self._tables

    @tables.setter
    def tables(self, tables: list[Table]):
        self._tables = tables

    @property
    def paragraphs(self):
        return self._paragraphs

    @paragraphs.setter
    def paragraphs(self, paragraphs: list[Paragraph]):
        self._paragraphs = paragraphs

    @property
    def lists(self):
        return self._lists

    @lists.setter
    def lists(self, lists: list[List]):
        self._lists = lists

    @property
    def formulas(self):
        return self._formulas

    @formulas.setter
    def formulas(self, formulas: list[Formula]):
        self._formulas = formulas
