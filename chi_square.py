#!/usr/bin/env python3

from collections import Counter
from typing import Iterable
import re

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

def load_bigrams():
    with open("english_bigrams_1.txt", "r") as f:
        bigrams = {}
        for line in f:
            bigram, count = line.split()
            bigrams[bigram] = int(count)
    total = sum(bigrams.values())
    bigrams = {b: c / total for b, c in bigrams.items()}
    return bigrams

BIGRAM_FREQUENCIES = load_bigrams()

ALPHA_REGEX = re.compile(r"[^A-Za-z]+")
def clean_text(text: str) -> str:
    return ALPHA_REGEX.sub("", text).upper()


def chi_squared(Os: Iterable[float], Es: Iterable[float]) -> float:
    return sum((O - E) ** 2 / E for O, E in zip(Os, Es))


def chi_squared_freq(text: str) -> float:
    text = clean_text(text)
    observed_freq = Counter(text)
    total = sum(observed_freq.values())
    observed_freq = {k: v / total for k, v in observed_freq.items()}
    expected_freq = [LETTER_FREQUENCIES[k] for k in observed_freq]
    return chi_squared(observed_freq.values(), expected_freq)


def chi_squared_bigram_freq(text: str) -> float:
    text = clean_text(text)
    observed_freq = Counter(
        text[i : i + 2]
        for i in range(len(text) - 2 + 1)
        if text[i : i + 2] in BIGRAM_FREQUENCIES
    )
    observed_freq = {
        k: observed_freq[k] / len(text) if k in observed_freq else 0.0
        for k in BIGRAM_FREQUENCIES
    }
    return chi_squared(observed_freq.values(), BIGRAM_FREQUENCIES.values())

def chi_squared_bigram_freq(text: str, quadgram_freqs: dict[str, float]) -> float:
    text = clean_text(text)
    observed_freq = Counter(
        text[i : i + 2]
        for i in range(len(text) - 2 + 1)
        if text[i : i + 2] in BIGRAM_FREQUENCIES
    )
    observed_freq = {
        k: observed_freq[k] / len(text) if k in observed_freq else 0.0
        for k in BIGRAM_FREQUENCIES
    }
    return chi_squared(observed_freq.values(), BIGRAM_FREQUENCIES.values())
