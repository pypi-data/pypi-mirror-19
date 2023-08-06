BlindSpin: Braille Spinner for Python
=====================================

Sometimes you would just like to show the user some progress,
but a progress bar is not suitable because you don’t know how much longer it would take.
In these cases you might want to display a simple spinner using the `spinner()` function.

Example usage::

    with blindspin.spinner():
        do_something()
        do_something_else()


It looks like this:

.. image:: http://media.kennethreitz.com.s3.amazonaws.com/spinner.gif

Spinner class based on on a [gist by @cevaris](https://gist.github.com/cevaris/79700649f0543584009e).


Install
-------

::

    $ pip install blindspin


Supports Python 2.7 and 3.

Based on the work of:
---------------------

- Yoav Ram (@yoavram)
- Andreas Maier (@andy-maier)
