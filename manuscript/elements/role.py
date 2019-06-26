import os
import re

from gtts import gTTS
from pydub import AudioSegment

from manuscript.elements.sound import Sound
import manuscript.exceptions as mex
from manuscript.messages import message_text
from manuscript.tools.audio_tools import speed_change, pitch_change
from manuscript.tools.castings import bool_, int_, language
import manuscript.tools.constants as mc

from manuscript.tools.counter import Counter


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

    def do(self, **kwargs):
        """ Do Role object call

        Makes a temporary copy of the original Rile object
        Overrides parameters given in kwargs
        Creates either audio object or a SOUND object

        Example:
         (A [text] [SOUND B)] [(lang_like AA)] [param])
         - parameters:
           text: the text to be spoken, default=A.alias
           SOUND: create Sound object B with audio=A.speak(text), empty: say
           lang_like: use lang=AA.lang
           _params: Role _params, override A's _params, not allowed lang_like & lang
        - action:
          -- generate audio object
          -- if SOUND given
                create Sound object B (B.audio=A.speak(text)
                otherwise play audio
        Parameters
        ----------
        kwargs : dict
            parameters

        Returns
        -------
            None or audio object
            - None : if creates a *new* SOUND object
            - audio object if not SOUND defined

        """
        """ Do Role object call
        
        Example:
         (A [text] [SOUND B)] [(lang_like AA)] [param])
         - parameters:
           text: the text to be spoken, default=A.alias
           SOUND: create Sound object B with audio=A.speak(text), if empty, an audio object           lang_like: set lang=AA.lang
           _params: Role _params, override A's _params, not allowed lang_like & lang
        - action:
          generate audio object
          if SOUND given
                create Sound object B (B.audio=A.speak(text))
                otherwise play audio (return it)
        """
        # ----------------------------------
        # text to be spoken default is alias
        # ----------------------------------
        text_ = kwargs.pop(mc.VALUES, "")
        if text_ == "":
            text_ = self.alias
            kwargs[mc.VALUES] = text_

        # ----------------------------------
        # override language
        # ----------------------------------
        lang_like = kwargs.pop("lang_like", "")
        lang = kwargs.get("lang", "")
        if lang_like != "" and lang != "":
            raise mex.MMValueError(message_text("self.work, RO8010", (lang_like, lang)))
        if lang_like != "":
            like = self.work.defined_actions.get(lang_like, None)
            if like is None or not isinstance(like, Role):
                raise mm.MMValueError(message_text(self.work, "RO8020", (lang_like,)))
            kwargs["lang"] = like.lang

        me = super().copy(**kwargs)
        the_audio = me.speak(text_)

        #message(self.work, f"Created speak: {self.name} says,", audio)

        sound_name = kwargs.get(mc.SOUND, "")
        if sound_name == "":
            return the_audio

        if self.work.definition_allowed(sound_name):
            Sound.from_audio(self.work, name=sound_name, audio=the_audio, **kwargs)
            return None

        if sound_name in self.work.defined_actions:
            sound_object = self.work.defined_actions[sound_name]
            if sound_object.audio is None:
                sound_object.audio = the_audio
                return None
            raise mex.MMValueError(f"*** {sound_name} already has audio")

        raise mex.MMValueError(message_text(self.work, "RO8030", (sound_name,)))

    @staticmethod
    def say(text_, lang=mc.DEFAULT_LANG):
        if text_ == "":
            audio = None
        else:
            tts = gTTS(text=text_, lang=lang)
            prefix = "tmp"
            with Counter(prefix) as counter:
                tmp_file = prefix + f"_{counter:010d}.mp3"
                tts.save(tmp_file)
                audio = AudioSegment.from_mp3(tmp_file)
                os.remove(tmp_file)
        return audio

    def speak(self, text_):
        """ Convert text to AudioSegment (sound) object"""
        # If the line contains only following special chars, it is considered empty
        if re.sub('[(){}<> .!?,;]', '', text_) == "":
            # Nothing to say!
            return None
        sound = Role.say(text_, lang=self.lang)
        sound = speed_change(sound, self.speed)
        sound = pitch_change(sound, self.pitch)
        sound = sound + self.gain
        return sound
