from nose.tools import assert_raises

from manuscript.elements.definition import Definition
from manuscript.elements.work import Work
import manuscript.exceptions as mex
from manuscript.tools.castings import as_is, int_
import manuscript.tools.constants as mc


def test___init__()
    assert_raises(TypeError, Definition)

    text = "Test"
    work = Work(text)
    assert_raises(mex.MMParameterError, Definition, work)

    element = Definition(work, name='NAME')
    assert element.params == [
        {"name": (as_is, None)},
        {mc.VALUES: (str, "")},
        {}
    ]
    assert element.__dict__.get("name", None) == "NAME"
    assert element.__dict__.get(mc.VALUES, None) == ""
    assert work.defined_actions == {"NAME": element}

    assert_raises(mex.MMParameterError, Definition, work, name='NAME', illegal="error")

    class Subdef(Definition):
        COMMAND = "SUBDEF"
        params = [{"X": (as_is, None)}, {'Y': (int_, 0)}, {"Z": (str, "Y")}]

    s = Subdef(work, name="SNAME", X="XXX", Y="10", **{mc.VALUES: "values"})
    assert s.__dict__.get("name", None) == "SNAME"
    assert s.__dict__.get(mc.VALUES, None) == "values"
    assert s.__dict__.get("X", None) == "XXX"
    assert s.__dict__.get("Y", None) == 10
    assert s.__dict__.get("Z", None) == "10"


def test___repr__():
    text = "Test"
    work = Work(text)
    d = Definition(work, name="NAME")
    assert d.__repr__() == "Definition(name='NAME')"

    class X(Definition):
        pass
    x = X(work, name="XNAME")
    assert x.__repr__() == "X(name='XNAME')"


def test_get_params():
    text = "Test"
    work = Work(text)

    class Subdef(Definition):
        COMMAND = "SUBDEF"
        params = [{"X": (as_is, None)}, {'Y': (int_, 0)}, {"Z": (str, "Y")}]

    s = Subdef(work, name="SNAME", X="XXX", Y="10", **{mc.VALUES: "values"})
    print(f"get_params={s.get_params()}")
    assert (s.get_params() ==
        [{"name": (as_is, None), "X": (as_is, None)},
         {mc.VALUES: (str, ""), "Y": (int_, 0)},
         {"Z": (str, "Y")}]
    )


def test_get_params_as_text():
    text = "Test"
    work = Work(text)

    class Subdef(Definition):
        COMMAND = "SUBDEF"
        params = [{"X": (as_is, None)}, {'Y': (int_, 0)}, {"Z": (str, "Y")}]

    s = Subdef(work, name="SNAME", X="XXX", Y="10", **{mc.VALUES: "values"})
    assert (s.get_params_as_text() ==
            "\nPARAMETERS OF ELEMENT: SNAME of class Subdef"
            "\nRequired parameters"
            "\n     X              : XXX"
            "\n     name           : SNAME"
            "\nOptional parameters"
            "\n     Y              : 10"
            "\n     __VALUES__     : values"
            "\nDependent parameters"
            "\n     Z              : 10")


if __name__ == "__main__":
    test___init__()
    test___repr__()
    test_get_params()
    test_get_params_as_text()
