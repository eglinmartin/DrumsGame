import numpy as np
from enum import Enum


class Input(Enum):
    KICK = {'id': 0, 'channel': 0}
    SNARE = {'id': 1, 'channel': 1}
    RACKTOM = {'id': 2, 'channel': 2}
    FLOORTOM = {'id': 3, 'channel': 3}
    HIHAT = {'id': 4, 'channel': 4}
    HIHAT_OPEN = {'id': 5, 'channel': 4}
    CRASH1 = {'id': 6, 'channel': 5}
    RIDE = {'id': 7, 'channel': 6}
    CRASH2 = {'id': 8, 'channel': 7}


def create_sine_wave(frequency, amplitude, duration, sampling_rate):
    t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)
    sine = amplitude * np.sin(2 * np.pi * frequency * t)
    return sine
