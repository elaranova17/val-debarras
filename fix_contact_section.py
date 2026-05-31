#!/usr/bin/env python3
"""Idempotent: rend le bloc .form-info (Contact + titre + contacts + 4 photos)
identique sur les pages services, en utilisant index.html comme source canonique.
"""
import sys

CANON_FILE = "index.html"
TARGETS = [
    "ge-appartement.html",
    "ge-maison.html",
    "ge-succession.html",
    "ge-ems.html",
    "ge-diogene.html",
    "ge-nettoyage.html",
]

START = '<div class="form-info">'
END = '<div class="form-card">'


def extract_block(text, fname):
    i = text.find(START)
    if i == -1:
        raise SystemExit(f"{fname}: '{START}' introuvable")
    j = text.find(END, i)
    if j == -1:
        raise SystemExit(f"{fname}: '{END}' introuvable après form-info")
    return i, j, text[i:j]


def main():
    with open(CANON_FILE, encoding="utf-8") as f:
        canon_text = f.read()
    _, _, canon_block = extract_block(canon_text, CANON_FILE)

    changed = []
    for fname in TARGETS:
        with open(fname, encoding="utf-8") as f:
            text = f.read()
        i, j, block = extract_block(text, fname)
        if block == canon_block:
            print(f"{fname}: déjà à jour (no-op)")
            continue
        new_text = text[:i] + canon_block + text[j:]
        with open(fname, "w", encoding="utf-8") as f:
            f.write(new_text)
        changed.append(fname)
        print(f"{fname}: mis à jour")

    print(f"\n{len(changed)} page(s) modifiée(s): {changed}")


if __name__ == "__main__":
    main()
