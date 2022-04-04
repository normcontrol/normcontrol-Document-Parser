from odf.opendocument import load
from odf.opendocument import OpenDocumentText
from odf.style import Style, TextProperties
from odf import text
from odf.table import Table
from odf.text import H, P, Span
from guppy import hpy
import timing

from src.styles import Auto
from src.styles import Default
from src.styles import Style
from src import const



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

#отсюда не переносила
        # Получение параметов текста из стилей
    def get_styles_paragraph_alignment(self):
        doc = load(self.filePath)
        stylesDict = {}
        for ast in doc.styles.childNodes:
            if ast.qname[1] == "style":
                name = ast.getAttribute('name')
                style = {}
                stylesDict[name] = style

                for n in ast.childNodes:
                    if n.qname[1] == "paragraph-properties":
                        for k in n.attributes.keys():
                            if k[1] == "text-align":
                                style[n.qname[1] + "/" + k[1]] = n.attributes[k]
        print(stylesDict)

    def get_paragraph_alignment(self,stylename):
        doc1 = load(self.filePath)
        style = {}
        flag = 0
        for ast in doc1.automaticstyles.childNodes:
            if ast.getAttribute("name") == stylename:
                for k in ast.attributes.keys():
                    style[k[1]] = ast.attributes[k]
                for n in ast.childNodes:
                    if n.qname[1] == "paragraph-properties":
                        for k in n.attributes.keys():
                            if k[1] == "text-align":
                                flag=1
                                style[n.qname[1] + "/" + k[1]] = n.attributes[k]
                    if flag==0:
                        parent = style["parent-style-name"]
                        print(doc.get_style(parent))
    #проба рекурсии для поиска не работает
    def get_paragraph_alignment_par_pro(self,parpro):
        print(parpro)
        print(parpro["paragraph-properties/text-align"])

    #параметры параграфа втоматического стиля конкретного
    def get_paragraph_properties_auto(self,stylename):
        doc1 = load(self.filePath)
        style = {}
        for ast in doc1.automaticstyles.childNodes:
            if ast.getAttribute("name") == stylename:
                for k in ast.attributes.keys():
                    style[k[1]] = ast.attributes[k]
                for n in ast.childNodes:
                    if n.qname[1] == "paragraph-properties":
                        for k in n.attributes.keys():
                            style[n.qname[1] + "/" + k[1]] = n.attributes[k]
        return style
    #получение первого родителя стиля
    def get_style_base_auto(self,stylename):
        doc1 = load(self.filePath)
        style = {}
        for ast in doc1.automaticstyles.childNodes:
            if ast.getAttribute("name") == stylename:
                style["name"] = stylename
                for k in ast.attributes.keys():
                    if k[1] == "parent-style-name":
                        flag = 1
                        style["parent-style-name/"+str(flag)] = ast.attributes[k]
                        doc.get_parent_auto(flag, style, ast.attributes[k])
                return style

    #получение остальных родиделей без по умолчанию
    def get_parent_auto(self,flag, style, stylename):
        doc1 = load(self.filePath)
        for ast in doc1.styles.childNodes:
            if ast.qname[1] == "style":
                if ast.getAttribute("name") == stylename:
                    for k in ast.attributes.keys():
                        if k[1] == "parent-style-name":
                            style["parent-style-name/"+str(flag+1)] = ast.attributes[k]
                            doc.get_parent_auto(flag+1, style, ast.attributes[k])
                    return style

                    #получение первого родителя стиля
    def get_style_base_auto2(self,stylename):
        doc1 = load(self.filePath)
        style = {}
        flag = 0
        for ast in doc1.automaticstyles.childNodes:
            if ast.getAttribute("name") == stylename:
                style["name"] = stylename
                for n in ast.childNodes:
                    if n.qname[1] == "paragraph-properties":
                        for k in n.attributes.keys():
                            if k[1] == "text-align":
                                flag=1
                                style[n.qname[1] + "/" + k[1]] = n.attributes[k]
                    if flag==0:
                        for k in ast.attributes.keys():
                            if k[1] == "parent-style-name":
                                flag = 1
                                style["parent-style-name/" + str(flag)] = ast.attributes[k]
                                doc.get_parent_auto2(flag, style, ast.attributes[k])
                    return style

    #получение остальных родиделей без по умолчанию
    def get_parent_auto2(self,flag, style, stylename):
        doc1 = load(self.filePath)
        flag_first = flag
        for ast in doc1.styles.childNodes:
            if ast.qname[1] == "style":
                if ast.getAttribute("name") == stylename:
                    for n in ast.childNodes:
                        if n.qname[1] == "paragraph-properties":
                            for k in n.attributes.keys():
                                if k[1] == "text-align":
                                    flag=1
                                    style[n.qname[1] + "/" + k[1]] = n.attributes[k]
                        if flag==flag_first:
                            for k in ast.attributes.keys():
                                if k[1] == "parent-style-name":
                                    style["parent-style-name/"+str(flag+1)] = ast.attributes[k]
                                    doc.get_parent_auto(flag+1, style, ast.attributes[k])
                        return style

                        #получение первого родителя стиляИТОГ
    def get_style_base_auto3(self,stylename, paramname, default):
        style = Auto.get_style_by_name(self.filePath,stylename)
        stylepar = {}
        stylepar["param"] = const.DEFAULT_PARAM[paramname]
        param = Auto.get_paragraph_params(style, paramname)
        if param is None:
            for k in style.attributes.keys():
                if k[1] == "parent-style-name":
                    default = doc.get_parent_auto3(default, style.attributes[k], paramname)
        else:
            default = paramname
        return default

    def get_style_base3(self,stylename, paramname, default):
        return doc.get_parent_auto3(default,stylename,paramname)


    #получение остальных родиделей без по умолчанию
    def get_parent_auto3(self, default, stylename, paramname):
        style = Style.get_style_new(self.filePath,stylename)
        param = Style.get_paragraph_params(style,paramname)
        if param is None:
            for k in style.attributes.keys():
                if k[1] == "parent-style-name":
                   default = doc.get_parent_auto3(default, style.attributes[k], paramname)
            doc.get_parent_def3(default, style.getAttribute("family"), paramname)
        else:
            default = param
        return default

    #получение остальных родиделей по умолчанию
    def get_parent_def3(self, stylepar, family, paramname):
        style = Default.get_style_new(self.filePath,family)
        param = Default.get_paragraph_params(style,paramname)
        if param is not None:
            stylepar = param
        return stylepar






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
    h = hpy()
    h1 = h.heap()

    doc = DocumentParser('dipbac.odt')
    print("Получение текста и автоматических стилей:\n")
    doc.all_odt_text()
    print(doc.get_styles_automatic_styles())
    print(Auto.get_styles(doc))
    print("-----------------------------------------\n")

    print("Получение таблиц заголовка:\n")
    table_doc = DocumentParser('tabl1.odt')
    table_doc.all_odt_table()
    print("-----------------------------------------\n")

    print("Получение узлов:\n")
    doc2 = load('dipbac.odt')
    print(odf_dump_nodes(doc2.text))
    print("-----------------------------------------\n")

    print("Получение стилей:\n")
    doc.get_styles_default_style()
    print("-------------------------------------------")
    doc.get_styles_style()
    print("-------------------------------------------")
    doc.get_styles_text()
    print("-------------------------------------------")
    doc.get_styles_automatic_styles_text()
    # doc.get_styles_tree()
    print(doc.get_style("Заголовок1"))
    print("-----------------------------------------\n")
    print(doc.get_style_default('table'))
    print("-----------------------------------------\n")
    print(doc.get_style_automatic_by_name('P105'))
    print("-----------------------------------------\n")
    print(doc.get_text_style_by_name('T13'))
    print("-------------------------------------------\n")
    print("Получение конкретных характеристик:")
    print(doc.get_paragraph_alignment('P1'))
    print("-------------------------------------------\n")
    print(doc.get_style_base_auto2('P1'))
    print("-------------------------------------------\n")
    print(doc.get_style_base_auto3('P12', "text-align", const.DEFAULT_PARAM["text-align"]))
    print("-------------------------------------------\n")

    ast = Style.get_style_new('dipbac.odt', 'Текстнатитульнойстранице')
    print(Style.get_paragraph_params(ast, 'text-align'))

    print("-------------------------------------------\n")
    print(doc.get_style_base3("Текстнатитульнойстранице", "text-align", const.DEFAULT_PARAM["text-align"]))

    h2 = h.heap()
    print(h2)
    print("\nMemory Usage After Creation Of Objects : ", h2.size - h1.size, " bytes")
