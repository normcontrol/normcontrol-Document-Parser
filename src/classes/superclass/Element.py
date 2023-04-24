from dataclasses import dataclass
from src.helpers.enums.AlignmentEnum import AlignmentEnum


@dataclass(kw_only=True)
class Element:
    _indent: float
    _line_spacing: float
    _alignment: AlignmentEnum = None
    _mrgrg: float = None
    _mrglf: float = None
    _mrgtop: float = None
    _mrgbtm: float = None
    _page_breake_before: bool = None
    _keep_lines_together: bool = None
    _keep_with_next: bool = None
    _outline_level: str = None

    @property
    def line_spacing(self):
        return self._line_spacing

    @line_spacing.setter
    def line_spacing(self, value):
        if value >= 0:
            self._line_spacing = value
        else:
            raise ValueError

    @property
    def keep_lines_together(self):
        return self._keep_lines_together

    @keep_lines_together.setter
    def keep_lines_together(self, keep_lines_together):
        self._keep_lines_together = keep_lines_together

    @property
    def outline_level(self):
        return self._outline_level

    @outline_level.setter
    def outline_level(self, outline_level):
        self._outline_level = outline_level

    @property
    def keep_with_next(self):
        return self._keep_with_next

    @keep_with_next.setter
    def keep_with_next(self, keep_with_next):
        self._keep_with_next = keep_with_next

    @property
    def indent(self):
        return self._indent

    @indent.setter
    def indent(self, indent):
        self._indent = indent

    @property
    def mrgrg(self):
        return self._mrgrg

    @mrgrg.setter
    def mrgrg(self, mrgrg):
        self._mrgrg = mrgrg

    @property
    def mrglf(self):
        return self._mrglf

    @mrglf.setter
    def mrglf(self, mrglf):
        self._mrglf = mrglf

    @property
    def mrgtop(self):
        return self._mrgtop

    @mrgtop.setter
    def mrgtop(self, mrgtop):
        self._mrgtop = mrgtop

    @property
    def mrgbtm(self):
        return self._mrgbtm

    @mrgbtm.setter
    def mrgbtm(self, mrgbtm):
        self._mrgbtm = mrgbtm
