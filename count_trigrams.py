import re
from collections import Counter

with open("names.txt", "r") as f:
    text = f.read()

print("read text in")
text = re.sub(r"[^A-Za-z]+", '', text).upper()

print("text cleaned")
L = 3
counts = Counter(text[i:i + L] for i in range(len(text) - L + 1))
print("counted")

with open("names_trigrams.txt", "w") as o:
    counts = reversed(sorted(counts.items(), key=lambda p: p[1]))
    for gram, count in counts:
        o.write(f"{gram} {count}\n")
