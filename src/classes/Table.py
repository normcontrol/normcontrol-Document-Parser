from dataclasses import dataclass
from typing import Any

from src.classes.superclass.StructuralElement import StructuralElement


@dataclass
class Table(StructuralElement):
    """
    Description: Table class for ODT document.

    Attributes:
        _table_name - attribute specifies the name of a table,
        _table_family - attribute specifies the family of a style (style:family),
        _table_master_page_name - attribute specifies the name of element that contains the content
            of headers and footers.
        _table_properties_width - attribute specifies the width of a table relative to the width of
            the area that the table is in (style:table-properties),
        _table_properties_margin_left - attribute sets the left margin of a table.
        _table_properties_align - attribute specifies the horizontal alignment of a table (table:align).
    """
    _inner_text: list
    _master_page_number: int
    _master_page: Any
    _family: str = None
    _width: float = None
    _align: str = None
    _bbox: tuple[int | float, int | float, int | float, int | float] = None

    @property
    def inner_text(self):
        return self._inner_text

    @inner_text.setter
    def inner_text(self, value):
        self._inner_text = value

    @property
    def master_page(self):
        return self._master_page

    @master_page.setter
    def master_page(self, value):
        self._master_page = value

    @property
    def bbox(self):
        return self._bbox

    @bbox.setter
    def bbox(self, value):
        self._bbox = value

    @property
    def family(self):
        return self._family

    @family.setter
    def family(self, value):
        self._family = value

    @property
    def master_page_number(self):
        return self._master_page_number

    @master_page_number.setter
    def master_page_number(self, value):
        self._master_page_number = value

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value


    @property
    def align(self):
        return self._align

    @align.setter
    def align(self, value):
        self._align = value
