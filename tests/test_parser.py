from nose.tools import assert_raises

from manuscript.elements.role import Role
from manuscript.elements.sound import Sound
from manuscript.elements.work import Work
import manuscript.exceptions as mex
from manuscript.mmlanguage.lexer import ManuscriptLexer
from manuscript.mmlanguage.parser import ManuscriptParser
import manuscript.tools.constants as mc


work = Work("X")
lexer = ManuscriptLexer()
parser = ManuscriptParser(work)


def test_commands():
    # text = """Role A"""
    # pp = parser.parse(lexer.tokenize(text))
    # assert pp[0][0] == mc.NARRATOR
    # assert isinstance(pp[0][1], Role)
    # assert pp[0][2] == {mc.VALUES: 'Role A'}
    #
    # text = """(ROLE AA) """
    # pp = parser.parse(lexer.tokenize(text))
    # assert pp[0][0] == "ROLE"
    # assert isinstance(pp[0][1], Role)
    # assert pp[0][2] == {"name": "AA"}
    #
    # text = """(ROLE B (lang fi))"""
    # pp = parser.parse(lexer.tokenize(text))
    # assert pp[0][0] == "ROLE"
    # assert isinstance(pp[0][1], Role)
    # assert pp[0][2] == {"name": "B", "lang": "fi"}
    #
    # text = """(ROLE A B (alias 1 2 "xy z" (# string continues! #) 'a b c'))"""
    # pp = parser.parse(lexer.tokenize(text))
    # assert pp[0][0] == "ROLE"
    # assert isinstance(pp[0][1], Role)
    # assert pp[0][2] == {"name": "A B", "alias": '1 2 "xy z" \'a b c\''}
    #
    # text = """(A (param1 1))"""
    # with assert_raises(mex.MMParameterError):
    #     parser.parse(lexer.tokenize(text))
    #
    # text = """(A)"""
    # pp = parser.parse(lexer.tokenize(text))
    # assert pp[0][0].startswith("#tmp")
    # assert isinstance(pp[0][1], Sound)
    # assert pp[0][2] == {}
    #
    # text = """(A (gain 10))"""
    # pp = parser.parse(lexer.tokenize(text))
    # assert pp[0][0].startswith("#tmp")
    # assert isinstance(pp[0][1], Sound)
    # assert pp[0][2] == {}  # TODO: CK should this be {'gain': 10} ?

    text = """
        (SETTINGS SETTINGS 
            (default_lang sv)
            (print_manuscript_parsed False)
        )
        (ROLE BBB)
        (BBB Moi)
    """
    pp = parser.parse(lexer.tokenize(text))
    print(f"\nParsed manuscript")
    for p in pp:
        print(p)
    print(f"\nwork.settings:")
    for key, val in work.settings.__dict__.items():
        print(f"{key}: {val}")


if __name__ == "__main__":
    test_commands()
