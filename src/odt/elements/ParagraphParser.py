"""
    Description: The module stores a class that containing methods for working with paragraphs styles in an ODT document.
    ----------
    Описание: Модуль хранит класс, содержащий методы для работы со стилями абзацев в документе формата ODT.
"""
from src.odt.elements.ODTDocument import ODTDocument
from src.helpers.odt.converters import convert_to_paragraph

class ParagraphParser:
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
        for node in style.childNodes:
            if node.qname[1] == property_type:
                for key in node.attributes.keys():
                    if key[1] == parameter_name:
                       return node.attributes[key]
        return None

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
        styles_dict = {}
        for ast in doc.document.automaticstyles.childNodes:
            if ast.getAttribute("name") == style_name:
                for key in ast.attributes.keys():
                    styles_dict[key[1]] = ast.attributes[key]
                for node in ast.childNodes:
                    if node.qname[1] == "paragraph-properties":
                        for node_keys in node.attributes.keys():
                            styles_dict[node.qname[1] + "/" + node_keys[1]] = node.attributes[node_keys]
        return styles_dict

    def get_paragraph_styles_from_regular_styles(self, doc: ODTDocument):
        """Returns text parameters from regular styles.

        Keyword arguments:
            doc - an instance of the ODTDocument class containing the data of the document under study.
        ----------
        Возвращает параметры текста из обычных стилей.

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
                    if node.qname[1] == "paragraph-properties":
                        for key in node.attributes.keys():
                            style[node.qname[1] + "/" + key[1]] = node.attributes[key]
        print(styles_dict)

    def paragraphs_helper(self, styles_data):
        par_objs = []
        for style in styles_data.keys():
            for objs in styles_data[style]['nodes']:
                if 'p' in objs:
                    help = styles_data[style]['nodes'][objs]
                    par_objs.append(convert_to_paragraph(help))
        return par_objs