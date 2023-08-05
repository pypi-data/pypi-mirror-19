========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |requires|
        |
    * - package
      - |version| |downloads| |wheel| |supported-versions| |supported-implementations|

.. |docs| image:: https://readthedocs.org/projects/attendant/badge/?style=flat
    :target: https://readthedocs.org/projects/attendant
    :alt: Documentation Status

.. |requires| image:: https://requires.io/github/LGuerra/attendant/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/LGuerra/attendant/requirements/?branch=master

.. |version| image:: https://img.shields.io/pypi/v/attendant.svg?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/attendant

.. |downloads| image:: https://img.shields.io/pypi/dm/attendant.svg?style=flat
    :alt: PyPI Package monthly downloads
    :target: https://pypi.python.org/pypi/attendant

.. |wheel| image:: https://img.shields.io/pypi/wheel/attendant.svg?style=flat
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/attendant

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/attendant.svg?style=flat
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/attendant

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/attendant.svg?style=flat
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/attendant


.. end-badges

General utilities for creating micro-services

* Free software: BSD license

Installation
============

::

    pip install attendant

Documentation
=============

https://attendant.readthedocs.io/

Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
