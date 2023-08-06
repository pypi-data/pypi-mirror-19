Pelican FrontMark
=================

.. image:: https://travis-ci.org/noirbizarre/pelican-frontmark.svg?tag=1.0.1
    :target: https://travis-ci.org/noirbizarre/pelican-frontmark
    :alt: Build Status

.. image:: https://coveralls.io/repos/github/noirbizarre/pelican-frontmark/badge.svg?tag=1.0.1
    :target: https://coveralls.io/github/noirbizarre/pelican-frontmark?tag=1.0.1
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

Settings
********

- **`FRONTMARK_PARSE_LITERAL`**: `True` by default. Set it to `False` if you don't want multiline string literals (`|`)
  to be parsed as markdown.

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



.. _travis-badge: https://travis-ci.org/noirbizarre/pelican-frontmark.svg?tag=1.0.1
.. _travis-badge-url: https://travis-ci.org/noirbizarre/pelican-frontmark
.. _coveralls-badge: https://coveralls.io/repos/github/noirbizarre/pelican-frontmark/badge.svg?tag=1.0.1
.. _coveralls-badge-url: https://coveralls.io/github/noirbizarre/pelican-frontmark?tag=1.0.1
.. _license-badge: https://img.shields.io/pypi/l/pelican-frontmark.svg
.. _license-badge-url: https://pypi.python.org/pypi/pelican-frontmark
.. _format-badge: https://img.shields.io/pypi/format/pelican-frontmark.svg
.. _format-badge-url: https://pypi.python.org/pypi/pelican-frontmark
.. _python-version-badge: https://img.shields.io/pypi/pyversions/pelican-frontmark.svg
.. _python-version-badge-url: https://pypi.python.org/pypi/pelican-frontmark

Changelog
=========

1.0.1 (2017-01-08)
------------------

- Test and fix plugin registeration
- Make version and description available at module level

1.0.0 (2017-01-08)
------------------

- Initial release



