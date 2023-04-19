from dataclasses import dataclass, field
from typing import List
from src.classes.TableCell import TableCell
from src.classes.TableColumn import TableColumn
from src.classes.TableRow import TableRow

@dataclass
class Table:
    """
    Description: Table class for document.

    Attributes:
        _table_name - attribute specifies the name of a table,
        _table_family - attribute specifies the family of a style (style:family),
        _table_master_page_name - attribute specifies the name of element that contains the content
            of headers and footers,
        _table_properties_width - attribute specifies the width of a table relative to the width of
            the area that the table is in (style:table-properties),
        _table_properties_margin_left - attribute sets the left margin of a table,
        _table_properties_align - attribute specifies the horizontal alignment of a table (table:align),
        _table_cells - a list containing table cell objects,
        _table_columns - a list containing table colum objects,
        _table_rows - a list containing table row objects.
    """

    _table_name: str = None
    _table_family: str = None
    _table_master_page_name: str = None
    _table_properties_width: float = None
    _table_properties_margin_left: float = None
    _table_properties_align: str = None
    _table_cells: List[TableCell] = field(default_factory=list)
    _table_columns: List[TableColumn] = field(default_factory=list)
    _table_rows: List[TableRow] = field(default_factory=list)

    @property
    def table_name(self):
        return self._table_name

    @table_name.setter
    def table_name(self, value):
        self._table_name = value

    @property
    def table_family(self):
        return self._table_family

    @table_family.setter
    def table_family(self, value):
        self._table_family = value

    @property
    def table_master_page_name(self):
        return self._table_master_page_name

    @table_master_page_name.setter
    def table_master_page_name(self, value):
        self._table_master_page_name = value

    @property
    def table_properties_width(self):
        return self._table_properties_width

    @table_properties_width.setter
    def table_properties_width(self, value):
        self._table_properties_width = value

    @property
    def table_properties_margin_left(self):
        return self._table_properties_margin_left

    @table_properties_margin_left.setter
    def table_properties_margin_left(self, value):
        self._table_properties_margin_left = value

    @property
    def table_properties_align(self):
        return self._table_properties_align

    @table_properties_align.setter
    def table_properties_align(self, value):
        self._table_properties_align = value

    @property
    def table_cells(self):
        return self._table_cells

    @table_cells.setter
    def table_cells(self, value):
        self._table_cells = value

    @property
    def table_columns(self):
        return self._table_columns

    @table_columns.setter
    def table_columns(self, values):
        self._table_columns = values

    @property
    def table_rows(self):
        return self._table_rows

    @table_rows.setter
    def table_rows(self, value):
        self._table_rows = value