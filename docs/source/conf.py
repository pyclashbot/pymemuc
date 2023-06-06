import os
import sys

sys.path.insert(0, os.path.abspath("."))
sys.path.insert(0, os.path.abspath(".."))
sys.path.insert(0, os.path.abspath("../.."))


project = "pymemuc"
copyright = "2023, Martin Miglio"  # noqa #pylint: disable=redefined-builtin
author = "Martin Miglio"

locale_dirs = ["locales/"]

extensions = [
    "sphinx.ext.todo",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinxext.opengraph",
    "sphinx_copybutton",
]
templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

autodoc_default_options = {
    "member-order": "bysource",
}
add_module_names = False


html_theme = "furo"
html_theme_options = {
    "sidebarwidth": "19em",
}
html_static_path = ["_static"]
htmlhelp_basename = "pymemuc"
intersphinx_mapping = {"Python Docs": ("http://docs.python.org/", None)}
