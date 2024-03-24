from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.shared import Pt


class DefaultFormatStyle:
    line_spacing: str
    left_indent: str
    right_indent: str
    space_after: str
    space_before: str
    keep_together: str
    keep_with_next: str
    page_break_before: str
    first_line_indent: str
    alignment: WD_PARAGRAPH_ALIGNMENT

    def __init__(self, alignment = WD_PARAGRAPH_ALIGNMENT.LEFT, line_spacing = None, left_indent = None, right_indent = None,
                 space_after = None, space_before = None, keep_together = None,
                 keep_with_next = None, page_break_before = None, first_line_indent = None):
        self.alignment = alignment
        self.line_spacing = line_spacing
        self.left_indent = left_indent
        self.right_indent = right_indent
        self.space_after = space_after
        self.space_before = space_before
        self.keep_together = keep_together
        self.keep_with_next = keep_with_next
        self.page_break_before = page_break_before
        self.first_line_indent = first_line_indent
