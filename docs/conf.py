# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
import sys
from pathlib import Path

project = "unbrowsed"
copyright = "2025, Valentino Gagliardi"
author = "Valentino Gagliardi"
release = "0.1.0a13"

# -- General configuration ---------------------------------------------------
extensions = [
    "sphinx.ext.napoleon",
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
]

autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": True,
}

exclude_patterns = [
    ".venv",
    "_build",
]

language = "en"

# -- Options for HTML output -------------------------------------------------
html_theme = "furo"

# -- Intersphinx configuration -----------------------------------------------
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "selectolax": ("https://selectolax.readthedocs.io/en/latest/", None),
}

# -- Setup for autodoc -------------------------------------------------------
here = Path(__file__).parent.resolve()
sys.path.insert(0, str(here / ".." / "src"))
