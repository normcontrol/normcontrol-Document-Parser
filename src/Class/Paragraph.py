import re


class Paragraph:

    def __init__(self, text, indent, lineSpacing, fontName, textSize, nochangeFontName, nochangeTextSize, alignment = None, mrgrg = None, mrglf  = None, mrgtop  = None, mrgbtm  = None, bold = None, italics = None,
                 underlining = None ,subText = None , superText = None , colorText = "White",
                 keepLinesTogether = None, keepWithNext = None, outlineLevel = None,
                 noSpaceBetweenParagraphsOfSameStyle = None, pageBreakBefore = None):
        self.__text = text
        self.countOfSpSbl = Paragraph.getCountOfSpSbl(text)
        self.countSbl = Paragraph.getCountSbl(text)
        self.lowercase = Paragraph.getlowercase(text)
        self.uppercase = Paragraph.getuppercase(text)
        self.lastSbl = Paragraph.getlastSbl(text)
        self.firstkey = None  #Paragraph.getfirstkey(text)
        self.prevEl = None
        self.curEl = None
        self.nexEl = None
        self.__alignment = alignment
        self.__indent = indent
        self.__mrgrg = mrgrg
        self.__mrglf = mrglf
        self.__lineSpacing = lineSpacing
        self.__mrgtop = mrgtop
        self.__mrgbtm = mrgbtm
        self.__fontName = fontName
        self.__bold = bold
        self.__italics = italics
        self.__underlining = underlining
        self.__subText = subText
        self.__superText = superText
        self.__textSize = textSize
        self.__colorText = colorText
        self.__pageBreakBefore = pageBreakBefore # имеет значение
        ## Нужны дополнительные исследования классификатора
        self.__keepLinesTogether = keepLinesTogether
        self.__keepWithNext = keepWithNext
        self.__outlineLevel = outlineLevel
        self.__noSpaceBetweenParagraphsOfSameStyle = noSpaceBetweenParagraphsOfSameStyle
        self.nochangeFontName = nochangeFontName
        self.nochangeTextSize = nochangeTextSize


    @classmethod
    def getCountOfSpSbl(cls,text):
        return len(re.findall("[,.!?;:\'\"«»~]", text))
    @classmethod
    def getCountSbl(cls,text):
        return len(text)
    @classmethod
    def getlowercase(cls,text):
        return True if text.islower() else False
    @classmethod
    def getuppercase(cls,text):
        return True if text.isupper() else False
    @classmethod
    def getlastSbl(cls,text):
        return text[len(text)-2]
    @classmethod
    def getfirstkey(cls,text):
        return text.split(' ')[0]
    @classmethod
    def getprevEl(cls,text):
        return False
    @classmethod
    def getcurEl(cls,text):
        return False
    @classmethod
    def getnextEl(cls,text):
        return False

    @property
    def text(self):
        return self.__text

    @property
    def keepLinesTogether(self):
        return self.__keepLinesTogether

    @property
    def outlineLevel(self):
        return self.__outlineLevel


    @property
    def noSpaceBetweenParagraphsOfSameStyle(self):
        return self.__noSpaceBetweenParagraphsOfSameStyle

    @property
    def keepWithNext(self):
        return self.__keepWithNext

    @property
    def indent(self):
        return self.__indent

    @property
    def mrgrg(self):
        return self.__mrgrg

    @property
    def mrglf(self):
        return self.__mrglf

    @property
    def mrgtop(self):
        return self.__mrgtop

    @property
    def mrgbtm(self):
        return self.__mrgbtm

    @property
    def fontName(self):
        return self.__fontName

    @property
    def colorText(self):
        return self.__colorText

    @property
    def lineSpacing(self):
        return self.__lineSpacing

    @lineSpacing.setter
    def lineSpacing(self, l):
        if l >= 0:
            self.__lineSpacing = l
        else:
            raise ValueError

    @property
    def bold(self):
        return self.__bold

    @bold.setter
    def bold(self, b):
        if b == True or b == False:
            self.__bold = b
        else:
            raise ValueError

    @property
    def italics(self):
        return self.__italics

    @italics.setter
    def italics(self, i):
        if i == True or i == False:
            self.__italics = i
        else:
            raise ValueError

    @property
    def underlining(self):
        return self.__underlining

    @underlining.setter
    def underlining(self, u):
        if u == True or u == False:
            self.__underlining = u
        else:
            raise ValueError

    @property
    def subText(self):
        return self.__subText

    @subText.setter
    def subText(self, s):
        if s == True or s == False:
            self.__subText = s
        else:
            raise ValueError

    @property
    def superText(self):
        return self.__superText

    @superText.setter
    def superText(self, s):
        if s == True or s == False:
            self.__superText = s
        else:
            raise ValueError

    @property
    def textSize(self):
        return self.__textSize

    @textSize.setter
    def textSize(self, s):
        if s >= 8:
            self.__textSize = s
        else:
            raise ValueError
