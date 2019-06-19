from nose.tools import assert_raises

from manuscript.tools.castings import as_is, bool_, list_, int_, language
from manuscript.elements.role import Role
from manuscript.elements.work import Work
import manuscript.exceptions as mex
import manuscript.tools.constants as mc


def test___init__():
    assert_raises(TypeError, Role)

    text = "Test"
    work = Work(text)
    assert_raises(mex.MMParameterError, Role, work)

    r = Role(work, name="RNAME")
    print(f"{r.get_params()}")
    assert r.params[0].keys() == {"name"}
    assert r.params[1].keys() == {"pitch", "speed", "desc", "noname",
                                  "lang_like", "audio_like", "text_like",
                                  "paragraph", "left_margin", "right_margin",
                                  "align", "caps", "underline",
                                  "leading_newline", "trailing_newline",
                                  mc.SOUND, mc.DEFINING, "gain", "input",
                                  "audio", "overlay", "reverse", "export",
                                  "start", "end", "remove_start", "remove_end",
                                  mc.VALUES}
    assert r.params[2].keys() == {"alias", "lang"}
    assert (r.params == [
        {"name": (as_is, None)},
        {"pitch": (float, 0.0),
         "speed": (float, 0.0),
         "desc": (str, "No description"),
         "noname": (bool_, False),
         "lang_like": (str, mc.NARRATOR),
         "audio_like": (str, ""),
         "text_like": (str, ""),
         "paragraph": (str, ""),
         "left_margin": (int_, mc.LEFT_MARGIN),
         "right_margin": (int_, mc.RIGHT_MARGIN),
         "align": (str, mc.ALIGN),
         "caps": (bool_, mc.CAPS),
         "underline": (str, mc.UNDERLINE),
         "leading_newline": (bool_, mc.LEADING_NEWLINE),
         "trailing_newline": (bool_, mc.TRAILING_NEWLINE),
         mc.SOUND: (str, ""),
         mc.DEFINING: (bool, True),  # normal bool
         "gain": (float, 1.0),
         "input": (list_, ""),
         "audio": (as_is, mc.NON_DEFINED),
         "overlay": (bool_, False),
         "reverse": (bool_, False),
         "export": (str, ""),
         "start": (int_, 0),
         "end": (int_, -1),
         "remove_start": (int_, -1),
         "remove_end": (int_, 0),
         mc.VALUES: (str, "")},
        {"alias": (str, "name"),
         "lang": (language, "default_lang")}
        ]
    )


if __name__ == "__main__":
    test___init__()
