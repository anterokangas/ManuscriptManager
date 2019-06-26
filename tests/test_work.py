from manuscript.elements.definition import Definition
# from manuscript.elements.role import Role
import manuscript.tools.constants as mc
from manuscript.tools.audio_tools import play_audio


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
    assert work.defined_actions == {mc.SETTINGS: work.settings,
                                    mc.NARRATOR: work.narrator,
                                    mc.BREAK: work.break_,
                                    "title": work.paragraphs[0],
                                    "title_line": work.paragraphs[1],
                                    "synopsis": work.paragraphs[2],
                                    "header": work.paragraphs[3],
                                    "parenthesis": work.paragraphs[4],
                                    "name": work.paragraphs[5],
                                    "reply": work.paragraphs[6]}
    assert work.manuscript_as_mm == text
    assert work.defaults == {
        'lang': 'en',
        'pitch': 0.0,
        'speed': 0.0,
        'gain': 1.0,
    }
    print(f"work.paragraphs={work.paragraphs}")
    #paragraph_names = {paragraph.name for paragraph in work.paragraphs}
    #paragraph_types = {type(paragraph) for paragraph in work.paragraphs}
    #assert paragraph_names == {"title", "title_line", "synopsis", "header", "parenthesis", "name", "reply"}
    # assert paragraph_types == {type(work.narrator)}
    assert len(work.audio) == 1200
    play_audio(work.audio)


def test_define_action():
    text = "Manuscript"
    work = Work(text)
    test_action = object()
    work.define_action("Test_action", test_action)
    print(f"={work.defined_actions}")
    assert work.defined_actions == {mc.SETTINGS: work.settings,
                                    mc.NARRATOR: work.narrator,
                                    mc.BREAK: work.break_,
                                    "title": work.paragraphs[0],
                                    "title_line": work.paragraphs[1],
                                    "synopsis": work.paragraphs[2],
                                    "header": work.paragraphs[3],
                                    "parenthesis": work.paragraphs[4],
                                    "name": work.paragraphs[5],
                                    "reply": work.paragraphs[6],
                                    "Test_action": test_action}

def test___init__2():
    text = """
    (*(NARRATOR Test begins and I am speaking English. 
      (lang en))*)
    (SETTINGS SETTINGS
        (default_lang fi))
    
    No nyt minä her-ke-sin puhumaan suomea.
    (A)
    (ROLE A (alias Herra Aa))
    (*(A Hei, minä olen)(A)*)
    Se oli siis herra Aa
    
    """
    work = Work(text)
    play_audio(work.audio)


if __name__ == "__main__":
    test___init__()
    test_define_action()
    test___init__2()
