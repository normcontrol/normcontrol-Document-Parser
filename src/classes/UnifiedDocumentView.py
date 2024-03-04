import dataclasses
import json
import csv
from bestconfig import Config
from .Paragraph import Paragraph
from .superclass.StructuralElement import StructuralElement
from ..helpers.errors.errors import DocumentEmptyContentException


class UnifiedDocumentView:
    """
    Description: a unified class representing a text document, its properties and content

    Attributes:
    ----------
        _owner: str
            The attribute specifies the owner of a document
        _time: datetime
            The attribute specifies document creation time
        _content: dictionary
            The attribute specifies the content of a document


    Methods:
    ----------
        add_content(self, id, paragraph)
            Adds a paragraph to the content list

        create_json(self)
            Creates and returns a json string, which will later be sent to the classifier

        write_CSV(seld, path, **kwargs):
            Generates csv file based on content

    """
    __config = Config("settings.ini")

    def __init__(self, owner: str, time: str, page_count: int = None):
        self._owner = owner
        self._time = time
        self._page_count = page_count
        self._content = {}

    def add_content(self, element_id: int, element: StructuralElement):
        """

        Adds a paragraph to the content list

        :param
            element_id: int
                Paragraph number to be added
            element: object
                The paragraph to be added as a Paragraph class

        """
        self.content[element_id] = element

    def create_json(self):
        """

        Creates and returns a json string, which will later be sent to another api

        :return
            json_text: JSON
                Generated Json string

        """
        try:
            if len(self.content) < 1:
                raise DocumentEmptyContentException
            content = {}
            json_text = {'owner': self.owner, 'time': self.time, 'page_count': self.page_count}
            for key, values in self.content.items():
                temp = {'element_class': type(values).__name__}
                for attribute_name, value in dataclasses.asdict(values).items():
                    temp[attribute_name[1::]] = value
                content[key] = temp
            json_text['content'] = content
            json_text = json.loads(json.dumps(json_text))
            return json_text
        except DocumentEmptyContentException as e:
            print(e)
            raise

    def write_CSV(self, path: str = 'pdftocsv.csv', **kwargs):

        """

        Generates csv file based on content

        :param
            path: str
                Path to save csv file
            **kwargs:
                output_attributes: list[str]
                    List of attribute names that should be saved

        """
        if 'output_attributes' in kwargs.keys():
            output_attributes = kwargs['output_attributes']
        else:
            output_attributes = ["text", "count_of_sp_sbl", "count_sbl", "uppercase", "lowercase", "font_name",
                                 "last_sbl", "first_key", "indent", "line_spacing", "text_size"]
        try:
            with open(path, 'w', newline='', encoding="utf-8") as csvfile:
                filewriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
                filewriter.writerow(output_attributes)
                for key, value in self.content.items():
                    if isinstance(value, Paragraph):
                        filewriter.writerow([value.__getattribute__('_' + attribute) for attribute in output_attributes])
        except (FileExistsError,FileNotFoundError) as e:
            print(e)

    @property
    def content(self):
        return self._content

    @property
    def time(self):
        return self._time

    @property
    def owner(self):
        return self._owner

    @owner.setter
    def owner(self, owner: str):
        self._owner = owner

    @time.setter
    def time(self, time: str):
        self._time = time

    @content.setter
    def content(self, content: dict):
        self._content = content

    @property
    def page_count(self):
        return self._page_count

    @page_count.setter
    def page_count(self, page_count: int):
        self._page_count = page_count
