Contributing
===========

Thank you for considering contributing to Unbrowsed! This document provides guidelines and instructions for contributing to the project.

Setting Up Development Environment
---------------------------------

1. Fork the repository on GitHub
2. Clone your fork locally:

   .. code-block:: bash

       git clone https://github.com/your-username/unbrowsed.git
       cd unbrowsed

3. Create a virtual environment and install development dependencies:

   .. code-block:: bash

       python -m venv venv
       source venv/bin/activate  # On Windows: venv\Scripts\activate
       pip install -e ".[test,docs]"

Running Tests
------------

Unbrowsed uses pytest for testing. To run the tests:

.. code-block:: bash

    pytest

To run tests with coverage:

.. code-block:: bash

    pytest --cov=unbrowsed

Code Style
---------

Unbrowsed follows PEP 8 style guidelines. Please ensure your code adheres to these standards.

Documentation
------------

When adding new features, please update the documentation accordingly:

1. Add docstrings to all public modules, functions, classes, and methods
2. Update the relevant documentation files in the ``docs/source`` directory
3. Build the documentation to verify your changes:

   .. code-block:: bash

       cd docs
       make html

Pull Request Process
------------------

1. Create a new branch for your feature or bugfix
2. Make your changes and commit them with clear, descriptive commit messages
3. Push your branch to your fork on GitHub
4. Submit a pull request to the main repository
5. Ensure all tests pass and the documentation builds correctly

Reporting Issues
--------------

If you find a bug or have a feature request, please open an issue on the GitHub repository. Please include:

- A clear, descriptive title
- A detailed description of the issue or feature request
- Steps to reproduce the issue (for bugs)
- Expected behavior and actual behavior (for bugs)
- Any relevant code snippets or error messages
