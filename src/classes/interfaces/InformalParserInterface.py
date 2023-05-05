from abc import ABC, abstractmethod
from src.classes.UnifiedDocumentView import UnifiedDocumentView
from src.classes.superclass.StructuralElement import StructuralElement


class InformalParserInterface(ABC):
    def load_data_source(self, path: str):
        pass

    @abstractmethod
    def get_tables(self) -> list[StructuralElement]:
        pass

    @abstractmethod
    def get_pictures(self) -> list[StructuralElement]:
        pass

    @abstractmethod
    def get_formulas(self) -> list[StructuralElement]:
        pass

    @abstractmethod
    def get_all_elements(self) -> UnifiedDocumentView:
        pass

    @abstractmethod
    def get_paragraphs(self) -> list[StructuralElement]:
        pass

    @abstractmethod
    def get_lists(self) -> list[StructuralElement]:
        pass
