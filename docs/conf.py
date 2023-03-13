from pkg_resources import get_distribution

import sys


project = "plone.distribution"
copyright = "2023, Plone Foundation"

# The full version, including alpha/beta/rc tags.
release = get_distribution(project).version
# The short X.Y version.
version = ".".join(release.split(".")[0:2])

# The suffix of source filenames.
source_suffix = {
    ".md": "markdown",
    ".rst": "restructuredtext",
}

extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.coverage",
    "sphinx.ext.doctest",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "sphinx_copybutton",
    "sphinx_design",
    "sphinxext.opengraph",
    "sphinx.ext.graphviz",
]
master_doc = "index"

# locale_dirs = ['translated/']
language = "en"

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass [howto/manual])
# This enables PDF generation.
latex_documents = [
    (
        "index",
        "ploneapi.tex",
        "plone.distribution Documentation",
        "",
        "manual",
    )
]


class Mock:
    def __init__(self, *args, **kwargs):
        pass

    def __call__(self, *args, **kwargs):
        return Mock()

    @classmethod
    def __getattr__(cls, name):
        if name in ("__file__", "__path__"):
            return "/dev/null"
        elif name[0] == name[0].upper():
            mockType = type(name, (), {})
            mockType.__module__ = __name__
            return mockType
        else:
            return Mock()


MOCK_MODULES = ["lxml"]
for mod_name in MOCK_MODULES:
    sys.modules[mod_name] = Mock()


# -- Options for myST markdown conversion to html -----------------------------

# For more information see:
# https://myst-parser.readthedocs.io/en/latest/syntax/optional.html
myst_enable_extensions = [
    "deflist",  # You will be able to utilise definition lists
    # https://myst-parser.readthedocs.io/en/latest/syntax/optional.html#definition-lists
    "colon_fence",  # You can also use ::: delimiters to denote code fences,\
    #  instead of ```.
    "substitution",  # plone.restapi \
    # https://myst-parser.readthedocs.io/en/latest/syntax/optional.html#substitutions-with-jinja2
    "html_image",  # For inline images. \
    # See https://myst-parser.readthedocs.io/en/latest/syntax/optional.html
]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_book_theme"
html_logo = "_static/logo.svg"
html_favicon = "_static/favicon.ico"
html_css_files = ["styles.css", ("print.css", {"media": "print"})]
html_static_path = [
    "_static",  # Last path wins. See https://github.com/plone/documentation/pull/1442
]
