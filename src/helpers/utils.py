from docx.enum.text import WD_LINE_SPACING
from docx.shared import Pt


def check_for_key_and_return_value(key, dict_arg):
    return dict_arg[key] if key in dict_arg.keys() else None

def check_for_none(value):
    return value if value is not None else None

def get_line_spacing(value, spacing_rule):
    if value is None:
        return None
    if spacing_rule == WD_LINE_SPACING.MULTIPLE:
        return value/ Pt(12)