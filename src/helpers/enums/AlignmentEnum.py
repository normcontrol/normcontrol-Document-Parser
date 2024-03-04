import enum
from enum import Enum

@enum.unique
class AlignmentEnum(str, Enum):
    LEFT = 'left'
    RIGHT = 'right'
    CENTER = 'center'
    JUSTIFY = 'justify'
    DISTRIBUTE = 'distribute'
    JUSTIFY_MED = 'justify-med'
    JUSTIFY_HI = 'justify-hi'
    JUSTIFY_LOW = 'justify-low'
    THAI_JUSTIFY = 'thai-justify'

