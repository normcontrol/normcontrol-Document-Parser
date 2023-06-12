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
from src.odt.elements.NodeParser import NodeParser
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

    def __init__(self, doc: ODTDocument):
        self._doc = doc
        self._regular_style_parser = RegularStyleParser()
        self._automatic_style_parser = AutomaticStyleParser()
        self._default_style_parser = DefaultStyleParser()
        self._table_parser = TableParser()
        self._list_parser = ListParser()
        self._image_parser = ImageParser()
        self._paragraph_parser = ParagraphParser()
        self._node_parser = NodeParser()
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
    def node_parser(self):
        return self._node_parser

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
        pass

    def extract_pictures(self) -> list[Frame]:
        return self.image_parser.get_frame_styles(self.doc)

    def extract_formulas(self) -> list[Formula]:
        pass

    def get_all_elements(self) -> UnifiedDocumentView:
        creator = self.doc._document.element_dict[('http://purl.org/dc/elements/1.1/', 'creator')][0].lastChild.data
        creation_date = self.doc._document.element_dict[('urn:oasis:names:tc:opendocument:xmlns:meta:1.0',
                                                    'creation-date')][0].lastChild.data
        page_count = self.doc._document.element_dict[('urn:oasis:names:tc:opendocument:xmlns:meta:1.0',
                                                 'document-statistic')][0].attributes[
            ('urn:oasis:names:tc:opendocument:xmlns:meta:1.0', 'page-count')]
        unified_document = UnifiedDocumentView(owner=creator,
                                                     time=creation_date,
                                                     page_count=page_count)

        all_doc_info = self.get_nodes_with_style_full7(self.doc.document.text, consts.DEFAULT_PARAM)
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
        all_doc_info = self.get_nodes_with_style_full7(self.doc.document.text, consts.DEFAULT_PARAM)
        return self.paragraph_parser.paragraphs_helper(styles_data=all_doc_info)

    def extract_lists(self) -> list[StructuralElement]:
        all_doc_info = self.get_nodes_with_style_full7(self.doc.document.text, consts.DEFAULT_PARAM)
        return self.list_parser.get_list_styles_from_automatic_styles(self.doc, all_doc_info)

    def build_styles_dicts(self):
        self._all_default_styles = self.default_inher()
        self._all_regular_styles = self.styles_inher()
        self._all_automatic_styles = self.auto_inher()

    def styles_inher(self):
        while True:
            flag = 0
            for k in self._all_regular_styles.keys():
                if self._all_regular_styles[k] is not None:
                    if "parent-style-name" in self._all_regular_styles[k].keys():
                        parent = self._all_regular_styles[k]["parent-style-name"]
                        att = self._all_regular_styles[parent]
                    else:
                        if self._all_regular_styles[k]["family"] in self.all_default_styles.keys():
                            parent = self._all_regular_styles[k]["family"]
                            att = self.all_default_styles[parent]
                        else:
                            att = consts.DEFAULT_PARAM
                    for kk in self._all_regular_styles[k].keys():
                        if self._all_regular_styles[k][kk] is None:
                            print(self._all_regular_styles[k][kk])
                            if att[kk] is None:
                                flag = 1
                            else:
                                self._all_regular_styles[k][kk] = att[kk]
                            print(self._all_regular_styles[k][kk])

            if flag == 0:
                break
        return self._all_regular_styles

    def default_inher(self):
        for k in self._all_default_styles.keys():
            for kk in self._all_default_styles[k].keys():
                if self._all_default_styles[k][kk] is None:
                    print(self._all_default_styles[k][kk])
                    self._all_default_styles[k][kk] = consts.DEFAULT_PARAM[kk]
                    print(self._all_default_styles[k][kk])
        return self._all_default_styles

    def auto_inher(self):
        for k in self.all_automatic_styles.keys():
            for kk in self.all_automatic_styles[k].keys():
                if self.all_automatic_styles[k][kk] is None:
                    if "parent-style-name" in self.all_automatic_styles[k].keys():
                        parent = self.all_automatic_styles[k]["parent-style-name"]
                        att = self._all_regular_styles[parent][kk]
                    else:
                        att = consts.DEFAULT_PARAM[kk]
                    print(self.all_automatic_styles[k][kk])
                    self.all_automatic_styles[k][kk] = att
                    print(self.all_automatic_styles[k][kk])
        return self.all_automatic_styles

    def inher_start6(self, stylename):
        if stylename in self.all_automatic_styles:
            return self.all_automatic_styles[stylename]
        else:
            return self.all_regular_styles[stylename]

    def get_nodes_with_style_full6(self, start_node, parent_node, list=None, level=0):
        if list is None:
            list = {}
        if start_node.nodeType == 1:
            if start_node.qname[1] == "list":
                for k in start_node.attributes.keys():
                    if (k[1] == "style-name"):
                        att = self.inher_start6(start_node.attributes[k])
                        for kk in att.keys():
                            if kk in consts.DEFAULT_PARAM.keys():
                                if att[kk] is consts.DEFAULT_PARAM[kk]:
                                    att[kk] = parent_node[kk]
                        att["text"] = str(start_node)
                        parent_node = att
                        list[start_node.attributes[k]] = self.get_nodes_with_style_full_list(start_node, parent_node,
                                                                                             {})
                        print(list)
                        print("  " * level, "Список:", start_node.qname[1], " Аттрибуты:(",
                              k[1] + ':' + start_node.attributes[k],
                              ") ", str(start_node), "параметр ", att)
            else:
                if start_node.qname[1] == "p":
                    for k in start_node.attributes.keys():
                        if (k[1] == "style-name"):
                            att = self.inher_start6(start_node.attributes[k])
                            for kk in att.keys():
                                if kk in consts.DEFAULT_PARAM.keys():
                                    if att[kk] is consts.DEFAULT_PARAM[kk]:
                                        att[kk] = parent_node[kk]
                            att["text"] = str(start_node)
                            parent_node = att
                            par = Paragraph(_text=str(start_node), _font_name=att["font-name"],
                                            _text_size=att["font-size"])
                            if att["font-weight"] != "bold":
                                par.bold = False
                            else:
                                par.bold = True
                            print("  " * level, "Узел:", start_node.qname[1], " Аттрибуты:(",
                                  k[1] + ':' + start_node.attributes[k],
                                  ") ", str(start_node), "параметр ", att)
                else:
                    for k in start_node.attributes.keys():
                        if (k[1] == "style-name"):
                            att = self.inher_start6(start_node.attributes[k])
                            for kk in att.keys():
                                if kk in consts.DEFAULT_PARAM.keys():
                                    if att[kk] is consts.DEFAULT_PARAM[kk]:
                                        att[kk] = parent_node[kk]
                            att["text"] = str(start_node)
                            parent_node = att
                            print("  " * level, "Узел:", start_node.qname[1], " Аттрибуты:(",
                                  k[1] + ':' + start_node.attributes[k],
                                  ") ", str(start_node), "параметр ", att)
                    for n in start_node.childNodes:
                        self.get_nodes_with_style_full6(n, parent_node, list, level + 1)
        return

    def get_nodes_with_style_full_list(self, start_node, parent_node, list=None, level=0):
        if list is None:
            list = {}
        if start_node.nodeType == 1:
            for k in start_node.attributes.keys():
                if (k[1] == "style-name"):
                    att = self.inher_start6(start_node.attributes[k])
                    for kk in att.keys():
                        if kk in consts.DEFAULT_PARAM.keys():
                            if att[kk] is consts.DEFAULT_PARAM[kk]:
                                att[kk] = parent_node[kk]
                    att["text"] = str(start_node)
                    parent_node = att
                    list[start_node.attributes[k]] = att
            for n in start_node.childNodes:
                self.get_nodes_with_style_full_list(n, parent_node, list, level + 1)
        return list


    def get_nodes_with_style_full7(self, start_node, parent_node, level=0, list=None):
        if list is None:
            list = {}
        if start_node.nodeType == 1:
            for k in start_node.attributes.keys():
                if (k[1] == "style-name"):
                    att = self.inher_start6(start_node.attributes[k])
                    for kk in att.keys():
                        if kk in consts.DEFAULT_PARAM.keys():
                            if att[kk] is consts.DEFAULT_PARAM[kk]:
                                att[kk] = parent_node[kk]
                    att["text"] = str(start_node)
                    parent_node = att
                    list[start_node.qname[1] + " " + str(level)] = att
                    print("  " * level, "Узел:", start_node.qname[1], " Аттрибуты:(",
                          k[1] + ':' + start_node.attributes[k],
                          ") ", str(start_node), "параметр ", att)
            for n in range(0, len(start_node.childNodes)):
                list1 = {}
                list1["nodes"] = self.get_nodes_with_style_full7(start_node.childNodes[n], parent_node, level + 1)
                list1["type"] = start_node.qname[1]
                list[str(n)] = list1
                self.get_nodes_with_style_full7(start_node.childNodes[n], parent_node, level + 1)
        return list