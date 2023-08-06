"""Graph butler is a framework for generating simple, reproducible graphs.

The Graph class is used to specify the properties of a single graph. This is
usually done in what is called a recipe, an argument-less function returning
a Graph object.

The recipe decorator and the save_all function work together to provide an easy
interface for saving graphs to disk.

The Parameterized class simplifies creating graphs of minor variations of the
same function.

For usage examples, see the examples directory.
"""

import os
import functools
import matplotlib.pyplot as plt
import numpy

# See http://matplotlib.org/api/lines_api.html#matplotlib.lines.Line2D
LINE_OPTIONS = {
    "linewidth": 2
}

class Graph(object):
    """Represents the graph of a mathematical function.

    When defining a graph, subclass this class and provide an x and y numpy array."""

    def __init__(self):
        self.axes_options = {}

    def plot(self, arr, axes, **options):
        """Plot a numpy array to axes.

        options should be a dict contain matplotlib Line2D. The values in
        options take precedence over LINE_OPTIONS."""
        try:
            arr[arr < self.y_min] = numpy.nan
        except AttributeError:
            pass

        try:
            arr[arr > self.y_max] = numpy.nan
        except AttributeError:
            pass

        all_options = LINE_OPTIONS.copy()
        all_options.update(options)

        axes.plot(self.x, arr, **all_options)

    def draw_to(self, figure):
        """Draw the graph to a matplotlib figure."""
        try:
            figure.suptitle(self.title)
        except AttributeError:
            pass

        axes = figure.gca(**self.axes_options)

        if isinstance(self.y, Parameterized):
            for (y, label) in self.y:
                self.plot(y, axes, label=label)
            axes.legend()
        else:
            self.plot(self.y, axes)

    def show(self):
        """Draw the graph in a GUI frontend through pyplot."""
        figure = plt.figure()
        self.draw_to(figure)
        plt.show()
        plt.close()

    def path(self, dir, format="svg"):
        """Return the path where the graph will be saved by save()."""
        try:
            fn = getattr(self, "filename", None) or self.recipe.__name__
        except AttributeError:
            raise AttributeError("Graph must have filename or recipe.")

        extension = "." + format.lower()
        if not fn.lower().endswith(extension):
            fn += extension

        return os.path.join(dir, fn)

    def save(self, dir, format="svg"):
        """Save the graph as a file."""
        path = self.path(dir, format=format)
        print("Saving graph to %s" %path)

        self.draw_to(plt.figure())
        plt.savefig(path)
        plt.close()

class Parameterized(object):
    """A parameterized dependent variable.

    Use to graph multiple slight variations of the same function together.
    Implements the iterator protocol."""

    def __init__(self, name, template, values):
        self.name = name
        self.template = template
        self.values = values

    def __iter__(self):
        self.index = 0
        return self

    def next(self):
        try:
            value = self.values[self.index]
        except IndexError:
            raise StopIteration

        self.index += 1
        return self.template(value), "%s = %s" %(self.name, value)

recipes = set()

def recipe(func):
    """Decorator for graph recipes.

    Use this decorator to register recipes with save_all."""
    @functools.wraps(func)
    def wrapper():
        graph = func()
        graph.recipe = wrapper
        return graph

    recipes.add(wrapper)
    return wrapper

def save_all(dir=None, format="svg"):
    """Save all defined recipes as files."""
    if dir is None:
        dir = os.getcwd()

    for recipe in recipes:
        recipe().save(dir, format=format)
