SanePlot
========

A simple wrapper around some basic 2d matplotlib plotting which has some sane defaults. Developed mostly for personal use.

----

Motivation and use-cases:

    * Quickly set up multiple plot parameters (font sizes, text position, curve colors, x and y scales) without having to remember how to do that; provide some sane defaults

    * Have all this code in one place and not scattered around multiple jupyter notebooks

    * All of the above allows to quickly create plots of 2d dimensional data


Usage
-----

Everything is done by the SanePlot class. The initialization parameters which control the plot are:

    * ``figsize=(14.0, 10.0)`` - the size of the plot

    * ``legendloc='upper right'`` - the legend location

    * ``legend_frame_color='#FFFFFF'`` - color of the legend background

    * ``fontfamily='fantasy', font='Calibri'`` - these two parameters control the font. I only set them to use Cyrillic characters

    * ``legend_size=26`` - legend font size

    * ``tick_size=24`` - tick label size

    * ``xy_label_size=32`` - set the size of the X and Y axis labels

    * ``textsize=27`` - set the text size

    * ``linewidth=5`` - the width of the curves being plotted

    * ``markersize=5`` - the size of the markers being plotted

    * ``xlim=None`` - either None or a tuple/list; if set, sets the X-limits of the plot

    * ``ylim=None`` - either None or a tuple/list; if set, sets the Y-limits of the plot

    * ``text=None`` - either None or a string; if set, will place text somewhere on the plot

    * ``text_x_rel=None`` - controls the relative X-position of the text (thus, a value of 0.5 will place the text in the middle of the plot with respect to the X-axis)

    * ``text_x_abs=None`` - controls the absolute X-position of the text. If text_x_rel is set, will not do anything

    * ``text_y_rel=None`` - controls the relative Y-position of the text (thus, a value of 0.5 will place the text in the middle of the plot with respect to the Y-axis)

    * ``text_y_abs=None`` - controls the absolute Y-position of the text. If text_x_rel is set, will not do anything

    * ``log_x_base=0`` - if set to 0, the X axis is normal (linear). If different from 0, then the X axis is a log-axis with base equal to ``log_x_base``

    * ``log_y_base=0`` - if set to 0, the Y axis is normal (linear). If different from 0, then the X axis is a log-axis with base equal to ``log_y_base``

    * ``x_label=None`` - the label for the X axis

    * ``y_label=None`` - the label for the Y axis

    * ``linechange='monochrome'`` - sets the line styles. Can be either ``monochrome``, ``color`` or a list.
      If it is a list, curve number N on the plot will be plotted with a style set by the element number (N-1) % len(linechange) of the list.
      The list corresponding to ``'monochrome'``: ['k-', 'k--', 'ko', 'k^', 'k:', 'k*']
      The list corresponding to ``'color'``: ['k', 'g', 'b', 'r', 'c']



The methods are:

    * ``SanePlot.add_text(textsize=None)`` - adds text specified during the initialization. You can override the originally set textsize. Returns the Figure object.

    * ``SanePlot.plot(x, y, label=None, linewidth=None, markersize=None)`` - plots the curve specified by the (x,y) arrays.
      The label is set by the ``label`` parameter, and the originally set linewidth and markersize can be overridden. Returns the Figure object.

    * ``SanePlot.legend()`` - show the legend. Returns the Figure object.

    * ``SanePlot.show()`` - returns the Figure object.


Examples
--------

This can be inserted into a Jupyter notebook with ``%matplotlib inline`` added and will show the resulting plots right there.::

    import numpy as np
    from saneplot import SanePlot

    x = np.linspace(0, 30, 100)
    y1 = np.sin(x) * 1000 + 4000
    y2 = np.cos(x) * 1000 + 4000
    y3 = x**2 * 1000

    sp = SanePlot(x_label='x', y_label='y', text='(a)', text_x_abs=10, text_y_rel=0.5)

    sp.plot(x, y1, '0')
    sp.plot(x, y2+100, 'y2', linewidth=4)
    sp.plot(x, y2+500, 'y2', linewidth=4)
    sp.plot(x, y2+1000, 'y2', linewidth=3)
    sp.plot(x, y2+2000, 'y2', linewidth=3)
    sp.plot(x, y2+4000, 'y2', linewidth=4)
    sp.plot(x, y2+8000, 'y2', linewidth=5)
    sp.add_text(textsize=10)
    sp.legend()

Version history
---------------

    * 0.1 (01 February 2017) - first working version of the package created