import re

ALPHA_REGEX = re.compile(r"[^A-Za-z]+")

def clean_text(text: str) -> str:
    return ALPHA_REGEX.sub("", text).upper()
