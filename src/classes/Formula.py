from dataclasses import dataclass
from xml.etree.ElementTree import Element
from src.classes.superclass.StructuralElement import StructuralElement


@dataclass
class Formula(StructuralElement):
    """
    Description: This class is an abstraction of a formula that is contained in text documents

    Attributes
    ----------
        _content:Element:
            attribute specifies the xml-content of formula

    """

    _content: Element = None

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, text):
        self._content = text
