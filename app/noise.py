from typing import Dict

import numpy as np
from scipy.signal import correlate

from bokeh.layouts import column, row
from bokeh.plotting import figure
from bokeh.plotting.figure import Figure
from bokeh.models import ColumnDataSource

from .stats import mean_confidence_interval, mean_confidence_interval_colored_noise


START, END = 0, 200


def noise_stats(X: np.ndarray, Y: np.ndarray, is_colored: bool = False) -> Dict:
    data = {}
    
    # Функция шума и гистограмма
    data['source'] = ColumnDataSource({'x': X, 'y': Y})
    
    # Корреляционная функция шума
    rxx = correlate(Y, Y, mode='full')
    data['rxx'] = ColumnDataSource({'x': np.linspace(-END, END, len(rxx)), 'rxx': rxx})
    
    # Оценка среднего от числа отсчётов
    Mx = np.zeros_like(Y)
    Sx = np.zeros_like(Y)
    for i in range(len(Y-5)):
        if is_colored:
            Mx[i], Sx[i] = mean_confidence_interval_colored_noise(Y[:i+6])
        else:
            Mx[i], Sx[i] = mean_confidence_interval(Y[:i+6])
    data['confidence'] = ColumnDataSource({'x': X, 'Mx': Mx, 'Sx': Sx, '-Sx': -Sx})
    
    return data


def generate_noise_data_source() -> Dict:
    noise_data = {}
    N = 1000
    X = np.linspace(START, END, N)

    # Генерация белого шума
    Y_noise = np.random.uniform(-1, 1, size=(N, N)).mean(1)
    noise_data['white'] = noise_stats(X, Y_noise)

    # Генерация окрашенного шума
    T = 50
    k = np.sqrt(2 * T)
    Y_colored = np.zeros_like(Y_noise)
    for i in range(N-1):
        Y_colored[i+1] = (T-1)/T * Y_colored[i] + k/T * Y_noise[i+1]
    noise_data['colored'] = noise_stats(X, Y_colored, is_colored=True)
    
    return noise_data


def noise(source: Dict, title: str) -> Figure:
    p1 = figure(title=title, width=600, height=200, tools='')
    p1.line(
        x='x', y=0, line_width=1, color='black',
        source=source['source'], alpha=1
    )
    p1.line(
        x='x', y='y', line_width=2, color='blue',
        source=source['source'], alpha=0.8
    )
    p1.yaxis.axis_label = 'x1(t)'
    p1.yaxis.axis_label = 't'
    p1.x_range.start, p1.x_range.end = START, END

    p2 = figure(title='Гистограмма', width=200, height=200, tools='')
    measured = source['source'].data['y']
    hist, edges = np.histogram(measured, density=True, bins=25)
    p2.quad(
        top=hist, bottom=0, left=edges[:-1], right=edges[1:],
        fill_color='green', line_color='white', alpha=0.8
    )
    p2.y_range.start = 0

    p3 = figure(title='Корреляционная функция', width=300, height=200, tools='')
    p3.line(
        x='x', y='rxx', line_width=2, color='red',
        source=source['rxx'], alpha=0.8
    )
    p3.varea(x='x', y1=0, y2='rxx', alpha=0.6, color='red', source=source['rxx'])
    p3.xaxis.axis_label, p3.yaxis.axis_label = 'q', 'Rxx'

    p4 = figure(title='Оценка среднего от числа отсчётов', width=500, height=200, tools='')
    p4.line(
        x='x', y='Mx', line_width=2, color='blue',
        source=source['confidence'], alpha=0.8
    )
    p4.line(
        x='x', y='Sx', line_width=2, color='red', line_dash='dashed',
        source=source['confidence'], alpha=0.8
    )
    p4.line(
        x='x', y='-Sx', line_width=2, color='red', line_dash='dashed',
        source=source['confidence'], alpha=0.8
    )
    p4.xaxis.axis_label = 'N'
    p4.x_range.start, p4.x_range.end = START, END

    return column(row(p1, p2), row(p3, p4))

def noise_plot():
    noise_data_source = generate_noise_data_source()
    return column(
        noise(source=noise_data_source['white'], title='Белый шум'),
        noise(source=noise_data_source['colored'], title='Окрашенный шум')
    )