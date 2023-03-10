from src.odt.elements.ODTDocument import ODTDocument

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
        stylesDict = {}
        for ast in doc.document.styles.childNodes:
            if ast.qname[1] == "style":
                name = ast.getAttribute('name')
                style = {}
                stylesDict[name] = style
                for n in ast.childNodes:
                    if "list" in n.qname[1]:
                        for k in n.attributes.keys():
                            style[n.qname[1] + "/" + k[1]] = n.attributes[k]
        return stylesDict

    def get_lists_text_styles(self, doc: ODTDocument):
        """Returns a list of all text styles with their attributes from the lists styles of document.

        Keyword arguments:
            doc - an instance of the ODTDocument class containing the data of the document under study.
        ----------
        Возвращает список всех текстовых стилей с их атрибутами из списка стилей документа.

        Аргументы:
            doc - экземпляр класса ODTDocument, содержащий данные исследуемого документа.
        """
        stylesDict = {}
        for ast in doc.document.styles.childNodes:
            if ast.qname[1] == "style":
                name = ast.getAttribute('name')
                style = {}
                if 'Абзацсписка' in name or 'WW' in name or 'LF' in name:
                    stylesDict[name] = style
                    for n in ast.childNodes:
                        if n.qname[1] == "text-properties":
                            for k in n.attributes.keys():
                                style[n.qname[1] + "/" + k[1]] = n.attributes[k]
        return stylesDict

    def get_list_styles_from_automatic_styles(self, doc: ODTDocument):
        """Returns a list of all list styles from automatic document styles with their attributes.

        Keyword arguments:
            doc - an instance of the ODTDocument class containing the data of the document under study.
        ----------
        Возвращает список всех стилей списков из автоматических стилей документа с их атрибутами.

        Аргументы:
            doc - экземпляр класса ODTDocument, содержащий данные исследуемого документа.
        """
        styles = {}
        for ast in doc.document.automaticstyles.childNodes:
            name = ast.getAttribute('name')
            style = {}
            for n in ast.childNodes:
                if "list-level" in n.qname[1]:
                    styles[name] = style
                    for k in n.attributes.keys():
                        style[n.qname[1] + "/" + k[1]] = n.attributes[k]
        return styles

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
        for n in style.childNodes:
            if "list" in n.qname[1] or "text" in n.qname[1]:
                for k in n.attributes.keys():
                    if k[1] == parameter_name:
                        return n.attributes[k]