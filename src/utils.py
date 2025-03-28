import numpy as np
from enum import Enum


class Input(Enum):
    KICK = 0
    SNARE = 1
    RACKTOM = 2
    FLOORTOM = 3
    HIHAT = 4
    HIHAT_OPEN = 5
    CRASH1 = 6
    RIDE = 7
    CRASH2 = 8


class Colours(Enum):
    BLACK = (26, 28, 44)
    PURPLE = (93, 39, 93)
    RED = (117, 62, 83)
    ORANGE = (239, 125, 87)
    YELLOW = (255, 205, 117)
    LIME = (167, 240, 112)
    GREEN = (56, 183, 100)
    TURQUOISE = (37, 113, 121)
    DBLUE = (41, 54, 111)
    ROYALBLUE = (59, 93, 201)
    LBLUE = (65, 166, 246)
    CYAN = (115, 239, 247)
    WHITE = (244, 244, 244)
    LGREY = (148, 176, 194)
    MGREY = (86, 108, 134)
    DGREY = (51, 60, 87)


def create_sine_wave(frequency, amplitude, duration, sampling_rate):
    t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)
    sine = amplitude * np.sin(2 * np.pi * frequency * t)
    return sine
