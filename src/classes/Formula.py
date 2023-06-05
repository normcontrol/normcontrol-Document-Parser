from dataclasses import dataclass

from src.classes.superclass.StructuralElement import StructuralElement

@dataclass
class Formula(StructuralElement):
    """
    Description: This class is an abstraction of a formula that is contained in text documents

    Attributes
    ----------
        _text:str:
            attribute specifies the text of formula

    """

    _text: str = None

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text
