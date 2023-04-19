"""
    Description: The module stores a class that containing methods for working with lists styles in an ODT document.
    ----------
    Описание: Модуль хранит класс, содержащий методы для работы со стилями списков в документе формата ODT.
"""
from src.odt.elements.ODTDocument import ODTDocument
from src.classes.List import List
from src.helpers.odt.converters import convert_to_list
from dacite import from_dict

class ListsParser:
    """
    Description: A class containing methods for working with lists styles in an ODT document.

    Methods:
        get_list_styles(doc: ODTDocument) -
            Returns a list of all list styles with their attributes.

        get_lists_text_styles(doc: ODTDocument) -
            Returns a list of all text styles with their attributes from the lists styles of document.

        get_list_styles_from_automatic_styles(doc: ODTDocument) -
            Returns a list of all list styles from automatic document styles with their attributes.

        get_list_parameter(style, parameter_name: str) -
            Returns a style parameter by attribute among list styles.
    ----------
    Описание: Класс, содержащий методы для работы со стилями списков в документе формата ODT.

    Методы:
        get_list_styles(doc: ODTDocument) -
            Возвращает список всех стилей списков документа с их атрибутами.

        get_lists_text_styles(doc: ODTDocument) -
            Возвращает список всех текстовых стилей с их атрибутами из списка стилей документа.

        get_list_styles_from_automatic_styles(doc: ODTDocument) -
            Возвращает список всех стилей списков из автоматических стилей документа с их атрибутами.

        get_list_parameter(style, parameter_name: str) -
            Возвращает параметр стиля по атрибуту среди стилей списков.
    """

    def get_list_styles(self, doc: ODTDocument):
        """Returns a list of all list styles with their attributes.

        Keyword arguments:
            doc - an instance of the ODTDocument class containing the data of the document under study.
        ----------
        Возвращает список всех стилей списков документа с их атрибутами.

        Аргументы:
            doc - экземпляр класса ODTDocument, содержащий данные исследуемого документа.
        """
        styles_dict = {}
        for ast in doc.document.styles.childNodes:
            if ast.qname[1] == "style":
                name = ast.getAttribute('name')
                style = {}
                styles_dict[name] = style
                for node in ast.childNodes:
                    if "list" in node.qname[1]:
                        for key in node.attributes.keys():
                            style[node.qname[1] + "/" + key[1]] = node.attributes[key]
        return styles_dict

    def get_lists_text_styles(self, doc: ODTDocument):
        """Returns a list of all text styles with their attributes from the lists styles of document.

        Keyword arguments:
            doc - an instance of the ODTDocument class containing the data of the document under study.
        ----------
        Возвращает список всех текстовых стилей с их атрибутами из списка стилей документа.

        Аргументы:
            doc - экземпляр класса ODTDocument, содержащий данные исследуемого документа.
        """
        styles_dict = {}
        for ast in doc.document.styles.childNodes:
            if ast.qname[1] == "style":
                name = ast.getAttribute('name')
                style = {}
                if 'Абзацсписка' in name or 'WW' in name or 'LF' in name:
                    styles_dict[name] = style
                    for node in ast.childNodes:
                        if node.qname[1] == "text-properties":
                            for key in node.attributes.keys():
                                style[node.qname[1] + "/" + key[1]] = node.attributes[key]
        return styles_dict

    def get_list_styles_from_automatic_styles(self, doc: ODTDocument):
        """Returns a list of all list styles from automatic document styles with their attributes.

        Keyword arguments:
            doc - an instance of the ODTDocument class containing the data of the document under study.
        ----------
        Возвращает список всех стилей списков из автоматических стилей документа с их атрибутами.

        Аргументы:
            doc - экземпляр класса ODTDocument, содержащий данные исследуемого документа.
        """
        styles_dict = {}
        list_objs = []
        for ast in doc.document.automaticstyles.childNodes:
            name = ast.getAttribute('name')
            style = {}
            for node in ast.childNodes:
                if "list-level" in node.qname[1]:
                    styles_dict[name] = style
                    for key in node.attributes.keys():
                        style[node.qname[1] + "/" + key[1]] = node.attributes[key]
        for cur_style in styles_dict:
            list_objs.append(from_dict(data_class=List, data=convert_to_list(cur_style, styles_dict[cur_style])))
        return list_objs

    def get_list_parameter(self, style, parameter_name: str):
        """Returns a style parameter by attribute among list styles.

        Keyword arguments:
            style - a style object for research;
            parameter_name - string name of the desired parameter.
        ----------
        Возвращает параметр стиля по атрибуту среди стилей списков.

        Аргументы:
            style - объект стиля для исследования;
            parameter_name - строковое название искомого параметра.
        """
        for node in style.childNodes:
            if "list" in node.qname[1] or "text" in node.qname[1]:
                for key in node.attributes.keys():
                    if key[1] == parameter_name:
                        return node.attributes[key]
        return None