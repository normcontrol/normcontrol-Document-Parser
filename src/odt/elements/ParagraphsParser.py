from src.odt.elements.ODTDocument import ODTDocument

class ParagraphsParser:
    """
    Description: A class containing methods for working with paragraphs styles in an ODT document.

    Methods:
        get_paragraph_parameters(style, parameter_name: str, property_type: str) -
            Returns the value of the desired paragraph parameter.

        get_paragraph_properties_from_automatic_styles(doc: ODTDocument, style_name: str) -
            Returns the value of the paragraph parameter from automatic styles.

        get_paragraph_styles_from_regular_styles(doc: ODTDocument) -
            Returns text parameters from regular styles.
    ----------
    Описание: Класс, содержащий методы для работы со стилями абзацев в документе формата ODT.

    Методы:
        get_paragraph_parameters(style, parameter_name: str, property_type: str) -
            Возвращает значение искомого параметра абзаца.

        get_paragraph_properties_from_automatic_styles(doc: ODTDocument, style_name: str) -
            Возвращает значение параметра абзаца из автоматических стилей.

        get_paragraph_styles_from_regular_styles(doc: ODTDocument) -
            Возвращает параметры текста из обычных стилей.
    """

    def get_paragraph_parameters(self, style, parameter_name: str, property_type: str):
        """Returns the value of the desired paragraph parameter.

        Keyword arguments:
            style - a style object for research;
            parameter_name - string name of the desired parameter;
            property_type - string name of the desired attribute.
        ----------
        Возвращает значение искомого параметра абзаца.

        Аргументы:
            style - объект стиля для исследования;
            parameter_name - строковое название искомого параметра;
            property_type - строковое название искомого атрибута.
        """
        for n in style.childNodes:
            if n.qname[1] == property_type:
                for k in n.attributes.keys():
                    if k[1] == parameter_name:
                       return n.attributes[k]

    def get_paragraph_properties_from_automatic_styles(self, doc: ODTDocument, style_name: str):
        """Returns the value of the paragraph parameter from automatic styles.

        Keyword arguments:
            doc - an instance of the ODTDocument class containing the data of the document under study;
            style_name - string name of the style under study.
        ----------
        Возвращает значение параметра абзаца из автоматических стилей.

        Аргументы:
            doc - экземпляр класса ODTDocument, содержащий данные исследуемого документа;
            style_name - строковое название исследуемого стиля.
        """
        style = {}
        for ast in doc.document.automaticstyles.childNodes:
            if ast.getAttribute("name") == style_name:
                for k in ast.attributes.keys():
                    style[k[1]] = ast.attributes[k]
                for n in ast.childNodes:
                    if n.qname[1] == "paragraph-properties":
                        for k in n.attributes.keys():
                            style[n.qname[1] + "/" + k[1]] = n.attributes[k]
        return style

    def get_paragraph_styles_from_regular_styles(self, doc: ODTDocument):
        """Returns text parameters from regular styles.

        Keyword arguments:
            doc - an instance of the ODTDocument class containing the data of the document under study.
        ----------
        Возвращает параметры текста из обычных стилей.

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
                    if n.qname[1] == "paragraph-properties":
                        for k in n.attributes.keys():
                            if k[1] == "text-align":
                                style[n.qname[1] + "/" + k[1]] = n.attributes[k]
        print(stylesDict)