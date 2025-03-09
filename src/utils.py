import numpy as np


def create_sine_wave(frequency, amplitude, duration, sampling_rate):
    t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)
    sine = amplitude * np.sin(2 * np.pi * frequency * t)
    return sine
