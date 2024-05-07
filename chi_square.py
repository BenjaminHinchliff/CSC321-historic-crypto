#!/usr/bin/env python3

from collections import Counter
from typing import Iterable

from text import clean_text

# English letter frequencies (%)
LETTER_FREQUENCIES_PERCENT = {
    "A": 8.55,
    "B": 1.60,
    "C": 3.16,
    "D": 3.87,
    "E": 12.10,
    "F": 2.18,
    "G": 2.09,
    "H": 4.96,
    "I": 7.33,
    "J": 0.22,
    "K": 0.81,
    "L": 4.21,
    "M": 2.53,
    "N": 7.17,
    "O": 7.47,
    "P": 2.07,
    "Q": 0.10,
    "R": 6.33,
    "S": 6.73,
    "T": 8.94,
    "U": 2.68,
    "V": 1.06,
    "W": 1.83,
    "X": 0.19,
    "Y": 1.72,
    "Z": 0.11,
}
LETTER_FREQUENCIES = {k: v / 100.0 for k, v in LETTER_FREQUENCIES_PERCENT.items()}

def chi_squared(Os: Iterable[float], Es: Iterable[float]) -> float:
    return sum((O - E) ** 2 / E for O, E in zip(Os, Es))


def chi_squared_freq(text: str) -> float:
    text = clean_text(text)
    observed_freq = Counter(text)
    total = sum(observed_freq.values())
    observed_freq = {k: v / total for k, v in observed_freq.items()}
    expected_freq = [LETTER_FREQUENCIES[k] for k in observed_freq]
    return chi_squared(observed_freq.values(), expected_freq)
