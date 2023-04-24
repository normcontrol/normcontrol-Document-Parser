"""
    Description: The module stores a class that containing methods for working with tables styles in an ODT document.
    ----------
    Описание: Модуль хранит класс, содержащий методы для работы со стилями таблиц в документе формата ODT.
"""
from src.odt.elements.ODTDocument import ODTDocument
from src.helpers.odt.converters import get_tables_objects

class TablesParser:
    """
        Description: A class containing methods for working with tables styles in an ODT document.

        Methods:
            get_table_styles(doc: ODTDocument) -
                Returns a list of all tables styles with their attributes.

            get_automatic_table_styles(doc: ODTDocument) -
                Returns a list of all tables styles from automatic document styles with their attributes.

            get_table_parameter(style, parameter_name: str) -
                Returns a style parameter by attribute among table styles.

            get_table_row_parameter(style, parameter_name: str) -
                Returns a style parameter by attribute among tables rows styles.

            get_table_column_parameter(style, parameter_name: str) -
                Returns a style parameter by attribute among table columns styles.

            get_table_cell_parameter(style, parameter_name: str) -
                Returns a style parameter by attribute among table cells styles.

            get_all_odt_tables_text(doc: ODTDocument) -
                Returns the text of all the tables in the document.
        ----------
        Описание: Класс, содержащий методы для работы со стилями таблиц в документе формата ODT.

        Методы:
            get_table_styles(doc: ODTDocument) -
                Возвращает список всех стилей таблиц документа с их атрибутами.

            get_automatic_table_styles(doc: ODTDocument) -
                Возвращает список всех стилей таблиц из автоматических стилей документа с их атрибутами.

            get_table_parameter(style, parameter_name: str) -
                Возвращает параметр стиля по атрибуту среди стилей таблиц.

            get_table_row_parameter(style, parameter_name: str) -
                Возвращает параметр стиля по атрибуту среди стилей строк таблиц.

            get_table_column_parameter(style, parameter_name: str) -
                Возвращает параметр стиля по атрибуту среди стилей столбцов таблиц.

            get_table_cell_parameter(style, parameter_name: str) -
                Возвращает параметр стиля по атрибуту среди стилей ячеек таблиц.

            get_all_odt_tables_text(doc: ODTDocument) -
                Возвращает текст всех таблиц документа.
        """

    def get_table_styles(self, doc: ODTDocument):
        """Returns a list of all tables styles with their attributes.

        Keyword arguments:
            doc - an instance of the ODTDocument class containing the data of the document under study.
        ----------
        Возвращает список всех стилей таблиц документа с их атрибутами.

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
                    if node.qname[1] == "table-properties" or node.qname[1] == "table-column-properties" \
                            or node.qname[1] == "table-row-properties" or node.qname[1] == "table-cell-properties":
                        for key in node.attributes.keys():
                            style[node.qname[1] + "/" + key[1]] = node.attributes[key]
        return get_tables_objects(styles_dict)

    def get_automatic_table_styles(self, doc: ODTDocument):
        """Returns a list of all tables styles from automatic document styles with their attributes.

        Keyword arguments:
            doc - an instance of the ODTDocument class containing the data of the document under study.
        ----------
        Возвращает список всех стилей таблиц из автоматических стилей документа с их атрибутами.

        Аргументы:
            doc - экземпляр класса ODTDocument, содержащий данные исследуемого документа.
        """
        styles_dict = {}
        for ast in doc.document.automaticstyles.childNodes:
            name = ast.getAttribute('name')
            if name.count('able') > 0:
                style = {}
                styles_dict[name] = style
                for key in ast.attributes.keys():
                    style[ast.qname[1] + "/" + key[1]] = ast.attributes[key]
                for node in ast.childNodes:
                    for key in node.attributes.keys():
                        style[node.qname[1] + "/" + key[1]] = node.attributes[key]
        return get_tables_objects(styles_dict)

    def get_table_parameter(self, style, parameter_name: str):
        """Returns a style parameter by attribute among table styles.

        Keyword arguments:
            style - a style object for research;
            parameter_name - string name of the desired parameter.
        ----------
        Возвращает параметр стиля по атрибуту среди стилей таблиц.

        Аргументы:
            style - объект стиля для исследования;
            parameter_name - строковое название искомого параметра.
        """
        for node in style.childNodes:
            if node.qname[1] == "table-properties":
                for key in node.attributes.keys():
                    if key[1] == parameter_name:
                        return node.attributes[key]
        return None

    def get_table_row_parameter(self, style, parameter_name: str):
        """Returns a style parameter by attribute among tables rows styles.

        Keyword arguments:
            style - a style object for research;
            parameter_name - string name of the desired parameter.
        ----------
        Возвращает параметр стиля по атрибуту среди стилей строк таблиц.

        Аргументы:
            style - объект стиля для исследования;
            parameter_name - строковое название искомого параметра.
        """
        for node in style.childNodes:
            if node.qname[1] == "table-row-properties":
                for key in node.attributes.keys():
                    if key[1] == parameter_name:
                        return node.attributes[key]
        return None

    def get_table_column_parameter(self, style, parameter_name: str):
        """Returns a style parameter by attribute among table columns styles.

        Keyword arguments:
            style - a style object for research;
            parameter_name - string name of the desired parameter.
        ----------
        Возвращает параметр стиля по атрибуту среди стилей столбцов таблиц.

        Аргументы:
            style - объект стиля для исследования;
            parameter_name - строковое название искомого параметра.
        """
        for node in style.childNodes:
            if node.qname[1] == "table-column-properties":
                for key in node.attributes.keys():
                    if key[1] == parameter_name:
                        return node.attributes[key]
        return None

    def get_table_cell_parameter(self, style, parameter_name: str):
        """Returns a style parameter by attribute among table cells styles.

        Keyword arguments:
            style - a style object for research;
            parameter_name - string name of the desired parameter.
        ----------
        Возвращает параметр стиля по атрибуту среди стилей ячеек таблиц.

        Аргументы:
            style - объект стиля для исследования;
            parameter_name - строковое название искомого параметра.
        """
        for node in style.childNodes:
            if node.qname[1] == "table-cell-properties":
                for key in node.attributes.keys():
                    if key[1] == parameter_name:
                        return node.attributes[key]
        return None