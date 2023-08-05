=========================================================
A Python statsd client with DogTag-compatible tag support
=========================================================

statsd_ is a friendly front-end to Graphite_. This is a Python client
for the statsd daemon. More specifically, this is a fork of jsocol's
pystatsd client, with the addition of support for DogTag-compatible
tags.

:Code:          https://github.com/toddjames/statsd-tags
:License:       MIT; see LICENSE file
:Issues:        https://github.com/toddjames/statsd-tags/issues
:Documentation: https://statsd-tags.readthedocs.io/

Quickly, to use:

.. code-block:: python

    >>> import statsd
    >>> c = statsd.StatsClient('localhost', 8125)
    >>> c.incr('foo')  # Increment the 'foo' counter.
    >>> c.timing('stats.timed', 320)  # Record a 320ms 'stats.timed'.

You can also add a prefix to all your stats:

.. code-block:: python

    >>> import statsd
    >>> c = statsd.StatsClient('localhost', 8125, prefix='foo')
    >>> c.incr('bar')  # Will be 'foo.bar' in statsd/graphite.

DogTag-compatible tags are supported, as well:

.. code-block:: python

    >>> import statsd
    >>> c = statsd.StatsClient('localhost', 8125)
    >>> c.gauge('baz', 42, tags=['production', 'fqdn': 'example.org'])


Installing
==========

The easiest way to install statsd is with pip!

You can install from PyPI::

    $ pip install statsd-tags

Or GitHub::

    $ pip install -e git+https://github.com/toddjames/statsd-tags#egg=statsd

Or from source::

    $ git clone https://github.com/toddjames/statsd-tags
    $ cd statsd-tags
    $ python setup.py install


Docs
====

There are lots of docs in the ``docs/`` directory and on ReadTheDocs_.


.. _statsd: https://github.com/etsy/statsd
.. _Graphite: https://graphite.readthedocs.io/
.. _ReadTheDocs: https://statsd-tags.readthedocs.io/en/latest/index.html
