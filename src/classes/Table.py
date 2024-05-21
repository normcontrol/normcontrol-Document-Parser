from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Any
from src.classes.TableCell import TableCell
from src.classes.TableRow import TableRow
from src.classes.superclass.StructuralElement import StructuralElement


@dataclass
class Table(StructuralElement):
    """
    Description: The class is an abstraction of a table object that is contained in text documents

    Attributes:
    ----------
        _inner_text: str
            attribute specifies the text of all table cells
        _master_page_number: int
            attribute specifies the number of page
        _family: str
            attribute specifies the family of a style (style:family),
        _width: float
            attribute specifies the width of a table relative to the width
            of the area that the table is in (style:table-properties),
        _cells : list[TableCell]
            a list containing table cell objects,
        _rows: list[TableRow]
            a list containing table row objects.
        _bbox: tuple
            attribute specifies x0, y0, x1, y1 position of table in page
        _page_bbox: tuple
            attribute specifies size of page
    """
    _inner_text: list = None
    _master_page_number: int = None
    _family: str = None
    _width: float = None
    _bbox: tuple[int | float, int | float, int | float, int | float] = None
    _page_bbox: tuple[int | float, int | float, int | float, int | float] = None
    _cells: List[List[TableCell]] = field(default_factory=list)
    _rows: List[TableRow] = field(default_factory=list)


    @property
    def inner_text(self):
        return self._inner_text

    @inner_text.setter
    def inner_text(self, value):
        self._inner_text = value

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
    def table_cells(self):
        return self._cells

    @table_cells.setter
    def table_cells(self, value):
        self._cells = value

    @property
    def table_rows(self):
        return self._rows

    @table_rows.setter
    def table_rows(self, value):
        self._rows = value

    @property
    def page_bbox(self):
        return self._page_bbox

    @page_bbox.setter
    def page_bbox(self, value):
        self._page_bbox = value
