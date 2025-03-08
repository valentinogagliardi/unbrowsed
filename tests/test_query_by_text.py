import pytest

from unbrowsed import parse_html, query_by_text, MultipleElementsFoundError


def test_query_by_text():
    html = """
    <div>Hello World</div>
    <p>Another text</p>
    <span>Third element</span>
    """
    dom = parse_html(html)

    assert query_by_text(dom, "Hello World")
    assert not query_by_text(dom, "Hello")


def test_query_by_text_exact_match():
    html = """
    <div>Hello World</div>
    <p>Another text</p>
    <span>Third element</span>
    """
    dom = parse_html(html)

    assert query_by_text(dom, "Hello Worl", exact=False)
    assert not query_by_text(dom, "Hello")


def test_query_by_text_prioritize_child():
    html = """
    <input type="submit" value="Login" /></form><div><p>Invalid email address or password. Please correct and try again.</p></div></div></main>'
    """
    dom = parse_html(html)
    assert (
        query_by_text(
            dom, "Invalid email address or password. Please correct and try again."
        )
        is not None
    )


def test_query_by_text_no_match():
    html = """
    <div>Hello World</div>
    <p>Another text</p>
    """
    dom = parse_html(html)

    assert query_by_text(dom, "Missing Text") is None


def test_query_by_text_multiple_matches():
    html = """
    <div>Duplicate Text</div>
    <p>Duplicate Text</p>
    """
    dom = parse_html(html)

    with pytest.raises(MultipleElementsFoundError) as excinfo:
        query_by_text(dom, "Duplicate Text")

    assert "Found 2 elements" in str(excinfo.value)
    assert "Duplicate Text" in str(excinfo.value)
    assert "query_all_by_text" in str(excinfo.value)
