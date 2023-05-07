from dataclasses import dataclass

@dataclass
class TableColumn:
    """
    Description: Table column class for ODT document.

    Attributes:
        _column_name - attribute specifies the name of a column,
        _column_family - attribute specifies the family of a style (style:family),
        _column_properties_column_width - attribute specifies a fixed width for a column (style:table-column-properties),
        _column_properties_use_optimal_column_width - attribute specifies that a column width should be recalculated
            automatically if content in the column changes.
    """

    _column_name: str = None
    _column_family: str = None
    _column_properties_column_width: float = None
    _column_properties_use_optimal_column_width: bool = None

    @property
    def column_family(self):
        return self._column_family

    @column_family.setter
    def column_family(self, value):
        self._column_family = value

    @property
    def column_name(self):
        return self._column_name

    @column_name.setter
    def column_name(self, value):
        self._column_name = value

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
