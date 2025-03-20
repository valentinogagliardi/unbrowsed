from unittest.mock import Mock
from selectolax.lexbor import LexborHTMLParser
from unbrowsed.resolvers import (
    AccessibleNameResolver,
    AccessibleDescriptionResolver,
    RoleResolver,
)


def test_accessible_name_resolver_aria_labelledby():
    html = """
    <html>
    <body>
        <div id="element"
        aria-labelledby="title description">Test content</div>
        <h2 id="title">Important Notice</h2>
        <p id="description">Your account has been updated</p>
    </body>
    </html>
    """
    parser = LexborHTMLParser(html)
    element = parser.css_first("#element")

    name = AccessibleNameResolver(element).resolve()
    assert name == "Important Notice Your account has been updated"


def test_accessible_name_resolver_aria_labelledby_missing_id():
    html = """
    <html>
    <body>
        <div id="element"
        aria-labelledby="title missing description">Test content</div>
        <h2 id="title">Important Notice</h2>
        <p id="description">Your account has been updated</p>
    </body>
    </html>
    """
    parser = LexborHTMLParser(html)
    element = parser.css_first("#element")

    name = AccessibleNameResolver(element).resolve()
    assert name == "Important Notice Your account has been updated"


def test_accessible_name_resolver_aria_labelledby_empty_element():
    html = """
    <html>
    <body>
        <div id="element"
        aria-labelledby="title empty description">Test content</div>
        <h2 id="title">Important Notice</h2>
        <div id="empty"></div>
        <p id="description">Your account has been updated</p>
    </body>
    </html>
    """
    parser = LexborHTMLParser(html)
    element = parser.css_first("#element")

    name = AccessibleNameResolver(element).resolve()
    assert name == "Important Notice Your account has been updated"


def test_accessible_name_resolver_aria_label():
    html = """
    <html>
    <body>
        <button aria-label="Close dialog">X</button>
    </body>
    </html>
    """
    parser = LexborHTMLParser(html)
    element = parser.css_first("button")

    name = AccessibleNameResolver(element).resolve()
    assert name == "Close dialog"


def test_accessible_name_resolver_aria_label_empty():
    html = """
    <html>
    <body>
        <button aria-label="  ">X</button>
    </body>
    </html>
    """
    parser = LexborHTMLParser(html)
    element = parser.css_first("button")

    name = AccessibleNameResolver(element).resolve()
    assert name == "X"


def test_accessible_name_resolver_title_attribute():
    html = """
    <html>
    <body>
        <div title="Tooltip text">Hover me</div>
    </body>
    </html>
    """
    parser = LexborHTMLParser(html)
    element = parser.css_first("div")

    name = AccessibleNameResolver(element).resolve()
    assert name == "Tooltip text"


def test_accessible_name_resolver_title_attribute_empty():
    html = """
    <html>
    <body>
        <div title="  ">Hover me</div>
    </body>
    </html>
    """
    parser = LexborHTMLParser(html)
    element = parser.css_first("div")

    name = AccessibleNameResolver(element).resolve()
    assert name is None


def test_accessible_description_resolver_aria_describedby_all_missing():
    html = """
    <html>
    <body>
        <input id="phone" aria-describedby="missing1 missing2" type="tel">
    </body>
    </html>
    """
    parser = LexborHTMLParser(html)
    element = parser.css_first("input")

    description = AccessibleDescriptionResolver(element).resolve()
    assert description is None


def test_input_without_label():
    html = """
        <input id="username" type="text">
        <label>Username</label>
    """
    parser = LexborHTMLParser(html)
    input_element = parser.css_first("input")

    assert AccessibleNameResolver(input_element).resolve() is None


def test_get_footer_role():
    mock_node = Mock()
    mock_node.parent = None
    assert (
        RoleResolver(mock_node, target_role="contentinfo").get_footer_role()
        == "contentinfo"
    )
