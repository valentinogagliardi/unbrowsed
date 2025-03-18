import pytest

from unbrowsed import (
    MultipleElementsFoundError,
    NoElementsFoundError,
    get_by_label_text,
    parse_html,
)


@pytest.fixture
def labels_html():
    return """
    <label for="email">Email</label>
    <input id="email" type="email">
    <label for="password">Password</label>
    <input id="password" type="password">
    """


def test_get_by_label_text(labels_html):
    dom = parse_html(labels_html)

    get_by_label_text(dom, "Email")
    get_by_label_text(dom, "Password")

    with pytest.raises(NoElementsFoundError) as exc:
        get_by_label_text(dom, "email")
    assert (
        "No elements found with label 'email'. "
        "Use query_by_label_text if expecting no matches." == str(exc.value)
    )

    html = """
        <form>
            <label for="email">Email Address</label>
            <input id="email" type="email">
        </form>
        """
    dom = parse_html(html)

    get_by_label_text(dom, "Email Address")


def test_get_by_label_text_exact(labels_html):
    dom = parse_html(labels_html)

    get_by_label_text(dom, "email", exact=False)
    get_by_label_text(dom, "password", exact=False)
    get_by_label_text(dom, "passw", exact=False)


def test_get_by_label_text_no_match():
    html = """
    <label for="email">Email</label>
    <input id="email" type="email">
    """
    dom = parse_html(html)

    with pytest.raises(NoElementsFoundError) as exc:
        get_by_label_text(dom, "Phone")

    assert (
        "No elements found with label 'Phone'. "
        "Use query_by_label_text if expecting no matches." == str(exc.value)
    )


def test_get_by_label_text_multiple_matches():
    html = """
    <label for="email1">Contact</label>
    <input id="email1" type="email">
    <label for="email2">Contact</label>
    <input id="email2" type="email">
    """
    dom = parse_html(html)

    with pytest.raises(MultipleElementsFoundError) as exc:
        get_by_label_text(dom, "Contact")

    assert (
        "Found 2 elements with label 'Contact'. "
        "Use get_all_by_label_text if multiple matches are expected."
        == str(exc.value)
    )


def test_get_by_label_text_nested_control():
    html = """
    <label>
        Username
        <input type="text" name="username">
    </label>
    """
    dom = parse_html(html)

    get_by_label_text(dom, "Username")


def test_no_for_attr():
    html = """
    <label>Password</label>
    <input id="password" type="password">
    """
    dom = parse_html(html)
    with pytest.raises(NoElementsFoundError):
        get_by_label_text(dom, "Password")
