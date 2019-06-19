

from manuscript.elements.definition import Definition
from manuscript.elements.work import Work
import manuscript.tools.constants as mc


def test___init__():

    element = Definition(work, name='NAME')
    print(f"element.params={element.params}")
    print(f"work.defined_actions={work.defined_actions}")
    # assert element.params == [
    #     {"name": "NAME"},
    #     {mc.VALUES: ""},
    #     {}
    # ]
    # assert work.defined_actions == {"NAME": element}

def test__repr__():
    text = "Test"
    work = Work(text)
    d = Definition(work, name="NAME")
    assert d.__repr__() == "Definition(name='NAME')"

    class X(Definition):
        pass
    x = X(work, name="XNAME")
    assert x.__repr__() == "X(name='XNAME')"


if __name__ == "__main__":
    test___init__()
