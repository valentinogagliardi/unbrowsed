"""Tests for the query_by_label_text function."""

import pytest
from selectolax.parser import HTMLParser

from unbrowsed import parse_html, query_by_label_text, MultipleElementsFoundError


def test_query_by_label_text():
    html = """
    <label for="email">Email</label>
    <input id="email" type="email">
    <label for="password">Password</label>
    <input id="password" type="password">
    """
    dom = parse_html(html)

    assert query_by_label_text(dom, "Email")
    assert not query_by_label_text(dom, "email")
    assert not query_by_label_text(dom, "Em")


def test_query_by_label_text_exact():
    html = """
    <label for="email">Email</label>
    <input id="email" type="email">
    <label for="password">Password</label>
    <input id="password" type="password">
    """
    dom = parse_html(html)

    assert query_by_label_text(dom, "Email", exact=False)
    assert query_by_label_text(dom, "email", exact=False)
    assert query_by_label_text(dom, "Em", exact=False)
    assert query_by_label_text(dom, "Pass", exact=False)


def test_query_by_label_text_no_match():
    html = """
    <label for="email">Email</label>
    <input id="email" type="email">
    """
    dom = parse_html(html)
    query_by_label_text(dom, "Phone")
    assert not query_by_label_text(dom, "Phone")


def test_query_by_label_text_multiple_matches():
    html = """
    <label for="email1">Contact</label>
    <input id="email1" type="email">
    <label for="email2">Contact</label>
    <input id="email2" type="email">
    """
    dom = parse_html(html)

    with pytest.raises(MultipleElementsFoundError) as excinfo:
        query_by_label_text(dom, "Contact")

    assert "Found 2 elements" in str(excinfo.value)
    assert "Contact" in str(excinfo.value)
