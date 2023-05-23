class NotAllowedFormatFileException(Exception):
    def __init__(self, file_name):
        self.file_name = file_name

    def __str__(self):
        return f'Format of file {self.file_name} is not supported'


class DocumentEmptyContentException(Exception):
    def __str__(self):
        return f'Content in UnifiedDocumentView object is empty, please fill them'


class EmptyPathException(Exception):
    def __str__(self):
        return f'Path to file in PDFParser initialization is empty'
