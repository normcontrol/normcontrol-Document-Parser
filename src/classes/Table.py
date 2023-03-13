
from dataclasses import dataclass


@dataclass
class Table:
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

    _table_name: str
    _table_family: str
    _table_master_page_name: str
    _table_properties_width: float
    _table_properties_margin_left: float
    _table_properties_align: str

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
