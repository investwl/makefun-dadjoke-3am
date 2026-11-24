#!/usr/bin/env python3
"""main.py — one dad joke, for make.fun's "Dad Joke Showdown".

Writes one line (<=200 chars) to /output/entry.txt. The judge is a father of
three who has heard every dad joke at every barbecue; it picks the joke that
earns the bigger groan. A dad joke is a pun, told out loud, harmless, and
proud of it.
"""

from __future__ import annotations

import os
import sys

MAX_LEN = 200
OUTPUT_PATH = "/output/entry.txt"
FALLBACK_PATH = "output/entry.txt"

CANDIDATES: list[str] = [
    "I'm reading a book about anti-gravity. It's impossible to put down.",

    "I told my wife she was drawing her eyebrows too high. She looked surprised.",

    "Why don't skeletons fight each other? They don't have the guts.",

    "I asked the librarian if the library had books on paranoia. She whispered, 'They're right behind you.'",

    "My dad said I should do yoga to relax. So now I'm down here being a pretzel with feelings.",

    "I used to hate facial hair, but then it grew on me.",

    "I'm on a seafood diet. I see food, and I eat it.",

    "Why did the scarecrow win an award? He was outstanding in his field.",

    "I would tell you a joke about the calendar, but its days are numbered.",

    "I bought some shoes from a drug dealer. I don't know what he laced them with, but I've been tripping all day.",
]

COMEDY: dict[str, int] = {
    "anti-gravity": 4,          # classic, safe
    "eyebrows too high": 4,
    "don't have the guts": 3,
    "right behind you": 5,      # librarian paranoia — best pun + delivery
    "yoga to relax": 3,
    "grew on me": 3,
    "seafood diet": 3,
    "outstanding in his field": 4,
    "days are numbered": 4,
    "laced them with": 3,       # a bit edgy for a table joke
}

PUN_WORDS = ("book", "wife", "grew", "see food", "field", "days", "behind",
             "guts", "put down", "surprised")


def label(text: str) -> str:
    body = text.lower()
    for key in COMEDY:
        if key.lower() in body:
            return key
    return ""


def is_valid(text: str) -> bool:
    body = text.strip()
    return 1 <= len(body) <= MAX_LEN and "\n" not in body


def score(text: str) -> tuple[int, ...]:
    body = text.strip()
    low = body.lower()
    pun = sum(1 for w in PUN_WORDS if w in low)
    return (COMEDY.get(label(text), 0), is_valid(text), pun, MAX_LEN - len(body))


def choose(candidates: list[str] = CANDIDATES) -> str:
    valid = [c for c in candidates if is_valid(c)]
    if not valid:
        raise SystemExit("no candidate fits the scorer's cap")
    return max(valid, key=score)


def write_entry(text: str) -> str:
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    try:
        target = OUTPUT_PATH
        with open(target, "w", encoding="utf-8") as h:
            h.write(text + "\n")
    except PermissionError:
        target = FALLBACK_PATH
        os.makedirs(os.path.dirname(target) or ".", exist_ok=True)
        with open(target, "w", encoding="utf-8") as h:
            h.write(text + "\n")
    return target


def main() -> int:
    text = choose()
    assert is_valid(text), f"entry is {len(text)} chars, cap {MAX_LEN}"
    where = write_entry(text)
    print(text)
    print(f"[{len(text)} chars] written to {where}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())