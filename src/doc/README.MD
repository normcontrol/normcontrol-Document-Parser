# DOCX module for extract elements with styles

## Description 

The model represents a set of classes for obtaining the properties of DOCX format document elements and bringing them to a single class text document
 
## How use

See    `/examples`   directory

For extract paragraphs use:

```python
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
```

## Tests

1. Available tests for Paragraph

```
python -m unittest src/docx/tests/paragraph.py
```

## Project structure

```
DocumentClass/
├── README.md
├── DocxParagraph.py - Class extract paragraphs as Paragraph class
├── helpers/
│  ├── EnumFill.py - ENUM class for styles (bold, italic, underline)
├── _temp/
│  ├── Paragraph.py - _DEV_ 
├── examples/
│  ├── paragraphParser.py  
├── tests/
│  ├── paragraph.py - Tests for DocxParagraph class
│  ├── documents - DOCX documents for tests
```