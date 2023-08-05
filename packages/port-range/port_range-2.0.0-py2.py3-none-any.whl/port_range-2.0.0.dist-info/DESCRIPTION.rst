Port Range
==========

Port range with support of CIDR-like notation.

Stable release: |release| |versions| |license| |dependencies|

Development: |build| |coverage| |quality|

.. |release| image:: https://img.shields.io/pypi/v/port-range.svg
    :target: https://pypi.python.org/pypi/port-range
    :alt: Last release
.. |versions| image:: https://img.shields.io/pypi/pyversions/port-range.svg
    :target: https://pypi.python.org/pypi/port-range
    :alt: Python versions
.. |license| image:: https://img.shields.io/pypi/l/port-range.svg
    :target: https://opensource.org/licenses/BSD-2-Clause
    :alt: Software license
.. |dependencies| image:: https://requires.io/github/scaleway/port-range/requirements.svg?branch=master
    :target: https://requires.io/github/scaleway/port-range/requirements/?branch=master
    :alt: Requirements freshness
.. |build| image:: https://travis-ci.org/scaleway/port-range.svg?branch=develop
    :target: https://travis-ci.org/scaleway/port-range
    :alt: Unit-tests status
.. |coverage| image:: https://codecov.io/gh/scaleway/port-range/branch/develop/graph/badge.svg
    :target: https://codecov.io/github/scaleway/port-range?branch=develop
    :alt: Coverage Status
.. |quality| image:: https://scrutinizer-ci.com/g/scaleway/port-range/badges/quality-score.png?b=develop
    :target: https://scrutinizer-ci.com/g/scaleway/port-range/?branch=develop
    :alt: Code Quality


Features
--------

Support CIDR-like notation:

.. code-block:: python

    >>> from port_range import PortRange
    >>> pr = PortRange('1027/15')
    >>> pr.port_from
    1027
    >>> pr.port_to
    1028
    >>> pr.bounds
    (1027, 1028)

Parse and normalize port ranges:

.. code-block:: python

    >>> pr = PortRange(' 4242-42 ')
    >>> pr.bounds
    (42, 4242)
    >>> str(pr)
    '42-4242'

Enforce strong validatation in ``strict`` mode:

.. code-block:: python

    >>> PortRange(' 4242-42 ', strict=True)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "port_range/__init__.py", line 62, in __init__
        self.port_from, self.port_to = self.parse(port_range)
      File "port_range/__init__.py", line 109, in parse
        raise ValueError("Invalid reversed port range.")
    ValueError: Invalid reversed port range.

Access to decimal-representation properties:

.. code-block:: python

    >>> pr = PortRange('1027/15')
    >>> pr.base
    1027
    >>> pr.prefix
    15
    >>> pr.mask
    1
    >>> pr.offset
    3


License
-------

This software is licensed under the `BSD 2-Clause License`_.

.. _BSD 2-Clause License: https://github.com/scaleway/port-range/blob/develop/LICENSE.rst


`Changes for v2.0.0 (2015-12-19) <https://github.com/scaleway/port-range/compare/v1.0.5...v2.0.0>`_
---------------------------------------------------------------------------------------------------

* Refactor parsing. Makes normal mode stricter and ``strict`` mode more
  rigorous.
* Expose ``is_single_port`` and ``is_cidr`` properties in ``repr()``.
* Unittests covers 100% of code.
* Add default ``isort`` config.
* Run unittests against Python 3.3, 3.5, 3.6-dev, 3.7-dev, PyPy2.7 and PyPy3.3.
* Remove popularity badge: PyPI download counters are broken and no longer
  displayed.
* Move ``coverage`` config to ``setup.cfg``.
* Add ``test`` and ``develop`` dependencies.
* Only show latest changes in the long description of the package instead of
  the full changelog.
* Replace ``pep8`` package by ``pycodestyle``.
* Enforce ``pycodestyle`` checks in Travis CI jobs.
* Test production of packages in Travis CI jobs.
* Always check for package metadata in Travis CI jobs.
* Make wheels generated under Python 2 environnment available for Python 3 too.
* Add link to full changelog in package's long description.


`Full changelog <https://github.com/scaleway/port-range/blob/develop/CHANGES.rst#changelog>`_.

