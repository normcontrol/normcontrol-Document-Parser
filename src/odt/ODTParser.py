"""
    Description: The module contains a wrapper class that provides access to object parsing modules.
    ----------
    Описание: Модуль содержит класс-обертку, предоставляющую доступ к модулям парсинга объектов.
"""
from src.odt.elements.TablesParser import TablesParser
from src.odt.elements.RegularStylesParser import RegularStylesParser
from src.odt.elements.AutomaticStylesParser import AutomaticStylesParser
from src.odt.elements.DefaultStylesParser import DefaultStylesParser
from src.odt.elements.ListsParser import ListsParser
from src.odt.elements.ParagraphsParser import ParagraphsParser
from src.odt.elements.ImagesParser import ImagesParser
from src.odt.elements.NodesParser import NodesParser

class ODTParser:
    """
    Description: A wrapper class that provides access to object parsing modules.

    Parameters:
        _regular_styles_parser - a class containing methods for parsing regular styles;
        _automatic_styles_parser - a class containing methods for parsing automatic styles;
        _default_styles_parser - a class containing methods for parsing default styles;
        _tables_parser - a class containing methods for parsing tables;
        _lists_parser - a class containing methods for parsing lists;
        _images_parser - a class containing methods for parsing images;
        _paragraphs_parser - a class containing methods for parsing paragraphs;
        _nodes_parser - a class containing methods for parsing nodes.

    ----------
    Описание: Класс-обертка, предоставляющий доступ к модулям парсинга объектов.

    Свойства:
        _regular_styles_parser -  класс, содержащий методы парсинга обычных стилей;
        _automatic_styles_parser - класс, содержащий методы парсинга автоматических стилей;
        _default_styles_parser - класс, содержащий методы парсинга стилей по умолчанию;
        _tables_parser - класс, содержащий методы парсинга таблиц;
        _lists_parser - класс, содержащий методы парсинга списков;
        _images_parser - класс, содержащий методы парсинга изображений;
        _paragraphs_parser - класс, содержащий методы парсинга абзацев;
        _nodes_parser - класс, содержащий методы парсинга узлов документа.
    """

    def __init__(self):
        self._regular_styles_parser = RegularStylesParser()
        self._automatic_styles_parser = AutomaticStylesParser()
        self._default_styles_parser = DefaultStylesParser()
        self._tables_parser = TablesParser()
        self._lists_parser = ListsParser()
        self._images_parser = ImagesParser()
        self._paragraphs_parser = ParagraphsParser()
        self._nodes_parser = NodesParser()

    @property
    def regular_styles_parser(self):
        return self._regular_styles_parser

    @property
    def automatic_styles_parser(self):
        return self._automatic_styles_parser

    @property
    def default_styles_parser(self):
        return self._default_styles_parser

    @property
    def tables_parser(self):
        return self._tables_parser

    @property
    def lists_parser(self):
        return self._lists_parser

    @property
    def images_parser(self):
        return self._images_parser

    @property
    def paragraphs_parser(self):
        return self._paragraphs_parser

    @property
    def nodes_parser(self):
        return self._nodes_parser