python-ivona-api
================

|Build status| |Test coverage| |PyPI version| |Python versions|
|License|

Python library that helps you connect to Amazon's
`IVONA <https://www.ivona.com/>`__ Speech Cloud from within your Python
project. All you need to use it are the `access
keys <http://developer.ivona.com/en/speechcloud/introduction.html#Credentials>`__.

It currently only implements ``CreateSpeech`` and ``ListVoices``
endpoints, as they should cover the vast majority of use cases. Lexicons
endpoints may be added in the future.

If you're looking for out-of-the-box solution, you should probably use
`ivona-speak <https://github.com/Pythonity/ivona-speak>`__ - it's a
script that uses this library and lets you use its functionality
directly from your shell.

Installation
------------

With PyPI:

::

    $ pip install ivona_api

API
---

There's no documentation as of now, but the code is commented and
*should* be pretty straightforward to use.

That said - feel free to ask `me <mailto:pawel.adamczak@sidnet.info>`__
if anything is unclear.

Tests
-----

Package was tested with the help of ``py.test`` and ``tox`` on Python
2.7, 3.4, 3.5 and 3.6 (see ``tox.ini``).

To run tests yourself you need to set environment variables with secret
and access keys before running ``tox``:

Code coverage is available at
`Coveralls <https://coveralls.io/github/Pythonity/python-ivona-api>`__.

.. code:: shell

    $ pip install -r requirements/dev.txt
    $ export IVONA_ACCESS_KEY="YOUR_ACTUAL_ACCESS_KEY"
    $ export IVONA_SECRET_KEY="YOUR_ACTUAL_SECRET_KEY"
    $ tox

Contributions
-------------

Package source code is available at
`GitHub <https://github.com/Pythonity/python-ivona-api>`__.

Feel free to use, ask, fork, star, report bugs, fix them, suggest
enhancements, add functionality and point out any mistakes. Thanks!

Authors
-------

Developed and maintained by `Pythonity <http://pythonity.com/>`__.

Written by `Paweł Adamczak <https://github.com/pawelad>`__.

.. |Build status| image:: https://img.shields.io/travis/Pythonity/python-ivona-api.svg
   :target: https://travis-ci.org/Pythonity/python-ivona-api
.. |Test coverage| image:: https://img.shields.io/coveralls/Pythonity/python-ivona-api.svg
   :target: https://coveralls.io/github/Pythonity/python-ivona-api
.. |PyPI version| image:: https://img.shields.io/pypi/v/ivona_api.svg
   :target: https://pypi.python.org/pypi/ivona_api
.. |Python versions| image:: https://img.shields.io/pypi/pyversions/ivona_api.svg
   :target: https://pypi.python.org/pypi/ivona_api
.. |License| image:: https://img.shields.io/github/license/Pythonity/python-ivona-api.svg
   :target: https://github.com/Pythonity/python-ivona-api/blob/master/LICENSE


