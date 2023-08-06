.. role:: python(code)
    :language: python

============
Graph butler
============
A small framework for generating simple, reproducible graphs.

Example
=======

.. code:: python

    @recipe
    def sine_wave():
        g = Graph()
        g.x = numpy.arange(0.0, 10.0, 0.01)
        g.y = numpy.sin(g.x)
        return g

This defines a graph of the ``sin(x)`` function in the interval
``0 ≤ x ≤ 10``.

To save the graph to disk, call :python:`sine_wave().save()`. To save all
recipes, call :python:`graphbutler.save_all()`. To show a preview, call
:python:`sine_wave().show()`.

For more examples, see the examples directory.

Status
======
This project is in an experimental stage. Feel free to open an issue
`on Github <https://github.com/jacwah/graphbutler/issues>`_ and I'll get back
to you in a couple of days!
