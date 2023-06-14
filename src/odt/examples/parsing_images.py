from src.odt.elements.ODTDocument import ODTDocument
from src.odt.ODTParser import ODTParser

if __name__ == '__main__':
    doc_path = "/Users/vladtereshch/PycharmProjects/normcontrol-Document-Parser/src/odt/documents/listsimages.odt"
    doc = ODTDocument(doc_path)
    odt_parser = ODTParser(doc)

    print("Получение стилей image & frame:\n")
    print(odt_parser.image_parser.get_image_styles(doc))

    print("--------------------1-----------------------\n")
    print(odt_parser.image_parser.get_frame_styles(doc))

    print("--------------------2-----------------------")
    print("Получение конкретных характеристик:")
    print(odt_parser.image_parser.get_image_parameter(doc, 'image1', 'actuate'))
    print(odt_parser.image_parser.get_frame_parameter(doc, 'Рисунок_20_13', 'width'))