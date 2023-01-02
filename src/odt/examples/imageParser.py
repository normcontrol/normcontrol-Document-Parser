from guppy import hpy

from src.odt.styles import Style


class ImageParser():
    def __init__(self, file):
        self.filePath = file
        self.fileText = []

if __name__ == '__main__':
    h = hpy()
    h1 = h.heap()

    doc = ImageParser('/Users/vladtereshch/PycharmProjects/normcontrol-Document-Parser/src/odt/documents/listsimages.odt')
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