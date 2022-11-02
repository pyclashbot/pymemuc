import os
import sys

sys.path.insert(0, os.path.abspath("."))
sys.path.insert(0, os.path.abspath(".."))
sys.path.insert(0, os.path.abspath("../.."))


project = "pymemuc"
copyright = "2022, Martin Miglio"
author = "Martin Miglio"

extensions = [
    "sphinx.ext.todo",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
]
templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

autodoc_default_options = {
    'member-order': 'bysource',
}
add_module_names = False


html_theme = "classic"
html_theme_options = {
    "sidebarwidth": "19em",
}
html_static_path = ["_static"]
htmlhelp_basename = "pymemuc"
intersphinx_mapping = {"http://docs.python.org/": None}
