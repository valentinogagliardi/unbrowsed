import pytest

from unbrowsed import (
    parse_html,
    get_by_text,
    MultipleElementsFoundError,
    NoElementsFoundError,
)


def test_get_by_text():
    html = """
    <div>Hello World</div>
    <p>Another text</p>
    <span>Third element</span>
    """
    dom = parse_html(html)

    assert get_by_text(dom, "Hello World")

    with pytest.raises(NoElementsFoundError):
        get_by_text(dom, "hello world")

    with pytest.raises(NoElementsFoundError):
        get_by_text(dom, "Hello")


def test_get_by_text_exact():
    html = """
        <div>Hello World</div>
        <p>Another text</p>
        <span>Third element</span>
        """
    dom = parse_html(html)
    assert get_by_text(dom, "ello World", exact=False)


def test_get_by_text_prioritize_child():
    html = """
    <input type="submit" value="Login" /></form><div><p>Invalid email address or password. Please correct and try again.</p></div></div></main>'
    """
    dom = parse_html(html)
    assert (
        get_by_text(
            dom, "Invalid email address or password. Please correct and try again."
        )
        is not None
    )


def test_get_by_text_no_match():
    html = """
    <div>Hello World</div>
    <p>Another text</p>
    """
    dom = parse_html(html)

    with pytest.raises(NoElementsFoundError):
        get_by_text(dom, "Missing Text")


def test_get_by_text_multiple_matches():
    html = """
    <div>Duplicate Text</div>
    <p>Duplicate Text</p>
    """
    dom = parse_html(html)

    with pytest.raises(MultipleElementsFoundError) as excinfo:
        get_by_text(dom, "Duplicate Text")
    assert "Found 2 elements" in str(excinfo.value)
    assert "Duplicate Text" in str(excinfo.value)
    assert "get_all_by_text" in str(excinfo.value)



def test_to_have_attribute():
    html = """
    <button type="submit" class="primary">Submit</button>
    """
    dom = parse_html(html)

    button = get_by_text(dom, "Submit")
    assert button.to_have_attribute("type", "submit")
    assert button.to_have_attribute("class", "primary")
