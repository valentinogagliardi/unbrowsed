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


class TestQueryByRoleNonExactNameAndOrDescription:
    def test_accessible_name_partial_matching(self):
        html = """
        <button>Save Document</button>
        """
        dom = parse_html(html)
        result = query_by_role(dom, "button", name="Save", exact=False)
        assert result is not None
        assert result.element.tag == "button"

    def test_accessible_name_case_insensitive_partial_matching(self):
        html = """
        <button aria-label="Close Dialog">×</button>
        """
        dom = parse_html(html)
        result = query_by_role(dom, "button", name="close", exact=False)
        assert result is not None
        result = query_by_role(dom, "button", name="DIALOG", exact=False)
        assert result is not None

    def test_accessible_description_partial_matching(self):
        html = """
        <input type="text" aria-describedby="help">
        <div id="help">Enter your full name here</div>
        """
        dom = parse_html(html)
        result = query_by_role(
            dom, "textbox", description="full name", exact=False
        )
        assert result is not None
        result = query_by_role(
            dom, "textbox", description="nonexistent", exact=False
        )
        assert result is None

    def test_accessible_description_case_insensitive_partial_matching(self):
        html = """
        <input type="text" aria-describedby="help">
        <div id="help">Enter your full name here</div>
        """
        dom = parse_html(html)
        result = query_by_role(
            dom, "textbox", description="enter your full name", exact=False
        )
        assert result is not None
        result = query_by_role(
            dom, "textbox", description="ENTER YOUR FULL NAME", exact=False
        )
        assert result is not None

    def test_partial_matching_of_element_with_multiple_accessible_descriptions(
        self,
    ):
        html = """
        <input type="text" aria-describedby="help error">
        <div id="help">Enter your full name here</div>
        <div id="error">This field is required</div>
        """
        dom = parse_html(html)
        result = query_by_role(
            dom, "textbox", description="full name", exact=False
        )
        assert result is not None
        result = query_by_role(
            dom, "textbox", description="required", exact=False
        )
        assert result is not None

    def test_partial_matching_on_both_name_and_description(self):
        html = """
        <input type="text" aria-label="User Email" aria-describedby="help">
        <div id="help">Please enter a valid email address</div>
        """
        dom = parse_html(html)
        result = query_by_role(
            dom, "textbox", name="Email", description="valid", exact=False
        )
        assert result is not None

    def test_partial_matching_does_no_match_if_name_matches_but_description_not(
        self,
    ):
        html = """
        <input type="text" aria-label="User Email" aria-describedby="help">
        <div id="help">Please enter a valid email address</div>
        """
        dom = parse_html(html)
        result = query_by_role(
            dom, "textbox", name="Email", description="no match", exact=False
        )
        assert result is None

    def test_partial_matching_does_no_match_if_description_matches_but_name_not(
        self,
    ):
        html = """
        <input type="text" aria-label="User Email" aria-describedby="help">
        <div id="help">Please enter a valid email address</div>
        """
        dom = parse_html(html)
        result = query_by_role(
            dom, "textbox", name="no match", description="valid", exact=False
        )
        assert result is None

    def test_partial_match_of_name_that_spans_multiple_nodes(self):
        html = """
        <button aria-labelledby="first second">Button text</button>
        <span id="first">Save Important</span>
        <span id="second">Document File</span>
        """
        dom = parse_html(html)
        result = query_by_role(dom, "button", name="Important", exact=False)
        assert result is not None
        result = query_by_role(dom, "button", name="Document", exact=False)
        assert result is not None
        result = query_by_role(
            dom, "button", name="Save Important Document", exact=False
        )
        assert result is not None

    def test_partial_matching_prioritizes_aria_labelledby_over_aria_label(
        self,
    ):
        html = """
        <button aria-label="Blue Button" aria-labelledby="color">Red</button>
        <span id="color">Yellow Green</span>
        """
        dom = parse_html(html)
        result = query_by_role(dom, "button", name="Yellow", exact=False)
        assert result is not None
        result = query_by_role(dom, "button", name="Green", exact=False)
        assert result is not None
        # Should not match aria-label when aria-labelledby exists
        result = query_by_role(dom, "button", name="Blue", exact=False)
        assert result is None

    def test_does_not_match_if_dont_find_any_partial_matching(self):
        html = """
        <button>Save Document</button>
        """
        dom = parse_html(html)
        result = query_by_role(dom, "button", name="Upload", exact=False)
        assert result is None

    def test_does_not_match_if_multiple_matches_found(self):
        html = """
        <button>Save Document</button>
        <button>Save File</button>
        <button>Delete Save</button>
        """
        dom = parse_html(html)
        with pytest.raises(MultipleElementsFoundError) as exc:
            query_by_role(dom, "button", name="Save", exact=False)
        assert (
            "Found multiple elements with role 'button'. "
            "Use query_all_by_role if multiple matches are expected."
            == str(exc.value)
        )

    def test_does_not_match_if_multiple_matches_found_in_children(self):
        html = """
        <div>
            <button>Save Document</button>
            <button>Save File</button>
        </div>
        <div>
            <button>Cancel Save</button>
        </div>
        """
        dom = parse_html(html)
        with pytest.raises(MultipleElementsFoundError) as exc:
            query_by_role(dom, "button", name="Save", exact=False)
        assert (
            "Found multiple elements with role 'button'. "
            "Use query_all_by_role if multiple matches are expected."
            == str(exc.value)
        )

    def test_current_attribute_with_partial_name(self):
        html = """
        <nav>
          <a href="/home" aria-current="true">Home Page</a>
          <a href="/about">About Page</a>
        </nav>
        """
        dom = parse_html(html)
        result = query_by_role(
            dom, "link", current=True, name="Home", exact=False
        )
        assert result is not None

        result = query_by_role(
            dom, "link", current=True, name="About", exact=False
        )
        assert result is None

    @pytest.mark.parametrize(
        "exact_search_kwargs",
        [{}, {"exact": True}],
        ids=["default exact=true", "explicit exact=true"],
    )
    def test_does_not_match_partial_text_using_exact_query(
        self, exact_search_kwargs
    ):
        html = """
        <button>Save Document</button>
        <input type="text" aria-describedby="help">
        <div id="help">Enter your name</div>
        """
        # Does not match partial text when using exact query
        dom = parse_html(html)
        result = query_by_role(
            dom, "button", name="save", **exact_search_kwargs
        )
        assert result is None
        result = query_by_role(
            dom, "textbox", description="your name", **exact_search_kwargs
        )
        assert result is None

        # But should match with exact text
        result = query_by_role(
            dom, "button", name="Save Document", **exact_search_kwargs
        )
        assert result is not None
        result = query_by_role(
            dom,
            "textbox",
            description="Enter your name",
            **exact_search_kwargs,
        )
        assert result is not None

    def test_non_exact_query_when_elements_has_empty_name_or_description(self):
        html = """
        <button aria-label="">Empty Label</button>
        <input type="text" aria-describedby="empty">
        <div id="empty"></div>
        """
        dom = parse_html(html)
        result = query_by_role(dom, "button", name="anything", exact=False)
        assert result is None
        result = query_by_role(
            dom, "textbox", description="anything", exact=False
        )
        assert result is None

    def test_non_exact_search_supports_special_characters(self):
        html = """
        <button aria-label="Save & Exit (Ctrl+S)">Save</button>
        """
        dom = parse_html(html)
        result = query_by_role(dom, "button", name="Save & Exit", exact=False)
        assert result is not None
        result = query_by_role(dom, "button", name="Ctrl+S", exact=False)
        assert result is not None
