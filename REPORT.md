# CSC321 Historic Crypto Report

## Principles

### Caesar

Offset all letters in the source text by a fixed numerical shift based on a
given alphabet, usually the English alphabet. For example, a shift of 3 would
shift the letter A -> C. If it passes the end of the sequence wrap around to the
start of the sequence. To decrypt, simply shift the letter the opposite amount,
or an equivalent number in the period of 26.

### Monoalphabetic

Map all letters to another letter in the English alphabet based on a known
mapping. To decrypt, simply perform that mapping in reverse. For example, one
might map all As to Xs, and then to decrypt map all Xs to As.

### Vigenère

Encrypt each letter by addition of the source text with the letter of a
repeating key of fixed length, wrapping around the alphabet. To decrypt, one
uses the repeating key and subtracts it from the encrypted text to reverse the
process.

## Implementation

### Caesar

Iterate through a string character by character. For each character, convert it
to a numerical value using `ord`, and then subtract the letter A to get the
offset of the character from the start of the alphabet. Of course, a bit of
consideration is required to correctly shift both upper and lowercase English
characters in identical manners, since they correspond to different blocks of
ASCII codes, so the case of the character must be detected beforehand, and its
offset calculated by subtracting either `ord('A')` or `ord('a')`. Once the
offset is calculated, one can simply add the shift and modulo by 26 to properly
implement wrapping behavior.

For decryption, the same process can be followed but simply with an opposite
shift of the initial shift.

This is implemented in [caesar.py](./caesar.py) in `rotn`, which accepts the
text and the amount to shift it by.

Usage:
```shell
./caesar.py -s 18 decrypted/caesar_easy_decrypted.txt
```

```python
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
```

### Monoalphabetic

First construct a mapping between letters of the alphabet. In my implementation,
this is done by taking input from the user, where the user inputs a 26 character
long strong of uppercase alphabetic characters where each character corresponds
to the mapping of the equivalent place in the English alphabet. For example, a
strong staring with 'W' would indicate mapping the first letter, 'A' to 'W'.
This string is then converted to a Python dictionary. (I could've used an array
for better performance in theory but like I'm already using python.)

After constructing a mapping, the source text can be iterated
character-by-character and then mapped to the corresponding character via the
mapping. If a character is lowercase, it is converted to uppercase, mapped to
the corresponding character, and then converted back to lowercase. Any
characters not present in the mapping are mapped directly without modification.

For decryption with a known mapping, the same process can simply followed in
reverse. With my implementation this can simply be done by swapping the keys and
values in the dictionary to reverse the map and performing the same process.

This is implemented in [monoalphabetic.py](./monoalphabetic.py) in
`map_letters`, with mapping construction done in `alphabet_to_map`.

Usage:
```shell
./monoalphabetic.py --alphabet ZYORBUNXLPMJTISQVGFKWCAHDE decrypted/mono_easy_decrypted.txt
```

```python
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
```

### Vigenère

Iterate through each character in the source string and find the corresponding
index in the key based on a modulo of it's length (to cause it to repeat). After
applying appropriate math to get the offsets as with the previous ciphers, add
the two together to get a new offset and then convert that back to the final
code point. A minor note is that a separate index must be maintained for the key
than for the current character, as non-alphabetic character need to be mapped
directly without incrementing the index.

Decryption is the same process, only the key is subtracted from the offset in
the cypher text as opposed to adding it.

This is implemented in [vingere.py](./vingere.py) in `encrypt` and `decrypt`,
respectively.

Usage: 
```shell
./vingere.py --encrypt --key MFXJT decrypted/vigerene_easy_decrypted.txt
./vingere.py --key MFXJT encrypted/vigerene_easy_encrypted.txt
```

```python
def encrypt(text: str, key: str) -> str:
    """
    Encrypt the source text using the vingere cypher

    text - source text
    key - key

    returns - encrypted text
    """
    encrypted = ""
    i = 0
    for l in text:
        if l.isalpha():
            off = ord("A") if l.isupper() else ord("a")
            p = ord(l) - off
            k = ord(key[i % len(key)]) - ord("A")
            c = (p + k) % 26
            encrypted += chr(c + off)
            i += 1
        else:
            encrypted += l
    return encrypted

def decrypt(text: str, key: str) -> str:
    """
    Decrypt the source text using the vingere cypher

    text - source text
    key - key

    returns - decrypted text
    """
    decrypted = ""
    i = 0
    for l in text:
        if l.isalpha():
            off = ord("A") if l.isupper() else ord("a")
            p = ord(l) - off
            k = ord(key[i % len(key)]) - ord("A")
            c = (p - k) % 26
            decrypted += chr(c + off)
            i += 1
        else:
            decrypted += l
    return decrypted
```

## Cracking

### N-Gram Fitness Scoring

The core metric all these algorithms rely on for evaluating the quality of a
particular solve is based on English n-grams. The basic concept is that given a
sequence of characters the probability of all of them occurring in a given
language can be calculated using the joint probability that each n-letter
sequence can occur in the language, assuming the probabilities of each sequence
are independent.

In other words, the probability that a given sequence of
characters will occur in the English language is measured as:

$$p(s_1, s_2, ..., s_n) = p(s_1) * p(s_2) * ... * p(s_n)$$

However, multiplication is a comparatively costly operation and probabilities
for long sequences are at risk of growing untenably small, risking floating
point precision issues. To resolve this, we can simply apply log to both sides
of the equation to get the log probability, expressed as a sum of the log
individual probabilities using log properties.

$$\log (p(s_1, s_2, ..., s_n)) = \log (p(s_1)) * \log (p(s_2)) * ... * \log (p(s_n))$$
