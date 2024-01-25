class NumLvlStyle():
    ilvl: int
    start: str
    num_fmt: str
    lvl_text: str
    lvl_jc: str
    left_mrg: float
    right_mrg: float
    indent: float

    def __init__(self, ilvl, left_mrg=0, right_mrg=0, indent=0, start=None, num_fmt=None, lvl_text=None, lvl_jc=None):
        self.ilvl = ilvl
        self.start = start
        self.num_fmt = num_fmt
        self.lvl_text = lvl_text
        self.lvl_jc = lvl_jc
        self.left_mrg = left_mrg
        self.right_mrg = right_mrg
        self.indent = indent


class AbstractNum():
    abstract_num_id: int
    numbering_styles: list[NumLvlStyle]

    def __init__(self, abstract_num_id, numbering_styles):
        self.abstract_num_id = abstract_num_id
        self.numbering_styles = numbering_styles

    def add_numbering_style(self, numbering_style):
        self.numbering_styles.append(numbering_style)


class NumberingStyle():
    num_id: int
    abstract_style: AbstractNum
    override_numbering_styles: dict[int, NumLvlStyle] # int это заменяемый ilvl

    def __init__(self, num_id, abstract_style, override_numbering_styles=None):
        self.num_id = num_id
        self.abstract_style = abstract_style
        self.override_numbering_styles = override_numbering_styles

class NumeringStyles():
    num = dict[int, NumberingStyle]
    abstract_num = dict[int, AbstractNum]
    def __init__(self, num, abstract_num):
        self.num = num
        self.abstract_num = abstract_num
