import json

from src.Class.Paragraph import Paragraph
from src.PDF.PDFClasses.Table import PDFTable


class DocumentClass:
    """
    Description: a unified class representing a text document, its properties and content

    Parameters:
    ----------
        _owner: str
            The attribute specifies the owner of a document
        _time: datetime
            The attribute specifies document creation time
        _content: dictionary
            The attribute specifies the conten of a document


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

    def __init__(self, owner, time):
        self._owner = owner
        self._time = time
        self._content = {}

    def add_content(self, element_id, element):
        """

        Adds a paragraph to the content list

        :param element_id: Paragraph number to be added
        :param element: The paragraph to be added as a Paragraph class

        """
        self.content[element_id] = element

    def create_json_to_clasifier(self, list_of_attr=["countn_of_sp_sbl", "count_sbl", "lowercase", "uppercase",
                                                     "last_sbl", "first_key", "bold", "italics", "keep_lines_together",
                                                     "keep_with_next", "outline_level", "page_breake_before"]
                                 ):
        """

        Creates and returns a json string, which will later be sent to the classifier

        :param list_of_attr: List of attributes included in json string

        :return json_text: Generated Json string

        """

        json_string = "{"
        for attribute in dir(self):
            if attribute == "time" or attribute == "owner":
                json_string = json_string + "\"" + attribute + "\": \"" + str(getattr(self, attribute)) + "\", "
        json_string = json_string + "\"paragraphs\": {"
        for i, p in self.content.items():
            if p.__class__ == Paragraph:
                json_string = json_string + "\"" + str(i) + "\": {\""
                for attribute in dir(p):
                    if not attribute.startswith('_') and attribute in list_of_attr:
                        json_string = json_string + attribute + "\": \"" + str(getattr(p, attribute)) + "\",\""
                length = len(json_string)
                json_string = json_string[:length - 2] + "}, "
        length = len(json_string)
        json_string = json_string[:length - 2] + "}}"
        json_text = json.loads(json_string)
        return json_text

    @classmethod
    def request_to_clasify(cls, json_text, api="http://127.0.0.1:8001/clasify"):
        """

        Sends a request to the classification module

        :param json_text: The json string to send
        :param api: API where the request is sent

        :return response: Response received from the API

        """

        import requests
        response = requests.post(api, json=json_text)
        return response

    def write_CSV(self, path='pdftocsv.csv'):

        """

        Generates csv file based on content

        :param path: Path to save csv file

        """

        import csv
        with open(path, 'w', newline='', encoding="utf-8") as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            filewriter.writerow(["text", "countn_of_sp_sbl", "count_sbl", "uppercase", "lowercase", "font_name",
                                 "last_sbl", "first_key", "indent", "line_spasing", "text_size"])
            for key in self.content.keys():
                if type(self.content.get(key)) == Paragraph:
                    filewriter.writerow([self.content.get(key).text, self.content.get(key).count_of_sp_sbl,
                                         self.content.get(key).count_sbl, self.content.get(key).uppercase,
                                         self.content.get(key).lowercase, self.content.get(key).font_name,
                                         self.content.get(key).last_sbl, self.content.get(key).first_key,
                                         self.content.get(key).indent, self.content.get(key).line_spacing,
                                         self.content.get(key).text_size])

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
    def owner(self, owner):
        self._owner = owner

    @time.setter
    def time(self, time):
        self._time = time

    @content.setter
    def content(self, content):
        self._content = content
