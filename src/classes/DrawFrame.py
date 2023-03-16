class DrawFrame:
    """
    Description: Draw frame class for ODT document.

    Parameters:
        _frame_style_name - attribute specifies the style of current frame,
        _frame_name - attribute specifies the name of current frame,
        _frame_anchor_type - attribute specifies how a frame is bound to a text document,
        _frame_x - attribute specifies the position of the frame on the X axis,
        _frame_y - attribute specifies the position of the frame on the Y axis,
        _frame_width - attribute specifies the width of the frame,
        _frame_height - attribute specifies the height of the frame,
        _frame_rel_width - attribute specifies height of a drawing object as a relative value within a frame,
        _frame_rel_height - attribute specifies the width of a drawing object as a relative value within a frame,
        _image_href - attribute specifies the location of an embedded object,
        _image_type - attribute always has the value simple in OpenDocument document instances,
        _image_show - attribute is used to communicate the desired presentation of the ending resource on traversal
            from the starting resource,
        _image_actuate - attribute is used to communicate the desired timing of traversal from the starting resource
            to the ending resource.
    """

    def __init__(self, frame_style_name: str, frame_name: str, frame_anchor_type: str, frame_x: float, frame_y: float,
                 frame_width: float, frame_height: float, frame_rel_width: str, frame_rel_height: str, image_href: str,
                 image_type: str, image_show: str, image_actuate: str):
        self._frame_style_name = frame_style_name
        self._frame_name = frame_name
        self._frame_anchor_type = frame_anchor_type
        self._frame_x = frame_x
        self._frame_y = frame_y
        self._frame_width = frame_width
        self._frame_height = frame_height
        self._frame_rel_width = frame_rel_width
        self._frame_rel_height = frame_rel_height
        self._image_href = image_href
        self._image_type = image_type
        self._image_show = image_show
        self._image_actuate = image_actuate

    @property
    def frame_style_name(self):
        return self._frame_style_name

    @frame_style_name.setter
    def frame_style_name(self, value):
        self._frame_style_name = value

    @property
    def frame_name(self):
        return self._frame_name

    @frame_name.setter
    def frame_name(self, value):
        self._frame_name = value

    @property
    def frame_anchor_type(self):
        return self._frame_anchor_type

    @frame_anchor_type.setter
    def frame_anchor_type(self, value):
        self._frame_anchor_type = value

    @property
    def frame_x(self):
        return self._frame_x

    @frame_x.setter
    def frame_x(self, value):
        self._frame_x = value

    @property
    def frame_y(self):
        return self._frame_y

    @frame_y.setter
    def frame_y(self, value):
        self._frame_y = value

    @property
    def frame_width(self):
        return self._frame_width

    @frame_width.setter
    def frame_width(self, value):
        self._frame_width = value

    @property
    def frame_height(self):
        return self._frame_height

    @frame_height.setter
    def frame_height(self, value):
        self._frame_height = value

    @property
    def frame_rel_width(self):
        return self._frame_rel_width

    @frame_rel_width.setter
    def frame_rel_width(self, value):
        self._frame_rel_width = value

    @property
    def frame_rel_height(self):
        return self._frame_rel_height

    @frame_rel_height.setter
    def frame_rel_height(self, value):
        self._frame_rel_height = value

    @property
    def image_href(self):
        return self._image_href

    @image_href.setter
    def image_href(self, value):
        self._image_href = value

    @property
    def image_type(self):
        return self._image_type

    @image_type.setter
    def image_type(self, value):
        self._image_type = value

    @property
    def image_show(self):
        return self._image_show

    @image_show.setter
    def image_show(self, value):
        self._image_show = value

    @property
    def image_actuate(self):
        return self._image_actuate

    @image_actuate.setter
    def image_actuate(self, value):
        self._image_actuate = value