from guppy import hpy
from src.odt.styles import Style
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

class ImageParser:
    def __init__(self, file):
        self.filePath = file
        self.fileText = []

if __name__ == '__main__':
    h = hpy()
    h1 = h.heap()

    script_path = os.path.abspath(__file__)
    rel_path = "documents/listsimages.odt"
    doc = ImageParser(create_path(script_path, rel_path))
    print("-----------------------------------------\n")
    print("Получение стилей image & frame:\n")
    print(Style.get_styles_image(doc))
    print("--------------------1-----------------------\n")
    print(Style.get_styles_image_frame(doc))
    print("--------------------2-----------------------")
    print("Получение конкретных характеристик:")
    print(Style.get_image_param('/Users/vladtereshch/PycharmProjects/normcontrol-Document-Parser/src/odt/'
                                'documents/listsimages.odt', 'image1', 'actuate'))
    print(Style.get_frame_param('/Users/vladtereshch/PycharmProjects/normcontrol-Document-Parser/src/odt/'
                                'documents/listsimages.odt', 'Рисунок_20_13', 'width'))

    h2 = h.heap()
    print(h2)
    print("\nMemory Usage After Creation Of Objects : ", h2.size - h1.size, " bytes")