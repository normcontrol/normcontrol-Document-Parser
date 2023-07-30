"""
    Description: The module contains a class that stores the data of the file to be parsed. This object is accessed by
        library methods.
    ----------
    Описание: Модуль содержит класс, который хранит данные файла, подлежащего анализу. Доступ к этому объекту
        осуществляется с помощью библиотечных методов.
"""
from odf.opendocument import load
from odf.text import P


class ODTDocument:
    """
    Description: A class that stores the data of the file to be parsed. This object is accessed by library methods.

    Parameters:
        _file_path - attribute storing the path to the file;
        _document - the attribute stores ODF format documents loaded into memory;
        _file_text - the attribute stores the text of the document.

    Methods:
        all_odt_text -
            Returns the entire text of the document.
    ----------
    Описание: Класс, который хранит данные файла, подлежащего анализу. Доступ к этому объекту осуществляется с
        помощью библиотечных методов.

    Свойства:
        _file_path -  атрибут хранит путь к файлу;
        _document - атрибут хранит ODF документ, загруженный в память;
        _file_text - атрибут хранит текст документа.

    Методы:
        all_odt_text -
            Возвращает весь текст документа.
    """

    def __init__(self, file_path: str):
        self._file_path = file_path
        self._document = load(self._file_path)
        self._file_text = self.all_odt_text()

    def all_odt_text(self):
        """Returns the entire text content of the document.
        ----------
        Возвращает все текстовое содержимое документа.
        """
        all_text = []
        for paragraph in self.document.getElementsByType(P):
            all_text.append(paragraph)
            return all_text

    @property
    def file_path(self):
        return self._file_path

    @file_path.setter
    def file_path(self, value):
        self._file_path = value

    @property
    def document(self):
        return self._document

    @document.setter
    def document(self, value):
        self._document = value

    @property
    def file_text(self):
        return self._file_text

    @file_text.setter
    def file_text(self, value):
        self._file_text = value