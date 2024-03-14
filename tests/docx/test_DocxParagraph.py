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

    def test_font_name(self):
        path = os.path.join(os.path.dirname(__file__), "documents/elements/font_change.docx")
        docx = DocxParagraphParser(path)
        self.assertEqual(set(docx.paragraphs[0].font_name), {'Times New Roman'})
        self.assertEqual(set(docx.paragraphs[1].font_name),
                         {'Abadi MT Condensed Light', 'Courier New', 'Times New Roman', 'Calibri Light'})
        self.assertEqual(set(docx.paragraphs[2].font_name), {'Calibri', 'Times New Roman'})
        self.assertEqual(set(docx.paragraphs[3].font_name), {'Courier New', 'Times New Roman'})
        self.assertEqual(set(docx.paragraphs[4].font_name), {'Times New Roman'})
        self.assertEqual(set(docx.paragraphs[5].font_name), {'Times New Roman'})
        self.assertEqual(set(docx.paragraphs[6].font_name), {'Courier New', 'Times New Roman'})
        self.assertEqual(set(docx.paragraphs[7].font_name), {'Times New Roman'})
        self.assertEqual(set(docx.paragraphs[8].font_name), {'Calibri Light'})
        self.assertEqual(set(docx.paragraphs[9].font_name), {'Calibri', 'Abadi'})

    def test_font_size(self):
        path = os.path.join(os.path.dirname(__file__), "documents/elements/font_change.docx")
        docx = DocxParagraphParser(path)
        self.assertEqual(set(docx.paragraphs[0].text_size), {14.0})
        self.assertEqual(set(docx.paragraphs[1].text_size),
                         {14.0})
        self.assertEqual(set(docx.paragraphs[2].text_size), {14.0})
        self.assertEqual(set(docx.paragraphs[3].text_size), {14.0})
        self.assertEqual(set(docx.paragraphs[4].text_size), {14.0, 18.0})
        self.assertEqual(set(docx.paragraphs[5].text_size), {14.0, 16.0})
        self.assertEqual(set(docx.paragraphs[6].text_size), {14.0})

    def test_super_sub_text(self):
        path = os.path.join(os.path.dirname(__file__), "documents/elements/super_sub.docx")
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
        path = os.path.join(os.path.dirname(__file__), "documents/elements/color.docx")
        docx = DocxParagraphParser(path)

        paragraph = docx.paragraphs[0]
        self.assertEqual(paragraph.color_text, ['#000000'])

        paragraph = docx.paragraphs[1]
        self.assertEqual(paragraph.color_text, ['#00b0f0'])

        paragraph = docx.paragraphs[2]
        self.assertEqual(paragraph.color_text, ['#c45911'])

        paragraph = docx.paragraphs[3]
        self.assertEqual(paragraph.color_text, ['#2e74b5'])

        paragraph = docx.paragraphs[4]
        self.assertEqual(set(paragraph.color_text), {'#c45911', '#000000', '#00b050'})

        paragraph = docx.paragraphs[5]
        self.assertEqual(set(paragraph.color_text), {'#5b9bd5', '#000000', '#00b050'})

    def test_alignment(self):
        path = os.path.join(os.path.dirname(__file__), "documents/elements/alignment.docx")
        docx = DocxParagraphParser(path)

        paragraph = docx.paragraphs[0]
        self.assertEqual(paragraph.alignment, AlignmentEnum.LEFT)

        paragraph = docx.paragraphs[1]
        self.assertEqual(paragraph.alignment, AlignmentEnum.CENTER)

        paragraph = docx.paragraphs[2]
        self.assertEqual(paragraph.alignment, AlignmentEnum.RIGHT)

        paragraph = docx.paragraphs[3]
        self.assertEqual(paragraph.alignment, AlignmentEnum.JUSTIFY)

    def test_margin(self):
        path = os.path.join(os.path.dirname(__file__), "documents/elements/indent.docx")
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
        path = os.path.join(os.path.dirname(__file__), "documents/elements/bold.docx")
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
        path = os.path.join(os.path.dirname(__file__), "documents/elements/italic.docx")
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
        path = os.path.join(os.path.dirname(__file__), "documents/elements/underline.docx")
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
        path = os.path.join(os.path.dirname(__file__), "documents/elements/font_change.docx")
        docx = DocxParagraphParser(path)
        # Not change font
        self.assertEqual(docx.paragraphs[0].no_change_fontname, True)
        # Change second and third word in different font
        self.assertEqual(docx.paragraphs[1].no_change_fontname, False)
        # Change second word
        self.assertEqual(docx.paragraphs[2].no_change_fontname, False)
        # Change last symbol
        self.assertEqual(docx.paragraphs[3].no_change_fontname, False)
        # Change size last word
        self.assertEqual(docx.paragraphs[4].no_change_fontname, True)
        # Use style for last word
        self.assertEqual(docx.paragraphs[5].no_change_fontname, True)
        # Change one letter in middle
        self.assertEqual(docx.paragraphs[6].no_change_fontname, False)
        self.assertEqual(docx.paragraphs[7].no_change_fontname, True)
        self.assertEqual(docx.paragraphs[8].no_change_fontname, True)
        self.assertEqual(docx.paragraphs[9].no_change_fontname, False)

        if __name__ == 'main':
            unittest.main()
