import pytest

from unbrowsed import (
    NoElementsFoundError,
    get_all_by_role,
    parse_html,
)


def test_get_all_by_role_returns_multiple_elements():
    html = """
    <button>Button 1</button>
    <button>Button 2</button>
    """
    dom = parse_html(html)

    buttons = get_all_by_role(dom, "button")
    assert len(buttons) == 2


def test_get_all_by_role_with_attributes():
    html = """
    <a href="https://example.com" aria-current="true">Current Link</a>
    <a href="https://example.org">Other Link</a>
    """
    dom = parse_html(html)

    links_with_current = get_all_by_role(dom, "link", current=True)
    assert len(links_with_current) == 1

    all_links = get_all_by_role(dom, "link")
    assert len(all_links) == 2


def test_get_all_by_role_no_match():
    html = """
    <div>Some content</div>
    <p>Some paragraph</p>
    """
    dom = parse_html(html)

    with pytest.raises(NoElementsFoundError) as exc:
        get_all_by_role(dom, "button")
    assert (
        "No elements found with role 'button'. "
        "Use query_all_by_role if expecting no matches." == str(exc.value)
    )


def test_get_all_by_role_meter():
    html = """
    <div>
        <td><meter value="100">100%</meter></td>
        <td><meter value="0">0%</meter></td>
    </div>
    """
    dom = parse_html(html)

    meters = get_all_by_role(dom, "meter")
    assert len(meters) == 2

    first, second = meters
    assert first.to_have_attribute("value", "100")
    assert second.to_have_attribute("value", "0")


def test_get_all_by_role_generic():
    html = """
    <body>
    </body>
    """
    dom = parse_html(html)
    assert len(get_all_by_role(dom, "generic")) == 1

    html = """
    <html>
    <body>
        <a>Example Link</a>
        <button>Button</button>
    </body>
    </html>
    """
    dom = parse_html(html)
    assert len(get_all_by_role(dom, "generic")) == 2

    html = """
        <html>
        <body>
        <p>
          <b class="term">chemistry</b> (the study of chemicals
          and the composition of
          substances) and <b class="term">physics</b>
          (the study of the nature and
          properties of matter and energy).
        </p>
        </body>
        </html>
            """
    dom = parse_html(html)
    assert len(get_all_by_role(dom, "generic")) == 3


def test_get_all_by_role_document():
    html = """
        <html>
        <body>
        <img alt=""/>
        </body>
        </html>
    """
    dom = parse_html(html)
    assert len(get_all_by_role(dom, "document")) == 1

    html = """
        <html>
        <body>
        <img alt=""/>
        <article role="document"></article>
        </body>
        </html>
    """
    dom = parse_html(html)
    assert len(get_all_by_role(dom, "document")) == 2
    doc, article = get_all_by_role(dom, "document")
    assert doc.element.tag == "html"
    assert article.element.tag == "article"
