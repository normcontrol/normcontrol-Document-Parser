from src.odt.elements.ODTDocument import ODTDocument
from src.odt.elements.RegularStylesParser import RegularStylesParser
from src.odt.elements.ParagraphsParser import ParagraphsParser

class AutomaticStylesParser:
    """
    Description: A class containing methods for working with automatic styles in an ODT document.

    Methods:
        get_automatic_styles(doc: ODTDocument) -
            Returns a list of all automatic document styles with their attributes.

        get_text_styles_from_automatic_styles(doc: ODTDocument) -
            Returns a list of all text styles with their attributes from the automatic document styles.

        get_automatic_style_by_name(doc: ODTDocument, style_name: str) -
            Searches for a style by name among automatic styles and returns its attributes.

        get_text_style_by_name(doc: ODTDocument, text_name: str) -
            Searches for a text style by name among automatic styles and returns its attributes.

        get_automatic_style_object_by_name(doc: ODTDocument, style_name: str) -
            Searches for a style by name among automatic styles and returns it as an object to work with.

        has_automatic_style_parameter(doc: ODTDocument, style, param_name: str, default: str, property_type: str) -
            Checks whether the parameter is contained in the automatic styles.

        is_automatic_style(self, doc: ODTDocument, style_name: str, param_name: str, property_type: str,
        default: str) -
            Determines whether the specified style is automatic or embedded in the editor.
    ----------
    Описание: Класс, содержащий методы для работы с автоматическими стилями в документе формата ODT.

    Методы:
        get_automatic_styles(doc: ODTDocument) -
            Возвращает список всех автоматических стилей документа с их атрибутами.

        get_text_styles_from_automatic_styles(doc: ODTDocument) -
            Возвращает список всех стилей текста с их атрибутами из автоматических стилей документа.

        get_automatic_style_by_name(doc: ODTDocument, style_name: str) -
            Выполняет поиск стиля по имени среди автоматических стилей и возвращает его атрибуты.

        get_text_style_by_name(doc: ODTDocument, text_name: str) -
            Выполняет поиск текстового стиля по имени среди автоматических стилей и возвращает его атрибуты.

        get_automatic_style_object_by_name(doc: ODTDocument, style_name: str) -
            Выполняет поиск стиля по имени среди автоматических стилей и возвращает его как объект для работы.

        has_automatic_style_parameter(doc: ODTDocument, style, param_name: str, default: str, property_type: str) -
            Проверяет содержится ли параметр в автоматических стилях.

        is_automatic_style(self, doc: ODTDocument, style_name: str, param_name: str, property_type: str,
        default: str) -
            Определяет является ли указанный стиль автоматическим или встроенным в редактор.
    """

    def get_automatic_styles(self, doc: ODTDocument):
        """Returns a list of all automatic document styles with their attributes.

        Keyword arguments:
            doc - an instance of the ODTDocument class containing the data of the document under study.
        ----------
        Возвращает список всех автоматических стилей документа с их атрибутами.

        Аргументы:
            doc - экземпляр класса ODTDocument, содержащий данные исследуемого документа.
        """
        styles = {}
        for ast in doc.document.automaticstyles.childNodes:
            name = ast.getAttribute('name')
            style = {}
            styles[name] = style
            for k in ast.attributes.keys():
                style[k[1]] = ast.attributes[k]
            for n in ast.childNodes:
                for k in n.attributes.keys():
                    style[n.qname[1] + "/" + k[1]] = n.attributes[k]
        return styles

    def get_text_styles_from_automatic_styles(self, doc: ODTDocument):
        """Returns a list of all text styles with their attributes from the automatic document styles.

        Keyword arguments:
            doc - an instance of the ODTDocument class containing the data of the document under study.
        ----------
        Возвращает список всех стилей текста с их атрибутами из автоматических стилей документа.

        Аргументы:
            doc - экземпляр класса ODTDocument, содержащий данные исследуемого документа.
        """
        styles = {}
        for ast in doc.document.automaticstyles.childNodes:
            name = ast.getAttribute('name')
            style = {}
            styles[name] = style
            for n in ast.childNodes:
                if n.qname[1] == "text-properties":
                    for k in n.attributes.keys():
                        style[n.qname[1] + "/" + k[1]] = n.attributes[k]
        return styles

    def get_automatic_style_by_name(self, doc: ODTDocument, style_name: str):
        """Searches for a style by name among automatic styles and returns its attributes.

        Keyword arguments:
            doc - an instance of the ODTDocument class containing the data of the document under study;
            style_name - string name of the desired style.
        ----------
        Выполняет поиск стиля по имени среди автоматических стилей и возвращает его атрибуты.

        Аргументы:
            doc - экземпляр класса ODTDocument, содержащий данные исследуемого документа;
            style_name - строковое название искомого стиля.
        """
        style = {}
        for ast in doc.document.automaticstyles.childNodes:
            if ast.getAttribute("name") == style_name:
                for k in ast.attributes.keys():
                    style[k[1]] = ast.attributes[k]
                for n in ast.childNodes:
                    for k in n.attributes.keys():
                        style[n.qname[1] + "/" + k[1]] = n.attributes[k]
        return style

    def get_text_style_by_name(self, doc: ODTDocument, text_name: str):
        """Searches for a text style by name among automatic styles and returns its attributes.

        Keyword arguments:
            doc - an instance of the ODTDocument class containing the data of the document under study;
            text_name - string name of the desired text style.
        ----------
        Выполняет поиск текстового стиля по имени среди автоматических стилей и возвращает его атрибуты.

        Аргументы:
            doc - экземпляр класса ODTDocument, содержащий данные исследуемого документа;
            text_name - строковое название искомого текстового стиля.
        """
        text_styles = {}
        for ast in doc.document.automaticstyles.childNodes:
            if ast.qname[1] == "style":
                if ast.getAttribute("name") == text_name:
                    for k in ast.attributes.keys():
                        text_styles[k[1]] = ast.attributes[k]
                    for n in ast.childNodes:
                        for k in n.attributes.keys():
                            text_styles[n.qname[1] + "/" + k[1]] = n.attributes[k]
        return text_styles

    def get_automatic_style_object_by_name(self, doc: ODTDocument, style_name: str):
        """Searches for a style by name among automatic styles and returns it as an object to work with.

        Keyword arguments:
            doc - an instance of the ODTDocument class containing the data of the document under study;
            style_name - string name of the desired style.
        ----------
        Выполняет поиск стиля по имени среди автоматических стилей и возвращает его как объект для работы.

        Аргументы:
            doc - экземпляр класса ODTDocument, содержащий данные исследуемого документа;
            style_name - строковое название искомого стиля.
        """
        for ast in doc.document.automaticstyles.childNodes:
            if ast.getAttribute("name") == style_name:
                return ast

    def has_automatic_style_parameter(self, doc: ODTDocument, style, param_name: str, default: str,
                    property_type: str):
        """Checks whether the parameter is contained in the automatic styles.

        Keyword arguments:
            doc - an instance of the ODTDocument class containing the data of the document under study;
            style - a style object for research;
            param_name - string name of the desired parameter;
            default - default value for the desired attribute;
            property_type - string name of the desired attribute.
        ----------
        Проверяет содержится ли параметр в автоматических стилях.

        Аргументы:
            doc - экземпляр класса ODTDocument, содержащий данные исследуемого документа;
            style - объект стиля для исследования;
            param_name - строковое название искомого параметра;
            default - значение по умолчанию для искомого атрибута;
            property_type - строковое название искомого атрибута.
        """
        paragraphs_parser = ParagraphsParser()
        param = paragraphs_parser.get_paragraph_parameters(style, param_name, property_type)
        if param is None:
            for k in style.attributes.keys():
                if k[1] == "parent-style-name":
                    parser_regular_styles = RegularStylesParser()
                    default = parser_regular_styles.get_parameter_from_regular_style(doc, default, style.attributes[k],
                                                                                     param_name, property_type)
                    break
        else:
            default = param_name
        return default

    def is_automatic_style(self, doc: ODTDocument, style_name: str, param_name: str, property_type: str,
                    default: str):
        """Determines whether the specified style is automatic or embedded in the editor.

        Keyword arguments:
            doc - an instance of the ODTDocument class containing the data of the document under study;
            style_name - string name of the desired style;
            param_name - string name of the desired parameter;
            property_type - string name of the desired attribute;
            default - default value for the desired attribute.
        ----------
        Определяет является ли указанный стиль автоматическим или встроенным в редактор.

        Аргументы:
            doc - экземпляр класса ODTDocument, содержащий данные исследуемого документа;
            style_name - строковое название искомого стиля;
            param_name - строковое название искомого параметра;
            property_type - строковое название искомого атрибута;
            default - значение по умолчанию для искомого атрибута.
        """
        parser_regular_styles = RegularStylesParser()
        style = self.get_automatic_style_object_by_name(doc, style_name)
        if style is None:
            return parser_regular_styles.get_parameter_from_regular_style(doc, default, style_name, param_name,
                                                                          property_type)
        else:
            return self.has_automatic_style_parameter(doc, style, param_name, default, property_type)