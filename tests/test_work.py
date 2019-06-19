from manuscript.elements.definition import Definition
import manuscript.tools.constants as mc


class SubDefA(Definition):
    COMMAND = "SUBDEFA"


class SubDefB(Definition):
    COMMAND = "SUBDEFB"

#from tests.subdefinitions import SubDefA, SubDefB
from manuscript.elements.work import Work


def test___init__():
    text = "Manuscript"
    work = Work(text)
    print(f"work.defining_actions={work.defining_actions}")

    # This complicated test is because othere tests may add extra subclasses
    # to defining actions
    assert "SUBDEFA" in work.defining_actions
    assert "SUBDEFB" in work.defining_actions
    assert work.defining_actions["SUBDEFA"] == SubDefA
    assert work.defining_actions["SUBDEFB"] == SubDefB

    assert work.re_definition_allowed == {mc.SETTINGS}
    assert work.defined_actions == {}
    assert work.manuscript_as_mm == text


def test_define_action():
    text = "Manuscript"
    work = Work(text)
    test_action = object()
    work.define_action("Test_action", test_action)
    assert work.defined_actions == {"Test_action": test_action}


if __name__ == "__main__":
    test___init__()
    test_define_action()
