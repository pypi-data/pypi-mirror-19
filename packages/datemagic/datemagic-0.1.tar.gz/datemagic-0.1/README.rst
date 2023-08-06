.. image:: https://img.shields.io/aur/license/yaourt.svg
      :target: https://opensource.org/licenses/GPL-3.0
      :alt: License

==========
Date Magic
==========

``datemagic`` module provides convenience function for operating with dates and
time types.

Install the module the usual way using ``pip`` to start using it.

Example
-------

Splitting year in 30-day chunks

.. code:: python

    >>> import datetime
    >>> import datemagic
    >>> datemagic.split_interval(datetime.date(2016,1,1),
    ...                          datetime.date(2016,12,31))
    [(datetime.date(2016, 1, 1), datetime.date(2016, 1, 30)),
     (datetime.date(2016, 1, 31), datetime.date(2016, 2, 29)),
     (datetime.date(2016, 3, 1), datetime.date(2016, 3, 30)),
     (datetime.date(2016, 3, 31), datetime.date(2016, 4, 29)),
     (datetime.date(2016, 4, 30), datetime.date(2016, 5, 29)),
     (datetime.date(2016, 5, 30), datetime.date(2016, 6, 28)),
     (datetime.date(2016, 6, 29), datetime.date(2016, 7, 28)),
     (datetime.date(2016, 7, 29), datetime.date(2016, 8, 27)),
     (datetime.date(2016, 8, 28), datetime.date(2016, 9, 26)),
     (datetime.date(2016, 9, 27), datetime.date(2016, 10, 26)),
     (datetime.date(2016, 10, 27), datetime.date(2016, 11, 25)),
     (datetime.date(2016, 11, 26), datetime.date(2016, 12, 25)),
     (datetime.date(2016, 12, 26), datetime.date(2016, 12, 31))]

Default chunk size is 30 days.
 
For detailed description see the Python docstrings in the code.
