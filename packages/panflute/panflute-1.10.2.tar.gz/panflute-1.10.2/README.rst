:Date:   January 16, 2017

.. contents::
   :depth: 3
..

Panflute: Pythonic Pandoc Filters
=================================

|Python version| |PyPI version| |Development Status| |Build Status|

`panflute <http://scorreia.com/software/panflute/>`__ is a Python
package that makes creating Pandoc filters fun.

For a detailed user guide, documentation, and installation instructions,
see http://scorreia.com/software/panflute/. If you want to contribute,
head `here </CONTRIBUTING.md>`__.

Install
-------

To install panflute, open the command line and type:

.. code:: bash

    pip install panflute

-  Support Python 2.7, 3.3 or later, pypy, and pypy3.
-  On windows, the command line (``cmd``) must be run as administrator.

Uninstall
---------

.. code:: bash

    pip uninstall panflute

Dev Install
-----------

After cloning the repo and opening the panflute folder:

``python setup.py install``
    installs the package locally
``python setup.py develop``
    installs locally with a symlink so changes are automatically updated

In addition, if you use python2, you need to pasteurize the code before
running tests. In this directory, Run

.. code:: bash

    # install pasteurize if you didn't have it yet
    pip2 install -U future
    pasteurize -wnj 4 .

Contributing
------------

Feel free to submit push requests. For consistency, code should comply
with `pep8 <https://pypi.python.org/pypi/pep8>`__ (as long as its
reasonable), and with the style guides by
[@kennethreitz](http://docs.python-guide.org/en/latest/writing/style/)
and `google <http://google.github.io/styleguide/pyguide.html>`__. Read
more `here </CONTRIBUTING.md>`__.

License
-------

BSD3 license (following ``pandocfilters`` by @jgm).

.. |Python version| image:: https://img.shields.io/pypi/pyversions/panflute.svg
   :target: https://pypi.python.org/pypi/panflute/
.. |PyPI version| image:: https://img.shields.io/pypi/v/panflute.svg
   :target: https://pypi.python.org/pypi/panflute/
.. |Development Status| image:: https://img.shields.io/pypi/status/panflute.svg
   :target: https://pypi.python.org/pypi/panflute/
.. |Build Status| image:: https://travis-ci.org/sergiocorreia/panflute.svg?branch=master
   :target: https://travis-ci.org/sergiocorreia/panflute
