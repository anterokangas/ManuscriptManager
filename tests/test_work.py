from manuscript.elements.definition import Definition


# Notice: A and B must be defined AFTER import Definition and before import Work
class A(Definition):
    COMMAND = "A"


class B(Definition):
    COMMAND = "B"


from manuscript.elements.work import Work
import manuscript.tools.constants as mc


def test___init__():
    text = "Manuscript"
    work = Work(text)
    assert Work.defining_actions == {"A": A, "B": B}
    assert Work.re_definition_allowed == {mc.SETTINGS}
    assert work.manuscript_as_mm == text


if __name__ == "__main__":
    test___init__()


