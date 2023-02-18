class Line:
    def __init__(self,x0,y0,x1,y1,text,fontname,size,nochangeFontName,nochangeSize,page,chars):
        self.x0 = x0
        self.x1 = x1
        self.y0 = y0
        self.y1 = y1
        self.text = text
        self.fontname = fontname
        self.size = size
        self.nochangeFontName = nochangeFontName
        self.nochangeSize = nochangeSize
        self.page = page
        self.chars = chars