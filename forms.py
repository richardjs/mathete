from collections import Counter
from functools import lru_cache
import os
import re
import unicodedata

from config import MORPHGNT_DIR
import sentences

PRINCIPLE_PARTS = [
    '.PAI....',
    '.FAI....',
    '.AAI....',
    '.PAI....',
    '.PMI....',
    '.API....',
]


def principal_part(word):
    for i, part in enumerate(PRINCIPLE_PARTS):
        if re.match(part, lemma):
            return i+1


@lru_cache()
def principal_parts(lemma):
    forms = lemma_forms()[lemma]
    for form, words in forms.items():
        print(form, words)


@lru_cache()
def word_parses():
    parses = {}
    for book in os.listdir(MORPHGNT_DIR):
        with open(os.path.join(MORPHGNT_DIR, book)) as f:
            for line in f:
                line = unicodedata.normalize('NFC', line)
                _, _, parse, _, word, _, _ = line.split()
                if word not in parses:
                    parses[word] = set()
                parses[word].add(parse)
                if len(parses[word]) > 1:
                    print(word, parses[word])
                    input()
    return parses


@lru_cache()
def lemma_forms():
    forms = {}
    for book in os.listdir(MORPHGNT_DIR):
        with open(os.path.join(MORPHGNT_DIR, book)) as f:
            for line in f:
                line = unicodedata.normalize('NFC', line)
                _, _, parse, _, word, _, lemma = line.split()

                if lemma not in forms:
                    forms[lemma] = {}

                if parse not in forms[lemma]:
                    forms[lemma][parse] = Counter()

                forms[lemma][parse][word.lower()] += 1

    return forms


def enumerate_combos():
    combos = {}
    for book in os.listdir(MORPHGNT_DIR):
        with open(os.path.join(MORPHGNT_DIR, book)) as f:
            for line in f:
                line = unicodedata.normalize('NFC', line)
                _, part, parse, _, word, _, lemma = line.split()
                combo = part + parse
                if combo in combos:
                    occurrences = combos[combo]
                else:
                    occurrences = Counter()
                    combos[combo] = occurrences
                occurrences[word] += 1
    return combos


def top_words_for_combos():
    combos = enumerate_combos()

    combo_max = {}
    for combo in sorted(combos.keys()):
        max_word = None
        max_count = 0
        for word, count in combos[combo].items():
            if count > max_count:
                max_count = count
                max_word = word
        combo_max[combo] = (max_word, max_count)

    return combo_max


if __name__ == '__main__':
    print(top_words_for_forms())
