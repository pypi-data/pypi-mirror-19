import math
from omnicanvas import Canvas
from .series import Series, LineSeries

class Chart:
    """The base class for all charts. It controls the attributes common to all
    charts - namely dimensions and title.

    :param str title: The chart's title. This will be displayed at the top of\
    the chart.
    :param width: The width in pixels of the chart.
    :param height: The height in pixels of the chart."""

    def __init__(self, title="", width=700, height=500):
        if not isinstance(title, str):
            raise TypeError("title must be str, not '%s'" % str(title))
        self._title = title

        if not isinstance(width, int) and not isinstance(width, float):
            raise TypeError("width must be numeric, not '%s'" % str(width))
        self._width = width

        if not isinstance(height, int) and not isinstance(height, float):
            raise TypeError("height must be numeric, not '%s'" % str(height))
        self._height = height


    def __repr__(self):
        return "<Chart (%i×%i)>" % (self._width, self._height)


    def title(self, title=None):
        """Returns or sets (if a value is provided) the chart's title.

        :param str title: If given, the chart's title will be set to this.
        :rtype: ``str``"""

        if title is None:
            return self._title
        else:
            if not isinstance(title, str):
                raise TypeError("title must be str, not '%s'" % str(title))
            self._title = title


    def width(self, width=None):
        """Returns or sets (if a value is provided) the chart's width.

        :param width: If given, the chart's width will be set to this."""

        if width is None:
            return self._width
        else:
            if not isinstance(width, int) and not isinstance(width, float):
                raise TypeError("width must be numeric, not '%s'" % str(width))
            self._width = width


    def height(self, height=None):
        """Returns or sets (if a value is provided) the chart's height.

        :param height: If given, the chart's height will be set to this."""

        if height is None:
            return self._height
        else:
            if not isinstance(height, int) and not isinstance(height, float):
                raise TypeError("height must be numeric, not '%s'" % str(height))
            self._height = height


    def create(self):
        """Renders the chart to an OmniCanvas `canvas <https://omnicanvas.readt\
        hedocs.io/en/latest/api/canvas.html#omnicanvas.canvas.Canvas>`_. This
        object can then be `saved <https://omnicanvas.readthedocs.io/en/latest/\
        api/canvas.html#omnicanvas.canvas.Canvas.save>`_ or `rendered <https://\
        omnicanvas.readthedocs.io/en/latest/api/canvas.html#omnicanvas.canvas.C\
        anvas.render>`_ as SVG."""

        canvas = Canvas(self.width(), self.height())
        canvas.add_text(
         self.width() / 2, 0, self.title(),
         vertical_align="bottom", name="title"
        )
        return canvas


class AxisChart(Chart):
    """Base class: :py:class:`Chart`

    A chart with axes, onto which series can be shown. Line charts, scatter
    charts, bar charts etc. are all AxisCharts with the relevant series. An
    AxisChart can have multiple series associated with it, and they will all be
    drawn onto the chart.

    AxisCharts have the usual properties relating to axes, such as axes labels.

    :param Series \*series: One or more :py:class:`.Series` objects to be\
    associated with the chart.
    :param str title: The chart's title. This will be displayed at the top of\
    the chart.
    :param width: The width in pixels of the chart.
    :param height: The height in pixels of the chart.
    :param str x_label: The label for the x-axis.
    :param str y_label: The label for the y-axis.
    :raises ValueError: If no series are given."""

    def __init__(self, *series, x_label="", y_label="", **kwargs):
        Chart.__init__(self, **kwargs)

        for s in series:
            if not isinstance(s, Series):
                raise TypeError("'%s' is not a Series" % str(s))
        if len(series) == 0:
            raise ValueError("AxisChart needs at least one series")
        self._all_series = list(series)
        for s in series:
            s._chart = self

        if not isinstance(x_label, str):
            raise TypeError("x_label must be str, not '%s'" % str(x_label))
        self._x_label = x_label
        if not isinstance(y_label, str):
            raise TypeError("y_label must be str, not '%s'" % str(y_label))
        self._y_label = y_label

        self._horizontal_padding = 0.1
        self._vertical_padding = 0.1
        self._x_lower_limit = None
        self._x_upper_limit = None
        self._y_lower_limit = None
        self._y_upper_limit = None


    def __repr__(self):
        return "<AxisChart (%i series)>" % len(self._all_series)


    def all_series(self):
        """Returns a ``list`` of all the :py:class:`.Series` objects associated
        with the chart.

        :rtype: ``list``"""

        return list(self._all_series)


    def series(self):
        """Returns the first :py:class:`.Series` objects associated with the
        chart.

        :rtype: :py:class:`.Series`"""

        return self._all_series[0]


    def add_series(self, series):
        """Adds a :py:class:`.Series` to the chart.

        :param Series series: The :py:class:`.Series` to add."""

        if not isinstance(series, Series):
            raise TypeError("'%s' is not a Series" % str(series))
        self._all_series.append(series)
        series._chart = self


    def remove_series(self, series):
        """Removes a :py:class:`.Series` from the chart.

        :param Series series: The :py:class:`.Series` to remove.
        :raises ValueError: if you try to remove the last\
        :py:class:`.Series`."""

        if len(self.all_series()) == 1:
            raise ValueError("Cannot remove last series from %s" % str(self))
        self._all_series.remove(series)
        series._chart = None


    def line(self, *args, **kwargs):
        """Adds a :py:class:`.LineSeries` to the chart.

        :param \*data: The data for the series as either (x,y) values or two big\
        tuples/lists of x and y values respectively.
        :param str name: The name to be associated with the series.
        :param str color: The hex colour of the line.
        :param str linestyle: The line pattern. See\
        `OmniCanvas docs <https://omnicanvas.readthedocs.io/en/latest/api/graph\
        ics.html#omnicanvas.graphics.ShapeGraphic.line_style>`_ for acceptable \
        values.
        :raises ValueError: if the size and length of the data doesn't match\
        either format."""

        series = LineSeries(*args, **kwargs)
        self.add_series(series)


    def get_series_by_name(self, name):
        """Returns the first :py:class:`.Series` of a given name, or ``None``.

        :param str name: The name to search by."""

        if not isinstance(name, str):
            raise TypeError(
             "Can only search series by str name, not '%s'" % str(name)
            )
        for series in self.all_series():
            if series.name() == name:
                return series


    def x_label(self, x_label=None):
        """Returns or sets (if a value is provided) the chart's x-axis label.

        :param str x_label: If given, the chart's x_label will be set to this.
        :rtype: ``str``"""

        if x_label is None:
            return self._x_label
        else:
            if not isinstance(x_label, str):
                raise TypeError("x_label must be str, not '%s'" % str(x_label))
            self._x_label = x_label


    def y_label(self, y_label=None):
        """Returns or sets (if a value is provided) the chart's y-axis label.

        :param str y_label: If given, the chart's y_label will be set to this.
        :rtype: ``str``"""

        if y_label is None:
            return self._y_label
        else:
            if not isinstance(y_label, str):
                raise TypeError("y_label must be str, not '%s'" % str(y_label))
            self._y_label = y_label


    def horizontal_padding(self, padding=None):
        """Returns or sets (if a value is provided) the chart's horizontal
        padding. This determines how much space will be on either side of the
        display area, as a proportion of overall width, and should be a value
        between 0 and 0.5

        :param float padding: If given, the chart's horizontal_padding\
        will be set to this.
        :raises ValueError: if a value outside of 0 < n < 0.5 is given.
        :rtype: float"""

        if padding is None:
            return self._horizontal_padding
        else:
            if not isinstance(padding, float):
                raise TypeError("padding must be float, not '%s'" % str(padding))
            if not 0 < padding < 0.5:
                raise ValueError(
                 "padding must be between 0 and 0.5 (not inclusive), not '%s'" % str(padding)
                )
            self._horizontal_padding = padding


    def vertical_padding(self, padding=None):
        """Returns or sets (if a value is provided) the chart's vertical
        padding. This determines how much space will be above and below the
        display area, as a proportion of overall height, and should be a value
        between 0 and 0.5

        :param float padding: If given, the chart's vertical_padding\
        will be set to this.
        :raises ValueError: if a value outside of 0 < n < 0.5 is given.
        :rtype: float"""

        if padding is None:
            return self._vertical_padding
        else:
            if not isinstance(padding, float):
                raise TypeError("padding must be float, not '%s'" % str(padding))
            if not 0 < padding < 0.5:
                raise ValueError(
                 "padding must be between 0 and 0.5 (not inclusive), not '%s'" % str(padding)
                )
            self._vertical_padding = padding


    def smallest_x(self):
        """Returns the smallest x-value in all the :py:class:`.Series`
        associated with the chart."""

        return min(
         [series.data()[0][0] for series in self.all_series()]
        )


    def largest_x(self):
        """Returns the largest x-value in all the :py:class:`.Series`
        associated with the chart."""

        return max(
         [series.data()[-1][0] for series in self.all_series()]
        )


    def smallest_y(self):
        """Returns the smallest y-value in all the :py:class:`.Series`
        associated with the chart."""

        return min(
         [series.smallest_y() for series in self.all_series()]
        )


    def largest_y(self):
        """Returns the largest y-value in all the :py:class:`.Series`
        associated with the chart."""

        return max(
         [series.largest_y() for series in self.all_series()]
        )


    def x_lower_limit(self, limit=None):
        """Returns or sets (if a value is provided) the value at which the
        x-axis should start. By default this is zero (unless there are negative
        values).

        :param limit: If given, the chart's x_lower_limit will be set to this.
        :raises ValueError: if you try to make the lower limit larger than the\
        upper limit."""

        if limit is None:
            if self._x_lower_limit is None:
                if self.smallest_x() < 0:
                    if self.smallest_x() == self.largest_x():
                        return int(self.smallest_x() - 1)
                    else:
                        return self.smallest_x()
                else:
                    return 0
            else:
                return self._x_lower_limit
        else:
            if not isinstance(limit, int) and not isinstance(limit, float):
                raise TypeError(
                 "lower x limit must be numeric, not '%s'" % str(limit)
                )
            if limit >= self.largest_x():
                raise ValueError(
                 "lower x limit must be less than upper limit (%s), not %s" % (
                  str(self.largest_x()), str(limit)
                 )
                )
            self._x_lower_limit = limit


    def y_lower_limit(self, limit=None):
        """Returns or sets (if a value is provided) the value at which the
        y-axis should start. By default this is zero (unless there are negative
        values).

        :param limit: If given, the chart's y_lower_limit will be set to this.
        :raises ValueError: if you try to make the lower limit larger than the\
        upper limit."""

        if limit is None:
            if self._y_lower_limit is None:
                if self.smallest_y() < 0:
                    if self.smallest_y() == self.largest_y():
                        return int(self.smallest_y() - 1)
                    else:
                        return self.smallest_y()
                else:
                    return 0
            else:
                return self._y_lower_limit
        else:
            if not isinstance(limit, int) and not isinstance(limit, float):
                raise TypeError(
                 "lower y limit must be numeric, not '%s'" % str(limit)
                )
            if limit >= self.largest_y():
                raise ValueError(
                 "lower y limit must be less than upper limit (%s), not %s" % (
                  str(self.largest_y()), str(limit)
                 )
                )
            self._y_lower_limit = limit


    def x_upper_limit(self, limit=None):
        """Returns or sets (if a value is provided) the value at which the
        x-axis should end. By default this is the highest x value in the
        associated series.

        :param limit: If given, the chart's x_upper_limit will be set to this.
        :raises ValueError: if you try to make the upper limit smaller than the\
        lower limit."""

        if limit is None:
            if self._x_upper_limit is None:
                if self.smallest_x() == self.largest_x():
                    if int(self.largest_x()) == float(self.largest_x()):
                        return self.largest_x() + 1
                    else:
                        return math.ceil(self.largest_x())
                else:
                    return self.largest_x()
            else:
                return self._x_upper_limit
        else:
            if not isinstance(limit, int) and not isinstance(limit, float):
                raise TypeError(
                 "upper x limit must be numeric, not '%s'" % str(limit)
                )
            if limit <= self.smallest_x():
                raise ValueError(
                 "upper x limit must be greater than lower limit (%s), not %s" % (
                  str(self.smallest_x()), str(limit)
                 )
                )
            self._x_upper_limit = limit


    def y_upper_limit(self, limit=None):
        """Returns or sets (if a value is provided) the value at which the
        y-axis should end. By default this is the highest y value in the
        associated series.

        :param limit: If given, the chart's y_upper_limit will be set to this.
        :raises ValueError: if you try to make the upper limit smaller than the\
        lower limit."""

        if limit is None:
            if self._y_upper_limit is None:
                if self.smallest_y() == self.largest_y():
                    if int(self.largest_y()) == float(self.largest_y()):
                        return self.largest_y() + 1
                    else:
                        return math.ceil(self.largest_y())
                else:
                    return self.largest_y()
            else:
                return self._y_upper_limit
        else:
            if not isinstance(limit, int) and not isinstance(limit, float):
                raise TypeError(
                 "upper y limit must be numeric, not '%s'" % str(limit)
                )
            if limit <= self.smallest_y():
                raise ValueError(
                 "upper y limit must be greater than lower limit (%s), not %s" % (
                  str(self.smallest_y()), str(limit)
                 )
                )
            self._y_upper_limit = limit


    def create(self):
        """Renders the chart to an OmniCanvas `canvas <https://omnicanvas.readt\
        hedocs.io/en/latest/api/canvas.html#omnicanvas.canvas.Canvas>`_. This
        object can then be `saved <https://omnicanvas.readthedocs.io/en/latest/\
        api/canvas.html#omnicanvas.canvas.Canvas.save>`_ or `rendered <https://\
        omnicanvas.readthedocs.io/en/latest/api/canvas.html#omnicanvas.canvas.C\
        anvas.render>`_ as SVG."""

        canvas = Chart.create(self)

        for index, series in enumerate(self.all_series(), start=1):
            series.write_to_canvas(canvas, "series%i" % index)
        canvas.add_rectangle(
         0, 0, self.horizontal_padding() * canvas.width(), canvas.height(),
         opacity=1,
         line_width=0,
         name="block-w"
        )
        canvas.add_rectangle(
         0, 0, canvas.width(), self.vertical_padding() * canvas.height(),
         opacity=1,
         line_width=0,
         name="block-n"
        )
        canvas.add_rectangle(
         canvas.width() - (self.horizontal_padding() * canvas.width()), 0,
         self.horizontal_padding() * canvas.width(), canvas.height(),
         opacity=1,
         line_width=0,
         name="block-e"
        )
        canvas.add_rectangle(
         0, canvas.height() - (self.vertical_padding() * canvas.height()),
         canvas.width(), self.vertical_padding() * canvas.height(),
         opacity=1,
         line_width=0,
         name="block-s"
        )
        canvas._graphics.append(canvas._graphics.pop(0)) # Dirty hack
        canvas.graphics()[-1].y(self.vertical_padding() * canvas.height() * 0.5)
        canvas.graphics()[-1].vertical_align("center")

        axes = canvas.add_rectangle(
         self.horizontal_padding() * canvas.width(),
         self.vertical_padding() * canvas.height(),
         canvas.width() - (2 * self.horizontal_padding() * canvas.width()),
         canvas.height() - (2 * self.vertical_padding() * canvas.height()),
         name="axes",
         opacity=0
        )

        if self.x_label():
            canvas.add_text(
             canvas.width() / 2,
             canvas.height() - (self.vertical_padding() * canvas.height() * 0.5),
             self.x_label(),
             name="x_label"
            )
        y_label_x = self.horizontal_padding() * canvas.width() * 0.5
        if self.y_label():
            canvas.add_text(
             y_label_x,
             canvas.height() * 0.5,
             self.y_label(),
             rotation=(y_label_x, canvas.height() * 0.5, 270),
             name="y_label"
            )
        return canvas
