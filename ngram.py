import re
import math

ALPHA_REGEX = re.compile(r"[^A-Za-z]+")


def clean_text(text: str) -> str:
    return ALPHA_REGEX.sub("", text).upper()


class NGramScore:
    def __init__(self, ngram_path: str) -> None:
        ngram = None
        with open(ngram_path, "r") as f:
            self.ngrams = {}
            for line in f:
                ngram, count = line.split()
                self.ngrams[ngram] = int(count)
        self.n = len(ngram) if ngram is not None else 0
        total = sum(self.ngrams.values())
        self.ngrams = {b: math.log(c / total) for b, c in self.ngrams.items()}
        self.floor = math.log(0.01 / self.n)

    def score(self, text):
        text = clean_text(text)
        return sum(
            (
                self.ngrams[text[i : i + self.n]]
                if text[i : i + self.n] in self.ngrams
                else self.floor
            )
            for i in range(len(text) - self.n + 1)
        )
