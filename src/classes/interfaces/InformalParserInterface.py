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

