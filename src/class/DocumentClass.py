import json

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
        print(s)
        jsonText = json.loads(s)
        for text in jsonText:
            for attribute in text:
                print(f"{attribute}")
            for attribute in text["paragraphs"]:
                print(f"\t{attribute}")
        return jsonText

    def createJsonToClassificator(self):
        s = '[{"time": "' + self.time + '",' + '"owner": "' + self.owner + '",' + '"paragraphs":{"'
        for i, p in self.d.items():
            s = s + str(i) + '":"' + p.alignment + '","'
        l = len(s)
        s = s[:l - 2] + "}}]"
        print(s)
        jsonText = json.loads(s)
        print(jsonText[0]["time"])
        for text in jsonText:
            print(text)
        return

    @property
    def d(self):
        return self.__d

    @property
    def time(self):
        return self.__time

    @property
    def owner(self):
        return self.__owner
