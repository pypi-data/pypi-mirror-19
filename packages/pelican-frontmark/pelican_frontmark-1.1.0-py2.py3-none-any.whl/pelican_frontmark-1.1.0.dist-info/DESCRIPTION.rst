Pelican FrontMark
=================

.. image:: https://travis-ci.org/noirbizarre/pelican-frontmark.svg?tag=1.1.0
    :target: https://travis-ci.org/noirbizarre/pelican-frontmark
    :alt: Build Status

.. image:: https://coveralls.io/repos/github/noirbizarre/pelican-frontmark/badge.svg?tag=1.1.0
    :target: https://coveralls.io/github/noirbizarre/pelican-frontmark?tag=1.1.0
    :alt: Coverage Status

.. image:: https://img.shields.io/pypi/l/pelican-frontmark.svg
    :target: https://pypi.python.org/pypi/pelican-frontmark
    :alt: License

.. image:: https://img.shields.io/pypi/format/pelican-frontmark.svg
    :target: https://pypi.python.org/pypi/pelican-frontmark
    :alt: Format

.. image:: https://img.shields.io/pypi/pyversions/pelican-frontmark.svg
    :target: https://pypi.python.org/pypi/pelican-frontmark
    :alt: Supported versions



A Pelican CommonMark/Front Matter reader.

This reader marse Markdown files with YAML frontmatter headers and formatted using the CommonMark specifications.


Requirements
------------

Pelican FrontMark works with Pelican 3.7+ and Python 3.3+

Getting started
---------------

Install `pelican-frontmark` with pip:

.. code-block:: shell

    pip install pelican-frontmark



And enable the plugin in you `pelicanconf.py` (or any configuration file you want to use):

.. code-block:: Python

    PLUGINS = [
        '...',
        'frontmark',
        '...',
    ]



Files format
------------

Frontmark will only recognize files using `.md` extension.

Here an article example:

.. code-block:: 

    ---
    title: My article title
    date: 2017-01-04 13:10
    modified: 2017-01-04 13:13
    tags:
      - tag 1
      - tag 2
    slug: my-article-slug
    lang: en
    category: A category
    authors: Me
    summary: Some summary
    status: draft

    custom:
      title: A custom metadata
      details: You can add any structured and typed YAML metadata

    ---

    My article content




Advanced configuration
----------------------

Syntax highlighting
*******************

By default, `FrontMark` outputs code blocks in a standard html5 way,
ie. a `pre>code` block with a language class.
This allow to use any html5 syntax highlight JavaScript lib.

You can force Pygments usage to output html4 pre rendered syntax highlight
by setting `FRONTMARK_PYGMENTS` to `True` for default parameters
or manually setting it to a dict of Pygments HtmlRenderer parameters.

.. code-block:: python

    FRONTMARK_PYGMENTS = {
        'linenos': 'inline',
    }



Settings
********

- **`FRONTMARK_PARSE_LITERAL`**: `True` by default. Set it to `False` if you don't want multiline string literals (`|`)
  to be parsed as markdown.

- **`FRONTMARK_PYGMENTS`**: Not defined by default and output standard html5 code blocks.
  Can be set to `True` to force Pygments usage with default parameters or a `dict` of
  `Pygments parameters <http://docs.getpelican.com/en/stable/content.html#internal-pygments-options>`_


Registering custom YAML types
*****************************

You can register custom YAML types using the `frontmark_yaml_register` signal:

.. code-block:: python

    from frontmark.signals import frontmark_yaml_register


    def upper_constructor(loader, noder):
        return loader.construct_scalar(node).upper()


    def register_upper(reader):
        return '!upper', upper_constructor


    def register():
        frontmark_yaml_register.connected(register_upper):



Testing
-------

To test the plugin against all supported Python versions, run tox:

.. code-block:: shell

    tox



To test only within your current Python version with pytest:

.. code-block:: shell

    pip install -e .[test]  # Install with test dependencies
    pytest  # Launch pytest test suite



or let setuptools do the job:

.. code-block:: shell

    python setup.py test




.. _travis-badge: https://travis-ci.org/noirbizarre/pelican-frontmark.svg?tag=1.1.0
.. _travis-badge-url: https://travis-ci.org/noirbizarre/pelican-frontmark
.. _coveralls-badge: https://coveralls.io/repos/github/noirbizarre/pelican-frontmark/badge.svg?tag=1.1.0
.. _coveralls-badge-url: https://coveralls.io/github/noirbizarre/pelican-frontmark?tag=1.1.0
.. _license-badge: https://img.shields.io/pypi/l/pelican-frontmark.svg
.. _license-badge-url: https://pypi.python.org/pypi/pelican-frontmark
.. _format-badge: https://img.shields.io/pypi/format/pelican-frontmark.svg
.. _format-badge-url: https://pypi.python.org/pypi/pelican-frontmark
.. _python-version-badge: https://img.shields.io/pypi/pyversions/pelican-frontmark.svg
.. _python-version-badge-url: https://pypi.python.org/pypi/pelican-frontmark
.. _pygments-options: http://docs.getpelican.com/en/stable/content.html#internal-pygments-options

Changelog
=========

1.1.0 (2017-01-22)
------------------

- Added `FRONTMARK_PYGMENTS` optionnal setting for Pygments rendering
- Fix links handling (ie. `{filename}`...)

1.0.1 (2017-01-08)
------------------

- Test and fix plugin registeration
- Make version and description available at module level

1.0.0 (2017-01-08)
------------------

- Initial release



