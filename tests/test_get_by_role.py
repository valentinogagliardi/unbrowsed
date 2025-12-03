import pytest

from unbrowsed import (
    MultipleElementsFoundError,
    NoElementsFoundError,
    get_by_role,
    parse_html,
)


def test_get_by_role_address():
    html = """
        <address>
          <a href="mailto:jim@example.com">jim@example.com</a><br />
          <a href="tel:+14155550132">+1 (415) 555‑0132</a>
        </address>
    """
    dom = parse_html(html)
    get_by_role(dom, "group")


def test_get_by_role_form():
    html = """
    <html lang="en">
      <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Django Accessible Forms</title>
      </head>
      <body>
        <form class="" method="post" novalidate="">
          <div class="form-group">
            <label for="id_title">Title (required):</label>
            <div class="helptext" id="id_title_helptext">
              Enter the title of the book.
            </div>
            <input type="text" name="title" maxlength="200"
                  aria-describedby="id_title_errorlist id_title_helptext"
                  aria-invalid="false" required="" id="id_title">
            <ul id="id_title_errorlist" class="errorlist">
                <li>This field is required.</li>
            </ul>
          </div>
        </form>
      </body>
    </html>
    """
    dom = parse_html(html)
    assert get_by_role(dom, "form").to_have_attribute("novalidate")


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
    get_by_role(dom, "link", current=True)

    html = """
    <a href="#anchor" aria-current="true">
      <span>The text</span>
    </a>
    """
    dom = parse_html(html)
    get_by_role(dom, "link", current="true")

    html = """
    <a href="#anchor" aria-current="page">
      <span>The text</span>
    </a>
    """
    dom = parse_html(html)
    get_by_role(dom, "link", current="page")


def test_get_by_role_button():
    html = """
    <button id="main-button">Regular Button</button>
    <input type="submit" value="Submit Button">
    """
    dom = parse_html(html)

    get_by_role(dom, "button")


def test_get_by_role_generic():
    html = """
    <a>Example Link</a>
    <button>Button</button>
    """
    dom = parse_html(html)
    get_by_role(dom, "generic")

    html = """
        <p>
          The two most popular science
          courses offered by the school are
          (the study of chemicals and the composition of
          substances) and <b class="term">physics</b>
          (the study of the nature and
          properties of matter and energy).
        </p>
    """
    dom = parse_html(html)
    get_by_role(dom, "generic")


def test_get_by_role_with_attributes():
    html = """
    <a href="https://example.com" aria-current="true">Current Link</a>
    <a href="https://example.org">Other Link</a>
    """
    dom = parse_html(html)

    get_by_role(dom, "link", current="true")
    get_by_role(dom, "link", current=True)


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

    get_by_role(dom, "link")


def test_by_role_input():
    html = """
    <input type="checkbox">
    """
    dom = parse_html(html)
    get_by_role(dom, "checkbox")

    html = """
    <input type="radio">
    """
    dom = parse_html(html)
    get_by_role(dom, "radio")

    html = """
    <input type="text">
    """
    dom = parse_html(html)
    get_by_role(dom, "textbox")


def test_by_role_meter():
    html = """
        <td><meter value="100">100%</meter></td>
        """
    dom = parse_html(html)
    get_by_role(dom, "meter").to_have_attribute("value", "100")


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
    get_by_role(dom, "group").to_have_attribute("name", "the name")
    get_by_role(dom, "group", name="Choose your favorite monster")

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
    get_by_role(dom, "textbox", description="This field is required.")

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

    html = """
    <html lang="en">
      <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Django Accessible Forms</title>
      </head>
      <body>
        <form class="" method="post" novalidate="">
          <div class="form-group">
            <label for="id_title">Title (required):</label>
            <div class="helptext" id="id_title_helptext">
              Enter the title of the book.
            </div>
            <input type="text" name="title" maxlength="200"
                  aria-describedby="id_title_errorlist id_title_helptext"
                  aria-invalid="false" required="" id="id_title">
            <ul id="id_title_errorlist" class="errorlist"></ul>
          </div>
          <div class="form-group">
            <label for="id_publication_date">
            Publication Date (required):
            </label>
            <div class="helptext" id="id_publication_date_helptext">
              Enter the publication date.
            </div>
            <input type="text" name="publication_date"
                  aria-describedby="id_publication_date_errorlist
                                    id_publication_date_helptext"
                  aria-invalid="false" required="" id="id_publication_date">
            <ul id="id_publication_date_errorlist" class="errorlist"></ul>
          </div>
          <div class="form-group">
            <label for="id_description">Description (optional):</label>
            <textarea name="description" cols="40" rows="10"
                      aria-describedby="id_description_errorlist
                                      id_description_helptext"
                      id="id_description"></textarea>
            <ul id="id_description_errorlist" class="errorlist"></ul>
          </div>
          <div class="form-group">
            <label for="id_author">Author (required):</label>
            <div class="helptext" id="id_author_helptext">
              Select the author of the book.
            </div>
            <select name="author"
                    aria-describedby="id_author_errorlist id_author_helptext"
                    aria-invalid="false" required="" id="id_author">
              <option value="" selected="">---------</option>
            </select>
            <ul id="id_author_errorlist" class="errorlist"></ul>
          </div>
          <button type="submit">Submit</button>
        </form>
      </body>
    </html>
    """
    dom = parse_html(html)
    get_by_role(dom, "form")
    get_by_role(dom, "textbox", description="Enter the title of the book.")
    get_by_role(dom, "textbox", description="Enter the publication date.")
    get_by_role(dom, "combobox", description="Select the author of the book.")


def test_get_by_role_accessible_descriptions():
    html = """
    <html lang="en">
      <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Django Accessible Forms</title>
      </head>
      <body>
        <form class="" method="post" novalidate="">
          <div class="form-group">
            <label for="id_title">Title (required):</label>
            <div class="helptext" id="id_title_helptext">
              Enter the title of the book.
            </div>
            <input type="text" name="title" maxlength="200"
                  aria-describedby="id_title_errorlist id_title_helptext"
                  aria-invalid="false" required="" id="id_title">
            <ul id="id_title_errorlist" class="errorlist">
                <li>This field is required.</li>
            </ul>
          </div>
          <div class="form-group">
            <label for="id_publication_date">
            Publication Date (required):
            </label>
            <div class="helptext" id="id_publication_date_helptext">
              Enter the publication date.
            </div>
            <input type="text" name="publication_date"
                  aria-describedby="id_publication_date_errorlist
                                    id_publication_date_helptext"
                  aria-invalid="false" required="" id="id_publication_date">
            <ul id="id_publication_date_errorlist" class="errorlist">
                <li>This field is required.</li>
            </ul>
          </div>
          <div class="form-group">
            <label for="id_description">Description (optional):</label>
            <textarea name="description" cols="40" rows="10"
                      aria-describedby="id_description_errorlist
                                      id_description_helptext"
                      id="id_description"></textarea>
            <ul id="id_description_errorlist" class="errorlist">
                <li>This field is required.</li>
            </ul>
          </div>
          <div class="form-group">
            <label for="id_author">Author (required):</label>
            <div class="helptext" id="id_author_helptext">
              Select the author of the book.
            </div>
            <select name="author"
                    aria-describedby="id_author_errorlist id_author_helptext"
                    aria-invalid="false" required="" id="id_author">
              <option value="" selected="">---------</option>
            </select>
            <ul id="id_author_errorlist" class="errorlist">
                <li>This field is required.</li>
            </ul>
          </div>
          <button type="submit">Submit</button>
        </form>
      </body>
    </html>
    """
    dom = parse_html(html)
    get_by_role(dom, "form")
    get_by_role(
        dom,
        "textbox",
        description="This field is required. Enter the title of the book.",
    )
    get_by_role(
        dom,
        "textbox",
        description="This field is required. Enter the publication date.",
    )
    get_by_role(
        dom,
        "combobox",
        description="This field is required. Select the author of the book.",
    )


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
    get_by_role(dom, "textbox", name="The name")

    html = """
      <button aria-label="Blue" aria-labelledby="color">Red</button>
      <span id="color">Yellow</span>
    """
    dom = parse_html(html)
    get_by_role(dom, "button", name="Yellow")

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
    get_by_role(dom, "button", name="Yellow Red")

    html = """
    <html>
    <body>
    <button aria-label="Blue" aria-labelledby="color">Red</button>
    <span id="color">Yellow</span>
    </body>
    </html>
    """
    dom = parse_html(html)
    get_by_role(dom, "button", name="Yellow")

    html = """
      <a role="button" aria-label="Close popup" href="#close">
      <span aria-hidden="true">×</span></a>
    """
    dom = parse_html(html)
    get_by_role(dom, "button", name="Close popup")

    html = '<img src="tequila.png" alt="Chamukos tequila">'
    dom = parse_html(html)
    get_by_role(dom, "img", name="Chamukos tequila")

    html = """
    <a href="tequila.html">
      <img src="tequila.png" alt="Chamukos tequila">
    </a>'
    """
    dom = parse_html(html)
    get_by_role(dom, "link", name="Chamukos tequila")

    html = """
    <a href="tequila.html">
      <img src="tequila.png" alt="Chamukos tequila"> £40
    </a>
    """
    dom = parse_html(html)
    get_by_role(dom, "link", name="Chamukos tequila £40")

    html = """
    <button aria-label="Add Chamukos tequila to cart">Add to cart</button>
    """
    dom = parse_html(html)
    get_by_role(dom, "button", name="Add Chamukos tequila to cart")

    html = """
    <input type="search" aria-labelledby="this">
    <button id="this">Search</button>
    """
    dom = parse_html(html)
    get_by_role(dom, "searchbox", name="Search")

    html = """
        <label for="id_name">The name</label>
        <input type="text" name="name" id="id_name">
        <label for="id_surname">The surname</label>
        <input type="text" name="surname" id="id_surname">
    """
    dom = parse_html(html)
    get_by_role(dom, "textbox", name="The name")

    html = """
        <label for="id_name">The name</label>
        <input type="text" name="name" id="id_name">
        <label for="id_surname">The surname</label>
        <input type="text" name="surname" id="id_surname">
    """
    dom = parse_html(html)
    get_by_role(dom, "textbox", name="The name")
    get_by_role(dom, "textbox", name="The surname")


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
    get_by_role(
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
    get_by_role(dom, "button", name="Hello World")

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
    get_by_role(dom, "textbox", name="First Middle Last")


def test_get_by_role_cell():
    html = """
    <table role="table">
      <tbody>
      <tr>
        <td aria-label="Activation with identifier 8">
          ID: 8
        </td>
      </tr>
      </tbody>
    </table>
    """
    dom = parse_html(html)
    get_by_role(dom, "cell", name="Activation with identifier 8")

    html = """
    <table>
      <tbody>
      <tr>
        <td aria-label="Activation with identifier 8">
          ID: 8
        </td>
      </tr>
      </tbody>
    </table>
    """
    dom = parse_html(html)
    get_by_role(dom, "cell", name="Activation with identifier 8")

    html = """
    <table role="grid">
      <tbody>
      <tr>
        <td aria-label="Activation with identifier 8">
          ID: 8
        </td>
      </tr>
      </tbody>
    </table>
    """
    dom = parse_html(html)
    get_by_role(dom, "gridcell", name="Activation with identifier 8")

    html = """
    <table role="treegrid">
      <tbody>
      <tr>
        <td aria-label="Activation with identifier 8">
          ID: 8
        </td>
      </tr>
      </tbody>
    </table>
    """
    dom = parse_html(html)
    get_by_role(dom, "gridcell", name="Activation with identifier 8")

    html = """
    <table role="presentation">
      <tbody>
        <tr>
          <td>No role cell content</td>
        </tr>
      </tbody>
    </table>
    """
    dom = parse_html(html)
    with pytest.raises(NoElementsFoundError):
        get_by_role(dom, "cell")
    with pytest.raises(NoElementsFoundError):
        get_by_role(dom, "gridcell")


def test_get_by_role_img():
    html = """
        <div>
        <img alt="my funny image" src=""/>
        </div>
    """
    dom = parse_html(html)
    get_by_role(dom, "img")

    html = """
        <div>
        <img aria-label="the label" src=""/>
        </div>
    """
    dom = parse_html(html)
    get_by_role(dom, "img")

    html = """
        <div>
        <img aria-labelledby="the-label" src=""/>
        <span id="the-label">the image label<span/>
        </div>
    """
    dom = parse_html(html)
    get_by_role(dom, "img")


def test_get_by_role_img_no_accessible_name():
    html = """
        <div>
        <img alt=""/>
        </div>
    """
    dom = parse_html(html)
    get_by_role(dom, "presentation")

    html = """
         <div>
         <img/>
         </div>
     """
    dom = parse_html(html)
    get_by_role(dom, "presentation")


def test_gey_by_role_select():
    html = """
    <label for="pet-select">Choose a pet:</label>

    <select name="pets" id="pet-select">
      <option value="">--Please choose an option--</option>
      <option value="dog">Dog</option>
      <option value="cat">Cat</option>
      <option value="hamster">Hamster</option>
      <option value="parrot">Parrot</option>
      <option value="spider">Spider</option>
      <option value="goldfish">Goldfish</option>
    </select>
    """
    dom = parse_html(html)
    get_by_role(dom, "combobox")

    html = """
    <label for="shakes">Which shakes would you like to order?</label>
    <select id="shakes" name="shakes" size>
      <option>Vanilla Shake</option>
      <option>Strawberry Shake</option>
      <option>Chocolate Shake</option>
    </select>
    """
    dom = parse_html(html)
    get_by_role(dom, "combobox")

    html = """
    <label for="shakes">Which shakes would you like to order?</label>
    <select id="shakes" name="shakes" size="1">
      <option>Vanilla Shake</option>
      <option>Strawberry Shake</option>
      <option>Chocolate Shake</option>
    </select>
    """
    dom = parse_html(html)
    get_by_role(dom, "combobox")

    html = """
    <label for="shakes">Which shakes would you like to order?</label>
    <select id="shakes" name="shakes" size="2">
      <option>Vanilla Shake</option>
      <option>Strawberry Shake</option>
      <option>Chocolate Shake</option>
    </select>
    """
    dom = parse_html(html)
    get_by_role(dom, "listbox")

    html = """
    <label for="shakes">Which shakes would you like to order?</label>
    <select id="shakes" name="shakes" multiple>
      <option>Vanilla Shake</option>
      <option>Strawberry Shake</option>
      <option>Chocolate Shake</option>
    </select>
    """
    dom = parse_html(html)
    get_by_role(dom, "listbox")


def test_get_by_role_document():
    html = """
        <html>
        <body>
        <img alt=""/>
        </body>
        </html>
    """
    dom = parse_html(html)
    match = get_by_role(dom, "document")
    assert match.element.tag == "html"


def test_get_by_role_footer():
    html = """
    <html>
        <body>
            <footer>the footer</footer>
        </body>
    </html>
    """
    dom = parse_html(html)
    get_by_role(dom, "contentinfo")

    html = """
    <html>
        <body>
            <article>
            <footer>the footer</footer>
            </article>
        </body>
    </html>
    """
    dom = parse_html(html)
    generic = get_by_role(dom, "generic")
    assert generic.element.tag == "footer"

    html = """
    <html>
        <body>
            <aside>
            <footer>the footer</footer>
            </aside>
        </body>
    </html>
    """
    dom = parse_html(html)
    generic = get_by_role(dom, "generic")
    assert generic.element.tag == "footer"

    html = """
    <html>
        <body>
            <main>
            <footer>the footer</footer>
            </main>
        </body>
    </html>
    """
    dom = parse_html(html)
    generic = get_by_role(dom, "generic")
    assert generic.element.tag == "footer"

    html = """
    <html>
        <body>
            <nav>
            <footer>the footer</footer>
            </nav>
        </body>
    </html>
    """
    dom = parse_html(html)
    generic = get_by_role(dom, "generic")
    assert generic.element.tag == "footer"

    html = """
    <html>
        <body>
            <section>
            <footer>the footer</footer>
            </section>
        </body>
    </html>
    """
    dom = parse_html(html)
    generic = get_by_role(dom, "generic")
    assert generic.element.tag == "footer"

    html = """
    <div role="article">
      <h2>Heading of the segment</h2>
      <p>Paragraph for the segment.</p>
      <p>Another paragraph.</p>
      Controls to interact with the article, share it, etc.
      <footer>the footer</footer>
    </div>
    """
    dom = parse_html(html)
    generic = get_by_role(dom, "generic")
    assert generic.element.tag == "footer"

    html = """
    <div role="complementary">
        <h2>Our partners</h2>
        <footer>the footer</footer>
    </div>
    """
    dom = parse_html(html)
    generic = get_by_role(dom, "generic")
    assert generic.element.tag == "footer"

    html = """
    <div id="main" role="main">
      <h1>Avocados</h1>
      <footer>the footer</footer>
    </div>
    """
    dom = parse_html(html)
    generic = get_by_role(dom, "generic")
    assert generic.element.tag == "footer"

    html = """
    <div role="navigation" aria-label="Main">>
      <footer>the footer</footer>
    </div>
    """
    dom = parse_html(html)
    generic = get_by_role(dom, "generic")
    assert generic.element.tag == "footer"

    html = """
    <div role="region" aria-label="Example">>
      <footer>the footer</footer>
    </div>
    """
    dom = parse_html(html)
    generic = get_by_role(dom, "generic")
    assert generic.element.tag == "footer"


def test_get_by_role_paragraph():
    html = """
    <html>
        <body>
            <p>the paragraph</footer>
        </body>
    </html>
    """
    dom = parse_html(html)
    get_by_role(dom, "paragraph").to_have_text_content("the paragraph")
