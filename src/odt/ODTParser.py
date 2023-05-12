"""
    Description: The module contains a wrapper class that provides access to object parsing modules.
    ----------
    Описание: Модуль содержит класс-обертку, предоставляющую доступ к модулям парсинга объектов.
"""
from src.odt.elements.TableParser import TableParser
from src.odt.elements.RegularStyleParser import RegularStyleParser
from src.odt.elements.AutomaticStyleParser import AutomaticStyleParser
from src.odt.elements.DefaultStyleParser import DefaultStyleParser
from src.odt.elements.ListParser import ListParser
from src.odt.elements.ParagraphParser import ParagraphParser
from src.odt.elements.ImageParser import ImageParser
from src.odt.elements.NodeParser import NodeParser
from src.classes.UnifiedDocumentView import UnifiedDocumentView

class ODTParser:
    """
    Description: A wrapper class that provides access to object parsing modules.

    Parameters:
        _regular_style_parser - a class containing methods for parsing regular styles;
        _automatic_style_parser - a class containing methods for parsing automatic styles;
        _default_style_parser - a class containing methods for parsing default styles;
        _table_parser - a class containing methods for parsing tables;
        _list_parser - a class containing methods for parsing lists;
        _image_parser - a class containing methods for parsing images;
        _paragraph_parser - a class containing methods for parsing paragraphs;
        _node_parser - a class containing methods for parsing nodes.

    ----------
    Описание: Класс-обертка, предоставляющий доступ к модулям парсинга объектов.

    Свойства:
        _regular_style_parser -  класс, содержащий методы парсинга обычных стилей;
        _automatic_style_parser - класс, содержащий методы парсинга автоматических стилей;
        _default_style_parser - класс, содержащий методы парсинга стилей по умолчанию;
        _table_parser - класс, содержащий методы парсинга таблиц;
        _list_parser - класс, содержащий методы парсинга списков;
        _image_parser - класс, содержащий методы парсинга изображений;
        _paragraph_parser - класс, содержащий методы парсинга абзацев;
        _node_parser - класс, содержащий методы парсинга узлов документа.
    """

    def __init__(self):
        self._regular_style_parser = RegularStyleParser()
        self._automatic_style_parser = AutomaticStyleParser()
        self._default_style_parser = DefaultStyleParser()
        self._table_parser = TableParser()
        self._list_parser = ListParser()
        self._image_parser = ImageParser()
        self._paragraph_parser = ParagraphParser()
        self._node_parser = NodeParser()

    @property
    def regular_style_parser(self):
        return self._regular_style_parser

    @property
    def automatic_style_parser(self):
        return self._automatic_style_parser

    @property
    def default_style_parser(self):
        return self._default_style_parser

    @property
    def table_parser(self):
        return self._table_parser

    @property
    def list_parser(self):
        return self._list_parser

    @property
    def image_parser(self):
        return self._image_parser

    @property
    def paragraph_parser(self):
        return self._paragraph_parser

    @property
    def node_parser(self):
        return self._node_parser