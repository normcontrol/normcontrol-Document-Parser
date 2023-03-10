from odf.table import Table
from src.odt.elements.ODTDocument import ODTDocument

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
        stylesDict = {}
        for ast in doc.document.styles.childNodes:
            if ast.qname[1] == "style":
                name = ast.getAttribute('name')
                style = {}
                stylesDict[name] = style

                for n in ast.childNodes:
                    if n.qname[1] == "table-properties" or n.qname[1] == "table-column-properties" \
                            or n.qname[1] == "table-row-properties" or n.qname[1] == "table-cell-properties":
                        for k in n.attributes.keys():
                            style[n.qname[1] + "/" + k[1]] = n.attributes[k]
        return stylesDict

    def get_automatic_table_styles(self, doc: ODTDocument):
        """Returns a list of all tables styles from automatic document styles with their attributes.

        Keyword arguments:
            doc - an instance of the ODTDocument class containing the data of the document under study.
        ----------
        Возвращает список всех стилей таблиц из автоматических стилей документа с их атрибутами.

        Аргументы:
            doc - экземпляр класса ODTDocument, содержащий данные исследуемого документа.
        """
        styles = {}
        for ast in doc.document.automaticstyles.childNodes:
            name = ast.getAttribute('name')
            style = {}
            styles[name] = style
            for n in ast.childNodes:
                if n.qname[1] == "table-properties" or n.qname[1] == "table-column-properties" \
                        or n.qname[1] == "table-row-properties" or n.qname[1] == "table-cell-properties":
                    for k in n.attributes.keys():
                        style[n.qname[1] + "/" + k[1]] = n.attributes[k]
        return styles

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
        for n in style.childNodes:
            if n.qname[1] == "table-properties":
                for k in n.attributes.keys():
                    if k[1] == parameter_name:
                        return n.attributes[k]

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
        for n in style.childNodes:
            if n.qname[1] == "table-row-properties":
                for k in n.attributes.keys():
                    if k[1] == parameter_name:
                        return n.attributes[k]

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
        for n in style.childNodes:
            if n.qname[1] == "table-column-properties":
                for k in n.attributes.keys():
                    if k[1] == parameter_name:
                        return n.attributes[k]

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
        for n in style.childNodes:
            if n.qname[1] == "table-cell-properties":
                for k in n.attributes.keys():
                    if k[1] == parameter_name:
                        return n.attributes[k]

    def get_all_odt_tables_text(self, doc: ODTDocument):
        """Returns the text of all the tables in the document.

        Keyword arguments:
            doc - an instance of the ODTDocument class containing the data of the document under study.
        ----------
        Возвращает текст всех таблиц документа.

        Аргументы:
            doc - экземпляр класса ODTDocument, содержащий данные исследуемого документа.
        """
        table_text = []
        for table in doc.document.getElementsByType(Table):
            table_text.append(table)
            print(table)
        return table_text