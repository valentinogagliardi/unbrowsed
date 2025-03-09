import pytest

from unbrowsed import parse_html, query_by_role, MultipleElementsFoundError


def test_query_by_role_filtered_matches():
    html = """
    <html>
      <body>
        <h1>Heading 1</h1>
        <h2>Heading 2</h2>
      </body>
    </html>
    """
    dom = parse_html(html)

    with pytest.raises(MultipleElementsFoundError):
        query_by_role(dom, "heading")


def test_query_by_role_html_body_filtering():
    html = """
    <html>
      <body>
        <nav>Navigation</nav>
        <nav>Secondary Navigation</nav>
      </body>
    </html>
    """
    dom = parse_html(html)

    with pytest.raises(MultipleElementsFoundError):
        query_by_role(dom, "navigation")


def test_query_by_role_parent_child_relationship():
    html = """
    <nav>
      Outer Navigation
      <a href="/home">Home</a>
      <nav>
        Inner Navigation
        <a href="/about">About</a>
      </nav>
    </nav>
    """
    dom = parse_html(html)

    result = query_by_role(dom, "navigation")
    assert result
    html_single_nav = """
    <nav>
      Navigation
      <a href="/about">About</a>
    </nav>
    """
    dom_single_nav = parse_html(html_single_nav)
    result = query_by_role(dom_single_nav, "navigation")
    assert result

    with pytest.raises(MultipleElementsFoundError):
        query_by_role(dom, "link")


def test_query_by_role_current_attribute():
    html = """
    <nav>
      <a href="/home" aria-current="true">Home</a>
      <a href="/about">About</a>
    </nav>
    """
    dom = parse_html(html)

    result = query_by_role(dom, "link", current=True)
    assert result

    result = query_by_role(dom, "link", current="true")
    assert result
