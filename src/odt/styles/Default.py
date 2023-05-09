from odf.opendocument import load
from src.odt.helpers import const


# Получение стилей по умолчанию
def get_styles(self):
    doc = load(self.filePath)
    stylesDict = {}
    for ast in doc.styles.childNodes:
        if ast.qname[1] == "default-style":
            family = ast.getAttribute('family')
            style = {}
            stylesDict[family] = style
            for k in ast.attributes.keys():
                style[k[1]] = ast.attributes[k]
            for n in ast.childNodes:
                for k in n.attributes.keys():
                    style[n.qname[1] + "/" + k[1]] = n.attributes[k]
    return stylesDict

# Получение конкретного стиля по умолчанию
def get_style_default(self, stylefamily):
    doc = load(self.filePath)
    style = {}
    for ast in doc.styles.childNodes:
        if ast.qname[1] == "default-style":
            if ast.getAttribute("family") == stylefamily:
                for k in ast.attributes.keys():
                    style[k[1]] = ast.attributes[k]
                for n in ast.childNodes:
                    for k in n.attributes.keys():
                        style[n.qname[1] + "/" + k[1]] = n.attributes[k]
    return style

#ниже новое


# Получение стиля
def get_style_new(filePath,family):
    doc = load(filePath)
    for ast in doc.styles.childNodes:
        if ast.qname[1] == "default-style":
            if ast.getAttribute("family") == family:
                return ast

# Получение параметров
def get_paragraph_params(style, paramname, propertytype):
    for n in style.childNodes:
        if n.qname[1] == propertytype:
            for k in n.attributes.keys():
                if k[1] == paramname:
                    return n.attributes[k]



#Новый метод


# Получение стилей по умолчанию
def get_styles_new(filePath):
    doc = load(filePath)
    styles = {}
    for ast in doc.styles.childNodes:
        if ast.qname[1] == "default-style":
            family = ast.getAttribute('family')
            style = {}
            style["text-align"] = None
            style["text-indent"] = None
            style["margin-right"] = None
            style["margin-left"] = None
            style["line-height"] = None
            style["margin-top"] = None
            style["margin-bottom"] = None
            style["keep-together"] = None
            style["keep-with-next"] = None
            style["widows"] = None
            style["orphans"] = None
            style["font-name"] = None
            style["font-weight"] = None
            style["font-style"] = None
            style["text-underline-mode"] = None
            style["text-underline-width"] = None
            style["text-underline-style"] = None
            style["text-underlinea-type"] = None
            style["text-position"] = None
            style["font-size"] = None
            style["color"] = None
            style["hyphenate"] = None
            styles[family] = style
            for k in ast.attributes.keys():
                style[k[1]] = ast.attributes[k]
            for n in ast.childNodes:
                for k in n.attributes.keys():
                    if k[1] in const.DEFAULT_PARAM.keys():
                        style[k[1]] = n.attributes[k]
    return styles