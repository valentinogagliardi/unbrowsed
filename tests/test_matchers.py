import pytest
from unbrowsed.matchers import TextMatch


def test_text_match_exact_match():
    matcher = TextMatch("the string")
    assert matcher == "the string"
    assert matcher != "The String"
    assert matcher != "the string with more text"


def test_text_match_non_string_comparison():
    matcher = TextMatch("the string")
    result = matcher.__eq__(123)
    assert result is NotImplemented

    result = matcher.__eq__(None)
    assert result is NotImplemented

    result = matcher.__eq__(["the string"])
    assert result is NotImplemented


def test_invariant():
    with pytest.raises(TypeError):
        TextMatch(4)  # type: ignore
