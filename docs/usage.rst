Usage
=====

Basic Usage
-----------

unbrowsed provides a simple API for testing HTML content without a browser. Here's a basic example:

.. code-block:: python

    from unbrowsed import parse_html, query_by_label_text

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

Querying Elements
-----------------

unbrowsed provides several query functions inspired by testing-library:

By Text
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

    assert query_by_text(dom, "Welcome", exact=False)
    assert get_by_text(dom, "Click me")

By Label Text
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

    assert query_by_label_text(dom, "Email Address")
    assert get_by_label_text(dom, "Email Address")

Assertions
----------

unbrowsed provides assertion helpers for testing element properties:

.. code-block:: python

    from unbrowsed import parse_html, get_by_text

    html = """
    <div>
        <a href="https://example.com" class="link">Visit Example</a>
    </div>
    """
    dom = parse_html(html)

    link = get_by_text(dom, "Visit Example")
    assert link.to_have_attribute("href", "https://example.com")
    assert link.to_have_attribute("class", "link")


Usage with Django
-----------------

unbrowsed can be used in Django to test the HTML returned from responses:

.. code-block:: python

    from django.test import TestCase
    from unbrowsed import parse_html, get_by_label_text


    class TestBookCreateView(TestCase):
        def test_form_labels(self):
            response = self.client.get("/books/create/")
            dom = parse_html(response.content)

            expected_labels = [
                "Insert the book title",
                "Select the book authors",
            ]

            for label in expected_labels:
                get_by_label_text(dom, label)
