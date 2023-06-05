from dataclasses import dataclass


@dataclass
class TableRow:
    """
    Description: Table row class for ODT document.

    Attributes:
        _name: str
            The attribute specifies the name of a row,
        _family: str
            The attribute specifies the family of a style (style:family),
        _properties_min_height: float
            The attribute specifies a fixed minimum height for a row (style:table-row-properties)
    """

    _name: str = None
    _family: str = None
    _properties_min_height: float = None

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def family(self):
        return self._family

    @family.setter
    def family(self, value):
        self._family = value

    @property
    def properties_min_height(self):
        return self._properties_min_height

    @properties_min_height.setter
    def properties_min_height(self, value):
        self._properties_min_height = value
