from odf.opendocument import load


# Получение стилей
from src.odt.helpers import const


def get_styles(self):
    doc = load(self.filePath)
    styles = {}
    for ast in doc.automaticstyles.childNodes:

        name = ast.getAttribute('name')
        style = {}
        styles[name] = style

        for k in ast.attributes.keys():
            style[k[1]] = ast.attributes[k]
        for n in ast.childNodes:
            for k in n.attributes.keys():
                style[n.qname[1] + "/" + k[1]] = n.attributes[k]
    return styles

# Получение параметов текста из автоматических стилей
def get_styles_automatic_styles_text(self):
    doc = load(self.filePath)
    styles = {}
    for ast in doc.automaticstyles.childNodes:

        name = ast.getAttribute('name')
        style = {}
        styles[name] = style

        for n in ast.childNodes:
            if n.qname[1] == "text-properties":
                for k in n.attributes.keys():
                    style[n.qname[1] + "/" + k[1]] = n.attributes[k]
    print(styles)


# Получение конкретного стиля автоматического
def get_style_automatic_by_name(self, stylename):
    doc = load(self.filePath)
    style = {}
    for ast in doc.automaticstyles.childNodes:
        if ast.getAttribute("name") == stylename:
            for k in ast.attributes.keys():
                style[k[1]] = ast.attributes[k]
            for n in ast.childNodes:
                for k in n.attributes.keys():
                    style[n.qname[1] + "/" + k[1]] = n.attributes[k]
    return style

# Получение характеристик текста
def get_text_style_by_name(self, textname):
    doc = load(self.filePath)
    text_styles = {}
    for ast in doc.automaticstyles.childNodes:
        if ast.qname[1] == "style":
            if ast.getAttribute("name") == textname:
                for k in ast.attributes.keys():
                    text_styles[k[1]] = ast.attributes[k]
                for n in ast.childNodes:
                    for k in n.attributes.keys():
                        text_styles[n.qname[1] + "/" + k[1]] = n.attributes[k]
    return text_styles

#ниже новое

# Получение конкретного стиля автоматического
def get_style_by_name(filePath, stylename):
    doc = load(filePath)
    for ast in doc.automaticstyles.childNodes:
        if ast.getAttribute("name") == stylename:
            return ast

#"paragraph-properties"
def get_paragraph_params(ast, paramname, propertytype):
    for n in ast.childNodes:
        if n.qname[1] == propertytype:
            for k in n.attributes.keys():
                if k[1] == paramname:
                   return n.attributes[k]

# --------------Таблицы
# Получение параметов колонок, ячеек, столбцов и строк таблиц из автоматических стилей
def get_styles_automatic_styles_table(self):
    doc = load(self.filePath)
    styles = {}
    for ast in doc.automaticstyles.childNodes:
        name = ast.getAttribute('name')
        style = {}
        styles[name] = style
        for n in ast.childNodes:
            if n.qname[1] == "table-properties" or n.qname[1] == "table-column-properties" \
                    or n.qname[1] == "table-row-properties" or n.qname[1] == "table-cell-properties":
                for k in n.attributes.keys():
                    style[n.qname[1] + "/" + k[1]] = n.attributes[k]
    return styles

# --------------Списки
# Получение параметов списков из автоматических стилей
def get_styles_automatic_styles_list(self):
    doc = load(self.filePath)
    styles = {}
    for ast in doc.automaticstyles.childNodes:
        name = ast.getAttribute('name')
        style = {}
        for n in ast.childNodes:
            if "list-level" in n.qname[1]:
                styles[name] = style
                for k in n.attributes.keys():
                    style[n.qname[1] + "/" + k[1]] = n.attributes[k]
    return styles

# Получение свойств текста списков из обычных стилей
def get_styles_automatic_listsText(self):
    doc = load(self.filePath)
    stylesDict = {}
    for ast in doc.automaticstyles.childNodes:
        if ast.qname[1] == "style":
            name = ast.getAttribute('name')
            style = {}
            if 'Абзацсписка' in name or 'WW' in name or 'LF' in name:
                stylesDict[name] = style
                for n in ast.childNodes:
                    if n.qname[1] == "text-properties":
                        for k in n.attributes.keys():
                            style[n.qname[1] + "/" + k[1]] = n.attributes[k]
    return stylesDict

# новый
def get_styles_new(filePath):
    doc = load(filePath)
    styles = {}

    for ast in doc.automaticstyles.childNodes:

        name = ast.getAttribute('name')
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

        styles[name] = style

        for k in ast.attributes.keys():
            style[k[1]] = ast.attributes[k]
        for n in ast.childNodes:
            for k in n.attributes.keys():
                if k[1] in const.DEFAULT_PARAM.keys():
                    style[k[1]] = n.attributes[k]
    return styles