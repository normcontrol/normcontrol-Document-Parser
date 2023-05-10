"""
    Description: The module stores a class that containing methods for working with default styles in an ODT document.
    ----------
    Описание: Модуль хранит класс, содержащий методы для работы со стилями по умолчанию в документе формата ODT.
"""
from src.odt.elements.ODTDocument import ODTDocument
from src.odt.elements.DefaultStyleParser import DefaultStyleParser
from src.odt.elements.ParagraphParser import ParagraphParser

class RegularStyleParser:
    """
        Description: A class containing methods for working with regular styles in an ODT document.

        Methods:
            get_regular_styles(doc: ODTDocument) -
                Returns a list of all regular document styles with their attributes.

            get_text_styles_from_regular_styles(doc: ODTDocument) -
                Returns a list of all text styles with their attributes from the regular document styles.

            get_regular_style(doc: ODTDocument, style_name: str) -
                Returns a list of attributes of the specified regular style.

            get_regular_style_object(doc: ODTDocument, style_name: str) -
                Searches for a style by style-family among default styles and returns it as an object to work with.

            get_parameter_from_regular_style_fast(doc: ODTDocument, default: str, style_name: str, param_name: str,
            property_type: str) - Checks for the presence of the specified style in the editor styles without recursion.

            get_parameter_from_regular_style(doc: ODTDocument, default: str, style_name: str, param_name: str,
            property_type: str) -
                Checks for the presence of the specified style in the editor styles using recursion.

            get_paragraph_alignment(doc: ODTDocument, style_name: str) -
                Returns the alignment value of the paragraph parameter.
        ----------
        Описание: Класс, содержащий методы для работы с обычными стилями в документе формата ODT.

        Методы:
            get_regular_styles(doc: ODTDocument) -
                Возвращает список всех обычных стилей документа с их атрибутами.

            get_text_styles_from_regular_styles(doc: ODTDocument) -
                Возвращает список всех стилей текста с их атрибутами из обычных стилей документа.

            get_regular_style(doc: ODTDocument, style_name: str) -
                Возвращает список атрибутов заданного обычного стиля.

            get_regular_style_object(doc: ODTDocument, style_name: str) -
                Выполняет поиск стиля по семейству стилей среди стилей по умолчанию и возвращает его как
                объект для работы.

            get_parameter_from_regular_style_fast(doc: ODTDocument, default: str, style_name: str, param_name: str,
            property_type: str) - Проверяет наличие указанного стиля в стилях редактора без рекурсии.

            get_parameter_from_regular_style(doc: ODTDocument, default: str, style_name: str, param_name: str,
            property_type: str) -
                Проверяет наличие указанного стиля в стилях редактора с использованием рекурсии.

            get_paragraph_alignment(doc: ODTDocument, style_name: str) -
                Возвращает значение выравнивания параметра абзаца.
        """

    def get_regular_styles(self, doc: ODTDocument):
        """Returns a list of all regular document styles with their attributes.

        Keyword arguments:
            doc - an instance of the ODTDocument class containing the data of the document under study.
        ----------
        Возвращает список всех обычных стилей документа с их атрибутами.

        Аргументы:
            doc - экземпляр класса ODTDocument, содержащий данные исследуемого документа.
        """
        styles_dict = {}
        for ast in doc.document.styles.childNodes:
            if ast.qname[1] == "style":
                name = ast.getAttribute('name')
                style = {}
                styles_dict[name] = style

                for key in ast.attributes.keys():
                    style[key[1]] = ast.attributes[key]
                for node in ast.childNodes:
                    for node_keys in node.attributes.keys():
                        style[node.qname[1] + "/" + node_keys[1]] = node.attributes[node_keys]
        return styles_dict

    def get_text_styles_from_regular_styles(self, doc: ODTDocument):
        """Returns a list of all text styles with their attributes from the regular document styles.

        Keyword arguments:
            doc - an instance of the ODTDocument class containing the data of the document under study.
        ----------
        Возвращает список всех стилей текста с их атрибутами из обычных стилей документа.

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
                    if node.qname[1] == "text-properties":
                        for key in node.attributes.keys():
                            style[node.qname[1] + "/" + key[1]] = node.attributes[key]
        return styles_dict

    def get_regular_style(self, doc: ODTDocument, style_name: str):
        """Returns a list of attributes of the specified regular style.

        Keyword arguments:
            doc - an instance of the ODTDocument class containing the data of the document under study;
            style_name - string name of the desired style.
        ----------
        Возвращает список атрибутов заданного обычного стиля.

        Аргументы:
            doc - экземпляр класса ODTDocument, содержащий данные исследуемого документа;
            style_name - строковое название искомого стиля.
        """
        styles_dict = {}
        for ast in doc.document.styles.childNodes:
            if ast.qname[1] == "style":
                if ast.getAttribute("name") == style_name:
                    for key in ast.attributes.keys():
                        styles_dict[key[1]] = ast.attributes[key]
                    for node in ast.childNodes:
                        for node_keys in node.attributes.keys():
                            styles_dict[node.qname[1] + "/" + node_keys[1]] = node.attributes[node_keys]
        return styles_dict

    def get_regular_style_object(self, doc: ODTDocument, style_name: str):
        """Searches for a style by style-family among default styles and returns it as an object to work with.

        Keyword arguments:
            doc - an instance of the ODTDocument class containing the data of the document under study;
            style_name - string name of the desired style.
        ----------
        Выполняет поиск стиля по семейству стилей среди стилей по умолчанию и возвращает его как объект для работы.

        Аргументы:
            doc - экземпляр класса ODTDocument, содержащий данные исследуемого документа;
            style_name - строковое название искомого стиля.
        """
        for ast in doc.document.styles.childNodes:
            if ast.qname[1] == "style":
                if ast.getAttribute("name") == style_name:
                    return ast
        return None

    def get_parameter_from_regular_style_fast(self, doc: ODTDocument, default: str, style_name: str, param_name: str,
                property_type: str):
        """Checks for the presence of the specified style in the editor styles without recursion.

        Keyword arguments:
            doc - an instance of the ODTDocument class containing the data of the document under study;
            default - default value for the desired attribute;
            style_name - a string name of the style for research;
            param_name - string name of the desired parameter;
            property_type - string name of the desired attribute.
        ----------
        Проверяет наличие указанного стиля в стилях редактора без рекурсии.

        Аргументы:
            doc - экземпляр класса ODTDocument, содержащий данные исследуемого документа;
            default - значение по умолчанию для искомого атрибута;
            style_name - строкове название стиля для исследования;
            param_name - строковое название искомого параметра;
            property_type - строковое название искомого атрибута.
        """
        paragraph_parser = ParagraphParser()
        style = self.get_regular_style_object(doc, style_name)
        param = paragraph_parser.get_paragraph_parameters(style, param_name, property_type)
        if param is None:
            for key in style.attributes.keys():
                if key[1] == "parent-style-name":
                   default = \
                       self.get_parameter_from_regular_style_fast_helper(doc, default, style.attributes[key],
                                                                         param_name, property_type)
                   break
        else:
            default = param
        return default

    def get_parameter_from_regular_style_fast_helper(self, doc: ODTDocument, default: str, style_name: str,
                param_name: str, property_type: str):
        """An auxiliary method for getting a parameter from a regular style without recursion.

        Keyword arguments:
            doc - an instance of the ODTDocument class containing the data of the document under study;
            default - default value for the desired attribute;
            style_name - a string name of the style for research;
            param_name - string name of the desired parameter;
            property_type - string name of the desired attribute.
        ----------
        Вспомогательный метод для получения параметра из обычного стиля без рекурсии.

        Аргументы:
            doc - экземпляр класса ODTDocument, содержащий данные исследуемого документа;
            default - значение по умолчанию для искомого атрибута;
            style_name - строкове название стиля для исследования;
            param_name - строковое название искомого параметра;
            property_type - строковое название искомого атрибута.
        """
        paragraph_parser = ParagraphParser()
        style = self.get_regular_style_object(doc, style_name)
        param = paragraph_parser.get_paragraph_parameters(style, param_name, property_type)
        if param is None:
            parser_default_styles = DefaultStyleParser()
            default = parser_default_styles.has_default_parameter(doc, default, style.getAttribute("family"),
                                                                  param_name, property_type)
        else:
            default = param
        return default

    def get_parameter_from_regular_style(self, doc: ODTDocument, default: str, style_name: str, param_name: str,
                                                    property_type: str):
        """Checks for the presence of the specified style in the editor styles using recursion.

        Keyword arguments:
            doc - an instance of the ODTDocument class containing the data of the document under study;
            default - default value for the desired attribute;
            style_name - a string name of the style for research;
            param_name - string name of the desired parameter;
            property_type - string name of the desired attribute.
        ----------
        Проверяет наличие указанного стиля в стилях редактора с использованием рекурсии.

        Аргументы:
            doc - экземпляр класса ODTDocument, содержащий данные исследуемого документа;
            default - значение по умолчанию для искомого атрибута;
            style_name - строкове название стиля для исследования;
            param_name - строковое название искомого параметра;
            property_type - строковое название искомого атрибута.
        """
        paragraph_parser = ParagraphParser()
        style = self.get_regular_style_object(doc, style_name)
        param = paragraph_parser.get_paragraph_parameters(style, param_name, property_type)
        if param is None:
            flag = 0
            for key in style.attributes.keys():
                if key[1] == "parent-style-name":
                   default = self.get_parameter_from_regular_style(doc, default, style.attributes[key],
                                                                   param_name, property_type)
                   flag = 1
                   break
            if flag == 0:
                parser_default_styles = DefaultStyleParser()
                default = parser_default_styles.has_default_parameter(doc, default, style.getAttribute("family"),
                                                                      param_name, property_type)
        else:
            default = param
        return default

    def get_paragraph_alignment(self, doc: ODTDocument, style_name):
        """Returns the alignment value of the paragraph parameter.

        Keyword arguments:
            doc - an instance of the ODTDocument class containing the data of the document under study;
            style_name - string name of the style under study.
        ----------
        Возвращает значение выравнивания параметра абзаца.

        Аргументы:
            doc - экземпляр класса ODTDocument, содержащий данные исследуемого документа;
            style_name - строковое название исследуемого стиля.
        """
        style = {}
        flag = 0
        for ast in doc.document.automaticstyles.childNodes:
            if ast.getAttribute("name") == style_name:
                for key in ast.attributes.keys():
                    style[key[1]] = ast.attributes[key]
                for node in ast.childNodes:
                    if node.qname[1] == "paragraph-properties":
                        for node_keys in node.attributes.keys():
                            if node_keys[1] == "text-align":
                                flag=1
                                style[node.qname[1] + "/" + node_keys[1]] = node.attributes[node_keys]
                    if flag==0:
                        parent = style["parent-style-name"]
                        return self.get_regular_style(doc, parent)
        return None

    def regular_style_dict(self, doc: ODTDocument, attrs: dict):
        styles = {}
        for ast in doc.document.styles.childNodes:
            if ast.qname[1] == "style":
                name = ast.getAttribute('name')
                style = {}
                styles[name] = style
                for attr in attrs:
                    style[attr] = None
                for k in ast.attributes.keys():
                    style[k[1]] = ast.attributes[k]
                for n in ast.childNodes:
                    for k in n.attributes.keys():
                        if k[1] in attrs:
                            style[k[1]] = n.attributes[k]
        return styles