"""Tests for the query_by_label_text function."""

import pytest

from unbrowsed import (
    MultipleElementsFoundError,
    parse_html,
    query_by_label_text,
)


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

    html = """
        <form>
            <label for="username">Username</label>
            <input id="username" type="text">
            <label for="password">Password</label>
            <input id="password" type="password">
            <button type="submit">Login</button>
        </form>
        """
    dom = parse_html(html)
    username_input = query_by_label_text(dom, "Username")
    assert username_input

    html = """
        <form>
            <label for="email">Email Address</label>
            <input id="email" type="email">
        </form>
        """
    dom = parse_html(html)

    assert query_by_label_text(dom, "Email Address")


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

    with pytest.raises(MultipleElementsFoundError) as exc:
        query_by_label_text(dom, "Contact")

    assert (
        "Found 2 elements with label 'Contact'. "
        "Use get_all_by_label_text if multiple matches are expected."
        == str(exc.value)
    )


def test_query_by_label_text_no_target_id():
    html = """
    <label for="non-existent-id">Label Text</label>
    """
    dom = parse_html(html)
    assert not query_by_label_text(dom, "Label Text")


def test_query_by_label_text_no_control():
    html = """
    <label>Label Text</label>
    """
    dom = parse_html(html)
    assert not query_by_label_text(dom, "Label Text")


def test_query_by_label_text_with_empty_for():

    html = """
    <label for="">Label Text</label>
    """
    dom = parse_html(html)
    assert not query_by_label_text(dom, "Label Text")
