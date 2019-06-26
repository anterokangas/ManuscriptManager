from manuscript.elements.definition import Definition
import manuscript.exceptions as mex

from manuscript.tools.castings import bool_, list_, as_is, int_

import manuscript.tools.constants as mc
from manuscript.tools.audio_tools import reverse_audio


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

    @classmethod
    def from_audio(cls, work, **kwargs):
        """ Create a Sound object from audio segment

        (SOUND X (input Y)) -> 1. sleeping SOUND-object X with input, 2. X.audio=Y.audio
        Parameters
        ----------
        work :      Work object
            Current work, contains settings, and defining and defined actions
        kwargs :    dict
            parameters, must contain 'audio'

        Returns
        -------
        Sound object
        """
        # Accept only those kwargs that are also Sound attributes
        name = kwargs.pop("_name", None)
        if name is None:
            raise mex.MMParameterError(f"*** Trying to create Sound.from_audio by name {name}")

        audio = kwargs.pop("audio", None)
        if audio is None:
            raise mex.MMParameterError(f"*** ParameterError: Trying to create Sound.from_audio without audio")

        # Illegal names not allowed
        if not work.definition_allowed(name):
            raise mex.MMParameterError(f"*** Trying to create Sound.from audio by illegal name '{name}'")

        # Defined name allowed only if Sound without audio
        if name in work.defined_actions:
            raise mex.MMParameterError(f"*** Trying to Create Sound.from_audio by already defined name '{name}'")

        # Create Sound-object wit audio and define it
        kwargs[mc.DEFINING] = False     # Allow audio
        kwargs[mc.SOUND] = ""           # Create Sound-object with audio only once
        object_ = cls(work, name=name, audio=audio, **kwargs)
        work.define_action(name, object_)
        return object_


    def do(self, **kwargs):
        """
        Do Sound object call
        (X Y Z (input U V)) -> play X+Y+Z+U+V
        (X Y Z (input U V) (SOUND W)) -> create W=X+Y+Z+U+V
        if audio is not None --> process a copy
        else generate audio from input/values and process
        if SOUND --> create new SOUND-object

        Play, process or combine Sound object(s)

        Parameters
        ----------
        kwargs : dict
            Parameters
        Returns
        -------
        """
        if self.audio is None:
            # audio is generated only once
            me = self

            # combine sound-inputs: first from its definition (name + original input)
            # second the new parameters (values + new input)
            input_ = list_(self._name
                           + " ".join(self.input)
                           + " " + kwargs.get(mc.VALUES, "")
                           + " " + kwargs.get("input", ""))
            sounds = [Sound.get_audio(me.work, sf) for sf in input_]

            # sounds are either overlayed or joined
            me.combine_audios(sounds, **kwargs)
        else:
            me = self.copy(**kwargs)

        me.process_audio()

        # Is result new Sound-object or just audio
        sound_name = kwargs.get(mc.SOUND, "")
        if sound_name == "":
            return me.audio

        # Create Sound-onbject with audio
        kwargs[mc.DEFINING] = False
        Sound.from_audio(me.work, name=sound_name, audio=me.audio, **kwargs)
        return None

    def process_audio(self):
        """ Execute sound objects parameters to audio """
        if self.audio is None:
            return
        if self.audio == mc.NON_DEFINED:
            return
        if self.reverse:
            self.audio = reverse_audio(self.audio)
            self.reverse = False
