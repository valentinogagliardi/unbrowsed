import pytest

from unbrowsed.matchers import TextMatch


def test_text_match_type_error():

    with pytest.raises(TypeError) as exc:
        TextMatch(123)  # type: ignore
    assert "text must be a string" == str(exc.value)

    with pytest.raises(TypeError) as exc:
        TextMatch(None)
    assert "text must be a string" == str(exc.value)
