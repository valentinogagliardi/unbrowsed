import pytest

from unbrowsed import parse_html, query_by_text, MultipleElementsFoundError


def test_query_by_text_exact_match():
    html = """
    <div>Hello World</div>
    <p>Another text</p>
    <span>Third element</span>
    """
    dom = parse_html(html)
    
    result = query_by_text(dom, "Hello World")
    assert result is not None
    assert result.tag == "div"
    
    result = query_by_text(dom, "hello world")
    assert result is not None
    assert result.tag == "div"
    
    result = query_by_text(dom, "Hello")
    assert result is None


def test_query_by_text_whitespace_handling():
    html = """
    <div>  Hello   World  </div>
    <p>Another text</p>
    """
    dom = parse_html(html)
    
    result = query_by_text(dom, "Hello World")
    assert result is not None


def test_query_by_text_no_match():
    html = """
    <div>Hello World</div>
    <p>Another text</p>
    """
    dom = parse_html(html)
    result = query_by_text(dom, "Missing Text")
    
    assert result is None


def test_query_by_text_multiple_matches():
    html = """
    <div>Duplicate Text</div>
    <p>Duplicate Text</p>
    """
    dom = parse_html(html)
    
    with pytest.raises(MultipleElementsFoundError) as excinfo:
        query_by_text(dom, "Duplicate Text")
    
    assert "Found 2 elements" in str(excinfo.value)
    assert "Duplicate Text" in str(excinfo.value)
    assert "query_all_by_text" in str(excinfo.value)


def test_query_by_text_nested_elements():
    html = """
    <div>Parent <span>Child</span></div>
    """
    dom = parse_html(html)
    
    result = query_by_text(dom, "Parent Child")
    if result is None:
        result = query_by_text(dom, "ParentChild")
    assert result is not None
    assert result.tag == "div"

    result = query_by_text(dom, "Child")
    assert result is not None
    assert result.tag == "span"
