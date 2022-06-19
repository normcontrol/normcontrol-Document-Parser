import json
import re

class Class:
    def __init__(self, owner, time):
        self.__owner = owner
        self.__time = time
        self.__d = {}

    def addParagraph(self, id, paragraph):
        self.d[id] = paragraph

    def createJsonToDB(self):
        s ="[{"
        for attribute in dir(self):
            if attribute == "time" or attribute == "owner":
                s = s + "\"" + attribute + "\": \"" + str(getattr(self,attribute)) + "\", "
        s = s + "\"paragraphs\": {\""
        for i, p in self.d.items():
            for attribute in dir(p):
                if not attribute.startswith('_'):
                    s = s + attribute + "\": \"" + str(getattr(p,attribute)) + "\",\""
        l = len(s)
        s = s[:l - 2] + "}}]"
        jsonText = json.loads(s)
        return jsonText

    def createJsonToClassificator(self):
     #   listNeedAttribute = { "alignment", "indent", "mrgrg", "mrglf", "lineSpacing", "mrgtop", "mrgbtm", "bold", "italics",
     #            "keepLinesTogether", "keepWithNext", "outlineLevel", "pageBreakBefore",
     #            "noSpaceBetweenParagraphsOfSameStyle"} # будет убрано ,"alignment", "indent", "mrgrg", "mrglf", "lineSpacing", "mrgtop", "mrgbtm"
        listNeedAttribute = {"bold", "italics",
                 "keepLinesTogether", "keepWithNext", "outlineLevel", "pageBreakBefore",
                 "noSpaceBetweenParagraphsOfSameStyle"}
        s ="[{"
        for attribute in dir(self):
            if attribute == "time" or attribute == "owner":
                s = s + "\"" + attribute + "\": \"" + str(getattr(self,attribute)) + "\", "
        s = s + "\"paragraphs\": {"
        for i, p in self.d.items():
            s = s + "\"" + str(i) + "\":{"
            for attribute in dir(p):
                if not attribute.startswith('_') and attribute in listNeedAttribute:
                    s = s + "\"" +  attribute + "\": \"" + str(getattr(p,attribute)) + "\","
            for attribute in dir(p):
                if attribute == "text":
                    s = s + "\"countOfSpSbl\": \"" + str(self.getCountOfSpSbl(p.text)) + "\","
                    s = s + "\"countWord\": \"" + str(self.getCountword(getattr(p,attribute))) + "\","
                    s = s + "\"countSbl\": \"" + str(self.getCountSbl(getattr(p,attribute))) + "\","
                    s = s + "\"lowercase\": \"" + str(self.getlowercase(getattr(p,attribute))) + "\","
                    s = s + "\"uppercase\": \"" + str(self.getuppercase(getattr(p,attribute))) + "\","
                    s = s + "\"lastSbl\": \"" + str(self.getlastSbl(getattr(p,attribute))) + "\","
                    s = s + "\"firstkey\": \"" + str(self.getfirstkey(getattr(p,attribute))) + "\","
                    s = s + "\"pervEl\": \"" + str(self.getprevEl(getattr(p,attribute))) + "\","
                    s = s + "\"curEl\": \"" + str(self.getcurEl(getattr(p,attribute))) + "\","
                    s = s + "\"nextEl\": \"" + str(self.getnextEl(getattr(p,attribute))) + "\"}," ##Проверить необходимость разделять

        l = len(s)
        s = s[:l-2] + "}}}]"
        print(s)
        jsonText = json.loads(s)
        return jsonText

    def getCountOfSpSbl(self,text):
        return len(re.findall("[,.!?;:\'\"«»~]", text))

    def getCountword(self,text):
        return len(text.split(' '))
    def getCountSbl(self,text):
        return len(text)

    def getlowercase(self,text):
        return True if text.islower() else False

    def getuppercase(self, text):
        return True if text.isupper() else False

    def getlastSbl(self, text):
        return text[len(text)-1]

    def getfirstkey(self, text):
        return text.split(' ')[0]

    def getprevEl(self,text):
        return False

    def getcurEl(self, text):
        return False

    def getnextEl(self,text):
        return False

    @property
    def d(self):
        return self.__d

    @property
    def time(self):
        return self.__time

    @property
    def owner(self):
        return self.__owner
