# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path().absolute().parent.parent.parent))
import xrdimageutil

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

gh_org = "henryjsmith12"
project = "xrd-image-util"
copyright = "2023, Henry Smith"
author = "Henry Smith"

extensions = """
    sphinx.ext.autodoc
    sphinx.ext.autosummary
    sphinx.ext.coverage
    sphinx.ext.githubpages
    sphinx.ext.inheritance_diagram
    sphinx.ext.mathjax
    sphinx.ext.todo
    sphinx.ext.viewcode
""".split()

templates_path = ["_templates"]
exclude_patterns = []

html_theme = "pydata_sphinx_theme"
html_baseurl = '/xrd-image-util/'
html_theme_options = {
    "github_url": "https://github.com/henryjsmith12/xrd-image-util",
    "navbar_center": ["navbar-nav"],
    "navbar_end": ["navbar-icon-links", "theme-switcher"],
    "navbar_persistent": ["search-button"],
    "navbar_align": "content",
    "show_toc_level": 2
}
