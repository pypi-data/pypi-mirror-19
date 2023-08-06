seed-papertrail
=============================

.. image:: https://img.shields.io/travis/praekeltfoundation/seed-papertrail.svg
        :target: https://travis-ci.org/praekeltfoundation/seed-papertrail

.. image:: https://img.shields.io/pypi/v/seed-papertrail.svg
        :target: https://pypi.python.org/pypi/seed-papertrail

.. image:: https://coveralls.io/repos/praekeltfoundation/seed-papertrail/badge.png?branch=develop
    :target: https://coveralls.io/r/praekeltfoundation/seed-papertrail?branch=develop
    :alt: Code Coverage

.. image:: https://readthedocs.org/projects/seed-papertrail/badge/?version=latest
    :target: https://seed-papertrail.readthedocs.org
    :alt: seed-papertrail Docs

Some utilities to time things and log things.

.. code-block:: python

  >>> import logging
  >>> formatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
  >>> logger = logging.getLogger('papertrail')
  >>> consoleHandler = logging.StreamHandler()
  >>> consoleHandler.setFormatter(formatter)
  >>> logger.addHandler(consoleHandler)
  >>> logger.setLevel(logging.DEBUG)


Usage as a function decorator
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

  >>> from seed_papertrail.decorators import papertrail
  >>> @papertrail.warn
  ... def testing(): print 1
  ...
  >>> testing()
  1
  2017-01-24 11:16:02,100 [MainThread  ] [WARNI]  __main__.testing 0.000021:

One can also specify a custom log message and a sample size argument:

.. code-block:: python

  >>> @papertrail.warn('this is likely to explode', sample=0.5)
  ... def testing(): print 1
  ...
  >>> testing()
  1
  >>> testing()
  1
  >>> testing()
  1
  2017-01-24 11:38:56,068 [MainThread  ] [WARNI]  __main__.testing 0.000018: this is likely to explode
  >>> testing()
  1
  2017-01-24 11:38:59,628 [MainThread  ] [WARNI]  __main__.testing 0.000019: this is likely to explode
  >>> testing()
  1
  >>>



Usage as a context manager
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

  >>> from seed_papertrail.decorators import papertrail
  >>> with papertrail.timer('hulloo') as l:
  ...     l.debug('more logging here!')
  ...     print 1
  ...
  2017-01-24 11:32:23,109 [MainThread  ] [DEBUG]  more logging here!
  1
  2017-01-24 11:32:23,115 [MainThread  ] [DEBUG]  0.002581: hulloo, threshold:OK
  >>>

You can also specify custom thresholds:

.. code-block:: python

  >>> with papertrail.timer('o_O', thresholds={'OK': (0, 0.1), 'FAIL': (0.1, 1000)}):
  ...     time.sleep(6)
  ...
  2017-01-24 11:45:00,717 [MainThread  ] [DEBUG]  6.000664: o_O, threshold:FAIL

Addtionally the ``timer`` function allows one to specify the following keyword arguments:

* ``level`` the logging level, defaults to ``DEBUG``
* ``logger`` the logger to log to, defaults to ``papertrail``
