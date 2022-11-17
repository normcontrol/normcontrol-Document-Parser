import json
import re

from src.PDF.Table import PDFTable


class Class:
    def __init__(self, owner, time):
        self.__owner = owner
        self.__time = time
        self.__content = {}

    def addParagraph(self, id, paragraph):
        self.content[id] = paragraph
    ## Пункт в сантиметры
    @classmethod
    def ptToSm(cls, value):
        return value/28.346
    ## Дюйм в сантиметры
    @classmethod
    def dmToSm(cls,value):
        return value * 2.54

    def createJsonToDB(self):
        listOfAttr = ["countOfSpSbl","countSbl","lowercase","uppercase","lastSbl","firstkey","prevEl","curEl","nexEl","bold","italics","keepLinesTogether","keepWithNext", "outlineLevel", "pageBreakBefore"]
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

    def requestToClasify(self, jsonText):
        import requests
        response = requests.get("http://api.open-notify.org/astros.json", params={
            "jsonText":jsonText
        })
        return response
    # def createJsonToClassificator(self):
    #  #   listNeedAttribute = { "alignment", "indent", "mrgrg", "mrglf", "lineSpacing", "mrgtop", "mrgbtm", "bold", "italics",
    #  #            "keepLinesTogether", "keepWithNext", "outlineLevel", "pageBreakBefore",
    #  #            "noSpaceBetweenParagraphsOfSameStyle"} # будет убрано ,"alignment", "indent", "mrgrg", "mrglf", "lineSpacing", "mrgtop", "mrgbtm"
    #  #    listNeedAttribute = {"bold", "italics",
    #  #             "keepLinesTogether", "keepWithNext", "outlineLevel", "pageBreakBefore",
    #  #             "noSpaceBetweenParagraphsOfSameStyle"}
    #      s ="[{"
    #  #    for attribute in dir(self):
    #  #        if attribute == "time" or attribute == "owner":
    #  #            s = s + "\"" + attribute + "\": \"" + str(getattr(self,attribute)) + "\", "
    #  #    for number, paragraph in enumerate(self.content):
    #  #        s = s + str(number) + "\"paragraphs\": {"
    #  #        for i, p in self.content.items():
    #  #            s = s + "\"" + str(i) + "\":{"
    #  #            for attribute in dir(p):
    #  #                if not attribute.startswith('_') and attribute in listNeedAttribute:
    #  #                    s = s + "\"" +  attribute + "\": \"" + str(getattr(p,attribute)) + "\","
    #  #            for attribute in dir(p):
    #  #                if attribute == "text":
    #  #                    s = s + "\"countOfSpSbl\": \"" + str(self.getCountOfSpSbl(p.text)) + "\","
    #  #                    s = s + "\"countWord\": \"" + str(self.getCountword(getattr(p,attribute))) + "\","
    #  #                    s = s + "\"countSbl\": \"" + str(self.getCountSbl(getattr(p,attribute))) + "\","
    #  #                    s = s + "\"lowercase\": \"" + str(self.getlowercase(getattr(p,attribute))) + "\","
    #  #                    s = s + "\"uppercase\": \"" + str(self.getuppercase(getattr(p,attribute))) + "\","
    #  #                    s = s + "\"lastSbl\": \"" + str(self.getlastSbl(getattr(p,attribute))) + "\","
    #  #                    s = s + "\"firstkey\": \"" + str(self.getfirstkey(getattr(p,attribute))) + "\","
    #  #                    s = s + "\"pervEl\": \"" + str(self.getprevEl(getattr(p,attribute))) + "\","
    #  #                    s = s + "\"curEl\": \"" + str(self.getcurEl(getattr(p,attribute))) + "\","
    #  #                    s = s + "\"nextEl\": \"" + str(self.getnextEl(getattr(p,attribute))) + "\"}" ##Проверить необходимость разделять
    #  #
    #  #    l = len(s)
    #  #    s = s[:l-2] + "}}}]"
    #  #    print(s)
    #     jsonText = json.loads(s)
    #     return jsonText


    @property
    def content(self):
        return self.__content

    @property
    def time(self):
        return self.__time

    @property
    def owner(self):
        return self.__owner
