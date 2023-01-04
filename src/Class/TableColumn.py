# Table column class for ODT document

class TableColumn:
    def __init__(self, column_name, column_family, column_properties_column_width,
                 column_properties_use_optimal_column_width):
        self.column_name = column_name
        self.column_family = column_family
        self.column_properties_column_width = column_properties_column_width
        self.column_properties_use_optimal_column_width = column_properties_use_optimal_column_width

    @property
    def column_name(self):
        return self._column_name

    @column_name.setter
    def column_name(self, value):
        self._column_name = value

    @property
    def column_family(self):
        return self._column_family

    @column_family.setter
    def column_family(self, value):
        self._column_family = value

    @property
    def column_properties_column_width(self):
        return self._column_properties_column_width

    @column_properties_column_width.setter
    def column_properties_column_width(self, value):
        self._column_properties_column_width = value

    @property
    def column_properties_use_optimal_column_width(self):
        return self._column_properties_use_optimal_column_width

    @column_properties_use_optimal_column_width.setter
    def column_properties_use_optimal_column_width(self, value):
        self._column_properties_use_optimal_column_width = value