#!/usr/bin/env python3

from chi_square import chi_squared_freq

def rotn(text: str, shift: int) -> str:
    def shift_rel_to(c: str, to: str) -> str:
        return chr(((ord(c) - ord(to) + shift) % 26) + ord(to))

    def rotnc(c: str) -> str:
        return shift_rel_to(c, "A") if c.isupper() else shift_rel_to(c, "a")

    return "".join(rotnc(c) if c.isalpha() else c for c in text)


if __name__ == "__main__":
    import sys

    with open(sys.argv[1]) as f:
        src = f.read()

    chi_squareds = [chi_squared_freq(rotn(src, shift)) for shift in range(26)]
    best_shift = min(range(len(chi_squareds)), key=chi_squareds.__getitem__)
    print(f"Best Shift: {best_shift} with chi-squared: {chi_squareds[best_shift]:.4f}", file=sys.stderr)

    print(rotn(src, best_shift))
