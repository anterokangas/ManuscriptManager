from nose.tools import assert_raises

import manuscript.exceptions as mex

from manuscript.tools.castings import bool_
from manuscript.tools.castings import list_
from manuscript.tools.castings import int_
from manuscript.tools.castings import str_
from manuscript.tools.castings import as_is
from manuscript.tools.castings import language
from manuscript.tools.castings import supported_languages_as_text


def test_bool_():
    assert bool_(False) is False
    assert bool_(True) is True

    assert bool_("False") is False
    assert bool_("FALSE") is False
    assert bool_("FaLsE") is False
    assert bool_("false") is False
    assert bool_("F") is False
    assert bool_("f") is False

    assert bool_("") is False
    assert bool_(" ") is False

    assert bool_("True") is True
    assert bool_("TRUE") is True
    assert bool_("TrUe") is True
    assert bool_("true") is True
    assert bool_("T") is True
    assert bool_("t") is True
    assert bool_("X") is True
    assert bool_("Xyzzy") is True

    assert bool_(0) is False
    assert bool_(1) is False
    assert bool_(100) is False
    assert bool_(-10) is False
    assert bool_([]) is False
    assert bool_([True]) is False
    assert bool_(()) is False
    assert bool_((True,)) is False
    assert bool_({'a': True}) is False
    assert bool_({}) is False
    assert bool_(set()) is False
    assert bool_({True}) is False
    assert bool_(None) is False


def test_list_():
    assert list_("") == []
    assert list_("a b c dfg") == ['a', 'b', 'c', 'dfg']
    assert list_("a 'b c' dfg") == ['a', "'b c'", 'dfg']
    assert list_('a "b c" dfg') == ['a', '"b c"', 'dfg']
    assert list_(' a  "b c" dfg' + " 'h i j' ") == ['a', '"b c"', 'dfg', "'h i j'"]
    assert list_("a b c dfg", tail="TAIL") == ['a', 'b', 'c', 'dfg', 'TAIL']


def test_as_is():
    assert as_is(None) is None
    assert as_is("Xyzzy") == "Xyzzy"


def test_int_():
    assert int_("10") == 10
    assert_raises(mex.MMValueError, int_, "10.5")
    assert_raises(mex.MMValueError, int_, "")
    assert_raises(mex.MMValueError, int_, None)
    assert_raises(mex.MMValueError, int_, "Xyzzy")


def test_str_():
    assert str_("Xyzzy") == "Xyzzy"
    assert str_("") == ""
    assert str_(100) == "100"
    assert str_(list()) == "[]"
    assert str_(None) is None


def test_language():
    assert language('fi') == 'fi'
    assert language('sv') == 'sv'
    assert_raises(mex.MMValueError, language, 'xyz')


def test_supported_languages():
    assert (supported_languages_as_text() ==
            "\nThe supported languages are:"
            "\n     af    : Afrikaans"
            "\n     sq    : Albanian"
            "\n     ar    : Arabic"
            "\n     hy    : Armenian"
            "\n     bn    : Bengali"
            "\n     ca    : Catalan"
            "\n     zh    : Chinese"
            "\n     zh-cn : Chinese (Mandarin/China)"
            "\n     zh-tw : Chinese (Mandarin/Taiwan)"
            "\n     zh-yue: Chinese (Cantonese)"
            "\n     hr    : Croatian"
            "\n     cs    : Czech"
            "\n     da    : Danish"
            "\n     nl    : Dutch"
            "\n     en    : English"
            "\n     en-au : English (Australia)"
            "\n     en-uk : English (United Kingdom)"
            "\n     en-us : English (United States)"
            "\n     eo    : Esperanto"
            "\n     fi    : Finnish"
            "\n     fr    : French"
            "\n     de    : German"
            "\n     el    : Greek"
            "\n     hi    : Hindi"
            "\n     hu    : Hungarian"
            "\n     is    : Icelandic"
            "\n     id    : Indonesian"
            "\n     it    : Italian"
            "\n     ja    : Japanese"
            "\n     ko    : Korean"
            "\n     la    : Latin"
            "\n     lv    : Latvian"
            "\n     mk    : Macedonian"
            "\n     no    : Norwegian"
            "\n     pl    : Polish"
            "\n     pt    : Portuguese"
            "\n     pt-br : Portuguese (Brazil)"
            "\n     ro    : Romanian"
            "\n     ru    : Russian"
            "\n     sr    : Serbian"
            "\n     sk    : Slovak"
            "\n     es    : Spanish"""
            "\n     es-es : Spanish (Spain)"
            "\n     es-us : Spanish (United States)"
            "\n     sw    : Swahili"
            "\n     sv    : Swedish"
            "\n     ta    : Tamil"
            "\n     th    : Thai"
            "\n     tr    : Turkish"
            "\n     vi    : Vietnamese"
            "\n     cy    : Welsh"
    )
