# Table row class for ODT document

class TableRow:
    def __init__(self, row_name, row_family, row_properties_min_row_height, row_properties_use_optimal_row_height):
        self.row_name = row_name
        self.row_family = row_family
        self.row_properties_min_row_height = row_properties_min_row_height
        self.row_properties_use_optimal_row_height = row_properties_use_optimal_row_height

    @property
    def row_name(self):
        return self._row_name

    @row_name.setter
    def row_name(self, value):
        self._row_name = value

    @property
    def row_family(self):
        return self._row_family

    @row_family.setter
    def row_family(self, value):
        self._row_family = value

    @property
    def row_properties_min_row_height(self):
        return self._row_properties_min_row_height

    @row_properties_min_row_height.setter
    def row_properties_min_row_height(self, value):
        self._row_properties_min_row_height = value

    @property
    def row_properties_use_optimal_row_height(self):
        return self._row_properties_use_optimal_row_height

    @row_properties_use_optimal_row_height.setter
    def row_properties_use_optimal_row_height(self, value):
        self._row_properties_use_optimal_row_height = value