import enum
from enum import Enum


@enum.unique
class StylePropertyCoverage(str, Enum):
    """
    Describes whether the property is applied to the entire element,
    only to part of it, or not applied at all

    NO_APPLY - property does not occur in the element
    APPLY_TO_ALL_ELEMENTS -  property is applied to the entire element
    APPLY_TO_SOME_ELEMENTS -  property is applied to a part of the element (unknown which one)
    IS_UNKNOWN -  It is not known whether the property is applied in any form to the text
    """
    NO = 0
    FULL = 1
    PARTLY = 2
    UNKNOWN = None
