import enum
from enum import Enum

@enum.unique
class AlignmentEnum(str, Enum):
    LEFT = 'left'
    RIGHT = 'right'
    CENTER = 'center'
    JUSTIFY = 'justify'
