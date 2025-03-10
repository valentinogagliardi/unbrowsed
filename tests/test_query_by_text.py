import pytest

from unbrowsed import MultipleElementsFoundError, parse_html, query_by_text


def test_query_by_text():
    html = """
    <div>Hello World</div>
    <p>Another text</p>
    <span>Third element</span>
    """
    dom = parse_html(html)

    assert query_by_text(dom, "Hello World")
    assert not query_by_text(dom, "Hello")

    html = """
        <div>
            <h1>Welcome to my site</h1>
            <p>This is a paragraph</p>
            <button>Click me</button>
        </div>
        """
    dom = parse_html(html)

    assert query_by_text(dom, "Welcome", exact=False)


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
    <input type="submit" value="Login" /></form>
    <div><p>Invalid email address or password.</p></div>'
    """
    dom = parse_html(html)
    assert query_by_text(dom, "Invalid email address or password.") is not None


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

    with pytest.raises(MultipleElementsFoundError) as exc:
        query_by_text(dom, "Duplicate Text")

    assert (
        "Found 2 elements with text 'Duplicate Text'. "
        "Use query_all_by_text if multiple matches are expected."
        == str(exc.value)
    )
