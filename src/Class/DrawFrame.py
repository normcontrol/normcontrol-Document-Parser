# Draw frame class for ODT document

class DrawFrame:
    def __init__(self, frame_style_name, frame_name, frame_anchor_type, frame_x, frame_y, frame_width, frame_height,
                 frame_rel_width, frame_rel_height, image_href, image_type, image_show, image_actuate):
        self.frame_style_name = frame_style_name
        self.frame_name = frame_name
        self.frame_anchor_type = frame_anchor_type
        self.frame_x = frame_x
        self.frame_y = frame_y
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.frame_rel_width = frame_rel_width
        self.frame_rel_height = frame_rel_height
        self.image_href = image_href
        self.image_type = image_type
        self.image_show = image_show
        self.image_actuate = image_actuate

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