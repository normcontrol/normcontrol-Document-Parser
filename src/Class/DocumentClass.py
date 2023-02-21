import json
import re

from src.Class.Table import Table
from src.PDF.Table import PDFTable

"""
Description: a unified class representing a text document, its properties and content

Parameters:

----------
    __owner - attribute specifies the owner of a document,
    __time - attribute specifies document creation time,
    __content - attribute specifies the conten of a document
    
    
Methods

----------
    add_content(id, paragraph)
        Adds a paragraph to the content list
    
    pt_to_sm(value)
        Converts topographical points to centimeters
    
    dm_to_sm(value)
        Converts inches to centimeters
    
    create_json_to_clasifier(listOfAttr)
        Creates and returns a json string, which will later be sent to the classifier
    
    request_to_clasify(jsonText, api =)
        Sends a request to the classification module
    
    write_CSV(path):
        Generates csv file based on content
    
"""
class Class:
    def __init__(self, owner, time):
        self.__owner = owner
        self.__time = time
        self.__content = {}

    def add_content(self, paragraph_id, paragraph):
        """

        Adds a paragraph to the content list

        :param paragraph_id: Paragraph number to be added
        :param paragraph: The paragraph to be added as a Paragraph class

        """
        self.content[paragraph_id] = paragraph
    ## Пункт в сантиметры
    @classmethod
    def pt_to_sm(cls, value):
        """

        Converts topographical points to centimeters

        :param value: Conventional value

        :return: The resulting value in centimeters

        """
        return value/28.346
    ## Дюйм в сантиметры
    @classmethod
    def dm_to_sm(cls, value):
        """

        Converts inches to centimeters

        :param value: Conventional value

        :return: The resulting value in centimeters

        """
        return value * 2.54

    def create_json_to_clasifier(self, list_of_attr = ["countn_of_sp_sbl","count_sbl","lowercase","uppercase","last_sbl",
                                                  "firstkey","prev_el","cur_el","next_el","bold","italics",
                                                  "keep_lines_together","keep_with_next", "outline_level",
                                                  "page_breake_before"]
                              ):
        """

        Creates and returns a json string, which will later be sent to the classifier

        :param list_of_attr: List of attributes included in json string

        :return json_text: Generated Json string

        """

        s ="{"
        for attribute in dir(self):
            if attribute == "time" or attribute == "owner":
                s = s + "\"" + attribute + "\": \"" + str(getattr(self,attribute)) + "\", "
        s = s + "\"paragraphs\": {"
        for i, p in self.content.items():
            if p.__class__ != PDFTable :
                s = s + "\"" + str(i) + "\": {\""
                for attribute in dir(p):
                    if not attribute.startswith('_') and attribute in list_of_attr:
                        s = s + attribute + "\": \"" + str(getattr(p,attribute)) + "\",\""
                l = len(s)
                s = s[:l - 2] + "}, "
        l = len(s)
        s = s[:l - 2] + "}}"
        json_text = json.loads(s)
        return json_text

    @classmethod
    def request_to_clasify(cls, json_text, api = "http://127.0.0.1:8001/clasify"):
        """

        Sends a request to the classification module

        :param json_text: The json string to send
        :param api: API where the request is sent

        :return response: Response received from the API

        """

        import requests
        response = requests.post(api, json= json_text)
        return response

    def write_CSV(self, path = 'pdftocsv.csv'):

        """

        Generates csv file based on content

        :param path: Path to save csv file

        """

        import csv
        with open(path, 'w', newline='', encoding="utf-8") as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            filewriter.writerow(["text","countn_of_sp_sbl","count_sbl","uppercase", "lowercase","font_name","last_sbl",
                                 "firstkey","indent","line_spasing","text_size"])
            for key in self.content.keys():
                if type(self.content.get(key))!= PDFTable:
                    filewriter.writerow([self.content.get(key).text, self.content.get(key).countn_of_sp_sbl,
                                         self.content.get(key).count_sbl,self.content.get(key).uppercase,
                                         self.content.get(key).lowercase, self.content.get(key).font_name,
                                         self.content.get(key).last_sbl,self.content.get(key).firstkey,
                                         self.content.get(key).indent, self.content.get(key).line_spasing,
                                         self.content.get(key).text_size])
                else:
                    filewriter.writerow([self.content.get(key).text])


    @property
    def content(self):
        return self.__content

    @property
    def time(self):
        return self.__time

    @property
    def owner(self):
        return self.__owner

    @owner.setter
    def owner(self, owner):
        self.__owner = owner

    @time.setter
    def time(self, time):
        self.__time = time

    @content.setter
    def content(self, content):
        self.__content = content