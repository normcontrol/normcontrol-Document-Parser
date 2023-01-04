# Table class for ODT document

class Table:
    def __init__(self, table_name, table_family, table_master_page_name, table_properties_width,
                 table_properties_margin_left, table_properties_align):
        self.table_name = table_name
        self.table_family = table_family
        self.table_master_page_name = table_master_page_name
        self.table_properties_width = table_properties_width
        self.table_properties_margin_left = table_properties_margin_left
        self.table_properties_align = table_properties_align

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