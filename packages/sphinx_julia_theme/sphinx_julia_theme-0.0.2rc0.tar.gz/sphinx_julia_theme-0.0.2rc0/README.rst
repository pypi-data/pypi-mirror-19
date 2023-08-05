.. _readthedocs.org: http://www.readthedocs.org
.. _sphinx: http://www.sphinx-doc.org
.. _hidden: http://sphinx-doc.org/markup/toctree.html

******************
Julia Sphinx Theme
******************

.. contents:: 

.. image:: screen_mobile.png
    :width: 100%

Installation
============

Download the package or add it to your ``requirements.txt`` file:

.. code:: bash

    $ pip install sphinx_julia_theme

In your ``conf.py`` file:

.. code:: python

    import sphinx_julia_theme

    html_theme = "sphinx_julia_theme"

    html_theme_path = [sphinx_julia_theme.get_html_theme_path()]


Configuration
=============

You can configure different parts of the theme.

Project-wide configuration
--------------------------

The theme's project-wide options are defined in the ``sphinx_julia_theme/theme.conf``
file of this repository, and can be defined in your project's ``conf.py`` via
``html_theme_options``. For example:

.. code:: python

    html_theme_options = {
        'collapse_navigation': False,
        'display_version': False,
        'navigation_depth': 3,
    }

Page-level configuration
------------------------

Pages support metadata that changes how the theme renders.
You can currently add the following:

* ``:github_url:`` This will force the "Edit on GitHub" to the configured URL
* ``:bitbucket_url:`` This will force the "Edit on Bitbucket" to the configured URL
* ``:gitlab_url:`` This will force the "Edit on GitLab" to the configured URL

