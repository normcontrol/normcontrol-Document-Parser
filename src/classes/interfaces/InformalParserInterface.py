from abc import ABC, abstractmethod

from src.classes.UnifiedDocumentView import UnifiedDocumentView
from src.classes.superclass.Element import Element


class InformalParserInterface(ABC):
    def load_data_source(self, path: str):
        pass

    @abstractmethod
    def __get_tables(self) -> list[Element]:
        pass

    @abstractmethod
    def __get_pictures(self) -> list[Element]:
        pass

    @abstractmethod
    def __get_formulas(self) -> list[Element]:
        pass

    @abstractmethod
    def get_all_elements(self) -> UnifiedDocumentView:
        pass

    @abstractmethod
    def __get_paragraphs(self) -> list[Element]:
        pass

    @abstractmethod
    def __get_lists(self) -> list[Element]:
        pass
