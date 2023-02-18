import unittest
from docx import Document
from src.docx.DocxParagraph import DocxParagraph
from src.docx.helpers.EnumFill import EnumFill
import os


class TestParagraphStyle(unittest.TestCase):

    def test_is_bold_text(self):
        path = os.path.join(os.path.dirname(__file__), "documents/bold.docx")
        document = Document(path)
        docx = DocxParagraph(path)
        # Not bold text
        self.assertEqual(docx.is_style_append_text(document.paragraphs[0], "bold"), EnumFill.NO_APPLY)
        # All bold paragraph
        self.assertEqual(docx.is_style_append_text(document.paragraphs[1], "bold"), EnumFill.APPLY_TO_ALL_ELEMENTS)
        # Part of text bold
        self.assertEqual(docx.is_style_append_text(document.paragraphs[2], "bold"), EnumFill.APPLY_TO_SOME_ELEMENTS)
        # First word is bold
        self.assertEqual(docx.is_style_append_text(document.paragraphs[3], "bold"), EnumFill.APPLY_TO_SOME_ELEMENTS)
        # Жирные пробелы
        self.assertEqual(docx.is_style_append_text(document.paragraphs[4], "bold"), EnumFill.APPLY_TO_SOME_ELEMENTS)
        # Bold space after text(/n)  in Word does not have affect
        self.assertEqual(docx.is_style_append_text(document.paragraphs[5], "bold"), EnumFill.NO_APPLY)
        # Empty String
        self.assertEqual(docx.is_style_append_text(document.paragraphs[6], "bold"), EnumFill.IS_UNKNOWN)
        # Spaces
        self.assertEqual(docx.is_style_append_text(document.paragraphs[7], "bold"), EnumFill.NO_APPLY)

    def test_is_italic_text(self):
        path = os.path.join(os.path.dirname(__file__), "documents/italic.docx")
        document = Document(path)
        docx = DocxParagraph(path)
        # Not bold text
        self.assertEqual(docx.is_style_append_text(document.paragraphs[0], "italic"), EnumFill.NO_APPLY)
        # All bold paragraph
        self.assertEqual(docx.is_style_append_text(document.paragraphs[1], "italic"), EnumFill.APPLY_TO_ALL_ELEMENTS)
        # Part of text bold
        self.assertEqual(docx.is_style_append_text(document.paragraphs[2], "italic"), EnumFill.APPLY_TO_SOME_ELEMENTS)
        # First word is bold
        self.assertEqual(docx.is_style_append_text(document.paragraphs[3], "italic"), EnumFill.APPLY_TO_SOME_ELEMENTS)
        # Жирные пробелы
        self.assertEqual(docx.is_style_append_text(document.paragraphs[4], "italic"), EnumFill.APPLY_TO_SOME_ELEMENTS)
        # Bold space after text(/n)  in Word does not have affect
        self.assertEqual(docx.is_style_append_text(document.paragraphs[5], "italic"), EnumFill.NO_APPLY)
        # Empty String
        self.assertEqual(docx.is_style_append_text(document.paragraphs[6], "italic"), EnumFill.IS_UNKNOWN)
        # Spaces
        self.assertEqual(docx.is_style_append_text(document.paragraphs[7], "italic"), EnumFill.NO_APPLY)

    def test_is_underline_text(self):
        path = os.path.join(os.path.dirname(__file__), "documents/underline.docx")
        document = Document(path)
        docx = DocxParagraph(path)
        # Not bold text
        self.assertEqual(docx.is_style_append_text(document.paragraphs[0], "underline"), EnumFill.NO_APPLY)
        # All bold paragraph
        self.assertEqual(docx.is_style_append_text(document.paragraphs[1], "underline"), EnumFill.APPLY_TO_ALL_ELEMENTS)
        # Part of text bold
        self.assertEqual(docx.is_style_append_text(document.paragraphs[2], "underline"),
                         EnumFill.APPLY_TO_SOME_ELEMENTS)
        # First word is bold
        self.assertEqual(docx.is_style_append_text(document.paragraphs[3], "underline"),
                         EnumFill.APPLY_TO_SOME_ELEMENTS)
        # Жирные пробелы
        self.assertEqual(docx.is_style_append_text(document.paragraphs[4], "underline"),
                         EnumFill.APPLY_TO_SOME_ELEMENTS)
        # Bold space after text(/n)  in Word does not have affect
        self.assertEqual(docx.is_style_append_text(document.paragraphs[5], "underline"), EnumFill.NO_APPLY)
        # Empty String
        self.assertEqual(docx.is_style_append_text(document.paragraphs[6], "underline"), EnumFill.IS_UNKNOWN)
        # Spaces
        self.assertEqual(docx.is_style_append_text(document.paragraphs[7], "underline"), EnumFill.NO_APPLY)

    def test_is_change_font(self):
        path = os.path.join(os.path.dirname(__file__), "documents/font_change.docx")
        document = Document(path)
        docx = DocxParagraph(path)
        # Not change font
        self.assertEqual(docx.is_change_font_name(document.paragraphs[0]), False)
        # Change second and third word in different font
        self.assertEqual(docx.is_change_font_name(document.paragraphs[1]), True)
        # Change second word
        self.assertEqual(docx.is_change_font_name(document.paragraphs[2]), True)
        # Change last symbol
        self.assertEqual(docx.is_change_font_name(document.paragraphs[3]), True)
        # Change size last word
        self.assertEqual(docx.is_change_font_name(document.paragraphs[4]), False)
        # Use style for last word
        self.assertEqual(docx.is_change_font_name(document.paragraphs[5]), True)
        # Change one letter in middle
        self.assertEqual(docx.is_change_font_name(document.paragraphs[6]), True)

    def test_standard_paragraph(self):
        path = os.path.join(os.path.dirname(__file__), "documents/paragraph.docx")
        document = Document(path)
        docx = DocxParagraph(path)

        # TODO: private methods:  nochangeFontName, nochangeTextSize, alignment

        paragraph = docx.get_standard_paragraph(document.paragraphs[0])
        self.assertEqual(paragraph.text,
                         "Параграф с очищенным форматом на две строки две. Да точно две и в нем два предложения.")
        self.assertIn(paragraph.indent, [35.45, 35.4])
        self.assertEqual(paragraph.lineSpacing, 1.5)
        self.assertIn("Times New Roman", paragraph.fontName)
        self.assertEqual(paragraph.textSize, 14)
        self.assertEqual(paragraph.mrgrg, None)
        self.assertEqual(paragraph.mrglf, None)
        self.assertEqual(paragraph.bold, EnumFill.NO_APPLY)
        self.assertEqual(paragraph.italics, EnumFill.NO_APPLY)
        self.assertEqual(paragraph.underlining, EnumFill.NO_APPLY)
        self.assertEqual(paragraph.keepLinesTogether, None)
        self.assertEqual(paragraph.keepWithNext, None)
        self.assertEqual(paragraph.outlineLevel, None)

        paragraph = docx.get_standard_paragraph(document.paragraphs[1])
        self.assertEqual(paragraph.text,
                         "Второй параграф выделен жирным весь.")
        self.assertIn(paragraph.indent, [35.45, 35.4])
        self.assertEqual(paragraph.lineSpacing, 1.5)
        self.assertIn("Times New Roman", paragraph.fontName)
        self.assertEqual(paragraph.textSize, 14)
        self.assertEqual(paragraph.mrgrg, None)
        self.assertEqual(paragraph.mrglf, None)
        self.assertEqual(paragraph.bold, EnumFill.APPLY_TO_ALL_ELEMENTS)
        self.assertEqual(paragraph.italics, EnumFill.NO_APPLY)
        self.assertEqual(paragraph.underlining, EnumFill.NO_APPLY)
        self.assertEqual(paragraph.keepLinesTogether, None)
        self.assertEqual(paragraph.keepWithNext, None)
        self.assertEqual(paragraph.outlineLevel, None)

        paragraph = docx.get_standard_paragraph(document.paragraphs[2])
        self.assertEqual(paragraph.text,
                         "Третий выделен курсивом.")
        self.assertIn(paragraph.indent, [35.45, 35.4])
        self.assertEqual(paragraph.lineSpacing, 1.5)
        self.assertIn("Times New Roman", paragraph.fontName)
        self.assertEqual(paragraph.textSize, 14)
        self.assertEqual(paragraph.mrgrg, None)
        self.assertEqual(paragraph.mrglf, None)
        self.assertEqual(paragraph.bold, EnumFill.NO_APPLY)
        self.assertEqual(paragraph.italics, EnumFill.APPLY_TO_ALL_ELEMENTS)
        self.assertEqual(paragraph.underlining, EnumFill.NO_APPLY)
        self.assertEqual(paragraph.keepLinesTogether, None)
        self.assertEqual(paragraph.keepWithNext, None)
        self.assertEqual(paragraph.outlineLevel, None)

        paragraph = docx.get_standard_paragraph(document.paragraphs[3])
        self.assertEqual(paragraph.text,
                         "Четвертый заголовок уровня 1.")
        self.assertIn(paragraph.indent, [35.45, 35.4])
        self.assertEqual(paragraph.lineSpacing, 1.5)
        self.assertIn("Times New Roman", paragraph.fontName)
        self.assertEqual(paragraph.textSize, 16)
        self.assertEqual(paragraph.mrgrg, None)
        self.assertEqual(paragraph.mrglf, None)
        self.assertEqual(paragraph.bold, EnumFill.NO_APPLY)
        self.assertEqual(paragraph.italics, EnumFill.NO_APPLY)
        self.assertEqual(paragraph.underlining, EnumFill.NO_APPLY)
        self.assertEqual(paragraph.keepLinesTogether, None)
        self.assertEqual(paragraph.keepWithNext, None)
        self.assertEqual(paragraph.outlineLevel, None)

        paragraph = docx.get_standard_paragraph(document.paragraphs[4])
        self.assertEqual(paragraph.text,
                         "Пятый цвет текста зеленый.")
        self.assertIn(paragraph.indent, [35.45, 35.4])
        self.assertEqual(paragraph.lineSpacing, 1.5)
        self.assertIn("Times New Roman", paragraph.fontName)
        self.assertEqual(paragraph.textSize, 14)
        self.assertEqual(paragraph.mrgrg, None)
        self.assertEqual(paragraph.mrglf, None)
        self.assertEqual(paragraph.bold, EnumFill.NO_APPLY)
        self.assertEqual(paragraph.italics, EnumFill.NO_APPLY)
        self.assertEqual(paragraph.underlining, EnumFill.NO_APPLY)
        self.assertEqual(paragraph.keepLinesTogether, None)
        self.assertEqual(paragraph.keepWithNext, None)
        self.assertEqual(paragraph.outlineLevel, None)

        paragraph = docx.get_standard_paragraph(document.paragraphs[5])
        self.assertEqual(paragraph.text,
                         "Шестой имеет фон.")
        self.assertIn(paragraph.indent, [35.45, 35.4])
        self.assertEqual(paragraph.lineSpacing, 1.5)
        self.assertIn("Times New Roman", paragraph.fontName)
        self.assertEqual(paragraph.textSize, 14)
        self.assertEqual(paragraph.mrgrg, None)
        self.assertEqual(paragraph.mrglf, None)
        self.assertEqual(paragraph.bold, EnumFill.NO_APPLY)
        self.assertEqual(paragraph.italics, EnumFill.NO_APPLY)
        self.assertEqual(paragraph.underlining, EnumFill.NO_APPLY)
        self.assertEqual(paragraph.keepLinesTogether, None)
        self.assertEqual(paragraph.keepWithNext, None)
        self.assertEqual(paragraph.outlineLevel, None)

        paragraph = docx.get_standard_paragraph(document.paragraphs[6])
        self.assertEqual(paragraph.text,
                         "Седьмой 	использует табы.")
        self.assertIn(paragraph.indent, [35.45, 35.4])
        self.assertEqual(paragraph.lineSpacing, 1.5)
        self.assertIn("Times New Roman", paragraph.fontName)
        self.assertEqual(paragraph.textSize, 14)
        self.assertEqual(paragraph.mrgrg, None)
        self.assertEqual(paragraph.mrglf, None)
        self.assertEqual(paragraph.bold, EnumFill.NO_APPLY)
        self.assertEqual(paragraph.italics, EnumFill.NO_APPLY)
        self.assertEqual(paragraph.underlining, EnumFill.NO_APPLY)
        self.assertEqual(paragraph.keepLinesTogether, None)
        self.assertEqual(paragraph.keepWithNext, None)
        self.assertEqual(paragraph.outlineLevel, None)

        paragraph = docx.get_standard_paragraph(document.paragraphs[7])
        self.assertEqual(paragraph.text,
                         "Отступ у этого абзаца 2")
        self.assertIn(paragraph.indent, [56.75, 56.7])
        self.assertEqual(paragraph.lineSpacing, 1.5)
        self.assertIn("Times New Roman", paragraph.fontName)
        self.assertEqual(paragraph.textSize, 14)
        self.assertEqual(paragraph.mrgrg, None)
        self.assertEqual(paragraph.mrglf, None)
        self.assertEqual(paragraph.bold, EnumFill.NO_APPLY)
        self.assertEqual(paragraph.italics, EnumFill.NO_APPLY)
        self.assertEqual(paragraph.underlining, EnumFill.NO_APPLY)
        self.assertEqual(paragraph.keepLinesTogether, None)
        self.assertEqual(paragraph.keepWithNext, None)
        self.assertEqual(paragraph.outlineLevel, None)

        paragraph = docx.get_standard_paragraph(document.paragraphs[8])
        self.assertEqual(paragraph.text,
                         "А у это текста будет 1 строчный интервал — вот как-то так и он на две строки.")
        self.assertIn(paragraph.indent, [35.45, 35.4])
        self.assertEqual(paragraph.lineSpacing, 1)
        self.assertIn("Times New Roman", paragraph.fontName)
        self.assertEqual(paragraph.textSize, 14)
        self.assertEqual(paragraph.mrgrg, None)
        self.assertEqual(paragraph.mrglf, None)
        self.assertEqual(paragraph.bold, EnumFill.NO_APPLY)
        self.assertEqual(paragraph.italics, EnumFill.NO_APPLY)
        self.assertEqual(paragraph.underlining, EnumFill.NO_APPLY)
        self.assertEqual(paragraph.keepLinesTogether, None)
        self.assertEqual(paragraph.keepWithNext, None)
        self.assertEqual(paragraph.outlineLevel, None)

        paragraph = docx.get_standard_paragraph(document.paragraphs[9])
        self.assertEqual(paragraph.text,
                         "Шрифт изменен на 18.")
        self.assertIn(paragraph.indent, [35.45, 35.4])
        self.assertEqual(paragraph.lineSpacing, 1.5)
        self.assertIn("Times New Roman", paragraph.fontName)
        self.assertEqual(paragraph.textSize, 18)
        self.assertEqual(paragraph.mrgrg, None)
        self.assertEqual(paragraph.mrglf, None)
        self.assertEqual(paragraph.bold, EnumFill.NO_APPLY)
        self.assertEqual(paragraph.italics, EnumFill.NO_APPLY)
        self.assertEqual(paragraph.underlining, EnumFill.NO_APPLY)
        self.assertEqual(paragraph.keepLinesTogether, None)
        self.assertEqual(paragraph.keepWithNext, None)
        self.assertEqual(paragraph.outlineLevel, None)

        paragraph = docx.get_standard_paragraph(document.paragraphs[10])
        self.assertEqual(paragraph.text,
                         "Кастомный шрифт")
        self.assertEqual(paragraph.indent, 0)
        self.assertEqual(paragraph.lineSpacing, 1.5)
        self.assertIn("Courier New", paragraph.fontName)
        self.assertEqual(paragraph.textSize, 14)
        self.assertEqual(paragraph.mrgrg, None)
        self.assertEqual(paragraph.mrglf, None)
        self.assertEqual(paragraph.bold, EnumFill.NO_APPLY)
        self.assertEqual(paragraph.italics, EnumFill.NO_APPLY)
        self.assertEqual(paragraph.underlining, EnumFill.NO_APPLY)
        self.assertEqual(paragraph.keepLinesTogether, None)
        self.assertEqual(paragraph.keepWithNext, None)
        self.assertEqual(paragraph.outlineLevel, None)
        if __name__ == 'main':
            unittest.main()
