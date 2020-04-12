import numpy as np
import pandas as pd

from bokeh.plotting import figure
from bokeh.plotting.figure import Figure
from bokeh.models import ColumnDataSource

from .stats import Kxx


def covariance_plot() -> Figure:
    '''
    Ковариационные функции
    '''
    covariance_df = pd.DataFrame()
    k_ranges = [9.5, 9, 8, 7, 5, 1]
    for k in k_ranges:
        T = 50
        a = -np.log(k*k/2/T)/T
        covariance_df[str(k)] = Kxx(a)
    source = ColumnDataSource(covariance_df)
    columns = covariance_df.columns
    
    p = figure(title='Ковариационные функции сигналов', width=600, height=300, tools='')
    
    p.line(x='index', y=columns[0], line_width=2, color='blue', legend_label='Окрашенный шум', source=source)
    for col in columns[1:-1]:
        p.line(x='index', y=col, line_width=2, color='blue', source=source)
    p.line(x='index', y=columns[-1], line_width=2, color='red', legend_label='Белый шум', source=source)
        
    p.xaxis.axis_label = 'N'
    p.yaxis.axis_label = 'Kxx'
    
    return p