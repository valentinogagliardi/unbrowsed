import pytest

from unbrowsed.matchers import RoleMatcher, TextMatch
from unbrowsed.parser import parse_html


def test_role_matcher_a():
    html = """
    <a>an invalid link</a>
    """
    dom = parse_html(html)
    link = dom.css_first("a")
    assert RoleMatcher.get_implicit_role(link) is None

    html = """
    <a href="/home">a invalid link</a>
    """
    dom = parse_html(html)
    link = dom.css_first("a")
    assert RoleMatcher.get_implicit_role(link) == "link"


def test_role_matcher_input_types():
    html = """
    <input type="checkbox">
    <input type="radio">
    <input type="text">
    <input type="unknown">
    """
    dom = parse_html(html)

    checkbox = dom.css_first('input[type="checkbox"]')
    assert RoleMatcher.get_implicit_role(checkbox) == "checkbox"

    radio = dom.css_first('input[type="radio"]')
    assert RoleMatcher.get_implicit_role(radio) == "radio"

    text_input = dom.css_first('input[type="text"]')
    assert RoleMatcher.get_implicit_role(text_input) == "textbox"

    unknown = dom.css_first('input[type="unknown"]')
    assert not RoleMatcher.get_implicit_role(unknown)


def test_text_match_type_error():

    with pytest.raises(TypeError) as exc:
        TextMatch(123)  # type: ignore
    assert "text must be a string" == str(exc.value)

    with pytest.raises(TypeError) as exc:
        TextMatch(None)
    assert "text must be a string" == str(exc.value)


def test_role_matcher():
    assert not RoleMatcher.get_implicit_role(None)  # type: ignore
