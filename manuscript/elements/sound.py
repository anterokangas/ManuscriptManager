from manuscript.elements.definition import Definition

from manuscript.tools.castings import bool_, list_, as_is, int_

import manuscript.tools.constants as mc


class Sound(Definition):

    COMMAND = mc.SOUND
    params = [
        {},
        {mc.SOUND: (str, ""),               # generate SOUND object (SOUND-name)
         mc.DEFINING: (bool, True),        # is the command just defining or not
         "gain": (float, 1.0),
         "input": (list_, ""),              # (sound/filename(s) separated by space)
         "audio": (as_is, mc.NON_DEFINED),  # possible AudioSegment object
         "overlay": (bool_, False),         # multiple sounds/files overlayed or concatenated
         "reverse": (bool_, False),         # reverse siund (once)
         "export": (str, ""),               # save sound
         "start": (int_, 0),
         "end": (int_, -1),
         "remove_start": (int_, -1),
         "remove_end": (int_, 0)},
        {}
    ]

    def __init__(self, work, *args, **kwargs):
        super().__init__(work, *args, **kwargs)
