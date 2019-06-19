from manuscript.elements.definition import Definition
import manuscript.tools.constants as mc

from tests.subdefinitions import SubDefA, SubDefB
from manuscript.elements.work import Work


def test___init__():
    text = "Manuscript"
    work = Work(text)
    assert work.defining_actions == {"SUBDEFA": SubDefA, "SUBDEFB": SubDefB}
    assert work.re_definition_allowed == {mc.SETTINGS}
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
