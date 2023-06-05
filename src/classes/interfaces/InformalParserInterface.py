from abc import ABC, abstractmethod

from src.classes.Formula import Formula
from src.classes.Frame import Frame
from src.classes.List import List
from src.classes.Paragraph import Paragraph
from src.classes.Table import Table
from src.classes.UnifiedDocumentView import UnifiedDocumentView
from src.classes.superclass.StructuralElement import StructuralElement


class InformalParserInterface(ABC):
    """
        Description: The class is an interface of a standard text document parser.

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

        Methods:
        ----------
            load_data_source(self, path: str):
                The method initializes the reading of the source document
            __extract_tables(self) -> list[StructuralElement]:
                The method extracts and returns a list of all the tables in the document
            __extract_pictures(self) -> list[StructuralElement]:
                The method extracts and returns a list of all the image in the document
            __extract_formulas(self) -> list[StructuralElement]:
                The method extracts and returns a list of all the formulas in the document
            get_all_elements(self) -> UnifiedDocumentView:
                The method extracts and returns a list of all the elements in the document
            __extract_paragraphs(self) -> list[StructuralElement]:
                The method extracts and returns a list of all the paragraphs in the document
            __extract_lists(self) -> list[StructuralElement]
                The method extracts and returns a list of all the list in the document:
        """

    _document: UnifiedDocumentView
    _pictures: list[Frame]
    _tables: list[Table]
    _paragraphs: list[Paragraph]
    _lists: list[List]
    _formulas: list[Formula]

    def load_data_source(self, path: str):
        pass

    @abstractmethod
    def extract_tables(self) -> list[Table]:
        pass

    @abstractmethod
    def extract_pictures(self) -> list[Frame]:
        pass

    @abstractmethod
    def extract_formulas(self) -> list[Formula]:
        pass

    @abstractmethod
    def get_all_elements(self) -> UnifiedDocumentView:
        pass

    @abstractmethod
    def extract_paragraphs(self) -> list[Paragraph]:
        pass

    @abstractmethod
    def extract_lists(self) -> list[StructuralElement]:
        pass
