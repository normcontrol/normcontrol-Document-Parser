"""
    Description: The module stores a class that containing methods for working with default styles in an ODT document.
    ----------
    Описание: Модуль хранит класс, содержащий методы для работы со стилями по умолчанию в документе формата ODT.
"""
from src.odt.elements.ODTDocument import ODTDocument

class DefaultStyleParser:
    """
    Description: A class containing methods for working with default styles in an ODT document.

    Methods:
        get_default_styles(doc: ODTDocument) -
            Returns a list of all default document styles with their attributes.

        get_default_style_by_family(doc: ODTDocument, style_family: str) -
            Searches for a style by style-family among default styles and returns its attributes.

        get_default_style_object_by_family(doc: ODTDocument, style_family: str) -
            Searches for a style by style-family among default styles and returns it as an object to work with.

        get_default_style_parameters(style, parameter_name: str, property_type: str) -
            Gets a style parameter by name and attribute among the default styles.

        has_default_parameter(self, doc: ODTDocument, style_parameter: str, family: str, parameter_name: str,
        property_type: str) -
            Checks whether the parameter is contained in the default styles.
    ----------
    Описание: Класс, содержащий методы для работы со стилями по умолчанию в документе формата ODT.

    Методы:
        get_default_styles(doc: ODTDocument) -
            Возвращает список всех стилей по умолчанию документа с их атрибутами.

        get_default_style_by_name(doc: ODTDocument, style_family: str) -
            Выполняет поиск стиля по семейству стилей среди стилей по умолчанию и возвращает его атрибуты.

        get_default_style_object_by_family(doc: ODTDocument, style_family: str) -
            Выполняет поиск стиля по семейству стилей среди стилей по умолчанию и возвращает его как
            объект для работы.

        get_default_style_parameters(style, parameter_name: str, property_type: str) -
            Получает параметр стиля по имени и атрибуту среди стилей по умолчанию.

        has_default_parameter(self, doc: ODTDocument, style_parameter: str, family: str, parameter_name: str,
        property_type: str) -
            Проверяет содержится ли параметр в стилях по умолчанию.
    """

    def get_default_styles(self, doc: ODTDocument):
        """Returns a list of all default document styles with their attributes.

        Keyword arguments:
            doc - an instance of the ODTDocument class containing the data of the document under study.
        ----------
        Возвращает список всех стилей по умолчанию документа с их атрибутами.

        Аргументы:
            doc - экземпляр класса ODTDocument, содержащий данные исследуемого документа.
        """
        styles_dict = {}
        for ast in doc.document.styles.childNodes:
            if ast.qname[1] == "default-style":
                family = ast.getAttribute('family')
                style = {}
                styles_dict[family] = style

                for key in ast.attributes.keys():
                    style[key[1]] = ast.attributes[key]
                for node in ast.childNodes:
                    for node_keys in node.attributes.keys():
                        style[node.qname[1] + "/" + node_keys[1]] = node.attributes[node_keys]
        return styles_dict

    def get_default_style_by_family(self, doc: ODTDocument, style_family: str):
        """Searches for a style by style-family among default styles and returns its attributes.

        Keyword arguments:
            doc - an instance of the ODTDocument class containing the data of the document under study;
            style_family - string name of the desired style.
        ----------
        Выполняет поиск стиля по родительскому стилю среди стилей по умолчанию и возвращает его атрибуты.

        Аргументы:
            doc - экземпляр класса ODTDocument, содержащий данные исследуемого документа;
            style_family - строковое название искомого стиля.
        """
        styles_dict = {}
        for ast in doc.document.styles.childNodes:
            if ast.qname[1] == "default-style":
                if ast.getAttribute("family") == style_family:
                    for key in ast.attributes.keys():
                        styles_dict[key[1]] = ast.attributes[key]
                    for node in ast.childNodes:
                        for node_keys in node.attributes.keys():
                            styles_dict[node.qname[1] + "/" + node_keys[1]] = node.attributes[node_keys]
        return styles_dict

    def get_default_style_object_by_family(self, doc: ODTDocument, style_family: str):
        """Searches for a style by style-family among default styles and returns it as an object to work with.

        Keyword arguments:
            doc - an instance of the ODTDocument class containing the data of the document under study;
            style_family - string name of the desired style.
        ----------
        Выполняет поиск стиля по родительскому стилю среди стилей по умолчанию и возвращает его как объект для работы.

        Аргументы:
            doc - экземпляр класса ODTDocument, содержащий данные исследуемого документа;
            style_family - строковое название искомого стиля.
        """
        for ast in doc.document.styles.childNodes:
            if ast.qname[1] == "default-style":
                if ast.getAttribute("family") == style_family:
                    return ast
        return None

    def get_default_style_parameters(self, style, parameter_name: str, property_type: str):
        """Gets a style parameter by name and attribute among the default styles.

        Keyword arguments:
            style - a style object for research;
            param_name - string name of the desired parameter;
            property_type - string name of the desired attribute.
        ----------
        Получает параметр стиля по имени и атрибуту среди стилей по умолчанию.

        Аргументы:
            style - объект стиля для исследования;
            param_name - строковое название искомого параметра;
            property_type - строковое название искомого атрибута.
        """
        for node in style.childNodes:
            if node.qname[1] == property_type:
                for key in node.attributes.keys():
                    if key[1] == parameter_name:
                        return node.attributes[key]
        return None

    def has_default_parameter(self, doc: ODTDocument, style_parameter: str, family: str, parameter_name: str,
                              property_type: str):
        """Checks whether the parameter is contained in the default styles.

        Keyword arguments:
            doc - an instance of the ODTDocument class containing the data of the document under study;
            style_param - parameter of the style object to be explored;
            family - a family style object for research;
            param_name - string name of the desired parameter;
            property_type - string name of the desired attribute.
        ----------
        Проверяет содержится ли параметр в стилях по умолчанию.

        Аргументы:
            doc - экземпляр класса ODTDocument, содержащий данные исследуемого документа;
            style_param - параметр объекта стиля для исследования;
            family - объект для исследования в семействе стиле;
            param_name - строковое название искомого параметра;
            property_type - строковое название искомого атрибута.
        """
        style = self.get_default_style_object_by_family(doc, family)
        if style is not None:
            param = self.get_default_style_parameters(style, parameter_name, property_type)
            if param is not None:
                style_parameter = param
        return style_parameter