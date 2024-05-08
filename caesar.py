#!/usr/bin/env python3

import argparse

from stderrprint import eprint
from ngram import NGramScore


def rotn(text: str, shift: int) -> str:
    """
    Rotate the alphabetic chracters in a given string by a known shift, with wrapping

    text - the input text
    shift - an integral value to shift the characters by (positive or negative)

    returns - the text shifted by `shift`
    """

    def shift_rel_to(c: str, to: str) -> str:
        return chr(((ord(c) - ord(to) + shift) % 26) + ord(to))

    def rotnc(c: str) -> str:
        return shift_rel_to(c, "A") if c.isupper() else shift_rel_to(c, "a")

    return "".join(rotnc(c) if c.isalpha() else c for c in text)


def decrypt_without_shift(text: str) -> str:
    ngram = NGramScore("english_trigrams.txt")

    chi_squareds = [ngram.score(rotn(text, shift)) for shift in range(26)]
    best_shift = max(range(len(chi_squareds)), key=chi_squareds.__getitem__)
    eprint(f"Best Shift: {best_shift} with chi-squared: {chi_squareds[best_shift]:.4f}")

    return rotn(text, best_shift)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="caesar",
        description="attempts to decrypt a caesar cipher in a given file",
    )
    parser.add_argument("filename")
    parser.add_argument("-s", "--shift", type=int, help="shift for the cipher")

    args = parser.parse_args()

    with open(args.filename) as f:
        text = f.read()

    if args.shift is not None:
        print(rotn(text, args.shift))
    else:
        print(decrypt_without_shift(text))
