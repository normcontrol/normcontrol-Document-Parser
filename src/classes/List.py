from dataclasses import dataclass

from src.classes.Paragraph import Paragraph

@dataclass
class List(Paragraph):
    list_level: int
    marker: str