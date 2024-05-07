#!/usr/bin/env python3

from collections import Counter
import random
import sys
import matplotlib.pyplot as plt

from ngram import NGramScore, clean_text

MAX_KEY_LENGTH = 20
MAX_EPOCHS = 1000
MAX_EPOCHS_TO_IMPROVE = 100


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def decrypt(text: str, key: str) -> str:
    decrypted = ""
    i = 0
    for l in text:
        if l.isalpha():
            off = ord('A') if l.isupper() else ord('a')
            p = ord(l) - off
            k = ord(key[i % len(key)]) - ord('A')
            c = (p - k) % 26
            decrypted += chr(c + off)
            i += 1
        else:
            decrypted += l
    return decrypted


def index_of_coincidence(text: str) -> float:
    counts = Counter(text)
    numerator = sum(c * (c - 1) for c in counts.values())
    total = sum(counts.values())
    return 26 * numerator / (total * (total - 1))

def slice_by_period(text: str, period: int) -> list[str]:
        slices = [""] * period
        for i in range(len(text)):
            slices[i % period] += text[i]
        return slices

def guess_period(text: str, max_period: int) -> int:
    text = clean_text(text)
    best_period = 1
    best_ioc = None
    for period in range(1, max_period):
        slices = slice_by_period(text, period)
        total = 0
        for i in range(period):
            total += index_of_coincidence(slices[i])
        ioc = total / period
        print(ioc)
        if best_ioc is None or ioc > best_ioc:
            best_period = period
            best_ioc = ioc
    return best_period


if __name__ == "__main__":
    ngram = NGramScore("english_trigrams.txt")

    with open(sys.argv[1]) as f:
        text = f.read()

    key_length = guess_period(text, MAX_KEY_LENGTH)
    print(f"key length: {key_length}")

    best_key = ["A"] * key_length
    best_score = ngram.score(decrypt(text, "".join(best_key)))
    epochs_since_improvement = 0
    for _ in range(MAX_EPOCHS):
        key = best_key[:]
        i = random.randrange(key_length)
        for c in range(26):
            key[i] = chr(ord('A') + c)
            solve = decrypt(text, "".join(key))
            score = ngram.score(solve)
            if score > best_score:
                best_key = key[:]
                best_score = score
                epochs_since_improvement = 0
                eprint(f"new best scrore: {best_score}")
                eprint(f"key: {''.join(key)}")

        if epochs_since_improvement > MAX_EPOCHS_TO_IMPROVE:
            break
        epochs_since_improvement += 1

    print(decrypt(text, "".join(best_key)))