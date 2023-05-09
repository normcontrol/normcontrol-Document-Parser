from datetime import datetime

from odf.opendocument import load
from odf.style import Style
from odf.table import Table
from odf.text import P
from guppy import hpy
from src.odt.styles import Style, Auto, Default
from src.odt.helpers import const
import os


def create_path(abs_path, rel_path):
    script_dir = str.split(abs_path, '/')
    path = ''
    ind = 0
    while ind < len(script_dir) - 2:
        path += script_dir[ind]
        path += '/'
        ind += 1
    return path + rel_path


class DocumentParser:
    def __init__(self, file):
        self.filePath = file
        self.fileText = []
        self.default_styles_dict = Default.get_styles_new(file)
        self.styles_dict = Style.get_styles_style_new(file)
        self.auto_styles_dict = Auto.get_styles_new(file)

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
        stylesTree = {}

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
            # доделать
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

    # отсюда не переносила
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

    def get_paragraph_alignment(self, stylename):
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
                                flag = 1
                                style[n.qname[1] + "/" + k[1]] = n.attributes[k]
                    if flag == 0:
                        parent = style["parent-style-name"]
                        print(doc.get_style(parent))

    # параметры параграфа втоматического стиля конкретного
    def get_paragraph_properties_auto(self, stylename):
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

    '''#получение первого родителя стиля
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
                        return style'''

    # определить автоматический стиль или редактора
    def isauto(self, stylename, paramname, propertytype, default):
        style = Auto.get_style_by_name(self.filePath, stylename)
        if style is None:
            return self.has_style_param(default, stylename, paramname, propertytype)
        else:
            return self.has_auto_param(style, paramname, default, propertytype)

    # проверка наличия в автоматическом стиле
    def has_auto_param(self, style, paramname, default, propertytype):
        param = Auto.get_paragraph_params(style, paramname, propertytype)
        if param is None:
            for k in style.attributes.keys():
                if k[1] == "parent-style-name":
                    default = self.has_style_param(default, style.attributes[k], paramname, propertytype)
                    break
        else:
            default = param
        return default

        # проверка наличия в стиле редактора

    def has_style_param(self, default, stylename, paramname, propertytype):
        style = Style.get_style_new(self.filePath, stylename)
        param = Style.get_paragraph_params(style, paramname, propertytype)
        if param is None:
            flag = 0
            for k in style.attributes.keys():
                if k[1] == "parent-style-name":
                    default = self.has_style_param(default, style.attributes[k], paramname, propertytype)
                    flag = 1
                    break
            if flag == 0:
                default = self.has_default_param(default, style.getAttribute("family"), paramname, propertytype)
        else:
            default = param
        return default

        # проверка наличия в стиле по умолчанию

    def has_default_param(self, stylepar, family, paramname, propertytype):
        style = Default.get_style_new(self.filePath, family)
        if style is not None:
            param = Default.get_paragraph_params(style, paramname, propertytype)
            if param is not None:
                stylepar = param
        return stylepar

        # проверка наличия в стиле редактора

    def has_style_param_without_recursion1(self, default, stylename, paramname, propertytype):
        style = Style.get_style_new(self.filePath, stylename)
        param = Style.get_paragraph_params(style, paramname, propertytype)
        if param is None:
            for k in style.attributes.keys():
                if k[1] == "parent-style-name":
                    default = \
                        doc.has_style_param_without_recursion2(default, style.attributes[k], paramname, propertytype)
                    break
        else:
            default = param
        return default

    def has_style_param_without_recursion2(self, default, stylename, paramname, propertytype):
        style = Style.get_style_new(self.filePath, stylename)
        param = Style.get_paragraph_params(style, paramname, propertytype)
        if param is None:
            default = doc.has_default_param(default, style.getAttribute("family"), paramname, propertytype)
        else:
            default = param
        return default

    # общее

    def build_dict(self):
        self.default_styles_dict = doc.default_inher()
        self.styles_dict = doc.styles_inher()
        self.auto_styles_dict = doc.auto_inher()
        #print()

    def styles_inher(self):
        while True :
            flag = 0
            for k in self.styles_dict.keys():
                if self.styles_dict[k] is not None:
                    if "parent-style-name" in self.styles_dict[k].keys():
                        parent = self.styles_dict[k]["parent-style-name"]
                        att = self.styles_dict[parent]
                    else:
                        if self.styles_dict[k]["family"] in self.default_styles_dict.keys():
                            parent = self.styles_dict[k]["family"]
                            att = self.default_styles_dict[parent]
                        else: att = const.DEFAULT_PARAM
                    for kk in self.styles_dict[k].keys():
                        if self.styles_dict[k][kk] is None:
                            print("!!!!!!!!!!!!")
                            print(self.styles_dict[k][kk])
                            if att[kk] is None:
                                flag = 1
                            else: self.styles_dict[k][kk] = att[kk]
                            print(self.styles_dict[k][kk])

            if flag == 0:
                break
        return self.styles_dict

    def default_inher(self):
        for k in self.default_styles_dict.keys():
            for kk in self.default_styles_dict[k].keys():
                if self.default_styles_dict[k][kk] is None:
                    print(self.default_styles_dict[k][kk])
                    self.default_styles_dict[k][kk] = const.DEFAULT_PARAM[kk]
                    print(self.default_styles_dict[k][kk])
        return self.default_styles_dict

    def auto_inher(self):
        for k in self.auto_styles_dict.keys():
            for kk in self.auto_styles_dict[k].keys():
                if self.auto_styles_dict[k][kk] is None:
                    if "parent-style-name" in self.auto_styles_dict[k].keys():
                        parent = self.auto_styles_dict[k]["parent-style-name"]
                        att = self.styles_dict[parent][kk]
                    else: att = const.DEFAULT_PARAM[kk]
                    print(self.auto_styles_dict[k][kk])
                    self.auto_styles_dict[k][kk] = att
                    print(self.auto_styles_dict[k][kk])
        return self.auto_styles_dict

    def inher_start6(self, stylename):
        if stylename in self.auto_styles_dict:
            return self.auto_styles_dict[stylename]
        else:
            return self.styles_dict[stylename]

    def inher_start(self, doc, stylename, paramname):
        if stylename in self.auto_styles_dict.keys():
            return doc.style_inherit(stylename, paramname)
        else:
            return doc.style_inherit2(stylename, paramname)

    def style_inherit_common(self, parent, paramname):
        if paramname in self.styles_dict[parent]:
            return self.styles_dict[parent][paramname]
        else:
            if 'parent-style-name' in self.styles_dict[parent]:
                parent2 = self.styles_dict[parent]['parent-style-name']
                return self.style_inherit_common(parent2, paramname)
            else:
                return None

    def style_inherit(self, stylename, paramname):
        if paramname in self.auto_styles_dict[stylename]:
            #print(self.auto_styles_dict[stylename][paramname])
            return self.auto_styles_dict[stylename][paramname]
        else:
            if 'parent-style-name' in self.auto_styles_dict[stylename]:
                parent = self.auto_styles_dict[stylename]['parent-style-name']
                #print(parent)
                param_from_common = self.style_inherit_common(parent, paramname)
                if param_from_common is not None:
                    #print(self.styles_dict[parent][paramname])
                    return param_from_common
                else:
                    family = self.auto_styles_dict[stylename]['family']
                    if family in self.default_styles_dict:
                        # print("       " + self.default_styles_dict[family]['family'])
                        if paramname in self.default_styles_dict[family]:
                            # print(self.default_styles_dict[family][paramname])
                            return self.default_styles_dict[family][paramname]
                        else:
                            # print(self.default_styles_dict[family]['family'])
                            return None
                    else:
                        return None
            else:
                return None

    def style_inherit2(self, stylename, paramname):
        param_from_common = self.style_inherit_common(stylename, paramname)
        if param_from_common is not None:
            return param_from_common
        else:
            family = self.styles_dict[stylename]['family']
            if family in self.default_styles_dict:
                # print("       " + self.default_styles_dict[family]['family'])
                if paramname in self.default_styles_dict[family]:
                    # print(self.default_styles_dict[family][paramname])
                    return self.default_styles_dict[family][paramname]
                else:
                    # print(self.default_styles_dict[family]['family'])
                    return None
            else:
                return None



# Функция описывающая узел (фрагмент текста) и его атрибуты
def odf_dump_nodes(start_node, level=0):
    if start_node.nodeType == 3:
        # text node
        print("  " * level, "NODE:", start_node.nodeType, ":(text):", str(start_node))
    else:
        # element node
        attrs = []
        for k in start_node.attributes.keys():
            attrs.append(k[1] + ':' + start_node.attributes[k])
        print("  " * level, "NODE:", start_node.nodeType, ":", start_node.qname[1], " ATTR:(", ",".join(attrs), ") ",
              str(start_node))

        for n in start_node.childNodes:
            odf_dump_nodes(n, level + 1)
    return

    # Для сдачи
    # Функция описывающая узел (фрагмент текста) и его атрибуты


def get_nodes(start_node, level=0):
    if start_node.nodeType == 1:
        attrs = []
        for k in start_node.attributes.keys():
            attrs.append(k[1] + ':' + start_node.attributes[k])
        print("  " * level, "Узел:", start_node.qname[1], " Аттрибуты:(", ",".join(attrs), ") ", str(start_node))

        for n in start_node.childNodes:
            get_nodes(n, level + 1)
    return


# узлы со стилями и род блоками
def get_nodes_with_style(start_node, global_style_name, level=0):
    if start_node.nodeType == 1:
        for k in start_node.attributes.keys():
            if (k[1] == "style-name"):
                print("  " * level, "Узел:", start_node.qname[1], " Аттрибуты:(", k[1] + ':' + start_node.attributes[k],
                      ") ", str(start_node), " род стиль ", global_style_name)
                global_style_name = start_node.attributes[k]
        for n in start_node.childNodes:
            get_nodes_with_style(n, global_style_name, level + 1)
    return


# узлы с прохождением по всем стилям
def get_nodes_with_style_full(start_node, global_style_name, doc, level=0):
    if start_node.nodeType == 1:
        for k in start_node.attributes.keys():
            if (k[1] == "style-name"):
                default = const.DEFAULT_PARAM["text-align"]
                par_detail = doc.isauto(start_node.attributes[k], "text-align", "paragraph-properties", default)
                if par_detail == default:
                    if global_style_name != "":
                        par_detail = doc.isauto(global_style_name, "text-align", "paragraph-properties", default)
                default2 = const.DEFAULT_PARAM["font-name"]
                par_detail2 = doc.isauto(start_node.attributes[k], "font-name", "text-properties", default2)
                if par_detail2 == default2:
                    if global_style_name != "":
                        par_detail2 = doc.isauto(global_style_name, "font-name", "text-properties", default2)
                print("  " * level, "Узел:", start_node.qname[1], " Аттрибуты:(", k[1] + ':' + start_node.attributes[k],
                      ") ", str(start_node), " род блок ", global_style_name, "параметр ", par_detail2, par_detail)
                global_style_name = start_node.attributes[k]
        for n in start_node.childNodes:
            get_nodes_with_style_full(n, global_style_name, doc, level + 1)
    return


# узлы с прохождением по всем стилям
def get_nodes_with_style_full3(start_node, global_style_name, global_style_name2, doc, level=0):
    if start_node.nodeType == 1:
        for k in start_node.attributes.keys():
            if (k[1] == "style-name"):
                default = const.DEFAULT_PARAM["text-align"]
                par_detail = doc.isauto(start_node.attributes[k], "text-align", "paragraph-properties", default)
                if par_detail == default:
                    par_detail = global_style_name
                default2 = const.DEFAULT_PARAM["text-align"]
                par_detail2 = doc.isauto(start_node.attributes[k], "font-name", "text-properties", default2)
                if par_detail2 == default2:
                    par_detail2 = global_style_name2
                print("  " * level, "Узел:", start_node.qname[1], " Аттрибуты:(", k[1] + ':' + start_node.attributes[k],
                      ") ", str(start_node), "параметр ", par_detail, par_detail2)
                global_style_name = par_detail
                global_style_name2 = par_detail2
        for n in start_node.childNodes:
            get_nodes_with_style_full3(n, global_style_name, global_style_name2, doc, level + 1)
    return


# узлы с прохождением по всем стилям
def get_nodes_with_style_full2(start_node, list, doc, level=0):
    if start_node.nodeType == 1:
        for k in start_node.attributes.keys():
            if (k[1] == "style-name"):
                default = const.DEFAULT_PARAM["text-align"]
                par_detail = doc.isauto(start_node.attributes[k], "text-align", "paragraph-properties", default)
                if par_detail == default:
                    par_detail = list["text-align"]
                else:
                    list["text-align"] = par_detail
                    list["style"] = start_node.attributes[k]
                print("  " * level, "Узел:", start_node.qname[1], " Аттрибуты:(", k[1] + ':' + start_node.attributes[k],
                      ") ", str(start_node), "параметр ", par_detail, " стиль ", list["style"])
        for n in start_node.childNodes:
            get_nodes_with_style_full2(n, list, doc, level + 1)
    return


# узлы с прохождением по всем стилям
def get_nodes_with_style_full4(start_node, list, doc, level=0):
    if start_node.nodeType == 1:
        for k in start_node.attributes.keys():
            if (k[1] == "style-name"):
                default = const.DEFAULT_PARAM["text-align"]
                par_detail = doc.isauto(start_node.attributes[k], "text-align", "paragraph-properties", default)
                if par_detail == default:
                    par_detail = list[0]
                else:
                    list[0] = par_detail
                print("  " * level, "Узел:", start_node.qname[1], " Аттрибуты:(", k[1] + ':' + start_node.attributes[k],
                      ") ", str(start_node), "параметр ", par_detail)
        for n in start_node.childNodes:
            get_nodes_with_style_full4(n, list, doc, level + 1)
    return
# узлы с прохождением по всем стилям НОВЫЙ
def get_nodes_with_style_full5(start_node, doc, style_val, level=0):
    if start_node.nodeType == 1:
        for k in start_node.attributes.keys():
            if (k[1] == "style-name"):
                #print(start_node.attributes[k])

                par_detail = doc.inher_start(doc, start_node.attributes[k], "text-align")
                if par_detail is None:
                    par_detail = style_val
                else:
                    style_val = par_detail

                print("  " * level, "Узел:", start_node.qname[1], " Аттрибуты:(", k[1] + ':' + start_node.attributes[k],
                      ") ", str(start_node), "параметр ", par_detail, "   ", style_val)
        for n in start_node.childNodes:
            get_nodes_with_style_full5(n, doc, style_val, level + 1)
    return
#новый новый
def get_nodes_with_style_full6(start_node, doc, parent_node, level=0):
    #if level == 0:
     #   doc.build_dict()
    if start_node.nodeType == 1:
        for k in start_node.attributes.keys():
            if (k[1] == "style-name"):
                #print(start_node.attributes[k])
                #doc.check()
                att= doc.inher_start6(start_node.attributes[k])
                for kk in att.keys():
                    if att[kk] is None:
                        att[kk] = parent_node[kk]
                parent_node = att
                print("  " * level, "Узел:", start_node.qname[1], " Аттрибуты:(", k[1] + ':' + start_node.attributes[k],
                      ") ", str(start_node), "параметр ", att)
        for n in start_node.childNodes:
            get_nodes_with_style_full6(n, doc, parent_node, level + 1)
    return


if __name__ == '__main__':

    script_path = os.path.abspath(__file__)
    rel_path = "documents/dipbac.odt"
    doc = DocumentParser('C:/Users/lario/PycharmProjects/normcontrol-Document-Parser/src/odt/documents/dipbac.odt')
    '''
    print(get_nodes_with_style_full3(doc2.text,"1","2", doc))
    h2 = h.heap()
    print(h2)
    print("\nMemory Usage After Creation Of Objects : ", h2.size - h1.size, " bytes")
    print(doc.isauto("Текстнатитульнойстранице", "text-align", "paragraph-properties", ""))
    print("-----------------------------------------\n")
    print(get_nodes_with_style_full3(doc2.text,"ar", doc))print(get_nodes_with_style_full(doc2.text,"", doc))

    print("-----------------------------------------\n")
    print(get_nodes(doc2.text))
    print(get_nodes_with_style_full(doc2.text,"", doc))
    print("-----------------------------------------\n")
    
    print(doc.isauto("Названиеработы", "text-align", "paragraph-properties"))print("Получение текста и автоматических стилей:\n")
    doc.all_odt_text()
    
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
    print(doc.get_text_style_by_name('T150'))
    print("-------------------------------------------\n")
    print("Получение конкретных характеристик:")
    print(doc.get_paragraph_alignment('P1'))
    print("-------------------------------------------\n")
    print(doc.get_style_base_auto('P1'))
    print("-------------------------------------------\n")
    print(doc.get_style_base_auto2('P1'))
    print("-------------------------------------------\n")
    print(doc.get_style_base_auto3('P12', "text-align", const.DEFAULT_PARAM["text-align"]))
    print("-------------------------------------------\n")

    ast = Style.get_style_new('dipbac.odt', 'Текстнатитульнойстранице')
    print(Style.get_paragraph_params(ast, 'text-align'))

    print("-------------------------------------------\n")


    print(doc.isauto("Текстнатитульнойстранице", "text-align", "paragraph-properties"))
    print(doc.isauto('P12', "text-align", "paragraph-properties"))
    print(get_nodes(doc2.text))
    print(doc.has_style_param(const.DEFAULT_PARAM["text-align"], "Оглавление1", "text-align", "paragraph-properties"))
    print(doc.has_style_param_without_recursion1(const.DEFAULT_PARAM["text-align"], "Оглавление1", "text-align",
                                                 "paragraph-properties"))
   
    


    print(get_nodes_with_style_full(doc2.text, "", doc))
    '''
    #print(Default.get_styles_new(doc))
    for key in const.DEFAULT_PARAM.keys():
        print(key)
    #doc.check()
    doc.style_inherit('P12', "text-align")
    now3 = datetime.now()

    current_time3 = now3.strftime("%H:%M:%S")
    print("Current Time =", current_time3)

    h = hpy()
    h1 = h.heap()
    doc3 = DocumentParser('C:/Users/lario/PycharmProjects/normcontrol-Document-Parser/src/odt/documents/dipbac.odt')
    doc2 = load("C:/Users/lario/PycharmProjects/normcontrol-Document-Parser/src/odt/documents/dipbac.odt")

    #print(get_nodes_with_style_full5(doc2.text,doc3, const.DEFAULT_PARAM["text-align"]))


   # doc.styles_inher(doc3)
    doc3.build_dict()
    print(get_nodes_with_style_full6(doc2.text,doc3, const.DEFAULT_PARAM))
    h2 = h.heap()
    print(h2)
    print("\nMemory Usage After Creation Of Objects : ", h2.size - h1.size, " bytes")
    now4 = datetime.now()
    current_time4 = now4.strftime("%H:%M:%S")
    print("Current Time =", current_time4)
    print(now4-now3)