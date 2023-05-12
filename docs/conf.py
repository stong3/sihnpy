# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------

project = u"sihnpy"
copyright = u"2022, Frederic St-Onge"
author = u"Frederic St-Onge"

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "myst_nb",
    "autoapi.extension",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.autosectionlabel"
]
autoapi_dirs = ["../src"]
autosectionlabel_prefix_document = True #Goes with ext. autosection label. Ensures targets
# are unique

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"
html_logo = "images/sihnpy_logo_small_no_bg.png" #Page logo for ReadTheDocs (200px max)
html_favicon = "images/sihnpy_logo_small_no_bg.png" #Page icon browser logo
myst_html_meta = { #Google Analytics Verification into the meta data of each page.
    "description lang=en":"Simple set of analytical tools to study inter-individual differences in neuroimaging.",
    "google-site-verification":"tL6GkVwBg1SO3nHWAJDCJsB03NTrUvxkYPAWrMWuwj0"
}