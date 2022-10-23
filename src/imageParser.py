from odf.opendocument import OpenDocumentText, OpenDocumentDrawing, OpenDocumentImage, load
from odf.style import Style
from odf.table import Table
from guppy import hpy
import timing

from src.styles import Auto
from src.styles import Default
from src.styles import Style

class ImageParser():
    def __init__(self, file):
        self.filePath = file
        self.fileText = []

if __name__ == '__main__':
    h = hpy()
    h1 = h.heap()

    doc = ImageParser('listsimages.odt')
    print("-----------------------------------------\n")
    print("Получение стилей image & frame:\n")
    print(Style.get_styles_image(doc))
    print("--------------------1-----------------------\n")
    print(Style.get_styles_image_frame(doc))
    print("--------------------2-----------------------")
    print("Получение конкретных характеристик:")
    print(Style.get_image_param('listsimages.odt', 'image1', 'actuate'))
    print(Style.get_frame_param('listsimages.odt', 'Рисунок_20_13', 'width'))

    h2 = h.heap()
    print(h2)
    print("\nMemory Usage After Creation Of Objects : ", h2.size - h1.size, " bytes")