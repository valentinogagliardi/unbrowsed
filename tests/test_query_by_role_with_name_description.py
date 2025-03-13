import pytest

from unbrowsed import (
    MultipleElementsFoundError,
    parse_html,
    query_by_role,
)


def test_query_by_role_with_name():
    html = """
    <html>
    <body>
        <button>Submit</button>
        <button>Cancel</button>
        <button>Reset</button>
    </body>
    </html>
    """
    dom = parse_html(html)

    result = query_by_role(dom, "button", name="Submit")
    assert result is not None

    result = query_by_role(dom, "button", name="Cancel")
    assert result is not None

    result = query_by_role(dom, "button", name="Reset")
    assert result is not None

    result = query_by_role(dom, "button", name="Save")
    assert result is None


def test_query_by_role_with_aria_label_name():
    html = """
    <html>
    <body>
        <button aria-label="Close dialog">X</button>
        <button aria-label="Submit form">OK</button>
    </body>
    </html>
    """
    dom = parse_html(html)

    result = query_by_role(dom, "button", name="Close dialog")
    assert result is not None

    result = query_by_role(dom, "button", name="Submit form")
    assert result is not None

    result = query_by_role(dom, "button", name="X")
    assert result is None


def test_query_by_role_with_aria_labelledby_name():
    html = """
    <html>
    <body>
        <button aria-labelledby="title1">Button 1</button>
        <span id="title1">First Button</span>

        <button aria-labelledby="title2">Button 2</button>
        <span id="title2">Second Button</span>
    </body>
    </html>
    """
    dom = parse_html(html)

    result = query_by_role(dom, "button", name="First Button")
    assert result is not None

    result = query_by_role(dom, "button", name="Second Button")
    assert result is not None

    result = query_by_role(dom, "button", name="Button 1")
    assert result is None


def test_query_by_role_with_description():
    html = """
    <html>
    <body>
        <button id="submit" aria-describedby="submit-desc">Submit</button>
        <div id="submit-desc">Submits the form</div>

        <button id="cancel" aria-describedby="cancel-desc">Cancel</button>
        <div id="cancel-desc">Cancels the operation</div>
    </body>
    </html>
    """
    dom = parse_html(html)

    result = query_by_role(dom, "button", description="Submits the form")
    assert result is not None

    result = query_by_role(dom, "button", description="Cancels the operation")
    assert result is not None

    result = query_by_role(dom, "button", description="Does something else")
    assert result is None


def test_query_by_role_with_name_and_description():
    html = """
    <html>
    <body>
        <button id="submit1" aria-describedby="submit-desc1">Submit</button>
        <div id="submit-desc1">Submits the first form</div>

        <button id="submit2" aria-describedby="submit-desc2">Submit</button>
        <div id="submit-desc2">Submits the second form</div>
    </body>
    </html>
    """
    dom = parse_html(html)

    with pytest.raises(MultipleElementsFoundError):
        query_by_role(dom, "button", name="Submit")

    result = query_by_role(
        dom, "button", name="Submit", description="Submits the first form"
    )
    assert result is not None

    result = query_by_role(
        dom, "button", name="Submit", description="Submits the second form"
    )
    assert result is not None

    result = query_by_role(
        dom, "button", name="Submit", description="Does something else"
    )
    assert result is None


def test_query_by_role_with_complex_name_and_description():
    html = """
    <html>
    <body>
        <div>
            <label for="username">Username</label>
            <input id="username" type="text" aria-describedby="username-help">
            <div id="username-help">Enter your username or email</div>
        </div>

        <div>
            <label for="password">Password</label>
            <input id="password" type="password"
            aria-describedby="password-help">
            <div id="password-help">Must be at least 8 characters</div>
        </div>
    </body>
    </html>
    """
    dom = parse_html(html)

    assert query_by_role(dom, "textbox", name="Username")
    assert query_by_role(dom, "textbox", name="Password")
    assert query_by_role(
        dom, "textbox", description="Enter your username or email"
    )
    assert query_by_role(
        dom, "textbox", description="Must be at least 8 characters"
    )
    assert query_by_role(
        dom,
        "textbox",
        name="Username",
        description="Enter your username or email",
    )
    assert query_by_role(
        dom,
        "textbox",
        name="Password",
        description="Must be at least 8 characters",
    )
    assert not query_by_role(
        dom,
        "textbox",
        name="Username",
        description="Must be at least 8 characters",
    )
    assert not query_by_role(
        dom,
        "textbox",
        name="Password",
        description="Enter your username or email",
    )
