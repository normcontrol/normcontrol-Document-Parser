from odf.opendocument import load
from odf.opendocument import OpenDocumentText
from odf.style import Style, TextProperties
from odf import text
from odf.table import Table
from odf.text import H, P, Span

class DocumentParser():
    def __init__(self, file):
        self.filePath = file
        self.fileText = []

    # Получаем весь текст документа
    def all_odt_text(self):
        doc = load(self.filePath)
        for paragraph in doc.getElementsByType(P):
            self.fileText.append(paragraph)
            print(paragraph)

    # Получаем таблицы ЗАГОТОВКА
    def all_odt_table(self):
        doc = load(self.filePath)
        for table in doc.getElementsByType(Table):
            self.fileText.append(table)
            print(table)


    # Получение стилей автоматических
    def get_styles_automatic_styles(self):
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

        # Получение стилей по умолчанию
    def get_styles_default_style(self):
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



    # Дерево
    def get_styles_tree(self):
        stylesDef = doc.get_styles_default_style()
        styles = doc.get_styles_style()
        stylesAuto = doc.get_styles_automatic_styles()
        stylesTree={}

        for sD in stylesDef:
            style = {}
            stylesTree[sD] = style

        for s in styles:
            styleS = doc.get_style(s)
            style = {}
            family = styleS.get('family')
            name = styleS.get('name')
            stylesTree[family][name] = style

        for sA in stylesAuto:
            styleA = doc.get_style_automatic(sA)
            style = {}
            #доделать
        return stylesTree



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

    # Получение конкретного стиля автоматического
    def get_style_automatic(self, stylename):
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






# Функция описывающая узел (фрагмент текста) и его атрибуты
def odf_dump_nodes(start_node, level=0):
    if start_node.nodeType==3:
        # text node
        print("  "*level, "NODE:", start_node.nodeType, ":(text):", str(start_node))
    else:
        # element node
        attrs= []
        for k in start_node.attributes.keys():
            attrs.append( k[1] + ':' + start_node.attributes[k]  )
        print("  "*level, "NODE:", start_node.nodeType, ":", start_node.qname[1], " ATTR:(", ",".join(attrs), ") ", str(start_node))

        for n in start_node.childNodes:
            odf_dump_nodes(n, level+1)
    return

if __name__ == '__main__':
    doc = DocumentParser('dipbac.odt')
    doc.all_odt_text()
    print(doc.get_styles_automatic_styles())
    doc.all_odt_table()
    doc2 = load('dipbac.odt')
    print(odf_dump_nodes(doc2.text))
    doc.get_styles_default_style()
    doc.get_styles_style()
    doc.get_styles_text()
    doc.get_styles_automatic_styles_text()
    doc.get_styles_tree()
    print(doc.get_style("Заголовок1"))
    print(doc.get_style_default('table'))
    print(doc.get_style_automatic('P1'))
