from src.helpers.odt import consts
from src.odt.elements.ODTDocument import ODTDocument
from src.odt.elements.AutomaticStylesParser import AutomaticStylesParser

class NodesParser:
    """
    Description: A class containing methods for traversing document style nodes.

    Methods:
        print_all_document_nodes(start_node, level=0) -
            Outputs each node of the document and its attributes.

        print_all_document_nodes_with_style(start_node, global_style_name: str, doc: ODTDocument, level=0) -
            Outputs each text node of the document and its attributes with a passage through all styles,
            performing a search at the same nesting level.

        print_all_document_nodes_with_higher_style_data(start_node, list, doc: ODTDocument, level=0) -
            Outputs each text node of the document and its attributes with a passage through all styles, searching,
            in case of absence, in nodes at a higher level.
    ----------
    Описание: Класс, содержащий методы для обхода узлов стилей документа.

    Методы:
        print_all_document_nodes(start_node, level=0) -
            Выводит каждый узел документа и его атрибуты.

        print_all_document_nodes_with_style(start_node, global_style_name, doc: ODTDocument, level=0) -
            Выводит каждый каждый текстовый узел документа и его атрибуты с прохождением по всем стилям,
            выполняя поиск на одном уровне вложенности.

        print_all_document_nodes_with_higher_style_data((start_node, list, doc: ODTDocument, level=0) -
            Выводит каждый каждый текстовый узел документа и его атрибуты с прохождением по всем стилям,
            выполняя поиск, в случае отсутствия, в узлах уровнем выше.
    """

    def print_all_document_nodes(self, start_node, level=0):
        """Outputs each node of the document and its attributes.

        Keyword arguments:
            start_node - initial search node;
            level - search level and recursion nesting.
        ----------
        Выводит каждый узел документа и его атрибуты.

        Аргументы:
            start_node - начальный узел поиска;
            level - уровень поиска и вложенности рекурсии.
        """
        if start_node.nodeType == 1:
            attrs = []
            for k in start_node.attributes.keys():
                attrs.append(k[1] + ':' + start_node.attributes[k])
            print("  " * level, "Узел:", start_node.qname[1], " Аттрибуты:(", ",".join(attrs), ") ", str(start_node))

            for n in start_node.childNodes:
                self.print_all_document_nodes(n, level + 1)
        return

    def print_all_document_nodes_with_style_data(self, start_node, global_style_name: str, doc: ODTDocument, level=0):
        """Outputs each text node of the document and its attributes with a passage through all styles,
        performing a search at the same nesting level.

        Keyword arguments:
            start_node - initial search node;
            global_style_name - a string name of global style for research;
            doc - an instance of the ODTDocument class containing the data of the document under study;
            level - search level and recursion nesting.
        ----------
        Выводит каждый каждый текстовый узел документа и его атрибуты с прохождением по всем стилям,
        выполняя поиск на одном уровне вложенности.

        Аргументы:
            start_node - начальный узел поиска;
            global_style_name - строковое название глобаьного стиля для исследования;
            doc - экземпляр класса ODTDocument, содержащий данные исследуемого документа;
            level - уровень поиска и вложенности рекурсии.
        """
        parser_auto_styles = AutomaticStylesParser()
        if start_node.nodeType == 1:
            for k in start_node.attributes.keys():
                if (k[1] == "style-name"):
                    default = consts.DEFAULT_PARAM["text-align"]
                    par_detail = parser_auto_styles.is_automatic_style(doc, start_node.attributes[k], "text-align",
                                                            "paragraph-properties", default)
                    if par_detail == default:
                        if global_style_name != "":
                            par_detail = parser_auto_styles.is_automatic_style(doc, global_style_name, "text-align",
                                                                    "paragraph-properties", default)
                    default2 = consts.DEFAULT_PARAM["font-name"]
                    par_detail2 = parser_auto_styles.is_automatic_style(doc, start_node.attributes[k], "font-name",
                                                             "text-properties", default2)
                    if par_detail2 == default2:
                        if global_style_name != "":
                            par_detail2 = parser_auto_styles.is_automatic_style(doc, global_style_name, "font-name",
                                                                     "text-properties", default2)
                    print("  " * level, "Узел:", start_node.qname[1], " Аттрибуты:(",
                          k[1] + ':' + start_node.attributes[k],
                          ") ", str(start_node), " род блок ", global_style_name, "параметр ", par_detail2, par_detail)
                    global_style_name = start_node.attributes[k]
            for n in start_node.childNodes:
                self.print_all_document_nodes_with_style_data(n, global_style_name, doc, level + 1)
        return

    def print_all_document_nodes_with_higher_style_data(self, start_node, list, doc: ODTDocument, level=0):
        """Outputs each text node of the document and its attributes with a passage through all styles, searching,
        in case of absence, in nodes at a higher level.

        Keyword arguments:
            start_node - initial search node;
            list - a list of style attributes;
            doc - an instance of the ODTDocument class containing the data of the document under study;
            level - search level and recursion nesting.
        ----------
        Выводит каждый каждый текстовый узел документа и его атрибуты с прохождением по всем стилям,
        выполняя поиск, в случае отсутствия, в узлах уровнем выше.

        Аргументы:
            start_node - начальный узел поиска;
            list - список атрибутов стиля;
            doc - экземпляр класса ODTDocument, содержащий данные исследуемого документа;
            level - уровень поиска и вложенности рекурсии.
        """
        parser_auto_styles = AutomaticStylesParser()
        if start_node.nodeType == 1:
            for k in start_node.attributes.keys():
                if (k[1] == "style-name"):
                    default = consts.DEFAULT_PARAM["text-align"]
                    par_detail = parser_auto_styles.is_automatic_style(doc, start_node.attributes[k],
                                                                       "text-align", "paragraph-properties", default)
                    if par_detail == default:
                        par_detail = list["text-align"]
                    else:
                        list["text-align"] = par_detail
                        list["style"] = start_node.attributes[k]
                    print("  " * level, "Узел:", start_node.qname[1], " Аттрибуты:(",
                          k[1] + ':' + start_node.attributes[k],
                          ") ", str(start_node), "параметр ", par_detail, " стиль ", list["style"])
            for n in start_node.childNodes:
                self.print_all_document_nodes_with_higher_style_data(n, list, doc, level + 1)
        return