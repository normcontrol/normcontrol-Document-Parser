import unittest
import sys
import os

from docx import Document

from src.docx.DocxParagraphParser import DocxParagraphParser
from src.helpers.enums.AlignmentEnum import AlignmentEnum
from src.helpers.enums.StylePropertyCoverage import StylePropertyCoverage
import docx
from docx.text.paragraph import Paragraph

class TestDocxParagraph(unittest.TestCase):
    def test_super_sub_text(self):
        path = os.path.join(os.path.dirname(__file__), "documents/super_sub.docx")
        docx = DocxParagraphParser(path)

        paragraph = docx.paragraphs[0]
        self.assertEqual(paragraph.sub_text, False)
        self.assertEqual(paragraph.super_text, True)

        paragraph = docx.paragraphs[1]
        self.assertEqual(paragraph.sub_text, True)
        self.assertEqual(paragraph.super_text, False)

        paragraph = docx.paragraphs[2]
        self.assertEqual(paragraph.sub_text, True)
        self.assertEqual(paragraph.super_text, True)

        paragraph = docx.paragraphs[3]
        self.assertEqual(paragraph.sub_text, False)
        self.assertEqual(paragraph.super_text, False)

    def test_color(self):
        path = os.path.join(os.path.dirname(__file__), "documents/color.docx")
        docx = DocxParagraphParser(path)

        paragraph = docx.paragraphs[0]
        self.assertEqual(paragraph.color_text, '#000')

        paragraph = docx.paragraphs[1]
        self.assertEqual(paragraph.color_text, '#00b0f0')

        paragraph = docx.paragraphs[2]
        self.assertEqual(paragraph.color_text, '#c45911')

        paragraph = docx.paragraphs[3]
        self.assertEqual(paragraph.color_text, '#2e74b5')

        paragraph = docx.paragraphs[4]
        self.assertEqual(paragraph.color_text, '#c45911')

        paragraph = docx.paragraphs[5]
        self.assertEqual(paragraph.color_text, '#000')

    def test_alignment(self):
        path = os.path.join(os.path.dirname(__file__), "documents/alignment.docx")
        docx = DocxParagraphParser(path)

        paragraph = docx.paragraphs[0]
        self.assertEqual(paragraph.alignment, AlignmentEnum.LEFT)

        paragraph = docx.paragraphs[1]
        self.assertEqual(paragraph.alignment, AlignmentEnum.CENTER)

        paragraph = docx.paragraphs[2]
        self.assertEqual(paragraph.alignment, AlignmentEnum.RIGHT)

        paragraph = docx.paragraphs[3]
        self.assertEqual(paragraph.alignment, AlignmentEnum.JUSTIFY)

    def test_indent(self):
        path = os.path.join(os.path.dirname(__file__), "documents/indent.docx")
        docx = DocxParagraphParser(path)

        paragraph = docx.paragraphs[0]
        self.assertEqual(paragraph.mrgrg, 1.5)
        self.assertEqual(paragraph.mrglf, 1.5)
        self.assertEqual(paragraph.mrgtop, 1.5)
        self.assertEqual(paragraph.mrgbtm, 1.5)

        paragraph = docx.paragraphs[1]
        self.assertEqual(paragraph.mrgrg, 2)
        self.assertEqual(paragraph.mrglf, 2)
        self.assertEqual(paragraph.mrgtop, 2)
        self.assertEqual(paragraph.mrgbtm, 2)

        paragraph = docx.paragraphs[2]
        self.assertEqual(paragraph.mrgrg, 0)
        self.assertEqual(paragraph.mrglf, 2)
        self.assertEqual(paragraph.mrgtop, 0)
        self.assertEqual(paragraph.mrgbtm, 0)

        paragraph = docx.paragraphs[3]
        self.assertEqual(paragraph.mrgrg, 2)
        self.assertEqual(paragraph.mrglf, 0)
        self.assertEqual(paragraph.mrgtop, 0)
        self.assertEqual(paragraph.mrgbtm, 0)

        paragraph = docx.paragraphs[4]
        self.assertEqual(paragraph.mrgrg, 0)
        self.assertEqual(paragraph.mrglf, 0)
        self.assertEqual(paragraph.mrgtop, 0)
        self.assertEqual(paragraph.mrgbtm, 0)

        paragraph = docx.paragraphs[5]
        self.assertEqual(paragraph.mrgrg, 0)
        self.assertEqual(paragraph.mrglf, -1.25)
        self.assertEqual(paragraph.mrgtop, 0)
        self.assertEqual(paragraph.mrgbtm, 0)

        paragraph = docx.paragraphs[6]
        self.assertEqual(paragraph.mrgrg, 0)
        self.assertEqual(paragraph.mrglf, 0)
        self.assertEqual(paragraph.mrgtop, 1)
        self.assertEqual(paragraph.mrgbtm, 0)

        paragraph = docx.paragraphs[7]
        self.assertEqual(paragraph.mrgrg, 0)
        self.assertEqual(paragraph.mrglf, 0)
        self.assertEqual(paragraph.mrgtop, 0)
        self.assertEqual(paragraph.mrgbtm, 1)

    def test_is_bold_text(self):
        path = os.path.join(os.path.dirname(__file__), "documents/bold.docx")
        docx = DocxParagraphParser(path)
        # Not bold text
        self.assertEqual(docx.paragraphs[0].bold, StylePropertyCoverage.NO)
        # All bold paragraph
        self.assertEqual(docx.paragraphs[1].bold, StylePropertyCoverage.FULL)
        # Part of text bold
        self.assertEqual(docx.paragraphs[2].bold, StylePropertyCoverage.PARTLY)
        # First word is bold
        self.assertEqual(docx.paragraphs[3].bold, StylePropertyCoverage.PARTLY)
        # Жирные пробелы
        self.assertEqual(docx.paragraphs[4].bold, StylePropertyCoverage.PARTLY)
        # Bold space after text(/n)  in Word does not have affect
        self.assertEqual(docx.paragraphs[5].bold, StylePropertyCoverage.NO)
        # Empty String
        self.assertEqual(docx.paragraphs[6].bold, StylePropertyCoverage.UNKNOWN)
        # Spaces
        self.assertEqual(docx.paragraphs[7].bold, StylePropertyCoverage.NO)

    def test_is_italic_text(self):
        path = os.path.join(os.path.dirname(__file__), "documents/italic.docx")
        docx = DocxParagraphParser(path)
        # Not italics text
        self.assertEqual(docx.paragraphs[0].italics, StylePropertyCoverage.NO)
        # All italics paragraph
        self.assertEqual(docx.paragraphs[1].italics, StylePropertyCoverage.FULL)
        # Part of text italics
        self.assertEqual(docx.paragraphs[2].italics, StylePropertyCoverage.PARTLY)
        # First word is italics
        self.assertEqual(docx.paragraphs[3].italics, StylePropertyCoverage.PARTLY)
        # Жирные пробелы
        self.assertEqual(docx.paragraphs[4].italics, StylePropertyCoverage.PARTLY)
        # Italics space after text(/n)  in Word does not have affect
        self.assertEqual(docx.paragraphs[5].italics, StylePropertyCoverage.NO)
        # Empty String
        self.assertEqual(docx.paragraphs[6].italics, StylePropertyCoverage.UNKNOWN)
        # Spaces
        self.assertEqual(docx.paragraphs[7].italics, StylePropertyCoverage.NO)

    def test_is_underline_text(self):
        path = os.path.join(os.path.dirname(__file__), "documents/underline.docx")
        docx = DocxParagraphParser(path)
        # Not bold text
        self.assertEqual(docx.paragraphs[0].underlining, StylePropertyCoverage.NO)
        # All bold paragraph
        self.assertEqual(docx.paragraphs[1].underlining,
                         StylePropertyCoverage.FULL)
        # Part of text bold
        self.assertEqual(docx.paragraphs[2].underlining,
                         StylePropertyCoverage.PARTLY)
        # First word is bold
        self.assertEqual(docx.paragraphs[3].underlining,
                         StylePropertyCoverage.PARTLY)
        # Жирные пробелы
        self.assertEqual(docx.paragraphs[4].underlining,
                         StylePropertyCoverage.PARTLY)
        # Bold space after text(/n)  in Word does not have affect
        self.assertEqual(docx.paragraphs[5].underlining, StylePropertyCoverage.NO)
        # Empty String
        self.assertEqual(docx.paragraphs[6].underlining, StylePropertyCoverage.UNKNOWN)
        # Spaces
        self.assertEqual(docx.paragraphs[7].underlining, StylePropertyCoverage.NO)

    def test_is_change_font(self):
        path = os.path.join(os.path.dirname(__file__), "documents/font_change.docx")
        document = Document(path)
        docx = DocxParagraphParser(path)
        # Not change font
        self.assertEqual(docx.paragraphs[0].no_change_fontname, False)
        # Change second and third word in different font
        self.assertEqual(docx.paragraphs[1].no_change_fontname, True)
        # Change second word
        self.assertEqual(docx.paragraphs[2].no_change_fontname, True)
        # Change last symbol
        self.assertEqual(docx.paragraphs[3].no_change_fontname, True)
        # Change size last word
        self.assertEqual(docx.paragraphs[4].no_change_fontname, False)
        # Use style for last word
        self.assertEqual(docx.paragraphs[5].no_change_fontname, True)
        # Change one letter in middle
        self.assertEqual(docx.paragraphs[6].no_change_fontname, True)

    def test_standard_paragraph(self):
        path = os.path.join(os.path.dirname(__file__), "documents/paragraph.docx")
        docx = DocxParagraphParser(path)

        # TODO: private methods:  nochange_font_name, nochange_text_size, alignment

        paragraph = docx.paragraphs[0]
        self.assertEqual(paragraph.text,
                         "Параграф с очищенным форматом на две строки две. Да точно две и в нем два предложения.")
        self.assertIn(paragraph.indent, [35.45, 35.4])
        self.assertEqual(paragraph.line_spacing, 1.5)
        self.assertEqual(paragraph.font_name, ["Times New Roman"])
        self.assertEqual(paragraph.text_size, [14])
        self.assertEqual(paragraph.mrgrg, 0)
        self.assertEqual(paragraph.mrglf, 0)
        self.assertEqual(paragraph.bold, StylePropertyCoverage.NO)
        self.assertEqual(paragraph.italics, StylePropertyCoverage.NO)
        self.assertEqual(paragraph.underlining, StylePropertyCoverage.NO)
        self.assertEqual(paragraph.keep_lines_together, None)
        self.assertEqual(paragraph.keep_with_next, None)
        self.assertEqual(paragraph.outline_level, None)

        paragraph = docx.paragraphs[1]
        self.assertEqual(paragraph.text,
                         "Второй параграф выделен жирным весь.")
        self.assertIn(paragraph.indent, [35.45, 35.4])
        self.assertEqual(paragraph.line_spacing, 1.5)
        self.assertEqual(paragraph.font_name, ["Times New Roman"])
        self.assertEqual(paragraph.text_size, [14])
        self.assertEqual(paragraph.mrgrg, 0)
        self.assertEqual(paragraph.mrglf, 0)
        self.assertEqual(paragraph.bold, StylePropertyCoverage.FULL)
        self.assertEqual(paragraph.italics, StylePropertyCoverage.NO)
        self.assertEqual(paragraph.underlining, StylePropertyCoverage.NO)
        self.assertEqual(paragraph.keep_lines_together, None)
        self.assertEqual(paragraph.keep_with_next, None)
        self.assertEqual(paragraph.outline_level, None)

        paragraph = docx.paragraphs[2]
        self.assertEqual(paragraph.text,
                         "Третий выделен курсивом.")
        self.assertIn(paragraph.indent, [35.45, 35.4])
        self.assertEqual(paragraph.line_spacing, 1.5)
        self.assertEqual(paragraph.font_name, ["Times New Roman"])
        self.assertEqual(paragraph.text_size, [14])
        self.assertEqual(paragraph.mrgrg, 0)
        self.assertEqual(paragraph.mrglf, 0)
        self.assertEqual(paragraph.bold, StylePropertyCoverage.NO)
        self.assertEqual(paragraph.italics, StylePropertyCoverage.FULL)
        self.assertEqual(paragraph.underlining, StylePropertyCoverage.NO)
        self.assertEqual(paragraph.keep_lines_together, None)
        self.assertEqual(paragraph.keep_with_next, None)
        self.assertEqual(paragraph.outline_level, None)

        paragraph = docx.paragraphs[3]
        self.assertEqual(paragraph.text,
                         "Четвертый заголовок уровня 1.")
        self.assertIn(paragraph.indent, [35.45, 35.4])
        self.assertEqual(paragraph.line_spacing, 1.5)
        self.assertEqual(paragraph.font_name, ["Times New Roman"])
        self.assertEqual(paragraph.text_size, [16])
        self.assertEqual(paragraph.mrgrg, 0)
        self.assertEqual(paragraph.mrglf, 0)
        self.assertEqual(paragraph.bold, StylePropertyCoverage.NO)
        self.assertEqual(paragraph.italics, StylePropertyCoverage.NO)
        self.assertEqual(paragraph.underlining, StylePropertyCoverage.NO)
        self.assertEqual(paragraph.keep_lines_together, None)
        self.assertEqual(paragraph.keep_with_next, None)
        self.assertEqual(paragraph.outline_level, None)

        paragraph = docx.paragraphs[4]
        self.assertEqual(paragraph.text,
                         "Пятый цвет текста зеленый.")
        self.assertIn(paragraph.indent, [35.45, 35.4])
        self.assertEqual(paragraph.line_spacing, 1.5)
        self.assertEqual(paragraph._font_name, ["Times New Roman"])
        self.assertEqual(paragraph.text_size, [14])
        self.assertEqual(paragraph.mrgrg, 0)
        self.assertEqual(paragraph.mrglf, 0)
        self.assertEqual(paragraph.bold, StylePropertyCoverage.NO)
        self.assertEqual(paragraph.italics, StylePropertyCoverage.NO)
        self.assertEqual(paragraph.underlining, StylePropertyCoverage.NO)
        self.assertEqual(paragraph.keep_lines_together, None)
        self.assertEqual(paragraph.keep_with_next, None)
        self.assertEqual(paragraph.outline_level, None)

        paragraph = docx.paragraphs[5]
        self.assertEqual(paragraph.text,
                         "Шестой имеет фон.")
        self.assertIn(paragraph.indent, [35.45, 35.4])
        self.assertEqual(paragraph.line_spacing, 1.5)
        self.assertEqual(paragraph.font_name, ["Times New Roman"])
        self.assertEqual(paragraph.text_size, [14])
        self.assertEqual(paragraph.mrgrg, 0)
        self.assertEqual(paragraph.mrglf, 0)
        self.assertEqual(paragraph.bold, StylePropertyCoverage.NO)
        self.assertEqual(paragraph.italics, StylePropertyCoverage.NO)
        self.assertEqual(paragraph.underlining, StylePropertyCoverage.NO)
        self.assertEqual(paragraph.keep_lines_together, None)
        self.assertEqual(paragraph.keep_with_next, None)
        self.assertEqual(paragraph.outline_level, None)

        paragraph = docx.paragraphs[6]
        self.assertEqual(paragraph.text,
                         "Седьмой 	использует табы.")
        self.assertIn(paragraph.indent, [35.45, 35.4])
        self.assertEqual(paragraph.line_spacing, 1.5)
        self.assertEqual(paragraph.font_name, ["Times New Roman"])
        self.assertEqual(paragraph.text_size, [14])
        self.assertEqual(paragraph.mrgrg, 0)
        self.assertEqual(paragraph.mrglf, 0)
        self.assertEqual(paragraph.bold, StylePropertyCoverage.NO)
        self.assertEqual(paragraph.italics, StylePropertyCoverage.NO)
        self.assertEqual(paragraph.underlining, StylePropertyCoverage.NO)
        self.assertEqual(paragraph.keep_lines_together, None)
        self.assertEqual(paragraph.keep_with_next, None)
        self.assertEqual(paragraph.outline_level, None)

        paragraph = docx.paragraphs[7]
        self.assertEqual(paragraph.text,
                         "Отступ у этого абзаца 2")
        self.assertIn(paragraph.indent, [56.75, 56.7])
        self.assertEqual(paragraph.line_spacing, 1.5)
        self.assertEqual(paragraph.font_name, ["Times New Roman"])
        self.assertEqual(paragraph.text_size, [14])
        self.assertEqual(paragraph.mrgrg, 0)
        self.assertEqual(paragraph.mrglf, 0)
        self.assertEqual(paragraph.bold, StylePropertyCoverage.NO)
        self.assertEqual(paragraph.italics, StylePropertyCoverage.NO)
        self.assertEqual(paragraph.underlining, StylePropertyCoverage.NO)
        self.assertEqual(paragraph.keep_lines_together, None)
        self.assertEqual(paragraph.keep_with_next, None)
        self.assertEqual(paragraph.outline_level, None)

        paragraph = docx.paragraphs[8]
        self.assertEqual(paragraph.text,
                         "А у это текста будет 1 строчный интервал — вот как-то так и он на две строки.")
        self.assertIn(paragraph.indent, [35.45, 35.4])
        self.assertEqual(paragraph.line_spacing, 1)
        self.assertEqual(paragraph._font_name, ["Times New Roman"])
        self.assertEqual(paragraph.text_size, [14])
        self.assertEqual(paragraph.mrgrg, 0)
        self.assertEqual(paragraph.mrglf, 0)
        self.assertEqual(paragraph.bold, StylePropertyCoverage.NO)
        self.assertEqual(paragraph.italics, StylePropertyCoverage.NO)
        self.assertEqual(paragraph.underlining, StylePropertyCoverage.NO)
        self.assertEqual(paragraph.keep_lines_together, None)
        self.assertEqual(paragraph.keep_with_next, None)
        self.assertEqual(paragraph.outline_level, None)

        paragraph = docx.paragraphs[9]
        self.assertEqual(paragraph.text,
                         "Шрифт изменен на 18.")
        self.assertIn(paragraph.indent, [35.45, 35.4])
        self.assertEqual(paragraph._line_spacing, 1.5)
        self.assertEqual(paragraph._font_name, ["Times New Roman"])
        self.assertEqual(paragraph.text_size, [18])
        self.assertEqual(paragraph.mrgrg, 0)
        self.assertEqual(paragraph.mrglf, 0)
        self.assertEqual(paragraph.bold, StylePropertyCoverage.NO)
        self.assertEqual(paragraph.italics, StylePropertyCoverage.NO)
        self.assertEqual(paragraph.underlining, StylePropertyCoverage.NO)
        self.assertEqual(paragraph.keep_lines_together, None)
        self.assertEqual(paragraph.keep_with_next, None)
        self.assertEqual(paragraph.outline_level, None)

        paragraph = docx.paragraphs[10]
        self.assertEqual(paragraph.text,
                         "Кастомный шрифт")
        self.assertEqual(paragraph.indent, 0)
        self.assertEqual(paragraph._line_spacing, 1.5)
        self.assertEqual(paragraph._font_name,['Courier New'])
        self.assertEqual(paragraph._text_size, [14])
        self.assertEqual(paragraph._mrgrg, 0)
        self.assertEqual(paragraph._mrglf, 0)
        self.assertEqual(paragraph.bold, StylePropertyCoverage.NO)
        self.assertEqual(paragraph.italics, StylePropertyCoverage.NO)
        self.assertEqual(paragraph.underlining, StylePropertyCoverage.NO)
        self.assertEqual(paragraph._keep_lines_together, None)
        self.assertEqual(paragraph._keep_with_next, None)
        self.assertEqual(paragraph._outline_level, None)
        if __name__ == 'main':
            unittest.main()
