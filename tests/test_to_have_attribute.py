import pytest

from unbrowsed import parse_html, get_by_label_text, query_by_text


def test_to_have_attribute_existence():
    html = """
    <label for="username">Username</label>
    <input id="username" required type="email" required>
    """
    dom = parse_html(html)

    input_element = get_by_label_text(dom, "Username")
    assert input_element.to_have_attribute("type")
    assert input_element.to_have_attribute("required")
    assert not input_element.to_have_attribute("placeholder")


def test_to_have_attribute_value_match():
    html = """
    <label for="username">Username</label>
    <input id="username" type="email" data-testid="username-input">
    """
    dom = parse_html(html)

    input_element = get_by_label_text(dom, "Username")

    assert input_element.to_have_attribute("type", "email")
    assert input_element.to_have_attribute("data-testid", "username-input")
    assert not input_element.to_have_attribute("type", "text")


def test_to_have_attribute_with_query_by_text():
    html = """
    <button type="submit" class="primary">Submit</button>
    """
    dom = parse_html(html)

    button = query_by_text(dom, "Submit")
    assert button.to_have_attribute("type", "submit")
    assert button.to_have_attribute("class", "primary")
