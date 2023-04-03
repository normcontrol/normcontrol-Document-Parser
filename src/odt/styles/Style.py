from odf.opendocument import load


# Получение стилей
from src.odt.helpers import const


def get_styles_style(self):
    doc = load(self.filePath)
    stylesDict = {}
    for ast in doc.styles.childNodes:
        if ast.qname[1] == "style":
            name = ast.getAttribute('name')
            style = {}
            stylesDict[name] = style

            for k in ast.attributes.keys():
                style[k[1]] = ast.attributes[k]
            for n in ast.childNodes:
                for k in n.attributes.keys():
                    style[n.qname[1] + "/" + k[1]] = n.attributes[k]
    return stylesDict


# Получение свойств текста из обычных стилей
def get_styles_text(self):
    doc = load(self.filePath)
    stylesDict = {}
    for ast in doc.styles.childNodes:
        if ast.qname[1] == "style":
            name = ast.getAttribute('name')
            style = {}
            stylesDict[name] = style

            for n in ast.childNodes:
                if n.qname[1] == "text-properties":
                    for k in n.attributes.keys():
                        style[n.qname[1] + "/" + k[1]] = n.attributes[k]
    print(stylesDict)


# Получение конкретного стиля
def get_style(self, stylename):
    doc = load(self.filePath)
    style = {}
    for ast in doc.styles.childNodes:
        if ast.qname[1] == "style":
            if ast.getAttribute("name") == stylename:
                for k in ast.attributes.keys():
                    style[k[1]] = ast.attributes[k]
                for n in ast.childNodes:
                    for k in n.attributes.keys():
                        style[n.qname[1] + "/" + k[1]] = n.attributes[k]
    return style


# ниже новое


# Получение стиля
def get_style_new(filePath, stylename):
    doc = load(filePath)
    for ast in doc.styles.childNodes:
        if ast.qname[1] == "style":
            if ast.getAttribute("name") == stylename:
                return ast

# Получение параметров
def get_paragraph_params(style, paramname, propertytype):
    for n in style.childNodes:
        if n.qname[1] == propertytype:
            for k in n.attributes.keys():
                if k[1] == paramname:
                    return n.attributes[k]

# --------------Таблицы
# Получение свойств таблиц из обычных стилей
def get_styles_table(self):
    doc = load(self.filePath)
    stylesDict = {}
    for ast in doc.styles.childNodes:
        if ast.qname[1] == "style":
            name = ast.getAttribute('name')
            style = {}
            stylesDict[name] = style

            for n in ast.childNodes:
                if n.qname[1] == "table-properties" or n.qname[1] == "table-column-properties" \
                        or n.qname[1] == "table-row-properties" or n.qname[1] == "table-cell-properties":
                    for k in n.attributes.keys():
                        style[n.qname[1] + "/" + k[1]] = n.attributes[k]
    return stylesDict

# Получение параметра таблицы
def get_table_param(style, paramname):
    for n in style.childNodes:
        if n.qname[1] == "table-properties":
            for k in n.attributes.keys():
                if k[1] == paramname:
                    return n.attributes[k]

# Получение параметра строки таблицы
def get_rowTable_param(style, paramname):
    for n in style.childNodes:
        if n.qname[1] == "table-row-properties":
            for k in n.attributes.keys():
                if k[1] == paramname:
                    return n.attributes[k]

# Получение параметра столбца таблицы
def get_columnTable_param(style, paramname):
    for n in style.childNodes:
        if n.qname[1] == "table-column-properties":
            for k in n.attributes.keys():
                if k[1] == paramname:
                    return n.attributes[k]

# Получение параметра ячейки таблицы
def get_cellTable_param(style, paramname):
    for n in style.childNodes:
        if n.qname[1] == "table-cell-properties":
            for k in n.attributes.keys():
                if k[1] == paramname:
                    return n.attributes[k]

# --------------Списки
# Получение свойств списков из обычных стилей
def get_styles_list(self):
    doc = load(self.filePath)
    stylesDict = {}
    for ast in doc.styles.childNodes:
        if ast.qname[1] == "style":
            name = ast.getAttribute('name')
            style = {}
            stylesDict[name] = style
            for n in ast.childNodes: #needbpoint
                if "list" in n.qname[1]:
                    for k in n.attributes.keys():
                        style[n.qname[1] + "/" + k[1]] = n.attributes[k]
    return stylesDict

# Получение свойств текста списков из обычных стилей
def get_styles_listText(self):
    doc = load(self.filePath)
    stylesDict = {}
    for ast in doc.styles.childNodes:
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

# Получение параметров стиля списка
def get_list_param(style, paramname):
    for n in style.childNodes:
        if  "list" in n.qname[1] or "text" in n.qname[1]:
            for k in n.attributes.keys():
                if k[1] == paramname:
                    return n.attributes[k]

# --------------Изображения
# Получение данных о frame изображения
def get_styles_image_frame(self):
    doc = load(self.filePath)
    stylesDict = {}
    help = list(doc.element_dict.keys())
    token = ''
    for i in help:
        if i[1] == 'frame':
            token = i

    objs = doc.element_dict.get(token)
    for ast in objs:
        if ast.qname[1] == "frame":
            name = ast.getAttribute('name')
            style = {}
            for i in ast.attributes.keys():
                style[ast.qname[1] + "/" + i[1]] = ast.attributes[i]
            for n in ast.childNodes:
                for k in n.attributes.keys():
                    style[n.qname[1] + "/" + k[1]] = n.attributes[k]
            stylesDict[name] = style
    return stylesDict

# Получение данных изображения
def get_styles_image(self):
    doc = load(self.filePath)
    stylesDict = {}
    help = list(doc.element_dict.keys())
    token = ''
    for i in help:
        if i[1] == 'image':
            token = i

    objs = doc.element_dict.get(token)
    for ast in objs:
        if ast.qname[1] == "image":
            name = ast.getAttribute('href')
            style = {}
            for n in ast.attributes.keys():
                style[n] = ast.attributes[n]
            stylesDict[name] = style
    return stylesDict

# Получение параметра frame
def get_frame_param(filePath, stylename, paramname):
    doc = load(filePath)
    help = list(doc.element_dict.keys())
    token = ''
    for i in help:
        if i[1] == 'frame':
            token = i

    objs = doc.element_dict.get(token)
    for ast in objs:
        if stylename in ast.getAttribute('name'):
            for i in ast.attributes.keys():
                if paramname in i:
                    return ast.attributes[i]

# Получение параметра image
def get_image_param(filePath, stylename, paramname):
    doc = load(filePath)
    help = list(doc.element_dict.keys())
    token = ''
    for i in help:
        if i[1] == 'image':
            token = i

    objs = doc.element_dict.get(token)
    for ast in objs:
        if stylename in ast.getAttribute('href'):
            for i in ast.attributes.keys():
                if paramname in i:
                    return ast.attributes[i]

#новое
# Получение стилей
def get_styles_style_new(filePath):
    doc = load(filePath)
    stylesDict = {}
    for ast in doc.styles.childNodes:
        if ast.qname[1] == "style":
            name = ast.getAttribute('name')
            style = {}
            stylesDict[name] = style

            for k in ast.attributes.keys():
                style[k[1]] = ast.attributes[k]
            for n in ast.childNodes:
                for k in n.attributes.keys() :
                    if k[1] in const.DEFAULT_PARAM.keys():
                        style[k[1]] = n.attributes[k]
    return stylesDict