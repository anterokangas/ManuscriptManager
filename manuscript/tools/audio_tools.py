"""
Interface to audio (AudioSegment) and how to play it

"""
import os
import time
import playsound

import manuscript.tools.constants as mc
from manuscript.tools.counter import Counter


def append(the_audio, sound):
    """ the_audio += asound, None==empty """
    print(f"the_audio={type(the_audio)} sound={type(sound)}")
    if sound is None:
        return the_audio
    if sound == mc.NON_DEFINED:
        return the_audio
    if the_audio is None:
        return sound
    if the_audio == mc.NON_DEFINED:
        return sound
    return the_audio + sound


def join(sounds, **kwargs):
    """ Join list of sounds to one audio """
    the_audio = None
    for sound in sounds:
        if sound is None:
            return None
        the_audio = append(the_audio, sound)
    return the_audio


def overlay(sounds, **kwargs):
    """ Overlay lst of sounds to one audio """
    if sounds is None or sounds == mc.NON_DEFINED or len(sounds) == 0:
        return mc.NON_DEFINED
    sounds.sort(reverse=True,
                key=lambda x: len(x) if x is not None else 0)
    the_audio = sounds[0]
    for sound in sounds[1:]:
        if sound is None or sound == mc.NON_DEFINED:
            return mc.NON_DEFINED
        the_audio = the_audio.overlay(sound)
    return the_audio


def speed_change(sound, speed=0.0):
    """ Change speed of audio

    Parameters
    ----------
    sound : AudioSegment object
    speed : int
        new speed

    Returns
    -------
    AudioSegment object with altered frame rate
    """
    # Manually override the frame_rate. This tells the computer how many
    # samples to play per second
    speed = 1.0 + speed / 10  # Tune speed value easier to use
    sound_with_altered_frame_rate = \
        sound._spawn(sound.raw_data,
                     overrides={"frame_rate": int(sound.frame_rate * speed)})
    # convert the sound with altered frame rate to a standard frame rate
    # so that regular playback programs will work right. They often only
    # know how to play audio at standard frame rate (like 44.1k)
    return sound_with_altered_frame_rate.set_frame_rate(sound.frame_rate)


def pitch_change(sound, pitch=0.0):
    """ Change pitch of audio

    Parameters
    ----------
    sound :
    pitch : int
        new pitch

    Returns
    -------
    AudioSegment object with altered pitch
    """
    pitch /= 10  # Tune pitch value easier to use
    new_sample_rate = int(sound.frame_rate * (2.0 ** pitch))
    sound_with_altered_pitch = \
        sound._spawn(sound.raw_data,
                     overrides={'frame_rate': new_sample_rate})
    return sound_with_altered_pitch

def play_audio(sound, block=True):
    """ Plays audio """
    if sound is not None:
        prefix = "tmp"
        with Counter(prefix) as counter:
            tmp_file = os.path.join(".", prefix + f"_{counter:010d}.mp3")
            sound.export(tmp_file)
            playsound.playsound(tmp_file, block=block)
            time.sleep(len(sound) / 1000.)
            os.remove(tmp_file)

def reverse_audio(audio_):
    """ Reverses audio """
    print(f"reverse_audio: audio_={audio_}")
    if audio_ is None or audio_ == mc.NON_DEFINED:
        return mc.NON_DEFINED
    else:
        return audio_.reverse()
