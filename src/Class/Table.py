class Table:
    """
    Description: Table class for ODT document.

    Parameters:
        _table_name - attribute specifies the name of a table,
        _table_family - attribute specifies the family of a style (style:family),
        _table_master_page_name - attribute specifies the name of element that contains the content
            of headers and footers.
        _table_properties_width - attribute specifies the width of a table relative to the width of
            the area that the table is in (style:table-properties),
        _table_properties_margin_left - attribute sets the left margin of a table.
        _table_properties_align - attribute specifies the horizontal alignment of a table (table:align).
    """

    def __init__(self, table_name: str, table_family: str, table_master_page_name: str, table_properties_width: float,
                 table_properties_margin_left: float, table_properties_align: str):
        self._table_name = table_name
        self._table_family = table_family
        self._table_master_page_name = table_master_page_name
        self._table_properties_width = table_properties_width
        self._table_properties_margin_left = table_properties_margin_left
        self._table_properties_align = table_properties_align

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