# Unbrowsed

A browserless HTML testing library for Python, inspired by [testing-library](https://testing-library.com/).

## Overview

Unbrowsed allows you to test HTML without spawning a browser. It provides a simple, intuitive API for querying HTML elements similar to testing-library's approach, encouraging accessible and maintainable tests.

## Features

- Fast HTML parsing using [selectolax](https://github.com/rushter/selectolax)
- Browser-free testing of HTML content
- Query functions that encourage accessible testing practices
- Simple, Pythonic API

## Installation

```bash
pip install unbrowsed
```

## Usage

### Basic Example

```python
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
```

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/username/unbrowsed.git
cd unbrowsed

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[test]"
```

### Running Tests

```bash
pytest
```

### Releasing a New Version

To release a new version:

1. Update the version in `pyproject.toml`
2. Create and push a new tag:

```bash
git tag 0.1.0
git push origin 0.1.0
```

This will trigger the CI pipeline to build and publish the package to PyPI automatically.

## License

MIT
