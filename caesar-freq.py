#!/usr/bin/env python3

import sys
import argparse

from stderrprint import eprint
from ngram import NGramScore, clean_text


def rotn(text: str, shift: int) -> str:
    def shift_rel_to(c: str, to: str) -> str:
        return chr(((ord(c) - ord(to) + shift) % 26) + ord(to))

    def rotnc(c: str) -> str:
        return shift_rel_to(c, "A") if c.isupper() else shift_rel_to(c, "a")

    return "".join(rotnc(c) if c.isalpha() else c for c in text)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="caesar-freq",
        description="attempts to decrypt a caesar cipher in a given file",
    )
    parser.add_argument("filename")

    args = parser.parse_args()

    ngram = NGramScore("english_trigrams.txt")

    with open(args.filename) as f:
        src = f.read()

    chi_squareds = [ngram.score(rotn(src, shift)) for shift in range(26)]
    best_shift = max(range(len(chi_squareds)), key=chi_squareds.__getitem__)
    eprint(f"Best Shift: {best_shift} with chi-squared: {chi_squareds[best_shift]:.4f}")

    print(rotn(src, best_shift))
