========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor| |requires|
        | |coveralls| |codecov|
        | |landscape| |scrutinizer| |codacy| |codeclimate|
	| |p3| |pup|
    * - package
      - |version| |downloads| |wheel| |supported-versions| |supported-implementations|

.. |docs| image:: https://readthedocs.org/projects/omniglot/badge/?style=flat
    :target: https://readthedocs.org/projects/omniglot
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/j340m3/omniglot.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/j340m3/omniglot

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/j340m3/omniglot?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/j340m3/omniglot

.. |requires| image:: https://requires.io/github/j340m3/omniglot/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/j340m3/omniglot/requirements/?branch=master

.. |coveralls| image:: https://coveralls.io/repos/j340m3/omniglot/badge.svg?branch=master&service=github
    :alt: Coverage Status
    :target: https://coveralls.io/github/j340m3/omniglot

.. |codecov| image:: https://codecov.io/github/j340m3/omniglot/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/j340m3/omniglot

.. |landscape| image:: https://landscape.io/github/j340m3/omniglot/master/landscape.svg?style=flat
    :target: https://landscape.io/github/j340m3/omniglot/master
    :alt: Code Quality Status

.. |codacy| image:: https://api.codacy.com/project/badge/Grade/46d7b7af5db442278b3d7fa1798bbed4
   :target: https://www.codacy.com/app/bergmann-jerome/omniglot?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=j340m3/omniglot&amp;utm_campaign=Badge_Grade

.. |codeclimate| image:: https://codeclimate.com/github/j340m3/omniglot/badges/gpa.svg
   :target: https://codeclimate.com/github/j340m3/omniglot
   :alt: CodeClimate Quality Status

.. |version| image:: https://img.shields.io/pypi/v/omniglot.svg?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/omniglot

.. |downloads| image:: https://img.shields.io/pypi/dm/omniglot.svg?style=flat
    :alt: PyPI Package monthly downloads
    :target: https://pypi.python.org/pypi/omniglot

.. |wheel| image:: https://img.shields.io/pypi/wheel/omniglot.svg?style=flat
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/omniglot

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/omniglot.svg?style=flat
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/omniglot

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/omniglot.svg?style=flat
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/omniglot

.. |scrutinizer| image:: https://img.shields.io/scrutinizer/g/j340m3/omniglot/master.svg?style=flat
    :alt: Scrutinizer Status
    :target: https://scrutinizer-ci.com/g/j340m3/omniglot/

.. |pup| image:: https://pyup.io/repos/github/j340m3/omniglot/shield.svg
     :target: https://pyup.io/repos/github/j340m3/omniglot/
     :alt: Updates

.. |p3| image:: https://pyup.io/repos/github/j340m3/omniglot/python-3-shield.svg
     :target: https://pyup.io/repos/github/j340m3/omniglot/
     :alt: Python 3

.. end-badges

A programming language with mutable syntax and semantics.

* Free software: BSD license

Installation
============

::

    pip install omniglot

Documentation
=============

https://omniglot.readthedocs.io/

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
