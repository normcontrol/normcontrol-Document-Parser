class StyleException(Exception):
    def __init__(self, *args):
        Exception.__init__(self, *args)

class AttributeNotFoundException(Exception):
    pass
