import csv
import json

import requests
from bestconfig import Config

from src.classes.Paragraph import Paragraph


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
        add_content(id, paragraph)
            Adds a paragraph to the content list

        create_json_to_clasifier(listOfAttr)
            Creates and returns a json string, which will later be sent to the classifier

        request_to_clasify(jsonText, api =)
            Sends a request to the classification module

        write_CSV(path):
            Generates csv file based on content

    """
    __config = Config("settings.ini")

    def __init__(self, owner: str, time: str):
        self._owner = owner
        self._time = time
        self._content = {}

    def add_content(self, element_id: int, element: object):
        """

        Adds a paragraph to the content list

        :param
            element_id: int
                Paragraph number to be added
            element: object
                The paragraph to be added as a Paragraph class

        """
        self.content[element_id] = element

    def create_json_to_clasifier(self, **kwargs):
        """

        Creates and returns a json string, which will later be sent to the classifier

        :param:
            **kwargs:
                list_of_attr: list[str]
                    List of attributes included in json string

        :return
            json_text: json
                Generated Json string

        """

        if 'list_of_attr' in kwargs.keys():
            list_of_attr = kwargs['list_of_attr']
        else:
            list_of_attr = ["countn_of_sp_sbl", "count_sbl", "lowercase", "uppercase",
                            "last_sbl", "first_key", "bold", "italics", "keep_lines_together",
                            "keep_with_next", "outline_level", "page_breake_before"]
        json_string = "{"
        for attribute in dir(self):
            if attribute in ("time", "owner"):
                json_string += "\"" + attribute + "\": \"" + str(getattr(self, attribute)) + "\", "
        json_string += "\"content\": {"
        for i, p in self.content.items():
            if p.__class__ == Paragraph:
                json_string += "\"" + str(i) + "\": {\""
                for attribute in dir(p):
                    if attribute in list_of_attr:
                        json_string += attribute + "\": \"" + str(getattr(p, attribute)) + "\",\""
                json_str_len = len(json_string)
                json_string = json_string[:json_str_len - 2] + "}, "
        length = len(json_string)
        json_string = json_string[:length - 2] + "}}"
        json_text = json.loads(json_string)
        return json_text

    @classmethod
    def request_to_clasify(cls, json_text: str):
        """

        Sends a request to the classification module

        :param
            json_text: json
                The json string to send

        :return
            response: Response
                Response received from the API

        """

        response = requests.post(cls.__config['CommonData']['clasify_ip'], json=json_text)
        return response

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
        with open(path, 'w', newline='', encoding="utf-8") as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            filewriter.writerow(output_attributes)
            for key, value in self.content.items():
                if isinstance(value, Paragraph):
                    filewriter.writerow([value.__getattribute__('_' + attribute) for attribute in output_attributes])

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
