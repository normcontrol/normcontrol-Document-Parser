from src.docx.DocxParagraph import DocxParagraph
import os

"""
Use for all paragraph
"""

# path to file
path = os.path.join(os.path.dirname(__file__), "../tests/documents/paragraph.docx")

# Load document
document = DocxParagraph(path)

# Get all paragraph and parse them to standard format
standard_class_paragraphs = document.get_all_paragraphs_in_standard

# List of object
print(standard_class_paragraphs)

"""
Use for one paragraph
"""
from docx import Document

document = Document(path)
docx = DocxParagraph(path)

paragraph = docx.get_standard_paragraph(document.paragraphs[8])

print(paragraph.text)
print(paragraph.bold)
