Installation
===========

Requirements
-----------

Unbrowsed requires Python 3.8 or higher.

Basic Installation
-----------------

You can install Unbrowsed using pip:

.. code-block:: bash

    pip install unbrowsed

Development Installation
-----------------------

For development, you can clone the repository and install it in development mode:

.. code-block:: bash

    # Clone the repository
    git clone https://github.com/username/unbrowsed.git
    cd unbrowsed

    # Create a virtual environment
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate

    # Install development dependencies
    pip install -e ".[test,docs]"
