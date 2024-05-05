# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join("..", "..", "..")))

project = 'CRUDCreator'
copyright = '2024, $name$, $email$'
author = '$name$'
release = '0.0.41'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",#https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html
    "sphinxcontrib.autodoc_pydantic",#https://autodoc-pydantic.readthedocs.io/en/stable/users/configuration.html
    "sphinx_rtd_theme",#https://sphinx-rtd-theme.readthedocs.io/en/stable/configuring.html
    "sphinx_sitemap",#https://sphinx-sitemap.readthedocs.io/en/latest/
    "sphinx.ext.linkcode"
]

templates_path = ['_templates']
exclude_patterns = []

language = 'en'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_logo = "images/logo.svg"
html_favicon = "images/favicon.png"
html_show_sourcelink = False
html_baseurl = "https://www.crudcreator.com/"
sitemap_url_scheme = "{link}"
html_context = {
    "display_github": True,
    "github_user": "nedelab",
    "github_repo": "crudcreator",
    "github_version": "master",
    "conf_py_path": "/src/crudcreator/docs/source/", # Path in the checkout to the docs root
}
html_theme_options = {
    "show_powered_by": False,
    "show_relbars": True,
    "page_width": "90%",
    "extra_nav_links": {
        "Company website : www.nedelab.com": "https://www.nedelab.com/"
    }
}
html_title = ""
autodoc_member_order = "groupwise"
autodoc_typehints = "both"
python_maximum_signature_line_length = 1
autodoc_pydantic_settings_show_config_summary = False
autodoc_pydantic_model_show_config_summary = False

def setup(app):
    app.add_js_file("replace.js", loading_method="defer")
    app.add_css_file("custom.css")

def linkcode_resolve(domain, info):
    file_path = info["module"].replace(".", "/")
    return f"https://github.com/nedelab/crudcreator/tree/master/src/{file_path}.py"

import crudcreator.proxy.proxy#https://github.com/pydantic/pydantic/discussions/7763#discussioncomment-8417097
import crudcreator.adaptator.sql.SimpleSQLAdaptator
import crudcreator.source.source.SQLSource
import crudcreator.adaptator.sql.proxy.SQLFilter