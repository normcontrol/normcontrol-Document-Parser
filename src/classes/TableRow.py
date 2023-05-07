from dataclasses import dataclass

@dataclass
class TableRow:
    """
    Description: Table row class for ODT document.

    Attributes:
        _row_name - attribute specifies the name of a row,
        _row_family - attribute specifies the family of a style (style:family),
        _row_properties_min_row_height - attribute specifies a fixed minimum height for a row
            (style:table-row-properties),
        _row_properties_use_optimal_row_height - attribute specifies that a row height should be recalculated
            automatically if content in the row changes.
    """

    _row_name: str = None
    _row_family: str = None
    _row_properties_min_row_height: float = None
    _row_properties_use_optimal_row_height: float = None

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
