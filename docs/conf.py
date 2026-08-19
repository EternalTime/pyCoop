# Sphinx configuration for pyCoop documentation.
# Build:  sphinx-build -b html docs <outdir>
# Deployed at https://damiansowinski.com/pyCoop/

import os
import sys

sys.path.insert(0, os.path.abspath(".."))

project = "pyCoop"
author = "Damian R. Sowinski"
copyright = "2026, Damian R. Sowinski"
release = "0.1.0"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.mathjax",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx_copybutton",
]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "networkx": ("https://networkx.org/documentation/stable/", None),
    "matplotlib": ("https://matplotlib.org/stable/", None),
}

copybutton_prompt_text = r">>> |\.\.\. "
copybutton_prompt_is_regexp = True

autodoc_member_order = "bysource"
autodoc_typehints = "none"

templates_path = ["_templates"]
exclude_patterns = ["_build"]

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_css_files = ["custom.css"]
