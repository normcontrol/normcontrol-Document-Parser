import re
from doc.helpers.StylePropertyCoverage import StylePropertyCoverage


class Paragraph:
    """

Parameters:

----------
        __text  - attribute specifies paragraph text
        __countOfSpSbl  - attribute specifies number of special characters in a paragraph
        __countSbl - attribute specifies number of characters in a paragraph
        __lowercase - attribute specifies lowercase text in the entire paragraph
        __uppercase - attribute specifies uppercase text in the entire paragraph
        __lastSbl - attribute specifies last paragraph character
        __firstkey - attribute specifies first paragraph character
        __prevEl - attribute specifies the class of the previous structural element
        __curEl - attribute specifies the class of the current structural element
        __nexEl - attribute specifies the class of the next structural element
        __alignment - attribute specifies text alignment
        __indent - attribute specifies indent from the red line
        __mrgrg - attribute specifies indent from the right side of the page
        __mrglf - attribute specifies indent from the left side of the page
        __lineSpacing - attribute specifies paragraph line spacing
        __mrgtop - attribute specifies attribute specifies indent from the top side of the page
        __mrgbtm - attribute specifies attribute specifies indent from the bottom side of the page
        __fontName - attribute specifies paragraph font
        __bold - attribute specifies paragraph text boldness
        __italics - attribute specifies paragraph text italics
        __underlining - attribute specifies paragraph text underlining
        __subText - attribute specifies
        __superText - attribute specifies
        __textSize - attribute specifies text size
        __colorText - attribute specifies text color
        __pageBreakBefore - attribute specifies start of a new page
        __keepLinesTogether - attribute specifies keeping the line style together
        __keepWithNext - attribute specifies keeping paragraphs together
        __outlineLevel - attribute specifies paragraph type
        __noSpaceBetweenParagraphsOfSameStyle - attribute specifies no extra space between paragraphs of the same style
        __nochangeFontName - attribute specifies no change in text font inside a paragraph
        __nochangeTextSize - attribute specifies no change in text size inside a paragraph

Methods

----------

    getCountOfSpSbl(cls, text)
        Counts and returns the number of special characters in a text

    getCountSbl(cls, text)
        Counts and returns the number of all characters in a text

    getlowercase(cls, text)
        Calculates whether the entire paragraph is lowercase

    getuppercase(cls, text)
        Calculates whether the entire paragraph is uppercase

    getlastSbl(cls, text)
        Calculates the last character of a paragraph

    getfirstkey(cls, text)
        Calculates the type of the first character of a paragraph

    """

    def __init__(self, text, indent, lineSpacing, fontName, textSize, nochangeFontName, nochangeTextSize,
                 alignment=None, mrgrg=None, mrglf=None, mrgtop=None, mrgbtm=None, bold: StylePropertyCoverage = None, italics=None,
                 underlining=None, subText=None, superText=None, colorText="White",
                 keepLinesTogether=None, keepWithNext=None, outlineLevel=None,
                 noSpaceBetweenParagraphsOfSameStyle=None, pageBreakBefore=None):
        self.__text = text
        self.__countOfSpSbl = Paragraph.getCountOfSpSbl(text)
        self.__countSbl = Paragraph.getCountSbl(text)
        self.__lowercase = Paragraph.getlowercase(text)
        self.__uppercase = Paragraph.getuppercase(text)
        self.__lastSbl = Paragraph.getlastSbl(text)
        self.__firstkey = Paragraph.getfirstkey(text)
        self.__prevEl = None
        self.__curEl = None
        self.__nexEl = None
        self.__alignment = alignment
        self.__indent = indent
        self.__mrgrg = mrgrg
        self.__mrglf = mrglf
        self.__lineSpacing = lineSpacing
        self.__mrgtop = mrgtop
        self.__mrgbtm = mrgbtm
        self.__fontName = fontName
        self.__bold = StylePropertyCoverage(bold)
        self.__italics = StylePropertyCoverage(italics)
        self.__underlining = StylePropertyCoverage(underlining)
        self.__subText = subText
        self.__superText = superText
        self.__textSize = textSize
        self.__colorText = colorText
        self.__pageBreakBefore = pageBreakBefore
        self.__keepLinesTogether = keepLinesTogether
        self.__keepWithNext = keepWithNext
        self.__outlineLevel = outlineLevel
        self.__noSpaceBetweenParagraphsOfSameStyle = noSpaceBetweenParagraphsOfSameStyle
        self.__nochangeFontName = nochangeFontName
        self.__nochangeTextSize = nochangeTextSize

    @classmethod
    def getCountOfSpSbl(cls, text):
        """

        Counts and returns the number of special characters in a text

        :param text: Paragraph text
        :return: The number of special characters in the text, such as dots and commas

        """

        return len(re.findall("[,.!?;:\'\"«»~]", text))

    @classmethod
    def getCountSbl(cls, text):
        """

        Counts and returns the number of all characters in a text

        :param text: Paragraph text
        :return: The number of all characters in the text

        """

        return len(text)

    @classmethod
    def getlowercase(cls, text):
        """

        Calculates whether the entire paragraph is lowercase

        :param text: Paragraph text
        :return: True if all text is in lowercase

        """

        return True if text.islower() else False

    @classmethod
    def getuppercase(cls, text):
        """

        Calculates whether the entire paragraph is uppercase

        :param text: Paragraph text
        :return: True if all text is in uppercase

        """

        return True if text.isupper() else False

    @classmethod
    def getlastSbl(cls, text):
        """

        Calculates the last character of a paragraph

        :param text: Paragraph text
        :return: The last character of a paragraph

        """

        if len(text) <= 1:
            return None
        if re.match(r'[A-Za-zА-Яа-я0-9()]', text[len(text) - 2]) is None:
            return text[len(text) - 2]
        else:
            return None

    @classmethod
    def getfirstkey(cls, text):
        """

        Calculates the type of the first character of a paragraph

        :param text: Paragraph text
        :return: The type of the first character of a paragraph

        """
        import re
        first_key = text.split(' ')[0]
        if re.match(r'−', first_key) is None:
            if re.match(r'(\d*)', first_key) is None:
                if re.match(r'(\d*.\d*)', first_key) is None:
                    if re.match(r'(\d*.\d*(.\d*)*)', first_key) is None:
                        if re.match(r'Таблица', first_key) is None:
                            if re.match(r'[(Рисунок)(Рис)(Рис.)]', first_key) is None:
                                return ''
                            else:
                                return 'Рисунок'
                        else:
                            return 'Таблица'
                    else:
                        return 'TitleLevel23'
                else:
                    return 'TitleLevel23'
            else:
                return 'TitleLevel1'
        else:
            return 'listLevel1'

    @property
    def prevEl(self):
        return self.__prevEl

    @prevEl.setter
    def prevEl(self, prevEl):
        self.__prevEl = prevEl

    @property
    def curEl(self):
        return self.__curEl

    @curEl.setter
    def curEl(self, curEl):
        self.__curEl = curEl

    @property
    def nextEl(self):
        return self.__nextEl

    @nextEl.setter
    def fontName(self, nextEl):
        self.__nextEl = nextEl

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, text):
        self.__text = text

    @property
    def keepLinesTogether(self):
        return self.__keepLinesTogether

    @keepLinesTogether.setter
    def keepLinesTogether(self, keepLinesTogether):
        self.__keepLinesTogether = keepLinesTogether

    @property
    def outlineLevel(self):
        return self.__outlineLevel

    @outlineLevel.setter
    def outlineLevel(self, outlineLevel):
        self.__outlineLevel = outlineLevel

    @property
    def noSpaceBetweenParagraphsOfSameStyle(self):
        return self.__noSpaceBetweenParagraphsOfSameStyle

    @noSpaceBetweenParagraphsOfSameStyle.setter
    def noSpaceBetweenParagraphsOfSameStyle(self, noSpaceBetweenParagraphsOfSameStyle):
        self.__noSpaceBetweenParagraphsOfSameStyle = noSpaceBetweenParagraphsOfSameStyle

    @property
    def keepWithNext(self):
        return self.__keepWithNext

    @keepWithNext.setter
    def keepWithNext(self, keepWithNext):
        self.__keepWithNext = keepWithNext

    @property
    def indent(self):
        return self.__indent

    @indent.setter
    def indent(self, indent):
        self.__indent = indent

    @property
    def mrgrg(self):
        return self.__mrgrg

    @mrgrg.setter
    def mrgrg(self, mrgrg):
        self.__mrgrg = mrgrg

    @property
    def mrglf(self):
        return self.__mrglf

    @mrglf.setter
    def mrglf(self, mrglf):
        self.__mrglf = mrglf

    @property
    def mrgtop(self):
        return self.__mrgtop

    @mrgtop.setter
    def mrgtop(self, mrgtop):
        self.__mrgtop = mrgtop

    @property
    def mrgbtm(self):
        return self.__mrgbtm

    @mrgbtm.setter
    def mrgbtm(self, mrgbtm):
        self.__mrgbtm = mrgbtm

    @property
    def fontName(self):
        return self.__fontName

    @fontName.setter
    def fontName(self, fontName):
        self.__fontName = fontName

    @property
    def colorText(self):
        return self.__colorText

    @colorText.setter
    def colorText(self, colorText):
        self.__colorText = colorText

    @property
    def lineSpacing(self):
        return self.__lineSpacing

    @lineSpacing.setter
    def lineSpacing(self, value):
        if value >= 0:
            self.__lineSpacing = value
        else:
            raise ValueError

    @property
    def bold(self):
        return self.__bold

    @bold.setter
    def bold(self, b):
        try:
            if b is not None:
                self.__bold = StylePropertyCoverage(b).name
        except ValueError:
            print(
                "You must use one of this state: NO_APPLY = 0 ; APPLY_TO_ALL_ELEMENTS = 1 ; APPLY_TO_SOME_ELEMENTS = 2; IS_UNKNOWN = None")

        # if b is True or b is False or b == 2:
        #     self.__bold = EnumFill(b).name
        # else:
        #     raise ValueError

    @property
    def italics(self):
        return self.__italics

    @italics.setter
    def italics(self, i):
        if i is True or i is False:
            self.__italics = i
        else:
            raise ValueError

    @property
    def underlining(self):
        return self.__underlining

    @underlining.setter
    def underlining(self, u):
        if u is True or u is False:
            self.__underlining = u
        else:
            raise ValueError

    @property
    def subText(self):
        return self.__subText

    @subText.setter
    def subText(self, s):
        if s is True or s is False:
            self.__subText = s
        else:
            raise ValueError

    @property
    def superText(self):
        return self.__superText

    @superText.setter
    def superText(self, s):
        if s is True or s is False:
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

    @property
    def countOfSpSbl(self):
        return self.__countOfSpSbl

    @countOfSpSbl.setter
    def countOfSpSbl(self, countOfSpSbl):
        self.__countOfSpSbl = countOfSpSbl

    @property
    def countSbl(self):
        return self.__countSbl

    @countSbl.setter
    def countSbl(self, countSbl):
        self.__countSbl = countSbl

    @property
    def lowercase(self):
        return self.__lowercase

    @lowercase.setter
    def lowercase(self, lowercase):
        self.__lowercase = lowercase

    @property
    def uppercase(self):
        return self.__uppercase

    @uppercase.setter
    def uppercase(self, uppercase):
        self.__uppercase = uppercase

    @property
    def lastSbl(self):
        return self.__lastSbl

    @lastSbl.setter
    def lastSbl(self, lastSbl):
        self.__lastSbl = lastSbl

    @property
    def firstkey(self):
        return self.__firstkey

    @firstkey.setter
    def firstkey(self, firstkey):
        self.__firstkey = firstkey

    @property
    def prevEl(self):
        return self.__prevEl

    @prevEl.setter
    def prevEl(self, prevEl):
        self.__prevEl = prevEl

    @property
    def curEl(self):
        return self.__curEl

    @curEl.setter
    def curEl(self, curEl):
        self.__curEl = curEl

    @property
    def nexEl(self):
        return self.__nexEl

    @nexEl.setter
    def nexEl(self, nexEl):
        self.__nexEl = nexEl
