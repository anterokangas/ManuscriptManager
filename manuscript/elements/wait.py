from manuscript.elements.sound import Sound
import manuscript.tools.constants as mc


class Wait(Sound):

    COMMAND = mc.WAIT
    params = [{},
              {"delay": (float, 0.3)},
              {}]

    def __init__(self, work, *args, **kwargs):
        super().__init__(work, *args, **kwargs)