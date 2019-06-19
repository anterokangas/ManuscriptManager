from manuscript.elements.sound import Sound

from manuscript.tools.castings import bool_, int_, language

import manuscript.tools.constants as mc


class Role(Sound):

    COMMAND = mc.ROLE

    params = [
        {},
        {"pitch": (float, 0.0),
         "speed": (float, 0.0),
         "desc": (str, "No description"), # description
         "noname": (bool_, False),        # name is never spoken
         "lang_like": (str, mc.NARRATOR), # speak as 'like' except lang, default text == alias
         "audio_like": (str, ""),
         "text_like": (str, ""),
         "paragraph": (str, ""),          # paragraph format
         "left_margin": (int_, mc.LEFT_MARGIN),
         "right_margin": (int_, mc.RIGHT_MARGIN),
         "align": (str, mc.ALIGN),
         "caps": (bool_, mc.CAPS),
         "underline": (str, mc.UNDERLINE),
         "leading_newline": (bool_, mc.LEADING_NEWLINE),
         "trailing_newline": (bool_, mc.TRAILING_NEWLINE)},
        {"alias": (str, "name"),          # default value == dependent on
         "lang": (language, "default_lang")}   # look first self, then settings
    ]

    def __init__(self, work, *args, **kwargs):
        super().__init__(work, *args, **kwargs)