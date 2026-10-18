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
    "myst_nb",
]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "networkx": ("https://networkx.org/documentation/stable/", None),
    "matplotlib": ("https://matplotlib.org/stable/", None),
}

copybutton_prompt_text = r">>> |\.\.\. "
copybutton_prompt_is_regexp = True
# Copy buttons go on code, not on the outputs of notebook cells.
copybutton_selector = "div:not(.output) > div.highlight pre"

# Pages written as Jupyter notebooks (docs/*.ipynb) are run from top to
# bottom on every build, so the outputs a reader sees always come from the
# code beside them and the repository stores the notebooks without outputs.
# A cell that raises fails the build, just like a warning does.  They run in
# a temporary directory, so files a guide saves along the way (the paw.gif of
# Getting Started) do not land in docs/.
nb_execution_mode = "force"
nb_execution_raise_on_error = True
nb_execution_timeout = 900
nb_execution_in_temp = True

# Notebook text writes math as $...$ and $$...$$, which Jupyter and Colab
# render too, where the {math} role would show up as raw markup.
myst_enable_extensions = ["dollarmath"]

# Every notebook page gets buttons that open it, runnable, on Binder and on
# Google Colab (see docs/_templates/page.html).  Both services read the
# notebook from this public repository and branch.
html_context = {
    "launch_repo": "EternalTime/pyCoop",
    "launch_branch": "main",
    "launch_path": "docs",
}

autodoc_member_order = "bysource"
autodoc_typehints = "none"

templates_path = ["_templates"]
source_suffix = {
    ".rst": "restructuredtext",
    ".ipynb": "myst-nb",
}
# myst-nb keeps its executed copies of the notebooks in jupyter_execute/, next
# to the output directory; they are not pages of their own.
exclude_patterns = ["_build", "jupyter_execute", "**.ipynb_checkpoints"]

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_css_files = ["custom.css"]


# -- Plain dash between a parameter's type and its description -------------
# Sphinx and napoleon join them with " -- ", which smart quotes draw as an
# en dash.

from docutils import nodes
from sphinx.transforms import SphinxTransform


class PlainDashFieldSeparator(SphinxTransform):
    default_priority = 700  # before smart quotes, which run at 750

    def apply(self, **kwargs):
        for body in self.document.findall(nodes.field_body):
            for text in list(body.findall(nodes.Text)):
                if " -- " in text and not isinstance(text.parent, nodes.literal):
                    plain = nodes.Text(str(text).replace(" -- ", " - "))
                    text.parent.replace(text, plain)


def setup(app):
    app.add_transform(PlainDashFieldSeparator)
