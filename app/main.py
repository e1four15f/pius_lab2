from bokeh.io import curdoc
from bokeh.layouts import column, row

from .noise import noise_plot
from .weight_function import weight_function_plot
from .covariance import covariance_plot


curdoc().add_root(
    row(
        noise_plot(),
        column(
            weight_function_plot(),
            covariance_plot()
        )
    )
)
