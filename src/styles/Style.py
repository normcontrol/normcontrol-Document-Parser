from odf.opendocument import load


# Получение стилей
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
def get_paragraph_params(style, paramname):
    for n in style.childNodes:
        if n.qname[1] == "paragraph-properties":
            for k in n.attributes.keys():
                if k[1] == paramname:
                    return n.attributes[k]


