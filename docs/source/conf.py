# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys

PATH = os.path.abspath(os.path.dirname(__file__))

sys.path.append(os.path.abspath(os.path.join(PATH, os.pardir, os.pardir, "src")))

project = 'Python Darwin Core Archive'
copyright = '2024, IEB-BIODATA'
author = 'Juan Saez Hidalgo'
release = '0.0.5'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.inheritance_diagram',
    'numpydoc',
]

autosummary_generate = True
numpydoc_show_class_members = True

templates_path = ['_templates']
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'pydata_sphinx_theme'

html_static_path = ['_static',]
html_js_files = [
    '_js/pypi-icon.js',
]

html_title = "Python Darwin Core Archive"

html_sidebars = {
    "index": [],
    "install": [],
    "usage": [],
}

html_theme_options = {
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/IEB-BIODATA/pydwca",
            "icon": "fa-brands fa-github",
        },
        {
            "name": "PyPI",
            "url": "https://pypi.org/project/pydwca/",
            "icon": "fa-custom fa-pypi",
        },
    ]
}
