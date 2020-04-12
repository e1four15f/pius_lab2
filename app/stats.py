from typing import Tuple

import numpy as np
import scipy.stats


def mean_confidence_interval(
    data: np.ndarray,
    confidence: float = 0.95
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Вычисляет доверительный интервал для выборки data для доверительной вероятности confidence
    """
    # размер выборки
    n = len(data)  
    # вычисляем среднее и стандартное отклонение
    m, se = np.mean(data), scipy.stats.sem(data)
    # вычисляем доверительный интервал
    h = se * scipy.stats.t.ppf((1 + confidence)/2, n-1) 
    return m, h


def mean_confidence_interval_colored_noise(
    data: np.ndarray,
    confidence: float = 0.95
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Вычисляет доверительный интервал для выборки data для доверительной вероятности confidence
    """
    n = len(data) #размер выборки
    m = np.mean(data)
    se = 0
    for p in range(n-1):
        se = se + (1 - (p + 1) / n) * np.exp(-(p+1)/50) * 0.05
    se = se * 2 / n + 1 / n
    h = se * scipy.stats.t.ppf((1 + confidence)/2., n-1) #вычисляем доверительный интервал
    return m, h


# TODO Не юзается, мб проебался?
def Kxxcn(X, t):
    """
    Ковариационная функция для окрашенного шума
    """
    X_ = np.mean(X)
    M = np.zeros(len(X)-t)
    for q in range(len(M)):
        M[q] = (X[q] - X_) * (X[q + t] - X_)
    return np.mean(M)


def Kxx(a: float) -> np.ndarray:
    """
    Ковариационная функция
    """
    return np.exp(-a * np.fabs(np.arange(100)))
