from selectolax.lexbor import LexborHTMLParser

from unbrowsed.resolvers import (
    AccessibleNameResolver,
    AccessibleDescriptionResolver,
    RoleResolver,
)
from unbrowsed.parser import parse_html


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

    name = AccessibleNameResolver.resolve(element)
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

    name = AccessibleNameResolver.resolve(element)
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

    name = AccessibleNameResolver.resolve(element)
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

    name = AccessibleNameResolver.resolve(element)
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

    name = AccessibleNameResolver.resolve(element)
    assert name == "X"


def test_accessible_name_resolver_fieldset_legend():
    html = """
    <html>
    <body>
        <fieldset>
            <legend>Personal Information</legend>
            <input type="text" placeholder="Name">
        </fieldset>
    </body>
    </html>
    """
    parser = LexborHTMLParser(html)
    element = parser.css_first("fieldset")

    name = AccessibleNameResolver.resolve(element)
    assert name == "Personal Information"


def test_accessible_name_resolver_input_label():
    html = """
    <html>
    <body>
        <label for="username">Username</label>
        <input id="username" type="text">
    </body>
    </html>
    """
    parser = LexborHTMLParser(html)
    element = parser.css_first("input")

    name = AccessibleNameResolver.resolve(element)
    assert name == "Username"


def test_accessible_name_resolver_img_alt():
    html = """
    <html>
    <body>
        <img src="example.jpg" alt="Example image">
    </body>
    </html>
    """
    parser = LexborHTMLParser(html)
    element = parser.css_first("img")

    name = AccessibleNameResolver.resolve(element)
    assert name == "Example image"


def test_accessible_name_resolver_img_alt_empty():
    html = """
    <html>
    <body>
        <img src="example.jpg" alt="  ">
    </body>
    </html>
    """
    parser = LexborHTMLParser(html)
    element = parser.css_first("img")

    name = AccessibleNameResolver.resolve(element)
    assert name == ""


def test_accessible_name_resolver_a_with_img_alt():
    html = """
    <html>
    <body>
        <a href="https://example.com">
            <img src="example.jpg" alt="Example image">
        </a>
    </body>
    </html>
    """
    parser = LexborHTMLParser(html)
    element = parser.css_first("a")

    name = AccessibleNameResolver.resolve(element)
    assert name == "Example image"


def test_accessible_name_resolver_a_with_img_alt_and_text():
    html = """
    <html>
    <body>
        <a href="https://example.com">
            <img src="example.jpg" alt="Example image">
            Visit Example
        </a>
    </body>
    </html>
    """
    parser = LexborHTMLParser(html)
    element = parser.css_first("a")

    name = AccessibleNameResolver.resolve(element)
    assert name == "Example image Visit Example"


def test_accessible_name_resolver_button_text():
    html = """
    <html>
    <body>
        <button>Submit Form</button>
    </body>
    </html>
    """
    parser = LexborHTMLParser(html)
    element = parser.css_first("button")

    name = AccessibleNameResolver.resolve(element)
    assert name == "Submit Form"


def test_accessible_name_resolver_heading_text():
    html = """
    <html>
    <body>
        <h1>Page Title</h1>
    </body>
    </html>
    """
    parser = LexborHTMLParser(html)
    element = parser.css_first("h1")

    name = AccessibleNameResolver.resolve(element)
    assert name == "Page Title"


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

    name = AccessibleNameResolver.resolve(element)
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

    name = AccessibleNameResolver.resolve(element)
    assert name is None


def test_accessible_name_resolver_no_accessible_name():
    html = """
    <html>
    <body>
        <div>No accessible name</div>
    </body>
    </html>
    """
    parser = LexborHTMLParser(html)
    element = parser.css_first("div")

    name = AccessibleNameResolver.resolve(element)
    assert name is None


def test_accessible_description_resolver_aria_describedby():
    html = """
    <html>
    <body>
        <input id="username" aria-describedby="username-help" type="text">
        <div id="username-help">Enter your username or email address</div>
    </body>
    </html>
    """
    parser = LexborHTMLParser(html)
    element = parser.css_first("input")

    description = AccessibleDescriptionResolver.resolve(element)
    assert description == "Enter your username or email address"


def test_accessible_description_resolver_aria_describedby_missing_id():
    html = """
    <html>
    <body>
        <input id="email" aria-describedby="email-help missing" type="email">
        <div id="email-help">Enter a valid email address</div>
    </body>
    </html>
    """
    parser = LexborHTMLParser(html)
    element = parser.css_first("input")

    description = AccessibleDescriptionResolver.resolve(element)
    assert description == "Enter a valid email address"


def test_accessible_description_resolver_aria_describedby_empty_element():
    html = """
    <html>
    <body>
        <input id="search" aria-describedby="search-help empty" type="search">
        <div id="search-help">Search for products</div>
        <div id="empty"></div>
    </body>
    </html>
    """
    parser = LexborHTMLParser(html)
    element = parser.css_first("input")

    description = AccessibleDescriptionResolver.resolve(element)
    assert description == "Search for products"


def test_accessible_description_resolver_no_aria_describedby():
    html = """
    <html>
    <body>
        <input id="name" type="text">
    </body>
    </html>
    """
    parser = LexborHTMLParser(html)
    element = parser.css_first("input")

    description = AccessibleDescriptionResolver.resolve(element)
    assert description is None


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

    description = AccessibleDescriptionResolver.resolve(element)
    assert description is None


def test_role_matcher_a():
    html = """
    <a>an invalid link</a>
    """
    dom = parse_html(html)
    link = dom.css_first("a")
    assert RoleResolver.get_implicit_role(link) == "generic"

    html = """
    <a href="/home">a invalid link</a>
    """
    dom = parse_html(html)
    link = dom.css_first("a")
    assert RoleResolver.get_implicit_role(link) == "link"


def test_role_matcher_input_types():
    html = """
    <input type="checkbox">
    <input type="radio">
    <input type="text">
    <input type="unknown">
    """
    dom = parse_html(html)

    checkbox = dom.css_first('input[type="checkbox"]')
    assert RoleResolver.get_implicit_role(checkbox) == "checkbox"

    radio = dom.css_first('input[type="radio"]')
    assert RoleResolver.get_implicit_role(radio) == "radio"

    text_input = dom.css_first('input[type="text"]')
    assert RoleResolver.get_implicit_role(text_input) == "textbox"

    unknown = dom.css_first('input[type="unknown"]')
    assert not RoleResolver.get_implicit_role(unknown)
