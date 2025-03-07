"""Tests for the to_have_attribute assertion method."""

import pytest

from unbrowsed import parse_html, get_by_label_text, query_by_label_text, query_by_text, NoElementsFoundError


def test_to_have_attribute_existence():
    html = """
    <label for="username">Username</label>
    <input id="username" type="email" required>
    """
    dom = parse_html(html)
    
    input_element = get_by_label_text(dom, "Username")
    input_element.to_have_attribute("type")
    input_element.to_have_attribute("required")
    
    with pytest.raises(AssertionError) as excinfo:
        input_element.to_have_attribute("placeholder")
    
    assert "Expected to have attribute: placeholder" in str(excinfo.value)
    assert "Actual attributes:" in str(excinfo.value)


def test_to_have_attribute_value_match():
    html = """
    <label for="username">Username</label>
    <input id="username" type="email" data-testid="username-input">
    """
    dom = parse_html(html)
    
    input_element = get_by_label_text(dom, "Username")
    
    input_element.to_have_attribute("type", "email")
    input_element.to_have_attribute("data-testid", "username-input")
    
    with pytest.raises(AssertionError) as excinfo:
        input_element.to_have_attribute("type", "text")
    
    assert "Attribute type value mismatch" in str(excinfo.value)
    assert "Expected: text" in str(excinfo.value)
    assert "Actual: email" in str(excinfo.value)


def test_to_have_attribute_with_query_by_text():
    html = """
    <button type="submit" class="primary">Submit</button>
    """
    dom = parse_html(html)
    
    button = query_by_text(dom, "Submit")
    button.to_have_attribute("type", "submit")
    button.to_have_attribute("class", "primary")


def test_to_have_attribute_with_element_not_found():
    html = """
    <div>Some content</div>
    """
    dom = parse_html(html)
    
    result = query_by_label_text(dom, "Non-existent Label")
    assert result is None
    
    with pytest.raises(NoElementsFoundError):
        get_by_label_text(dom, "Non-existent Label")
