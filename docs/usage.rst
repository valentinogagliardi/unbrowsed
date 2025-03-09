Usage
=====

Basic Usage
-----------

unbrowsed provides a simple API for testing HTML content without a browser. Here's a basic example:

.. code-block:: python

    from unbrowsed import parse_html, query_by_label_text

    # Parse HTML content
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

    # Query elements by label text
    username_input = query_by_label_text(dom, "Username")
    assert username_input is not None

Querying Elements
-----------------

unbrowsed provides several query functions inspired by testing-library:

Query by Text
~~~~~~~~~~~~~

Find elements containing specific text:

.. code-block:: python

    from unbrowsed import parse_html, query_by_text, get_by_text

    html = """
    <div>
        <h1>Welcome to my site</h1>
        <p>This is a paragraph</p>
        <button>Click me</button>
    </div>
    """
    dom = parse_html(html)

    # query_by_text returns None if no element is found
    heading = query_by_text(dom, "Welcome")
    assert heading.tag == "h1"

    # get_by_text raises an exception if no element is found
    button = get_by_text(dom, "Click me")
    assert button.tag == "button"

Query by Label Text
~~~~~~~~~~~~~~~~~~~

Find form elements by their associated label text:

.. code-block:: python

    from unbrowsed import parse_html, query_by_label_text

    html = """
    <form>
        <label for="email">Email Address</label>
        <input id="email" type="email">
    </form>
    """
    dom = parse_html(html)

    email_input = query_by_label_text(dom, "Email Address")
    assert email_input.attributes.get("type") == "email"

Assertions
---------~

Unbrowsed provides assertion helpers for testing element properties:

.. code-block:: python

    from unbrowsed import parse_html, get_by_text, to_have_attribute

    html = """
    <div>
        <a href="https://example.com" class="link">Visit Example</a>
    </div>
    """
    dom = parse_html(html)

    link = get_by_text(dom, "Visit Example")
    assert to_have_attribute(link, "href", "https://example.com")
    assert to_have_attribute(link, "class", "link")
