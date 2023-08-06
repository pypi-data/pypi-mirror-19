# coding=utf-8
from spikes.__data import __BARS


def print_spike(row):
    spike = ""
    for bar in row:
        spike += __BARS[bar]
    return spike
