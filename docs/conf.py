"""Sphinx configuration."""
project = "Numbers2Words Greek"
author = "Georgios K."
copyright = "2022, Georgios K."
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "furo"
