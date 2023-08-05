"""Sphinx Julia theme."""
import os

__version__ = '0.0.2'
__version_full__ = __version__


def get_theme_dir():
    """
    Returns path to directory containing this package's theme.

    This is designed to be used when setting the ``html_theme_path``
    option within Sphinx's ``conf.py`` file.
    """
    return os.path.abspath(os.path.dirname(__file__))


def default_sidebars():
    """
    Returns a dictionary mapping for the templates used to render the
    sidebar on the index page and sub-pages.
    """
    return {
        '**': ['localtoc.html', 'relations.html', 'searchbox.html'],
        'index': ['searchbox.html'],
        'search': [],
    }


def get_html_theme_path():
    """Return list of HTML theme paths."""
    cur_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    return cur_dir
