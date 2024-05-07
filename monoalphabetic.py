#!/usr/bin/env python3

import sys
import math
import random

MAX_EPOCHS = 10_000

from ngram import NGramScore

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def random_letter():
    return chr(random.randrange(ord("A"), ord("Z") + 1))


def map_letters(src: str, letters_map: dict[str, str]) -> str:
    return "".join(
        (
            letters_map[c]
            if c.isupper()
            else letters_map[c.upper()].lower() if c.islower() else c
        )
        for c in src
    )


def randomly_swap_letters(letters_map: dict[str, str]):
    # swap some stuff (how many?)
    first = random_letter()
    second = random_letter()
    letters_map = best_letters_map.copy()
    # print(letters_map)
    temp = letters_map[first]
    letters_map[first] = letters_map[second]
    letters_map[second] = temp
    return letters_map


if __name__ == "__main__":
    ngram = NGramScore("english_trigrams.txt")

    with open(sys.argv[1], "r") as f:
        src = f.read()

    best_letters_map = {chr(l): chr(l) for l in range(ord("A"), ord("Z") + 1)}
    best_score = ngram.score(map_letters(src, best_letters_map))
    epochs = 0
    for _ in range(MAX_EPOCHS):
        letters_map = randomly_swap_letters(best_letters_map.copy())
        solve = map_letters(src, letters_map)
        score = ngram.score(solve)
        # we sometimes need to accept suboptimal solutions to avoid converging to local maxima
        if score > best_score or random.random() < math.exp(score - best_score):
            best_letters_map = letters_map
            best_score = score
            epochs_since_improvement = 0
            eprint(solve)
            eprint(f"new best scrore: {best_score}")
        epochs += 1

    print(map_letters(src, best_letters_map))
