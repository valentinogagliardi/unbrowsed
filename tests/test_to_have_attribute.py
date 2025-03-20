from unbrowsed import get_by_label_text, parse_html, query_by_text, get_by_role


def test_to_have_attribute():
    html = """
    <label for="username">Username</label>
    <input id="username" required type="email" required>
    """
    dom = parse_html(html)

    input_element = get_by_label_text(dom, "Username")
    assert input_element.to_have_attribute("type")
    assert input_element.to_have_attribute("required")
    assert not input_element.to_have_attribute("placeholder")

    html = """
    <label for="username">Username</label>
    <input id="username" type="email" data-testid="username-input">
    """
    dom = parse_html(html)

    input_element = get_by_label_text(dom, "Username")

    assert input_element.to_have_attribute("type", "email")
    assert input_element.to_have_attribute("data-testid", "username-input")
    assert not input_element.to_have_attribute("data-testid", "username")
    assert not input_element.to_have_attribute("type", "text")

    html = """
    <button type="submit" class="primary">Submit</button>
    """
    dom = parse_html(html)

    button = query_by_text(dom, "Submit")
    assert button.to_have_attribute("type", "submit")
    assert button.to_have_attribute("class", "primary")

    html = """
    <meter class="dot-meter"
            value="70"
            min="0"
            max="100"
            low="31"
            high="69"
            optimum="19">
    </meter>
    """
    dom = parse_html(html)
    meter = get_by_role(dom, "meter")
    assert meter.to_have_attribute("value", "70")
    assert meter.to_have_attribute("min", "0")

    html = """
    <button aria-pressed=true>...</button>
    """
    dom = parse_html(html)
    button = get_by_role(dom, "button")
    assert button.to_have_attribute("aria-pressed", "true")
