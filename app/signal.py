from typing import Tuple

import numpy as np


def generate_sin_signal(
    N: int = 500, scale: float = 0.02
) -> Tuple[np.ndarray, np.ndarray]:
    '''
    Генерация сигнала вида sin(x)
    ''' 
    # TODO Что за 0.02? Бахнуть параметром?
    x = np.arange(0, N)
    y = np.sin(x*scale)
    return x, y


def transform_signal(X: np.ndarray, H: np.ndarray) -> np.ndarray:
    """
    Расчет выходных сигналов на основе входных
    """
    return np.array(
        [sum(X[:j+1] * H[:j+1][::-1]) for j in range(len(H))]
    )

