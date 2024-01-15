# PyOPDParse

![Your logo](https://itmo.ru/file/pages/213/logo_na_plashke_russkiy_belyy.png)

[![python](https://badgen.net/badge/python/3.9|3.10|3.11/blue?icon=python)](https://www.python.org/)
[![license](https://badgen.net/github/license/normcontrol/normcontrol-Document-Parser)](https://www.python.org/)
[![issueo](https://badgen.net/github/open-issues/normcontrol/normcontrol-Document-Parser)](https://github.com/normcontrol/normcontrol-Document-Parser/issues)
[![issuec](https://badgen.net/github/closed-issues/normcontrol/normcontrol-Document-Parser)](https://github.com/normcontrol/normcontrol-Document-Parser/issues?q=is%3Aissue+is%3Aclosed)

## The purpose of the project

PyOPDParse is a library written in Python that provides a set of classes to extract elements and attributes from ODT,
PDF and DOCX files. As a result, you always get a single structure of elements and their properties.

## Table of Contents

- [Core features](#core-features)
- [Installation](#installation)
- [Examples](#examples)
- [Project Structure](#project-structure)
- [Documentation](#documentation)
- [Getting started](#getting-started)
- [License](#license)
- [Acknowledgments](#acknowledgments)
- [Contacts](#contacts)
- [Authors](#authors)

## Core features

- parser of structural elements of PDF documents,
- parser of structural elements of ODT documents,
- parser of structural elements of DOCX documents,
- unified classes of structural elements for documents of the specified formats.

## Installation

```in dev```

## Examples

```in dev```

## Project Structure

```
PyOPDParse/
├── README.md
├── LICENSE.md
├── requirements.txt
├── src/
│   ├── classes/
│       ├── interfaces/
│           ├── InformalParserInterface.py
│       ├── superclasses/
│           ├── StructuralElement.py
│       ├── Frame.py
│       ├── Image.py
│       ├── List.py
│       ├── Paragraph.py
│       ├── Table.py
│       ├── TableRow.py
│       ├── TableCell.py
│       ├── UnifiedDocumentView.py
│   ├── odt/
│       ├── elements/
│           ├── AutomaticStyleParser.py
│           ├── DefaultStyleParser.py
│           ├── RegularStyleParser.py
│           ├── ImageParser.py
│           ├── ListParser.py
│           ├── NodeParser.py
│           ├── ParagraphParser.py
│           ├── TableParser.py
│           ├── ODTDocument.py
│       ├── ODTParser.py
│   ├── pdf/
│       ├── pdfclasses/
│           ├── Line.py
│           ├── PDFParagraph.py
│       ├── PDFParser.py
│   ├── docx/
│       ├── DocxParagraphParser.py
│   ├── helpers/
├── examples/
├── docs/
├── tests/
└──   
```

## Documentation

Current version available [here](https://normcontrol.github.io/normcontrol-Document-Parser/#/)

## Getting started

```in dev```

## License

```in dev```

## Acknowledgments

The development team expresses its deep gratitude for the support provided to ITMO University.

## Contacts

Your contacts. For example:

- [Telegram channel](https://t.me/+rIyKfiGQ7fFhZDEy) answering questions about project
- slavamarcin@yandex.ru
- vlad-tershch@yandex.ru

## Authors

[Viacheslav Martsinkevich](https://github.com/slavamarcin)

[Vladislav Tereshchenko](https://github.com/Vl-Tershch)

[Andrei Berezhkov](https://github.com/a-berezhkov)

[Galina Larionova](https://github.com/orgs/normcontrol/people/galinalar)
 
