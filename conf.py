# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------

project = "RelEng"
copyright = "2023, Mozilla Release Engineering"
author = "Mozilla Release Engineering"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinxcontrib.spelling",
    "recommonmark",
]

spelling_word_list_filename = ["releng_wordlist.txt"]

# turn on todo output
todo_include_todos = True

# Allow for markdown
source_parsers = {".md": "recommonmark.parser.CommonMarkParser"}
source_suffix = [".rst", ".md"]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# Intersphinx allows linking to external Sphinx based documentation using the
# standard roles and directives.
intersphinx_mapping = {
    "balrog": ("https://mozilla-balrog.readthedocs.io/en/latest", None),
    "firefox": ("https://firefox-source-docs.mozilla.org", None),
    "scriptworker": ("https://scriptworker.readthedocs.io/en/latest", None),
    "scriptworker-scripts": (
        "https://scriptworker-scripts.readthedocs.io/en/latest",
        None,
    ),
    "taskgraph": ("https://taskcluster-taskgraph.readthedocs.io/en/latest", None),
}

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_title = "RelEng Docs"
html_theme = "sphinx_book_theme"
html_theme_options = {
    "logo": {
        "image_light": "media/releng.png",
        "image_dark": "media/releng-dark.png",
    },
}
