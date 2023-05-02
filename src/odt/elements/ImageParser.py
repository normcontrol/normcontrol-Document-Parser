"""
    Description: The module stores a class that containing methods for working with image and frame styles in an
        ODT document.
    ----------
    Описание: Модуль хранит класс, содержащий методы для работы со стилями изображений и рамок в документе формата ODT.
"""
from src.odt.elements.ODTDocument import ODTDocument
from src.classes.Frame import Frame
from src.classes.Image import Image

class ImageParser:
    """
    Description: A class containing methods for working with image and frame styles in an ODT document.

    Methods:
        get_frame_styles(doc: ODTDocument) -
            Returns a list of all frame styles with their attributes.

        get_image_styles(doc: ODTDocument) -
            Returns a list of all image styles with their attributes.

        get_frame_parameter(doc: ODTDocument, style_name: str, parameter_name: str) -
            Gets a style parameter by name and attribute among the frame styles.

        get_image_parameter(doc: ODTDocument, style_name: str, parameter_name: str) -
            Gets a style parameter by name and attribute among the image styles.
    ----------
    Описание: Класс, содержащий методы для работы со стилями изображений и рамок в документе формата ODT.

    Методы:
        get_frame_styles(doc: ODTDocument) -
            Возвращает список всех стилей рамок документа с их атрибутами.

        get_image_styles(doc: ODTDocument) -
            Возвращает список всех стилей изображений документа с их атрибутами.

        get_frame_parameter(doc: ODTDocument, style_name: str, parameter_name: str) -
             Получает параметр стиля по имени и атрибуту среди стилей рамок.

        get_image_parameter(doc: ODTDocument, style_name: str, parameter_name: str) -
             Получает параметр стиля по имени и атрибуту среди стилей изображений.
    """

    def get_frame_styles(self, doc: ODTDocument) -> [Frame]:
        """Returns a list of all frame styles with their attributes.

        Keyword arguments:
            doc - an instance of the ODTDocument class containing the data of the document under study.
        ----------
        Возвращает список всех стилей рамок документа с их атрибутами.

        Аргументы:
            doc - экземпляр класса ODTDocument, содержащий данные исследуемого документа.
        """
        styles_dict = {}
        frame_objs = []
        elements_keys = list(doc.document.element_dict.keys())
        token = ''
        for key in elements_keys:
            if key[1] == 'frame':
                token = key

        objs = doc.document.element_dict.get(token)
        for ast in objs:
            if ast.qname[1] == "frame":
                name = ast.getAttribute('name')
                style = []
                for key in ast.attributes.keys():
                    style.append(ast.attributes[key])
                for node in ast.childNodes:
                    for node_keys in node.attributes.keys():
                        style.append(node.attributes[node_keys])
                styles_dict[name] = style
        for cur_frame in styles_dict.keys():
            frame_objs.append(Frame(styles_dict[cur_frame][0], styles_dict[cur_frame][1], styles_dict[cur_frame][2],
                                    styles_dict[cur_frame][3], styles_dict[cur_frame][4], styles_dict[cur_frame][5],
                                    styles_dict[cur_frame][6], styles_dict[cur_frame][7], styles_dict[cur_frame][8]))
        return frame_objs

    def get_image_styles(self, doc: ODTDocument) -> [Image]:
        """Returns a list of all image styles with their attributes.

        Keyword arguments:
            doc - an instance of the ODTDocument class containing the data of the document under study.
        ----------
        Возвращает список всех стилей изображений документа с их атрибутами.

        Аргументы:
            doc - экземпляр класса ODTDocument, содержащий данные исследуемого документа.
        """
        styles_dict = {}
        image_objs = []
        elements_keys = list(doc.document.element_dict.keys())
        token = ''
        for key in elements_keys:
            if key[1] == 'image':
                token = key

        objs = doc.document.element_dict.get(token)
        for ast in objs:
            if ast.qname[1] == "image":
                name = ast.getAttribute('href')
                style = []
                for node in ast.attributes.keys():
                    style.append(ast.attributes[node])
                styles_dict[name] = style
        for cur_image in styles_dict.keys():
            image_objs.append(Image(styles_dict[cur_image][0], styles_dict[cur_image][1], styles_dict[cur_image][2],
                                    styles_dict[cur_image][3]))
        return image_objs

    def get_frame_parameter(self, doc: ODTDocument, style_name: str, parameter_name: str):
        """Gets a style parameter by name and attribute among the frame styles.

        Keyword arguments:
            doc - an instance of the ODTDocument class containing the data of the document under study;
            style_name - a string name of style for research;
            parameter_name - string name of the desired parameter.
        ----------
        Получает параметр стиля по имени и атрибуту среди стилей рамок.

        Аргументы:
            doc - экземпляр класса ODTDocument, содержащий данные исследуемого документа;
            style_name - строковое название стиля для исследования;
            parameter_name - строковое название искомого параметра.
        """
        elements_keys = list(doc.document.element_dict.keys())
        token = ''
        for key in elements_keys:
            if key[1] == 'frame':
                token = key

        objs = doc.document.element_dict.get(token)
        for ast in objs:
            if style_name in ast.getAttribute('name'):
                for key in ast.attributes.keys():
                    if parameter_name in key:
                        return ast.attributes[key]
        return None

    def get_image_parameter(self, doc: ODTDocument, style_name: str, parameter_name: str):
        """Gets a style parameter by name and attribute among the image styles.

        Keyword arguments:
            doc - an instance of the ODTDocument class containing the data of the document under study;
            style_name - a string name of style for research;
            parameter_name - string name of the desired parameter.
        ----------
        Получает параметр стиля по имени и атрибуту среди стилей изображений.

        Аргументы:
            doc - экземпляр класса ODTDocument, содержащий данные исследуемого документа;
            style_name - строковое название стиля для исследования;
            parameter_name - строковое название искомого параметра.
        """
        elements_keys = list(doc.document.element_dict.keys())
        token = ''
        for key in elements_keys:
            if key[1] == 'image':
                token = key

        objs = doc.document.element_dict.get(token)
        for ast in objs:
            if style_name in ast.getAttribute('href'):
                for key in ast.attributes.keys():
                    if parameter_name in key:
                        return ast.attributes[key]
        return None