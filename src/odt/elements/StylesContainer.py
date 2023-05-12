from src.classes.Paragraph import Paragraph
from src.odt.ODTParser import ODTParser
from src.odt.elements.ODTDocument import ODTDocument
from src.helpers.odt import consts


class StylesContainer:
    def __init__(self, doc: ODTDocument):
        odt_parser = ODTParser()
        self._all_automatic_styles = odt_parser.automatic_style_parser.automatic_style_dict(doc, consts.DEFAULT_PARAM)
        self._all_default_styles = odt_parser.default_style_parser.default_style_dict(doc, consts.DEFAULT_PARAM)
        self._all_regular_styles = odt_parser.regular_style_parser.regular_style_dict(doc, consts.DEFAULT_PARAM)

    @property
    def all_automatic_styles(self):
        return self._all_automatic_styles

    @all_automatic_styles.setter
    def all_automatic_styles(self, value):
        self._all_automatic_styles = value

    @property
    def all_default_styles(self):
        return self._all_default_styles

    @all_default_styles.setter
    def all_default_styles(self, value):
        self._all_default_styles = value

    @property
    def all_regular_styles(self):
        return self._all_regular_styles

    @all_regular_styles.setter
    def all_regular_styles(self, value):
        self._all_regular_styles = value

    def build_dict(self):
        self._all_default_styles = self.default_inher()
        self._all_regular_styles = self.styles_inher()
        self.all_automatic_styles = self.auto_inher()

    def styles_inher(self):
        while True:
            flag = 0
            for k in self._all_regular_styles.keys():
                if self._all_regular_styles[k] is not None:
                    if "parent-style-name" in self._all_regular_styles[k].keys():
                        parent = self._all_regular_styles[k]["parent-style-name"]
                        att = self._all_regular_styles[parent]
                    else:
                        if self._all_regular_styles[k]["family"] in self.all_default_styles.keys():
                            parent = self._all_regular_styles[k]["family"]
                            att = self.all_default_styles[parent]
                        else:
                            att = consts.DEFAULT_PARAM
                    for kk in self._all_regular_styles[k].keys():
                        if self._all_regular_styles[k][kk] is None:
                            print(self._all_regular_styles[k][kk])
                            if att[kk] is None:
                                flag = 1
                            else:
                                self._all_regular_styles[k][kk] = att[kk]
                            print(self._all_regular_styles[k][kk])

            if flag == 0:
                break
        return self._all_regular_styles

    def default_inher(self):
        for k in self._all_default_styles.keys():
            for kk in self._all_default_styles[k].keys():
                if self._all_default_styles[k][kk] is None:
                    print(self._all_default_styles[k][kk])
                    self._all_default_styles[k][kk] = consts.DEFAULT_PARAM[kk]
                    print(self._all_default_styles[k][kk])
        return self._all_default_styles

    def auto_inher(self):
        for k in self.all_automatic_styles.keys():
            for kk in self.all_automatic_styles[k].keys():
                if self.all_automatic_styles[k][kk] is None:
                    if "parent-style-name" in self.all_automatic_styles[k].keys():
                        parent = self.all_automatic_styles[k]["parent-style-name"]
                        att = self._all_regular_styles[parent][kk]
                    else:
                        att = consts.DEFAULT_PARAM[kk]
                    print(self.all_automatic_styles[k][kk])
                    self.all_automatic_styles[k][kk] = att
                    print(self.all_automatic_styles[k][kk])
        return self.all_automatic_styles

    def inher_start6(self, stylename):
        if stylename in self._all_automatic_styles:
            return self._all_automatic_styles[stylename]
        else:
            return self._all_regular_styles[stylename]

    def get_nodes_with_style_full6(self, start_node, parent_node, list=None, level=0):
        if list is None:
            list = {}
        if start_node.nodeType == 1:
            if start_node.qname[1] == "list":
                for k in start_node.attributes.keys():
                    if (k[1] == "style-name"):
                        att = self.inher_start6(start_node.attributes[k])
                        for kk in att.keys():
                            if kk in consts.DEFAULT_PARAM.keys():
                                if att[kk] is consts.DEFAULT_PARAM[kk]:
                                    att[kk] = parent_node[kk]
                        att["text"] = str(start_node)
                        parent_node = att
                        list[start_node.attributes[k]] = self.get_nodes_with_style_full_list(start_node, parent_node,
                                                                                             {})
                        print(list)
                        print("  " * level, "Список:", start_node.qname[1], " Аттрибуты:(",
                              k[1] + ':' + start_node.attributes[k],
                              ") ", str(start_node), "параметр ", att["text-align"])
            else:
                if start_node.qname[1] == "p":
                    for k in start_node.attributes.keys():
                        if (k[1] == "style-name"):
                            att = self.inher_start6(start_node.attributes[k])
                            for kk in att.keys():
                                if kk in consts.DEFAULT_PARAM.keys():
                                    if att[kk] is consts.DEFAULT_PARAM[kk]:
                                        att[kk] = parent_node[kk]
                            att["text"] = str(start_node)
                            parent_node = att
                            par = Paragraph(_text=str(start_node), _font_name=att["font-name"],
                                            _text_size=att["font-size"])
                            if att["font-weight"] != "bold":
                                par.bold = False
                            else:
                                par.bold = True
                            print("  " * level, "Узел:", start_node.qname[1], " Аттрибуты:(",
                                  k[1] + ':' + start_node.attributes[k],
                                  ") ", str(start_node), "параметр ", att["text-align"])
                else:
                    for k in start_node.attributes.keys():
                        if (k[1] == "style-name"):
                            att = self.inher_start6(start_node.attributes[k])
                            for kk in att.keys():
                                if kk in consts.DEFAULT_PARAM.keys():
                                    if att[kk] is consts.DEFAULT_PARAM[kk]:
                                        att[kk] = parent_node[kk]
                            att["text"] = str(start_node)
                            parent_node = att
                            print("  " * level, "Узел:", start_node.qname[1], " Аттрибуты:(",
                                  k[1] + ':' + start_node.attributes[k],
                                  ") ", str(start_node), "параметр ", att["text-align"])
                    for n in start_node.childNodes:
                        self.get_nodes_with_style_full6(n, parent_node, list, level + 1)
        return

    def get_nodes_with_style_full_list(self, start_node, parent_node, list=None, level=0):
        if list is None:
            list = {}
        if start_node.nodeType == 1:
            for k in start_node.attributes.keys():
                if (k[1] == "style-name"):
                    att = self.inher_start6(start_node.attributes[k])
                    for kk in att.keys():
                        if kk in consts.DEFAULT_PARAM.keys():
                            if att[kk] is consts.DEFAULT_PARAM[kk]:
                                att[kk] = parent_node[kk]
                    att["text"] = str(start_node)
                    parent_node = att
                    list[start_node.attributes[k]] = att
            for n in start_node.childNodes:
                self.get_nodes_with_style_full_list(n, parent_node, list, level + 1)
        return list

    def get_nodes_with_style_full7(self, start_node, parent_node, level=0, list=None):
        if list is None:
            list = {}
        if start_node.nodeType == 1:
            for k in start_node.attributes.keys():
                if (k[1] == "style-name"):
                    att = self.inher_start6(start_node.attributes[k])
                    for kk in att.keys():
                        if kk in consts.DEFAULT_PARAM.keys():
                            if att[kk] is consts.DEFAULT_PARAM[kk]:
                                att[kk] = parent_node[kk]
                    list["text"] = str(start_node)
                    parent_node = att
                    list["data"] = att
                    print("  " * level, "Узел:", start_node.qname[1], " Аттрибуты:(",
                          k[1] + ':' + start_node.attributes[k],
                          ") ", str(start_node), "параметр ", att)
            for n in range(0, len(start_node.childNodes)):
                print(n)
                list1 = {}
                list1["nodes"] = self.get_nodes_with_style_full7(start_node.childNodes[n], parent_node, level + 1)
                if len(list1["nodes"]) > 0:
                    list1["type"] = start_node.qname[1]
                    list[str(n)] = list1
        return list
