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
    # This complicated test is because othere tests may add extra subclasses
    # to defining actions
    assert "SUBDEFA" in work.defining_actions
    assert "SUBDEFB" in work.defining_actions
    assert work.defining_actions["SUBDEFA"] == SubDefA
    assert work.defining_actions["SUBDEFB"] == SubDefB

    assert work.re_definition_allowed == {mc.SETTINGS}
    print(f"work.defined_actions={work.defined_actions}")
    assert work.defined_actions == {mc.SETTINGS: work.settings,
                                    mc.NARRATOR: work.narrator}
    assert work.manuscript_as_mm == text


def test_define_action():
    text = "Manuscript"
    work = Work(text)
    test_action = object()
    work.define_action("Test_action", test_action)
    assert work.defined_actions == {mc.SETTINGS: work.settings, "Test_action": test_action}


if __name__ == "__main__":
    test___init__()
    test_define_action()
