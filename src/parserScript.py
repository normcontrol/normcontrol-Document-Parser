from odf.opendocument import load
from odf.opendocument import OpenDocumentText
from odf.style import Style, TextProperties
from odf import text
from odf.text import H, P, Span

class DocumentParser():
    def __init__(self, file):
        self.filePath = file
        self.fileText = []

    # Получаем весь текст документа
    def all_odt_text(self):
        doc = load(self.filePath)
        for paragraph in doc.getElementsByType(text.P):
            self.fileText.append(paragraph)
            print(paragraph)

    # Получение стилей и информации о тексте
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
        print(styles)

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
    doc.get_styles()