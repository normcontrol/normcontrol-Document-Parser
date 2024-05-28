"""
    Description: The module contains a wrapper class that provides access to object parsing modules.
    ----------
    Описание: Модуль содержит класс-обертку, предоставляющую доступ к модулям парсинга объектов.
"""
from abc import ABC
from src.classes.Formula import Formula
from src.classes.Frame import Frame
from src.classes.Paragraph import Paragraph
from src.classes.Table import Table
from src.classes.interfaces.InformalParserInterface import InformalParserInterface
from src.classes.superclass.StructuralElement import StructuralElement
from src.helpers.odt import consts
from src.odt.elements import ODTDocument
from src.odt.elements.TableParser import TableParser
from src.odt.elements.RegularStyleParser import RegularStyleParser
from src.odt.elements.AutomaticStyleParser import AutomaticStyleParser
from src.odt.elements.DefaultStyleParser import DefaultStyleParser
from src.odt.elements.ListParser import ListParser
from src.odt.elements.ParagraphParser import ParagraphParser
from src.odt.elements.ImageParser import ImageParser
from src.classes.UnifiedDocumentView import UnifiedDocumentView

class ODTParser(InformalParserInterface, ABC):
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
        _all_automatic_styles - a collection containing all automatic document styles;
        _all_default_styles - a collection containing all default document styles;
        _all_regular_styles - a collection containing all regular document styles.

    Methods:
        def extract_tables(self) -> list[Table]: Extracts all tables from an ODT document;

        def extract_pictures(self) -> list[Frame]: Extracts all images from an ODT document;

        def extract_formulas(self) -> list[Formula]: Extracts all formulas from an ODT document;

        def extract_paragraphs(self) -> list[Paragraph]: Extracts all paragraphs from an ODT document;

        def extract_lists(self) -> list[StructuralElement]: Extracts all lists from an ODT document;

        def get_all_elements(self) -> UnifiedDocumentView: Forms structural elements of the document based on tables,
            paragraphs, lists and images;

        def build_styles_dicts(self): Implements an inheritance mechanism for document styles;

        def build_default_styles_inheritance(self): Implements the default styles inheritance mechanism in the document;

        def build_regular_styles_inheritance(self): Implements the regular styles inheritance mechanism in the document;

        def build_automatic_styles_inheritance(self): Implements the automatic styles inheritance mechanism
            in the document;

        def find_style_with_inheritance(self, style_name):Searches for the desired style among styles, taking into
            account their inheritance;

        def get_document_nodes_with_style_full_list(self, start_node, parent_node, list=None, level=0): Returns each
            node of the document and its attributes;

        def get_document_nodes_with_styles(self, start_node, parent_node, list_of_nodes=None, level=0):
            Returns each node of the document and its attributes with a passage through all styles, searching,
            in case of absence, in nodes at a higher level.;

        def get_document_nodes_with_higher_style_data(self, start_node, parent_node, level=0, list_of_nodes=None):
            Returns each node of the document and its attributes with a passage through all styles, searching,
            in case of absence, in nodes at a higher level.
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
        _all_automatic_styles - коллекция, содержащая все автоматические стили документа;
        _all_default_styles - коллекция, содержащая все стили по умолчанию документа;
        _all_regular_styles - коллекция, содержащая все обычные стили документа.

    Методы:
        def extract_tables(self) -> list[Table]: Извлекает все таблицы из ODT документа;

        def extract_pictures(self) -> list[Frame]: Извлекает все изображения из ODT документа;

        def extract_formulas(self) -> list[Formula]: Извлекает все формулы из ODT документа;

        def extract_paragraphs(self) -> list[Paragraph]: Извлекает все параграфы из ODT документа;

        def extract_lists(self) -> list[StructuralElement]: Извлекает все списки из ODT документа;

        def get_all_elements(self) -> UnifiedDocumentView: Формирует структурные элементы документа на основе таблиц,
            абзацев, списков и изображений;

        def build_styles_dicts(self): Реализует у стилей документа механизм наследования;

        def build_default_styles_inheritance(self): Реализует механизм наследования стилей по умолчанию в документе;

        def build_regular_styles_inheritance(self): Реализует механизм наследования обычных стилей в документе;

        def build_automatic_styles_inheritance(self): Реализует механизм наследования автоматических стилей в документе;

        def find_style_with_inheritance(self, style_name): Выполняет поиск нужного стиля среди стилей с учетом
            их наследования;

        def get_document_nodes_with_style_full_list(self, start_node, parent_node, list=None, level=0): Возвращает
            каждый узел документа и его атрибуты;

        def get_document_nodes_with_styles(self, start_node, parent_node, list_of_nodes=None, level=0):
            Возвращает каждый каждый узел документа и его атрибуты с прохождением по всем стилям, выполняя поиск, в
            случае отсутствия, в узлах уровнем выше;

        def get_document_nodes_with_higher_style_data(self, start_node, parent_node, level=0, list_of_nodes=None):
            Возвращает каждый каждый узел документа и его атрибуты с прохождением по всем стилям, выполняя поиск, в
            случае отсутствия, в узлах уровнем выше.
    """

    def __init__(self, doc: ODTDocument):
        self._doc = doc
        self._regular_style_parser = RegularStyleParser()
        self._automatic_style_parser = AutomaticStyleParser()
        self._default_style_parser = DefaultStyleParser()
        self._table_parser = TableParser()
        self._list_parser = ListParser()
        self._image_parser = ImageParser()
        self._paragraph_parser = ParagraphParser()
        self._all_automatic_styles = self.automatic_style_parser.automatic_style_dict(self.doc, consts.DEFAULT_PARAM)
        self._all_default_styles = self.default_style_parser.default_style_dict(self.doc, consts.DEFAULT_PARAM)
        self._all_regular_styles = self.regular_style_parser.regular_style_dict(self.doc, consts.DEFAULT_PARAM)
        self.build_styles_dicts()

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
    def doc(self):
        return self._doc

    @doc.setter
    def doc(self, value):
        self._doc = value

    @property
    def all_automatic_styles(self):
        return self._all_automatic_styles

    @all_automatic_styles.setter
    def all_automatic_styles(self, value):
        self._all_automatic_styles = value

    @property
    def all_default_styles(self):
        return self._all_default_styles

    @all_default_styles.setter
    def all_default_styles(self, value):
        self._all_default_styles = value

    @property
    def all_regular_styles(self):
        return self._all_regular_styles

    @all_regular_styles.setter
    def all_regular_styles(self, value):
        self._all_regular_styles = value

    def extract_tables(self) -> list[Table]:
        """Extracts all tables from an ODT document.

        Returns
            tables: list
                The list of tables in ODT document
        ----------
        Извлекает все таблицы из ODT документа.
        """
        pass

    def extract_pictures(self) -> list[Frame]:
        """Extracts all images from an ODT document.

        Returns
            frames: list
                The list of images in ODT document
        ----------
        Извлекает все изображения из ODT документа.
        """
        return self.image_parser.get_frame_styles(self.doc)

    def extract_formulas(self) -> list[Formula]:
        """Extracts all formulas from an ODT document.

        Returns
            formulas: list
                The list of formulas in ODT document
        ----------
        Извлекает все формулы из ODT документа.
        """
        pass

    def get_all_elements(self) -> UnifiedDocumentView:
        """Forms structural elements of the document based on tables, paragraphs, lists and images.

        Returns
            unified_document: UnifiedDocumentView
                List of all structural elements in the ODT document
        -------
        Формирует структурные элементы документа на основе таблиц, абзацев, списков и изображений.
        """
        creator = self.doc._document.element_dict[('http://purl.org/dc/elements/1.1/', 'creator')][0].lastChild.data
        creation_date = self.doc._document.element_dict[('urn:oasis:names:tc:opendocument:xmlns:meta:1.0',
                                                    'creation-date')][0].lastChild.data
        page_count = self.doc._document.element_dict[('urn:oasis:names:tc:opendocument:xmlns:meta:1.0',
                                                 'document-statistic')][0].attributes[
            ('urn:oasis:names:tc:opendocument:xmlns:meta:1.0', 'page-count')]
        unified_document = UnifiedDocumentView(owner=creator,
                                                     time=creation_date,
                                                     page_count=page_count)

        all_doc_info = self.get_document_nodes_with_higher_style_data(self.doc.document.content, consts.DEFAULT_PARAM)
        all_paragraphs = self.paragraph_parser.paragraphs_helper(styles_data=all_doc_info)
        all_frames = self.image_parser.get_frame_styles(self.doc)
        all_lists = self.list_parser.get_list_styles_from_automatic_styles(self.doc, all_doc_info)
        obj_id = 1
        for paragraph in all_paragraphs:
            unified_document.add_content(obj_id, paragraph)
            obj_id += 1
        for frame in all_frames:
            unified_document.add_content(obj_id, frame)
            obj_id += 1
        for list in all_lists:
            unified_document.add_content(obj_id, list)
            obj_id += 1
        return unified_document

    def extract_paragraphs(self) -> list[Paragraph]:
        """Extracts all paragraphs from an ODT document.

        Returns
            paragraphs: list
                The list of paragraphs in ODT document
        ----------
        Извлекает все параграфы из ODT документа.
        """
        all_doc_info = self.get_document_nodes_with_higher_style_data(self.doc.document.content, consts.DEFAULT_PARAM)
        return self.paragraph_parser.paragraphs_helper(styles_data=all_doc_info)

    def extract_lists(self) -> list[StructuralElement]:
        """Extracts all lists from an ODT document.

        Returns
            lists: list
                The list of lists in ODT document
        ----------
        Извлекает все списки из ODT документа.
        """
        all_doc_info = self.get_document_nodes_with_higher_style_data(self.doc.document.content, consts.DEFAULT_PARAM)
        return self.list_parser.get_list_styles_from_automatic_styles(self.doc, all_doc_info)

    def build_styles_dicts(self):
        """Implements an inheritance mechanism for document styles.
        -------
        Реализует у стилей документа механизм наследования.
        """
        self._all_default_styles = self.build_default_styles_inheritance()
        self._all_regular_styles = self.build_regular_styles_inheritance()
        self._all_automatic_styles = self.build_automatic_styles_inheritance()

    def build_regular_styles_inheritance(self):
        """Implements the regular styles inheritance mechanism in the document.

        Returns
            _all_regular_styles: dict
                Dictionary of all regular styles in the ODT document
        -------
        Реализует механизм наследования обычных стилей в документе.
        """
        while True:
            flag = 0
            for key in self._all_regular_styles.keys():
                if self._all_regular_styles[key] is not None:
                    if "parent-style-name" in self._all_regular_styles[key].keys():
                        parent = self._all_regular_styles[key]["parent-style-name"]
                        att = self._all_regular_styles[parent]
                    else:
                        if self._all_regular_styles[key]["family"] in self.all_default_styles.keys():
                            parent = self._all_regular_styles[key]["family"]
                            att = self.all_default_styles[parent]
                        else:
                            att = consts.DEFAULT_PARAM
                    for style_key in self._all_regular_styles[key].keys():
                        if self._all_regular_styles[key][style_key] is None:
                            if att[style_key] is None:
                                flag = 1
                            else:
                                self._all_regular_styles[key][style_key] = att[style_key]

            if flag == 0:
                break
        return self._all_regular_styles

    def build_default_styles_inheritance(self):
        """Implements the default styles inheritance mechanism in the document.

        Returns
            all_default_styles: dict
                Dictionary of all default styles in the ODT document
        -------
        Реализует механизм наследования стилей по умолчанию в документе.
        """
        for key in self._all_default_styles.keys():
            for style_key in self._all_default_styles[key].keys():
                if self._all_default_styles[key][style_key] is None:
                    self._all_default_styles[key][style_key] = consts.DEFAULT_PARAM[style_key]
        return self._all_default_styles

    def build_automatic_styles_inheritance(self):
        """Implements the automatic styles inheritance mechanism in the document.

        Returns
            all_automatic_styles: dict
                Dictionary of all automatic styles in the ODT document
        -------
        Реализует механизм наследования автоматических стилей в документе.
        """
        for key in self.all_automatic_styles.keys():
            for style_key in self.all_automatic_styles[key].keys():
                if self.all_automatic_styles[key][style_key] is None:
                    if "parent-style-name" in self.all_automatic_styles[key].keys():
                        parent = self.all_automatic_styles[key]["parent-style-name"]
                        att = self._all_regular_styles[parent][style_key]
                    else:
                        att = consts.DEFAULT_PARAM[style_key]
                    self.all_automatic_styles[key][style_key] = att
        return self._all_automatic_styles

    def find_style_with_inheritance(self, style_name):
        """Searches for the desired style among styles, taking into account their inheritance.

        Returns
            style: dict
                Dictionary with ODT document style data
        -------
        Выполняет поиск нужного стиля среди стилей с учетом их наследования.
        """
        if style_name in self.all_automatic_styles:
            return self.all_automatic_styles[style_name]
        else:
            return self.all_regular_styles[style_name]

    def get_document_nodes_with_style_full_list(self, start_node, parent_node, list_of_nodes=None, level=0):
        """Returns each node of the document and its attributes.

        Returns
            list_of_nodes: dict
                Dictionary with ODT document nodes data
        -------
        Возвращает каждый узел документа и его атрибуты.
        """
        if list_of_nodes is None:
            list_of_nodes = {}
        if start_node.nodeType == 1:
            for k in start_node.attributes.keys():
                if (k[1] == "style-name"):
                    att = self.find_style_with_inheritance(start_node.attributes[k])
                    for kk in att.keys():
                        if kk in consts.DEFAULT_PARAM.keys():
                            if att[kk] is consts.DEFAULT_PARAM[kk]:
                                att[kk] = parent_node[kk]
                    att["text"] = str(start_node)
                    parent_node = att
                    list_of_nodes[start_node.attributes[k]] = att
            for n in start_node.childNodes:
                self.get_document_nodes_with_style_full_list(n, parent_node, list_of_nodes, level + 1)
        return list_of_nodes

    def get_document_nodes_with_styles(self, start_node, parent_node, list_of_nodes=None, level=0):
        """Returns each node of the document and its attributes with a passage through all styles, searching,
        in case of absence, in nodes at a higher level.

        Keyword arguments:
            start_node - initial search node;
            parent_node - parent node of the current node.;
            level - search level and recursion nesting;
            list_of_nodes - the final collection of all nodes.

        Returns:
            list_of_nodes: dict
                Dictionary with document nodes
        ----------
        Возвращает каждый каждый узел документа и его атрибуты с прохождением по всем стилям,
        выполняя поиск, в случае отсутствия, в узлах уровнем выше.

        Аргументы:
            start_node - начальный узел поиска;
            parent_node - родительский узел текуще гоузла;
            level - уровень поиска и вложенности рекурсии;
            list_of_nodes - итоговая коллекция всех узлов.
        """
        if list_of_nodes is None:
            list_of_nodes = {}
        if start_node.nodeType == 1:
            if start_node.qname[1] == "list":
                for key in start_node.attributes.keys():
                    if (key[1] == "style-name"):
                        att = self.find_style_with_inheritance(start_node.attributes[key])
                        for style_key in att.keys():
                            if style_key in consts.DEFAULT_PARAM.keys():
                                if att[style_key] is consts.DEFAULT_PARAM[style_key]:
                                    att[style_key] = parent_node[style_key]
                        att["text"] = str(start_node)
                        parent_node = att
                        list_of_nodes[start_node.attributes[key]] = self.get_document_nodes_with_style_full_list(
                            start_node, parent_node, {})
            else:
                if start_node.qname[1] == "p":
                    for key in start_node.attributes.keys():
                        if (key[1] == "style-name"):
                            att = self.find_style_with_inheritance(start_node.attributes[key])
                            for style_key in att.keys():
                                if style_key in consts.DEFAULT_PARAM.keys():
                                    if att[style_key] is consts.DEFAULT_PARAM[style_key]:
                                        att[style_key] = parent_node[style_key]
                            att["text"] = str(start_node)
                            parent_node = att
                            par = Paragraph(_text=str(start_node), _font_name=att["font-name"],
                                            _text_size=att["font-size"])
                            if att["font-weight"] != "bold":
                                par.bold = False
                            else:
                                par.bold = True
                else:
                    for key in start_node.attributes.keys():
                        if (key[1] == "style-name"):
                            att = self.find_style_with_inheritance(start_node.attributes[key])
                            for style_key in att.keys():
                                if style_key in consts.DEFAULT_PARAM.keys():
                                    if att[style_key] is consts.DEFAULT_PARAM[style_key]:
                                        att[style_key] = parent_node[style_key]
                            att["text"] = str(start_node)
                            parent_node = att
                    for child_node in start_node.childNodes:
                        self.get_document_nodes_with_styles(child_node, parent_node, list_of_nodes, level + 1)
        return

    def get_document_nodes_with_higher_style_data(self, start_node, parent_node, level=0, list_of_nodes=None):
        """Returns each node of the document and its attributes with a passage through all styles, searching,
        in case of absence, in nodes at a higher level.

        Keyword arguments:
            start_node - initial search node;
            parent_node - parent node of the current node.;
            level - search level and recursion nesting;
            list_of_nodes - the final collection of all nodes.

        Returns:
            list_of_nodes: dict
                Dictionary with document nodes
        ----------
        Возвращает каждый каждый узел документа и его атрибуты с прохождением по всем стилям,
        выполняя поиск, в случае отсутствия, в узлах уровнем выше.

        Аргументы:
            start_node - начальный узел поиска;
            parent_node - родительский узел текуще гоузла;
            level - уровень поиска и вложенности рекурсии;
            list_of_nodes - итоговая коллекция всех узлов.
        """
        if list_of_nodes is None:
            list_of_nodes = {}
        if start_node.nodeType == 1:
            for key in start_node.attributes.keys():
                if (key[1] == "style-name"):
                    att = self.find_style_with_inheritance(start_node.attributes[key])
                    for style_key in att.keys():
                        if style_key in consts.DEFAULT_PARAM.keys():
                            if att[style_key] is consts.DEFAULT_PARAM[style_key]:
                                att[style_key] = parent_node[style_key]
                    att["text"] = str(start_node)
                    parent_node = att
                    list_of_nodes[start_node.qname[1] + " " + str(level)] = att
            for n in range(0, len(start_node.childNodes)):
                assistance_list = {}
                assistance_list["nodes"] = self.get_document_nodes_with_higher_style_data(start_node.childNodes[n],
                                                                                          parent_node, level + 1)
                assistance_list["type"] = start_node.qname[1]
                list_of_nodes[str(n)] = assistance_list
                self.get_document_nodes_with_higher_style_data(start_node.childNodes[n], parent_node, level + 1)
        return list_of_nodes