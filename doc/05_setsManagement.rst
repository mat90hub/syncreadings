The library to manage the sets of measures.
===========================================

The library `setsManagement.py` provides the functions to read the
input file containing the sets of measures and to transform them into a
table of synchronized data.

.. list-table:: Functions of `setsManagement.py`
    :widths: 25 75
    :header-rows: 1

    * - function
      - content
    * - ``read_measures``
      - Read from a csv file and store the result into a dictionary.
    * - ``check_constant_time_step``
      - From the time sets entered as a dictionary, check that the time
        steps are constant.
    * - ``check_datetime_format``
      - From a date string, deduct the datetime format to be used.
    * - ``sets_starts_ends_steps``
      - Extract from the sets the lists of starts, ends and steps.
    * - ``report_on_sets``
      - From the characteristic dictionary, ellaborate a report as a string	      (on several lines).
    * - ``choose_start_end_step``
      - From the measure sets and the choices of synchronisation deduct the
	      start, end and steps to be applied on the time frame that will be
	      used for the synchronized data.
    * - ``synchronized_sets``
      - From set of measure sets and the choices of synchronisation entered
        as a dictionary, return a Pandas DataFrame containing the table of
        synchronized measures.
	

The function ``read_measures``.
-------------------------------

The function ``read_measures`` takes as input the name of file and will
convert it to a dictionary. The keys of this dictionary is the name of the
measures, that will become the title of the columns. The values associated
to these keys are lists, themselves consisting of couples date-time and
values.

.. code-block:: python
   
   {"LBA10CP001":
     ["2023-10-22 08:30:00", 120.56],
     ["2023-10-22 08:30:30", 121.34],
     ["2023-10-22 08:31:00", 122.23],
     [ ... ],
    "LBA10CT001": [...],
    ...
    }
 
Indeed, the dates are not stored as string as shown in this figure. We are
using the ``DateTime`` format of the library `DateTime`_,
which allows later to use the functions of this library and simplify later
the export to a `Pandas DataFrame`_.

.. _DateTime: https://docs.python.org/3/library/datetime.html
.. _Pandas DataFrame: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html 

An important side effect of the function ``read_measures`` is to update the
global variable ``default_choices`` by changing or not the ``datetime_format``.

.. code-block:: python

  default_choices = {
    "start": "max",
    "end": "min",
    "step": "strict_sync",
    "datetime_format": "%Y-%m-%d %H:%M:%S"
  }

The alternative is this one, when it was detected, the input time are given
with an accuracy of milliseconds

.. code-block:: python

  default_choices = {
    "start": "max",
    "end": "min",
    "step": "strict_sync",
    "datetime_format": "%Y-%m-%d %H:%M:%S.%f"
  }

By default, `DateTime` is only taking into account microseconds. But Here
it was judged, that the measure will come only wil milliseconds accuracy
at the highest. Microseconds will be converted to milliseconds.


The functions ``sets_starts_ends_steps`` and ``report_on_sets``.
----------------------------------------------------------------

The first function ``sets_starts_ends_steps`` is the generic one and the
second ``report_on_sets`` is using the output of the first function to
build a report as a multi-lines string, easy to display in a tk text window.

These functions assume the input file was read and the global variable
``default_choices`` was updated, so they can differentiate the case when
using seconds or milliseconds as the finest time step.

The function ``sets_starts_ends_steps`` is providing in a dictionary The
list of starting and ending time of the different sets and the steps they
have plus different key analysis from these ones (the min, the max and
the gcd and lcm for steps).


The function ``choose_start_end_step``.
---------------------------------------

The transformation of the sets of data starts by choosing the proper start,
end and step of the common time frame that will be used for the table. This
is deducted from the results of ``sets_starts_ends_steps`` and from the 
global variable ``default_choices``, which stores our preferences.

