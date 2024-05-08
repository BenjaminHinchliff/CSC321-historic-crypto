#!/usr/bin/env python3

import sys
import math
import random
import argparse

MAX_EPOCHS = 10_000

from stderrprint import eprint
from ngram import NGramScore


def random_letter():
    return chr(random.randrange(ord("A"), ord("Z") + 1))


def map_letters(src: str, letters_map: dict[str, str]) -> str:
    """
    Maps the letters in the source string according to the given mapping

    src - the source string
    letters_map - a bijective function to map each letter to another in the english alphabet

    returns - the mapped string
    """
    return "".join(
        (
            letters_map[c]
            if c.isupper()
            else letters_map[c.upper()].lower() if c.islower() else c
        )
        for c in src
    )


def randomly_swap_letters(letters_map: dict[str, str]) -> dict[str, str]:
    # swap some stuff (how many?)
    first = random_letter()
    second = random_letter()
    # print(letters_map)
    temp = letters_map[first]
    letters_map[first] = letters_map[second]
    letters_map[second] = temp
    return letters_map


def decrypt_without_alphabet(text: str) -> str:
    best_letters_map = {chr(l): chr(l) for l in range(ord("A"), ord("Z") + 1)}
    best_score = ngram.score(map_letters(text, best_letters_map))
    epochs = 0
    for _ in range(MAX_EPOCHS):
        letters_map = randomly_swap_letters(best_letters_map.copy())
        solve = map_letters(text, letters_map)
        score = ngram.score(solve)
        # we sometimes need to accept suboptimal solutions to avoid converging to local maxima
        if score > best_score or random.random() < math.exp(score - best_score):
            best_letters_map = letters_map
            best_score = score
            eprint(solve)
            eprint(f"new best scrore: {best_score}")
        epochs += 1

    alphabet = "".join(best_letters_map[chr(l)] for l in range(ord("A"), ord("Z") + 1))
    eprint(f"decrypted with alphabet: {alphabet}")

    encrypt_map = {v: k for k, v in best_letters_map.items()}
    enc_alpha = "".join(encrypt_map[chr(l)] for l in range(ord("A"), ord("Z") + 1))
    eprint(f"encrypted with alphabet: {enc_alpha}")

    return map_letters(text, best_letters_map)


def alphabet_to_map(alphabet: str) -> dict[str, str]:
    return {chr(l): alphabet[i] for i, l in enumerate(range(ord("A"), ord("Z") + 1))}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="monoalphabetic",
        description="attempts to decrypt a monoalphabetic cipher in a given file",
    )
    parser.add_argument("filename")
    parser.add_argument("-a", "--alphabet", help="alphabet to map using, in A-Z order")

    args = parser.parse_args()

    ngram = NGramScore("english_trigrams.txt")

    with open(args.filename, "r") as f:
        text = f.read()

    if args.alphabet is not None:
        letters_map = alphabet_to_map(args.alphabet)
        print(map_letters(text, letters_map))
    else:
        print(decrypt_without_alphabet(text))
