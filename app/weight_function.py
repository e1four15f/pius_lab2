from typing import Dict, List

import numpy as np
import pandas as pd
from scipy.signal import correlate

from bokeh.io import curdoc
from bokeh.models import Select, Column, ColumnDataSource
from bokeh.plotting.figure import Figure
from bokeh.layouts import column, row
from bokeh.plotting import figure

from .signal import generate_sin_signal, transform_signal


class DataSourceFactory:
    def __init__(self, N: int = 500):
        self._N = N
        self._X, self._Y_sin = generate_sin_signal(N)

        self.factory = {
            'Безинерционное звено': self._create_f1,
            'Звено с чистым запаздыванием': self._create_f2,
            'Апериодическое звено 1-го порядка': self._create_f3,
            'Чёрный ящик': self._create_f4,
        }

    def get(self, source_name: str) -> ColumnDataSource:
        return ColumnDataSource(self.factory.get(source_name)())

    def get_expanded(self, source_name: str) -> Dict:
        source = self.get(source_name)
        sources = {}
        sources['weight'] = source
        X, Y = source.data['x'], source.data['y']
        rxx = correlate(Y, Y, mode='full')
        sources['rxx'] = ColumnDataSource({'x': np.linspace(-self._N, self._N, len(rxx)), 'y': rxx})
        sources['in'] = ColumnDataSource({'x': X, 'y': self._Y_sin})
        sources['out'] = ColumnDataSource({'x': X, 'y': transform_signal(self._Y_sin, Y)})
        return sources

    def _create_f1(self) -> Dict:
        # TODO тут есть коэффициент усиления!
        Y = np.zeros(self._N)
        Y[0] = 1
        return {'x': self._X, 'y': Y}

    def _create_f2(self) -> Dict:
        X_biased = (self._X - 0.2 * self._N)
        Y = np.zeros(self._N)
        Y[100] = 1
        return {'x': X_biased, 'y': Y}

    def _create_f3(self) -> Dict:
        T = 15 # TODO почему так? Это надо в параметры!
        Y = np.exp(-self._X/T)/T
        return {'x': self._X, 'y': Y}

    def _create_f4(self) -> Dict:
        Y = np.sin(self._X/100)/200      
        Y[self._X > 100 * np.pi] = 0
        return {'x': self._X, 'y': Y}


def wfplot(source: Dict) -> Figure:
    p1 = figure(title='Весовая функция', width=500, height=200, tools='')
    p1.line(x='x', y='y', line_width=2, color='blue', source=source['weight'])
    p1.xaxis.axis_label, p1.yaxis.axis_label = 't', 'h(t)'

    p2 = figure(title='Корреляционная функция', width=300, height=200, tools='')
    p2.line(x='x', y='y', line_width=2, color='red', source=source['rxx'])
    p2.varea(x='x', y1=0, y2='y', alpha=0.6, color='red', source=source['rxx'])
    p2.xaxis.axis_label, p2.yaxis.axis_label = 'q', 'Rxx'

    p3 = figure(title='Входной сигнал', width=400, height=200, tools='')
    p3.line(x='x', y='y', line_width=2, color='blue', source=source['in'])
    p3.xaxis.axis_label, p3.yaxis.axis_label = 'x', 'sin(x)'

    p4 = figure(title='Выходной сигнал', width=400, height=200, tools='')
    p4.line(x='x', y='y', line_width=2, color='blue', source=source['out'])
    p4.xaxis.axis_label = 'x'

    plot = column(row(p1, p2), row(p3, p4))
    return plot

def weight_function_plot() -> Figure:
    factory = DataSourceFactory()
    columns = [
        'Безинерционное звено',
        'Звено с чистым запаздыванием',
        'Апериодическое звено 1-го порядка',
        'Чёрный ящик'
    ]
    sources = factory.get_expanded(columns[0])
    plot = wfplot(sources)

    select_signal = Select(title='Объект', options=columns, value=columns[0])
    def update_layout(attr, old, new):
        for k, v in sources.items():
            sources[k].data = dict(factory.get_expanded(new)[k].data)

    select_signal.on_change('value', update_layout)
    
    return Column(select_signal, plot)
