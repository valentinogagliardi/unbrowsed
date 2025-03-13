import pytest

from unbrowsed import (
    MultipleElementsFoundError,
    NoElementsFoundError,
    get_by_role,
    parse_html,
)


def test_get_by_role_link():
    html = """
    <a href="https://example.com">Example Link</a>
    <button>Button</button>
    """
    dom = parse_html(html)
    assert get_by_role(dom, "link")

    html = """
    <a href="#anchor" aria-current="true">
      <span>The text</span>
    </a>
    """
    dom = parse_html(html)
    assert get_by_role(dom, "link", current=True)

    html = """
    <a href="#anchor" aria-current="true">
      <span>The text</span>
    </a>
    """
    dom = parse_html(html)
    assert get_by_role(dom, "link", current="true")

    html = """
    <a href="#anchor" aria-current="page">
      <span>The text</span>
    </a>
    """
    dom = parse_html(html)
    assert get_by_role(dom, "link", current="page")


def test_get_by_role_button():
    html = """
    <button id="main-button">Regular Button</button>
    <input type="submit" value="Submit Button">
    """
    dom = parse_html(html)

    assert get_by_role(dom, "button")


def test_get_by_role_with_attributes():
    html = """
    <a href="https://example.com" aria-current="true">Current Link</a>
    <a href="https://example.org">Other Link</a>
    """
    dom = parse_html(html)

    assert get_by_role(dom, "link", current="true")

    assert get_by_role(dom, "link", current=True)


def test_get_by_role_no_match():
    html = """
    <div>Some content</div>
    <p>Some paragraph</p>
    """
    dom = parse_html(html)

    with pytest.raises(NoElementsFoundError):
        get_by_role(dom, "button")


def test_get_by_role_multiple_matches():
    html = """
    <button>Button 1</button>
    <button>Button 2</button>
    """
    dom = parse_html(html)

    with pytest.raises(MultipleElementsFoundError) as exc:
        get_by_role(dom, "button")
    assert (
        "Found 2 elements with role 'button'. "
        "Use get_all_by_role if multiple matches are expected."
        == str(exc.value)
    )


def test_get_by_role_prioritize_child():
    html = """
    <nav>
        <a href="https://example.com">Link inside navigation</a>
    </nav>
    """
    dom = parse_html(html)

    link = get_by_role(dom, "link")
    assert link.element.tag == "a"


def test_by_role_input():
    html = """
    <input type="checkbox">
    """
    dom = parse_html(html)
    assert get_by_role(dom, "checkbox")

    html = """
    <input type="radio">
    """
    dom = parse_html(html)
    assert get_by_role(dom, "radio")

    html = """
    <input type="text">
    """
    dom = parse_html(html)
    assert get_by_role(dom, "textbox")


def test_by_role_meter():
    html = """
        <td><meter value="100">100%</meter></td>
        """
    dom = parse_html(html)
    assert get_by_role(dom, "meter").to_have_attribute("value", "100")


def test_by_role_group():
    html = """
    <form>
      <fieldset name="the name">
        <legend>Choose your favorite monster</legend>

        <input type="radio" id="kraken" name="monster" value="K" />
        <label for="kraken">Kraken</label><br />

        <input type="radio" id="sasquatch" name="monster" value="S" />
        <label for="sasquatch">Sasquatch</label><br />

        <input type="radio" id="mothman" name="monster" value="M" />
        <label for="mothman">Mothman</label>
      </fieldset>
    </form>
    """
    dom = parse_html(html)
    assert get_by_role(dom, "group").to_have_attribute("name", "the name")
    assert get_by_role(dom, "group", name="Choose your favorite monster")

    html = """
    <form>
      <fieldset>
        <input type="radio" id="kraken" name="monster" value="K" />
        <label for="kraken">Kraken</label><br />

        <input type="radio" id="sasquatch" name="monster" value="S" />
        <label for="sasquatch">Sasquatch</label><br />

        <input type="radio" id="mothman" name="monster" value="M" />
        <label for="mothman">Mothman</label>
      </fieldset>
    </form>
    """
    dom = parse_html(html)
    with pytest.raises(NoElementsFoundError):
        get_by_role(dom, "group", name="Choose your favorite monster")


def test_get_by_role_accessible_description():
    html = """
    <div>
        <label for="id_name">The name</label>
      <div>
          <input type="text" name="name"
          aria-describedby="id_name_errorlist" id="id_name">
      </div>
      <ul id="id_name_errorlist" class="errorlist">
        <li class="error">This field is required.</li>
      </ul>
      </div>
    """
    dom = parse_html(html)
    assert get_by_role(dom, "textbox", description="This field is required.")

    html = """
    <div>
        <label for="id_name">The name</label>
      <div>
          <input type="text" name="name"
          aria-describedby="id_name_errorlist" id="id_name">
      </div>
      <ul id="id_name_errorlist" class="errorlist">
        <li class="error">This field is required.</li>
      </ul>
      </div>
    """
    dom = parse_html(html)
    with pytest.raises(NoElementsFoundError):
        get_by_role(dom, "textbox", description="not there")


def test_get_by_role_accessible_name():
    html = """
    <div>
        <label for="id_name">The name</label>
      <div>
          <input type="text" name="name"
          aria-describedby="id_name_errorlist" id="id_name">
      </div>
      <ul id="id_name_errorlist" class="errorlist">
        <li class="error">This field is required.</li>
      </ul>
      </div>
    """
    dom = parse_html(html)
    assert get_by_role(dom, "textbox", name="The name")

    html = """
      <button aria-label="Blue" aria-labelledby="color">Red</button>
      <span id="color">Yellow</span>
    """
    dom = parse_html(html)
    assert get_by_role(dom, "button", name="Yellow")

    html = """
    <html>
    <body>
    <button aria-label="Blue" aria-labelledby="color color-1">Red</button>
    <span id="color">Yellow</span>
    <span id="color-1">Red</span>
    </body>
    </html>
    """
    dom = parse_html(html)
    assert get_by_role(dom, "button", name="Yellow Red")

    html = """
    <html>
    <body>
    <button aria-label="Blue" aria-labelledby="color">Red</button>
    <span id="color">Yellow</span>
    </body>
    </html>
    """
    dom = parse_html(html)
    assert get_by_role(dom, "button", name="Yellow")

    html = """
      <a role="button" aria-label="Close popup" href="#close">
      <span aria-hidden="true">×</span></a>
    """
    dom = parse_html(html)
    assert get_by_role(dom, "button", name="Close popup")

    html = '<img src="tequila.png" alt="Chamukos tequila">'
    dom = parse_html(html)
    assert get_by_role(dom, "img", name="Chamukos tequila")

    html = """
    <a href="tequila.html">
      <img src="tequila.png" alt="Chamukos tequila">
    </a>'
    """
    dom = parse_html(html)
    assert get_by_role(dom, "link", name="Chamukos tequila")

    html = """
    <a href="tequila.html">
      <img src="tequila.png" alt="Chamukos tequila"> £40
    </a>
    """
    dom = parse_html(html)
    assert get_by_role(dom, "link", name="Chamukos tequila £40")

    html = """
    <button aria-label="Add Chamukos tequila to cart">Add to cart</button>
    """
    dom = parse_html(html)
    assert get_by_role(dom, "button", name="Add Chamukos tequila to cart")

    html = """
    <input type="search" aria-labelledby="this">
    <button id="this">Search</button>
    """
    dom = parse_html(html)
    assert get_by_role(dom, "searchbox", name="Search")

    html = """
        <label for="id_name">The name</label>
        <input type="text" name="name" id="id_name">
        <label for="id_surname">The surname</label>
        <input type="text" name="surname" id="id_surname">
    """
    dom = parse_html(html)
    assert get_by_role(dom, "textbox", name="The name")

    html = """
        <label for="id_name">The name</label>
        <input type="text" name="name" id="id_name">
        <label for="id_surname">The surname</label>
        <input type="text" name="surname" id="id_surname">
    """
    dom = parse_html(html)
    assert get_by_role(dom, "textbox", name="The name")
    assert get_by_role(dom, "textbox", name="The surname")


def test_get_by_role_aria_labelledby_multiple_refs():
    html = """
    <html>
    <body>
        <div role="alert"
        aria-labelledby="title description note missing empty">
        Alert content</div>
        <h2 id="title">Important Notice</h2>
        <p id="description">Your account has been updated</p>
        <span id="note">Please</span>
        <div id="empty"></div>
    </body>
    </html>
    """
    dom = parse_html(html)
    assert get_by_role(
        dom,
        "alert",
        name="Important Notice Your account has been updated Please",
    )

    html = """
    <html>
    <body>
        <button aria-labelledby="first second third">Button text</button>
        <span id="first">Hello</span>
        <!-- second ID doesn't exist -->
        <div id="third">World</div>
    </body>
    </html>
    """
    dom = parse_html(html)
    assert get_by_role(dom, "button", name="Hello World")

    html = """
    <html>
    <body>
        <input type="text" aria-labelledby="label3 label1 label2" />
        <span id="label1">Middle</span>
        <span id="label2">Last</span>
        <span id="label3">First</span>
    </body>
    </html>
    """
    dom = parse_html(html)
    assert get_by_role(dom, "textbox", name="First Middle Last")
