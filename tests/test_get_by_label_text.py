import pytest

from unbrowsed import (
    parse_html,
    get_by_label_text,
    MultipleElementsFoundError,
    NoElementsFoundError,
)


def test_get_by_label_text_exact_match():
    html = """
    <label for="email">Email</label>
    <input id="email" type="email">
    <label for="password">Password</label>
    <input id="password" type="password">
    """
    dom = parse_html(html)
    
    assert get_by_label_text(dom, "Email") is not None
    
    with pytest.raises(NoElementsFoundError) as excinfo:
        get_by_label_text(dom, "email")
    assert "No elements found" in str(excinfo.value)
    
    assert get_by_label_text(dom, "Password") is not None


def test_get_by_label_text_no_match():
    html = """
    <label for="email">Email</label>
    <input id="email" type="email">
    """
    dom = parse_html(html)
    
    with pytest.raises(NoElementsFoundError) as excinfo:
        get_by_label_text(dom, "Phone")
    
    assert "No elements found" in str(excinfo.value)
    assert "Phone" in str(excinfo.value)


def test_get_by_label_text_multiple_matches():
    html = """
    <label for="email1">Contact</label>
    <input id="email1" type="email">
    <label for="email2">Contact</label>
    <input id="email2" type="email">
    """
    dom = parse_html(html)
    
    with pytest.raises(MultipleElementsFoundError) as excinfo:
        get_by_label_text(dom, "Contact")
    
    assert "Found 2 elements" in str(excinfo.value)
    assert "Contact" in str(excinfo.value)


def test_get_by_label_text_nested_control():
    html = """
    <label>
        Username
        <input type="text" name="username">
    </label>
    """
    dom = parse_html(html)
    
    assert get_by_label_text(dom, "Username") is not None
