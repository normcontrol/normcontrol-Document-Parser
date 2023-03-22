import unittest
import sys
import os

from docx import Document

from src.doc.DocxParagraphParser import DocxParagraphParser
from src.helpers.enums.StylePropertyCoverage import StylePropertyCoverage
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT



class TestDocxParagraph(unittest.TestCase):
    def test_super_sub_text(self):
        path = os.path.join(os.path.dirname(__file__), "documents/super_sub.docx")
        document = Document(path)
        docx = DocxParagraphParser(path)

        paragraph = docx.get_standard_paragraph(document.paragraphs[0])
        self.assertEqual(getattr(paragraph, '_sub_text'), False)
        self.assertEqual(getattr(paragraph, '_super_text'), True)

        paragraph = docx.get_standard_paragraph(document.paragraphs[1])
        self.assertEqual(getattr(paragraph, '_sub_text'), True)
        self.assertEqual(getattr(paragraph, '_super_text'), False)

        paragraph = docx.get_standard_paragraph(document.paragraphs[2])
        self.assertEqual(getattr(paragraph, '_sub_text'), True)
        self.assertEqual(getattr(paragraph, '_super_text'), True)

        paragraph = docx.get_standard_paragraph(document.paragraphs[3])
        self.assertEqual(getattr(paragraph, '_sub_text'), False)
        self.assertEqual(getattr(paragraph, '_super_text'), False)

    def test_color(self):
        path = os.path.join(os.path.dirname(__file__), "documents/color.docx")
        document = Document(path)
        docx = DocxParagraphParser(path)

        paragraph = docx.get_standard_paragraph(document.paragraphs[0])
        self.assertEqual(getattr(paragraph, '_color_text'), '#000')

        paragraph = docx.get_standard_paragraph(document.paragraphs[1])
        self.assertEqual(getattr(paragraph, '_color_text'), '#00b0f0')

        paragraph = docx.get_standard_paragraph(document.paragraphs[2])
        self.assertEqual(getattr(paragraph, '_color_text'), '#c45911')

        paragraph = docx.get_standard_paragraph(document.paragraphs[3])
        self.assertEqual(getattr(paragraph, '_color_text'), '#2e74b5')

        paragraph = docx.get_standard_paragraph(document.paragraphs[4])
        self.assertEqual(getattr(paragraph, '_color_text'),'#c45911')

        paragraph = docx.get_standard_paragraph(document.paragraphs[5])
        self.assertEqual(getattr(paragraph, '_color_text'),'#000')

    def test_alignment(self):
        path = os.path.join(os.path.dirname(__file__), "documents/alignment.docx")
        document = Document(path)
        docx = DocxParagraphParser(path)

        paragraph = docx.get_standard_paragraph(document.paragraphs[0])
        self.assertEqual(getattr(paragraph, '_alignment'), WD_PARAGRAPH_ALIGNMENT.LEFT)

        paragraph = docx.get_standard_paragraph(document.paragraphs[1])
        self.assertEqual(getattr(paragraph, '_alignment'), WD_PARAGRAPH_ALIGNMENT.CENTER)

        paragraph = docx.get_standard_paragraph(document.paragraphs[2])
        self.assertEqual(getattr(paragraph, '_alignment'), WD_PARAGRAPH_ALIGNMENT.RIGHT)

        paragraph = docx.get_standard_paragraph(document.paragraphs[3])
        self.assertEqual(getattr(paragraph, '_alignment'), WD_PARAGRAPH_ALIGNMENT.JUSTIFY)

    def test_indent(self):
        path = os.path.join(os.path.dirname(__file__), "documents/indent.docx")
        document = Document(path)
        docx = DocxParagraphParser(path)

        paragraph = docx.get_standard_paragraph(document.paragraphs[0])
        self.assertEqual(paragraph._mrgrg, 1.5)
        self.assertEqual(paragraph._mrglf, 1.5)
        self.assertEqual(paragraph.mrgtop, 1.5)
        self.assertEqual(paragraph.mrgbtm, 1.5)

        paragraph = docx.get_standard_paragraph(document.paragraphs[1])
        self.assertEqual(paragraph._mrgrg, 2)
        self.assertEqual(paragraph._mrglf, 2)
        self.assertEqual(paragraph.mrgtop, 2)
        self.assertEqual(paragraph.mrgbtm, 2)

        paragraph = docx.get_standard_paragraph(document.paragraphs[2])
        self.assertEqual(paragraph._mrgrg, 0)
        self.assertEqual(paragraph._mrglf, 2)
        self.assertEqual(paragraph.mrgtop, 0)
        self.assertEqual(paragraph.mrgbtm, 0)

        paragraph = docx.get_standard_paragraph(document.paragraphs[3])
        self.assertEqual(paragraph._mrgrg, 2)
        self.assertEqual(paragraph._mrglf, 0)
        self.assertEqual(paragraph.mrgtop, 0)
        self.assertEqual(paragraph.mrgbtm, 0)

        paragraph = docx.get_standard_paragraph(document.paragraphs[3])
        self.assertEqual(paragraph._mrgrg, 2)
        self.assertEqual(paragraph._mrglf, 0)
        self.assertEqual(paragraph.mrgtop, 0)
        self.assertEqual(paragraph.mrgbtm, 0)

        paragraph = docx.get_standard_paragraph(document.paragraphs[4])
        self.assertEqual(paragraph._mrgrg, 0)
        self.assertEqual(paragraph._mrglf, 0)
        self.assertEqual(paragraph.mrgtop, 0)
        self.assertEqual(paragraph.mrgbtm, 0)

        paragraph = docx.get_standard_paragraph(document.paragraphs[5])
        self.assertEqual(paragraph._mrgrg, 0)
        self.assertEqual(paragraph._mrglf, -1.25)
        self.assertEqual(paragraph.mrgtop, 0)
        self.assertEqual(paragraph.mrgbtm, 0)

        paragraph = docx.get_standard_paragraph(document.paragraphs[6])
        self.assertEqual(paragraph._mrgrg, 0)
        self.assertEqual(paragraph._mrglf, 0)
        self.assertEqual(paragraph.mrgtop, 1)
        self.assertEqual(paragraph.mrgbtm, 0)

        paragraph = docx.get_standard_paragraph(document.paragraphs[7])
        self.assertEqual(paragraph._mrgrg, 0)
        self.assertEqual(paragraph._mrglf, 0)
        self.assertEqual(paragraph.mrgtop, 0)
        self.assertEqual(paragraph.mrgbtm, 1)

    def test_is_bold_text(self):
        path = os.path.join(os.path.dirname(__file__), "documents/bold.docx")
        document = Document(path)
        docx = DocxParagraphParser(path)
        # Not bold text
        self.assertEqual(docx._is_style_append(document.paragraphs[0], "bold"), StylePropertyCoverage.NO)
        # All bold paragraph
        self.assertEqual(docx._is_style_append(document.paragraphs[1], "bold"), StylePropertyCoverage.FULL)
        # Part of text bold
        self.assertEqual(docx._is_style_append(document.paragraphs[2], "bold"), StylePropertyCoverage.PARTLY)
        # First word is bold
        self.assertEqual(docx._is_style_append(document.paragraphs[3], "bold"), StylePropertyCoverage.PARTLY)
        # Жирные пробелы
        self.assertEqual(docx._is_style_append(document.paragraphs[4], "bold"), StylePropertyCoverage.PARTLY)
        # Bold space after text(/n)  in Word does not have affect
        self.assertEqual(docx._is_style_append(document.paragraphs[5], "bold"), StylePropertyCoverage.NO)
        # Empty String
        self.assertEqual(docx._is_style_append(document.paragraphs[6], "bold"), StylePropertyCoverage.UNKNOWN)
        # Spaces
        self.assertEqual(docx._is_style_append(document.paragraphs[7], "bold"), StylePropertyCoverage.NO)

    def test_is_italic_text(self):
        path = os.path.join(os.path.dirname(__file__), "documents/italic.docx")
        document = Document(path)
        docx = DocxParagraphParser(path)
        # Not bold text
        self.assertEqual(docx._is_style_append(document.paragraphs[0], "italic"), StylePropertyCoverage.NO)
        # All bold paragraph
        self.assertEqual(docx._is_style_append(document.paragraphs[1], "italic"), StylePropertyCoverage.FULL)
        # Part of text bold
        self.assertEqual(docx._is_style_append(document.paragraphs[2], "italic"), StylePropertyCoverage.PARTLY)
        # First word is bold
        self.assertEqual(docx._is_style_append(document.paragraphs[3], "italic"), StylePropertyCoverage.PARTLY)
        # Жирные пробелы
        self.assertEqual(docx._is_style_append(document.paragraphs[4], "italic"), StylePropertyCoverage.PARTLY)
        # Bold space after text(/n)  in Word does not have affect
        self.assertEqual(docx._is_style_append(document.paragraphs[5], "italic"), StylePropertyCoverage.NO)
        # Empty String
        self.assertEqual(docx._is_style_append(document.paragraphs[6], "italic"), StylePropertyCoverage.UNKNOWN)
        # Spaces
        self.assertEqual(docx._is_style_append(document.paragraphs[7], "italic"), StylePropertyCoverage.NO)

    def test_is_underline_text(self):
        path = os.path.join(os.path.dirname(__file__), "documents/underline.docx")
        document = Document(path)
        docx = DocxParagraphParser(path)
        # Not bold text
        self.assertEqual(docx._is_style_append(document.paragraphs[0], "underline"), StylePropertyCoverage.NO)
        # All bold paragraph
        self.assertEqual(docx._is_style_append(document.paragraphs[1], "underline"),
                         StylePropertyCoverage.FULL)
        # Part of text bold
        self.assertEqual(docx._is_style_append(document.paragraphs[2], "underline"),
                         StylePropertyCoverage.PARTLY)
        # First word is bold
        self.assertEqual(docx._is_style_append(document.paragraphs[3], "underline"),
                         StylePropertyCoverage.PARTLY)
        # Жирные пробелы
        self.assertEqual(docx._is_style_append(document.paragraphs[4], "underline"),
                         StylePropertyCoverage.PARTLY)
        # Bold space after text(/n)  in Word does not have affect
        self.assertEqual(docx._is_style_append(document.paragraphs[5], "underline"), StylePropertyCoverage.NO)
        # Empty String
        self.assertEqual(docx._is_style_append(document.paragraphs[6], "underline"), StylePropertyCoverage.UNKNOWN)
        # Spaces
        self.assertEqual(docx._is_style_append(document.paragraphs[7], "underline"), StylePropertyCoverage.NO)

    def test_is_change_font(self):
        path = os.path.join(os.path.dirname(__file__), "documents/font_change.docx")
        document = Document(path)
        docx = DocxParagraphParser(path)
        # Not change font
        self.assertEqual(docx._is_change_font_name(document.paragraphs[0]), False)
        # Change second and third word in different font
        self.assertEqual(docx._is_change_font_name(document.paragraphs[1]), True)
        # Change second word
        self.assertEqual(docx._is_change_font_name(document.paragraphs[2]), True)
        # Change last symbol
        self.assertEqual(docx._is_change_font_name(document.paragraphs[3]), True)
        # Change size last word
        self.assertEqual(docx._is_change_font_name(document.paragraphs[4]), False)
        # Use style for last word
        self.assertEqual(docx._is_change_font_name(document.paragraphs[5]), True)
        # Change one letter in middle
        self.assertEqual(docx._is_change_font_name(document.paragraphs[6]), True)

    def test_standard_paragraph(self):
        path = os.path.join(os.path.dirname(__file__), "documents/paragraph.docx")
        document = Document(path)
        docx = DocxParagraphParser(path)

        # TODO: private methods:  nochange_font_name, nochange_text_size, alignment

        paragraph = docx.get_standard_paragraph(document.paragraphs[0])
        self.assertEqual(paragraph.text,
                         "Параграф с очищенным форматом на две строки две. Да точно две и в нем два предложения.")
        self.assertIn(paragraph.indent, [35.45, 35.4])
        self.assertEqual(paragraph._line_spacing, 1.5)
        self.assertEqual("Times New Roman", paragraph._font_name)
        self.assertEqual(paragraph._text_size, 14)
        self.assertEqual(paragraph._mrgrg, 0)
        self.assertEqual(paragraph._mrglf, 0)
        self.assertEqual(paragraph.bold, StylePropertyCoverage.NO)
        self.assertEqual(paragraph.italics, StylePropertyCoverage.NO)
        self.assertEqual(paragraph.underlining, StylePropertyCoverage.NO)
        self.assertEqual(paragraph._keep_lines_together, None)
        self.assertEqual(paragraph._keep_with_next, None)
        self.assertEqual(paragraph._outline_level, None)

        paragraph = docx.get_standard_paragraph(document.paragraphs[1])
        self.assertEqual(paragraph.text,
                         "Второй параграф выделен жирным весь.")
        self.assertIn(paragraph.indent, [35.45, 35.4])
        self.assertEqual(paragraph._line_spacing, 1.5)
        self.assertEqual("Times New Roman", paragraph._font_name)
        self.assertEqual(paragraph._text_size, 14)
        self.assertEqual(paragraph._mrgrg, 0)
        self.assertEqual(paragraph._mrglf, 0)
        self.assertEqual(paragraph.bold, StylePropertyCoverage.FULL)
        self.assertEqual(paragraph.italics, StylePropertyCoverage.NO)
        self.assertEqual(paragraph.underlining, StylePropertyCoverage.NO)
        self.assertEqual(paragraph._keep_lines_together, None)
        self.assertEqual(paragraph._keep_with_next, None)
        self.assertEqual(paragraph._outline_level, None)

        paragraph = docx.get_standard_paragraph(document.paragraphs[2])
        self.assertEqual(paragraph.text,
                         "Третий выделен курсивом.")
        self.assertIn(paragraph.indent, [35.45, 35.4])
        self.assertEqual(paragraph._line_spacing, 1.5)
        self.assertEqual("Times New Roman", paragraph._font_name)
        self.assertEqual(paragraph._text_size, 14)
        self.assertEqual(paragraph._mrgrg, 0)
        self.assertEqual(paragraph._mrglf, 0)
        self.assertEqual(paragraph.bold, StylePropertyCoverage.NO)
        self.assertEqual(paragraph.italics, StylePropertyCoverage.FULL)
        self.assertEqual(paragraph.underlining, StylePropertyCoverage.NO)
        self.assertEqual(paragraph._keep_lines_together, None)
        self.assertEqual(paragraph._keep_with_next, None)
        self.assertEqual(paragraph._outline_level, None)

        paragraph = docx.get_standard_paragraph(document.paragraphs[3])
        self.assertEqual(paragraph.text,
                         "Четвертый заголовок уровня 1.")
        self.assertIn(paragraph.indent, [35.45, 35.4])
        self.assertEqual(paragraph._line_spacing, 1.5)
        self.assertEqual("Times New Roman", paragraph._font_name)
        self.assertEqual(paragraph._text_size, 16)
        self.assertEqual(paragraph._mrgrg, 0)
        self.assertEqual(paragraph._mrglf, 0)
        self.assertEqual(paragraph.bold, StylePropertyCoverage.NO)
        self.assertEqual(paragraph.italics, StylePropertyCoverage.NO)
        self.assertEqual(paragraph.underlining, StylePropertyCoverage.NO)
        self.assertEqual(paragraph._keep_lines_together, None)
        self.assertEqual(paragraph._keep_with_next, None)
        self.assertEqual(paragraph._outline_level, None)

        paragraph = docx.get_standard_paragraph(document.paragraphs[4])
        self.assertEqual(paragraph.text,
                         "Пятый цвет текста зеленый.")
        self.assertIn(paragraph.indent, [35.45, 35.4])
        self.assertEqual(paragraph._line_spacing, 1.5)
        self.assertEqual("Times New Roman", paragraph._font_name)
        self.assertEqual(paragraph._text_size, 14)
        self.assertEqual(paragraph._mrgrg, 0)
        self.assertEqual(paragraph._mrglf, 0)
        self.assertEqual(paragraph.bold, StylePropertyCoverage.NO)
        self.assertEqual(paragraph.italics, StylePropertyCoverage.NO)
        self.assertEqual(paragraph.underlining, StylePropertyCoverage.NO)
        self.assertEqual(paragraph._keep_lines_together, None)
        self.assertEqual(paragraph._keep_with_next, None)
        self.assertEqual(paragraph._outline_level, None)

        paragraph = docx.get_standard_paragraph(document.paragraphs[5])
        self.assertEqual(paragraph.text,
                         "Шестой имеет фон.")
        self.assertIn(paragraph.indent, [35.45, 35.4])
        self.assertEqual(paragraph._line_spacing, 1.5)
        self.assertEqual("Times New Roman", paragraph._font_name)
        self.assertEqual(paragraph._text_size, 14)
        self.assertEqual(paragraph._mrgrg, 0)
        self.assertEqual(paragraph._mrglf, 0)
        self.assertEqual(paragraph.bold, StylePropertyCoverage.NO)
        self.assertEqual(paragraph.italics, StylePropertyCoverage.NO)
        self.assertEqual(paragraph.underlining, StylePropertyCoverage.NO)
        self.assertEqual(paragraph._keep_lines_together, None)
        self.assertEqual(paragraph._keep_with_next, None)
        self.assertEqual(paragraph._outline_level, None)

        paragraph = docx.get_standard_paragraph(document.paragraphs[6])
        self.assertEqual(paragraph.text,
                         "Седьмой 	использует табы.")
        self.assertIn(paragraph.indent, [35.45, 35.4])
        self.assertEqual(paragraph._line_spacing, 1.5)
        self.assertEqual("Times New Roman", paragraph._font_name)
        self.assertEqual(paragraph._text_size, 14)
        self.assertEqual(paragraph._mrgrg, 0)
        self.assertEqual(paragraph._mrglf, 0)
        self.assertEqual(paragraph.bold, StylePropertyCoverage.NO)
        self.assertEqual(paragraph.italics, StylePropertyCoverage.NO)
        self.assertEqual(paragraph.underlining, StylePropertyCoverage.NO)
        self.assertEqual(paragraph._keep_lines_together, None)
        self.assertEqual(paragraph._keep_with_next, None)
        self.assertEqual(paragraph._outline_level, None)

        paragraph = docx.get_standard_paragraph(document.paragraphs[7])
        self.assertEqual(paragraph.text,
                         "Отступ у этого абзаца 2")
        self.assertIn(paragraph.indent, [56.75, 56.7])
        self.assertEqual(paragraph._line_spacing, 1.5)
        self.assertEqual("Times New Roman", paragraph._font_name)
        self.assertEqual(paragraph._text_size, 14)
        self.assertEqual(paragraph._mrgrg, 0)
        self.assertEqual(paragraph._mrglf, 0)
        self.assertEqual(paragraph.bold, StylePropertyCoverage.NO)
        self.assertEqual(paragraph.italics, StylePropertyCoverage.NO)
        self.assertEqual(paragraph.underlining, StylePropertyCoverage.NO)
        self.assertEqual(paragraph._keep_lines_together, None)
        self.assertEqual(paragraph._keep_with_next, None)
        self.assertEqual(paragraph._outline_level, None)

        paragraph = docx.get_standard_paragraph(document.paragraphs[8])
        self.assertEqual(paragraph.text,
                         "А у это текста будет 1 строчный интервал — вот как-то так и он на две строки.")
        self.assertIn(paragraph.indent, [35.45, 35.4])
        self.assertEqual(paragraph._line_spacing, 1)
        self.assertEqual("Times New Roman", paragraph._font_name)
        self.assertEqual(paragraph._text_size, 14)
        self.assertEqual(paragraph._mrgrg, 0)
        self.assertEqual(paragraph._mrglf, 0)
        self.assertEqual(paragraph.bold, StylePropertyCoverage.NO)
        self.assertEqual(paragraph.italics, StylePropertyCoverage.NO)
        self.assertEqual(paragraph.underlining, StylePropertyCoverage.NO)
        self.assertEqual(paragraph._keep_lines_together, None)
        self.assertEqual(paragraph._keep_with_next, None)
        self.assertEqual(paragraph._outline_level, None)

        paragraph = docx.get_standard_paragraph(document.paragraphs[9])
        self.assertEqual(paragraph.text,
                         "Шрифт изменен на 18.")
        self.assertIn(paragraph.indent, [35.45, 35.4])
        self.assertEqual(paragraph._line_spacing, 1.5)
        self.assertEqual("Times New Roman", paragraph._font_name)
        self.assertEqual(paragraph._text_size, 18)
        self.assertEqual(paragraph._mrgrg, 0)
        self.assertEqual(paragraph._mrglf, 0)
        self.assertEqual(paragraph.bold, StylePropertyCoverage.NO)
        self.assertEqual(paragraph.italics, StylePropertyCoverage.NO)
        self.assertEqual(paragraph.underlining, StylePropertyCoverage.NO)
        self.assertEqual(paragraph._keep_lines_together, None)
        self.assertEqual(paragraph._keep_with_next, None)
        self.assertEqual(paragraph._outline_level, None)

        paragraph = docx.get_standard_paragraph(document.paragraphs[10])
        self.assertEqual(paragraph.text,
                         "Кастомный шрифт")
        self.assertEqual(paragraph.indent, 0)
        self.assertEqual(paragraph._line_spacing, 1.5)
        self.assertEqual("Courier New", paragraph._font_name)
        self.assertEqual(paragraph._text_size, 14)
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
