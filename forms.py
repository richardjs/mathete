from functools import lru_cache
import os
import unicodedata

from config import MORPHGNT_DIR


@lru_cache()
def lemma_forms():
    forms = {}
    for book in os.listdir(MORPHGNT_DIR):
        with open(os.path.join(MORPHGNT_DIR, book)) as f:
            for line in f:
                _, _, parse, _, word, _, lemma = line.split()
                lemma = unicodedata.normalize('NFC', lemma)

                if lemma not in forms:
                    forms[lemma] = {}

                if parse not in forms[lemma]:
                    forms[lemma][parse] = set()

                forms[lemma][parse].add(word)

    return forms


if __name__ == '__main__':
    print(lemma_forms())
