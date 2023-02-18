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
    addContent(id, paragraph)
        Adds a paragraph to the content list
    
    ptToSm(value)
        Converts topographical points to centimeters
    
    dmToSm(value)
        Converts inches to centimeters
    
    createJsonToClasifier(listOfAttr)
        Creates and returns a json string, which will later be sent to the classifier
    
    requestToClasify(jsonText, api =)
        Sends a request to the classification module
    
    writeCSV(path):
        Generates csv file based on content
    
"""
class Class:
    def __init__(self, owner, time):
        self.__owner = owner
        self.__time = time
        self.__content = {}

    def addContent(self, paragraph_id, paragraph):
        """

        Adds a paragraph to the content list

        :param paragraph_id: Paragraph number to be added
        :param paragraph: The paragraph to be added as a Paragraph class

        """
        self.content[paragraph_id] = paragraph
    ## Пункт в сантиметры
    @classmethod
    def ptToSm(cls, value):
        """

        Converts topographical points to centimeters

        :param value: Conventional value

        :return: The resulting value in centimeters

        """
        return value/28.346
    ## Дюйм в сантиметры
    @classmethod
    def dmToSm(cls, value):
        """

        Converts inches to centimeters

        :param value: Conventional value

        :return: The resulting value in centimeters

        """
        return value * 2.54

    def createJsonToClasifier(self, listOfAttr = ["countOfSpSbl","countSbl","lowercase","uppercase","lastSbl",
                                                  "firstkey","prevEl","curEl","nexEl","bold","italics",
                                                  "keepLinesTogether","keepWithNext", "outlineLevel",
                                                  "pageBreakBefore"]
                              ):
        """

        Creates and returns a json string, which will later be sent to the classifier

        :param listOfAttr: List of attributes included in json string

        :return jsonText: Generated Json string

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
                    if not attribute.startswith('_') and attribute in listOfAttr:
                        s = s + attribute + "\": \"" + str(getattr(p,attribute)) + "\",\""
                l = len(s)
                s = s[:l - 2] + "}, "
        l = len(s)
        s = s[:l - 2] + "}}"
        jsonText = json.loads(s)
        return jsonText

    @classmethod
    def requestToClasify(cls, jsonText, api = "http://127.0.0.1:8001/clasify"):
        """

        Sends a request to the classification module

        :param jsonText: The json string to send
        :param api: API where the request is sent

        :return response: Response received from the API

        """

        import requests
        response = requests.post(api, json= jsonText)
        return response

    def writeCSV(self, path = 'pdftocsv.csv'):

        """

        Generates csv file based on content

        :param path: Path to save csv file

        """

        import csv
        with open(path, 'w', newline='', encoding="utf-8") as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            filewriter.writerow(["text","countOfSpSbl","countSbl","uppercase", "lowercase","fontName","lastSbl",
                                 "firstkey","indent","lineSpacing","textSize"])
            for key in self.content.keys():
                if type(self.content.get(key))!= PDFTable:
                    filewriter.writerow([self.content.get(key).text, self.content.get(key).countOfSpSbl ,
                                         self.content.get(key).countSbl,self.content.get(key).uppercase,
                                         self.content.get(key).lowercase, self.content.get(key).fontName,
                                         self.content.get(key).lastSbl,self.content.get(key).firstkey,
                                         self.content.get(key).indent, self.content.get(key).lineSpacing,
                                         self.content.get(key).textSize])
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