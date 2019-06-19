from nose.tools import assert_raises

from manuscript.tools.castings import as_is, bool_, list_, int_
from manuscript.elements.wait import Wait
from manuscript.elements.work import Work
import manuscript.exceptions as mex
import manuscript.tools.constants as mc


def test___init__():
    assert_raises(TypeError, Wait)

    text = "Test"
    work = Work(text)
    assert_raises(mex.MMParameterError, Wait, work)

    w = Wait(work, name="WNAME")
    print(f"{w.get_params()}")
    assert (w.params == [
        {"name": (as_is, None)},
        {"delay": (float, 0.3),
         mc.SOUND: (str, ""),
         mc.DEFINING: (bool, True),  # PURE bool!
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
        {}
        ]
    )


if __name__ == "__main__":
    test___init__()
