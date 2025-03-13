import pytest

from unbrowsed import (
    NoElementsFoundError,
    get_all_by_role,
    parse_html,
    query_all_by_role,
)


def test_query_all_by_role_basic():
    html = """
    <html>
    <body>
        <button>Button 1</button>
        <button>Button 2</button>
        <button>Button 3</button>
    </body>
    </html>
    """
    dom = parse_html(html)

    results = query_all_by_role(dom, "button")
    assert len(results) == 3


def test_query_all_by_role_with_current():
    html = """
    <html>
    <body>
        <a href="/page1" aria-current="true">Page 1</a>
        <a href="/page2">Page 2</a>
        <a href="/page3" aria-current="true">Page 3</a>
    </body>
    </html>
    """
    dom = parse_html(html)

    results = query_all_by_role(dom, "link", current=True)
    assert len(results) == 2

    results = query_all_by_role(dom, "link", current=False)
    assert len(results) == 1


def test_query_all_by_role_no_matches():
    html = """
    <html>
    <body>
        <div>Some content</div>
        <p>Some paragraph</p>
    </body>
    </html>
    """
    dom = parse_html(html)

    results = query_all_by_role(dom, "button")
    assert len(results) == 0


def test_query_all_by_role_mixed_elements():
    html = """
    <html>
    <body>
        <button>Button 1</button>
        <input type="button" value="Input Button">
        <div role="button">Custom Button</div>
    </body>
    </html>
    """
    dom = parse_html(html)

    results = query_all_by_role(dom, "button")
    assert len(results) == 3


def test_get_all_by_role_basic():
    html = """
    <html>
    <body>
        <button>Button 1</button>
        <button>Button 2</button>
    </body>
    </html>
    """
    dom = parse_html(html)

    results = get_all_by_role(dom, "button")
    assert len(results) == 2


def test_get_all_by_role_no_matches():
    html = """
    <html>
    <body>
        <div>Some content</div>
        <p>Some paragraph</p>
    </body>
    </html>
    """
    dom = parse_html(html)

    with pytest.raises(NoElementsFoundError) as exc:
        get_all_by_role(dom, "button")

    assert (
        "No elements found with role 'button'. "
        "Use query_all_by_role if expecting no matches." == str(exc.value)
    )


def test_get_all_by_role_with_current():
    html = """
    <html>
    <body>
        <a href="/page1" aria-current="true">Page 1</a>
        <a href="/page2">Page 2</a>
        <a href="/page3" aria-current="true">Page 3</a>
    </body>
    </html>
    """
    dom = parse_html(html)

    results = get_all_by_role(dom, "link", current=True)
    assert len(results) == 2

    with pytest.raises(NoElementsFoundError):
        get_all_by_role(dom, "button", current=True)
