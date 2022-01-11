from typing import List

import numpy as np


def convert_to_observation(value: int, max_value: int):
    arr: List[int] = list(np.zeros(max_value, dtype=int))
    arr[value - 1] = 1
    return arr


def convert_from_observation(value: List[int]):
    for i in range(len(value)):
        if value[i] == 1:
            return i + 1
    return 0
