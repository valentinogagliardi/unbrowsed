from unbrowsed import (
    get_by_label_text,
    get_by_role,
    get_by_text,
    parse_html,
    query_by_label_text,
    query_by_text,
    Result,
)


def test_to_have_text_content_with_get_by_label_text():
    html = """
    <label for="username">Username</label>
    <input id="username" placeholder="Enter your username">
    <label for="bio">Bio</label>
    <textarea id="bio">User biography text</textarea>
    """
    dom = parse_html(html)

    input_element = get_by_label_text(dom, "Username")
    assert not input_element.to_have_text_content("Enter your username")

    textarea_element = get_by_label_text(dom, "Bio")
    assert textarea_element.to_have_text_content("User biography text")
    assert not textarea_element.to_have_text_content("biography")
    assert textarea_element.to_have_text_content("biography", exact=False)


def test_to_have_text_content_with_get_by_role():
    html = """
    <button>Submit Form</button>
    <a href="https://example.com">Visit Example</a>
    <input type="checkbox" aria-label="Accept terms">
    """
    dom = parse_html(html)

    button = get_by_role(dom, "button")
    assert button.to_have_text_content("Submit Form")
    assert not button.to_have_text_content("submit form")
    assert button.to_have_text_content("submit", exact=False)

    link = get_by_role(dom, "link")
    assert link.to_have_text_content("Visit Example")
    assert link.to_have_text_content("Visit", exact=False)
    assert not link.to_have_text_content("example")
    assert link.to_have_text_content("example", exact=False)


def test_to_have_text_content_with_get_by_text():
    html = """
    <div>Hello World</div>
    <p>Another text</p>
    <span>Third element</span>
    """
    dom = parse_html(html)

    div = get_by_text(dom, "Hello World")
    assert div.to_have_text_content("Hello World")
    assert not div.to_have_text_content("hello world")
    assert div.to_have_text_content("Hello", exact=False)

    p = get_by_text(dom, "Another text")
    assert p.to_have_text_content("Another text")
    assert p.to_have_text_content("Another", exact=False)

    span = get_by_text(dom, "Third element")
    assert span.to_have_text_content("Third element")
    assert not span.to_have_text_content("third element")
    assert span.to_have_text_content("element", exact=False)


def test_to_have_text_content_with_query_by_label_text():
    html = """
    <label for="email">Email Address</label>
    <input id="email" type="email">
    <label for="message">Your Message</label>
    <textarea id="message">Default message text</textarea>
    """
    dom = parse_html(html)

    message = query_by_label_text(dom, "Your Message")
    assert message.to_have_text_content("Default message text")
    assert message.to_have_text_content("Default", exact=False)
    assert not message.to_have_text_content("default message text")


def test_to_have_text_content_with_query_by_role():
    html = """
    <nav>
        <a href="/">Home</a>
        <a href="/about">About</a>
        <a href="/contact" aria-current="page">Contact</a>
    </nav>
    """
    dom = parse_html(html)

    contact_link = dom.css_first('a[aria-current="page"]')
    assert contact_link is not None
    current_link = Result(contact_link)

    assert current_link.to_have_text_content("Contact")
    assert not current_link.to_have_text_content("contact")
    assert current_link.to_have_text_content("cont", exact=False)


def test_to_have_text_content_with_query_by_text():
    html = """
    <div>First paragraph with some text.</div>
    <div>Second paragraph with different content.</div>
    """
    dom = parse_html(html)

    first_div = query_by_text(dom, "First paragraph with some text.")
    assert first_div.to_have_text_content("First paragraph with some text.")
    assert first_div.to_have_text_content("First", exact=False)
    assert first_div.to_have_text_content("some text", exact=False)
    assert not first_div.to_have_text_content("different content")

    second_div = query_by_text(dom, "Second paragraph with different content.")
    assert second_div.to_have_text_content(
        "Second paragraph with different content."
    )
    assert second_div.to_have_text_content("different", exact=False)
    assert not second_div.to_have_text_content("some text")
