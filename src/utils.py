import numpy as np
from enum import Enum


class Input(Enum):
    KICK = 0,
    SNARE = 1,
    RACKTOM = 2,
    FLOORTOM = 3,
    HIHAT = 4,
    CRASH1 = 5,
    RIDE = 6,
    CRASH2 = 7,
    SNAREROLL = 8,
    HIHAT_OPEN = 9


def create_sine_wave(frequency, amplitude, duration, sampling_rate):
    t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)
    sine = amplitude * np.sin(2 * np.pi * frequency * t)
    return sine
