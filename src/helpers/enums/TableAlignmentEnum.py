from typing import Optional


class __TableAlignmentEnum(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self['left'] = 'left'
        self['right'] = 'right'
        self['center'] = 'center'
        self['justify'] = 'justify'
        self['distribute'] = 'distribute'
        self['justify-med'] = 'justify-med'
        self['justify-hi'] = 'justify-hi'
        self['justify-low'] = 'justify-low'
        self['thai-justify'] = 'thai-justify'

    def __getitem__(self, key: Optional[str]):
        if key is None:
            key = 'left'
        return dict.__getitem__(self, key.lower())

    def __getattr__(self, attr: Optional[str]):
        if attr is None:
            attr = 'left'
        return self[attr.lower()]


TableAlignmentEnum = __TableAlignmentEnum()
