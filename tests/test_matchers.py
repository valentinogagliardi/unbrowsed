import pytest

from unbrowsed.matchers import RoleMatcher, TextMatch
from selectolax.lexbor import LexborHTMLParser as Parser


def test_role_matcher_input_types():
    html = """
    <input type="checkbox">
    <input type="radio">
    <input type="text">
    <input type="unknown">
    """
    dom = Parser(html)

    checkbox = dom.css_first('input[type="checkbox"]')
    assert RoleMatcher.get_implicit_role(checkbox) == "checkbox"

    radio = dom.css_first('input[type="radio"]')
    assert RoleMatcher.get_implicit_role(radio) == "radio"

    text_input = dom.css_first('input[type="text"]')
    assert RoleMatcher.get_implicit_role(text_input) == "textbox"

    unknown = dom.css_first('input[type="unknown"]')
    assert not RoleMatcher.get_implicit_role(unknown)


def test_text_match_type_error():

    with pytest.raises(TypeError) as excinfo:
        TextMatch(123)  # type: ignore
    assert "text must be a string" in str(excinfo.value)

    with pytest.raises(TypeError) as excinfo:
        TextMatch(None)
    assert "text must be a string" in str(excinfo.value)


def test_text_match_eq_not_implemented():

    text_match = TextMatch("test")

    result = text_match.__eq__(123)
    assert result is NotImplemented

    result = text_match.__eq__(None)
    assert result is NotImplemented

    result = text_match.__eq__([])
    assert result is NotImplemented

    assert text_match == "test"
    assert text_match != "other"

    text_match_non_exact = TextMatch("test", exact=False)
    assert text_match_non_exact == "This is a test string"
    assert text_match_non_exact != "other"
