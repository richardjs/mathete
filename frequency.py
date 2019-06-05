from collections import Counter
from functools import lru_cache
import heapq
import os
import re
import unicodedata

from config import MORPHGNT_DIR
import strongs


@lru_cache()
def count_lemmas():
    lemmas = Counter()
    for book in os.listdir(MORPHGNT_DIR):
        with open(os.path.join(MORPHGNT_DIR, book)) as f:
            for line in f:
                _, _, _, _, _, _, lemma = line.split()
                lemma = unicodedata.normalize('NFC', lemma)

                # special cases
                # if lemma == 'οἶδα':
                #    lemma = 'εἴδω'
                # elif lemma == 'ἀποθνῄσκω':
                #    lemma = 'ἀποθνήσκω'
                # elif lemma == 'σῴζω':
                #    lemma = 'σώζω'

                lemma = re.sub(r'\(.*\)', '', lemma)

                lemmas[lemma] += 1

    return lemmas


@lru_cache()
def lemma_frequency_ranks():
    lemma_counts = count_lemmas()
    pq = []
    for lemma, count in lemma_counts.items():
        heapq.heappush(pq, (count, lemma))

    lemmas = []
    while pq:
        lemmas.append(heapq.heappop(pq)[1])

    return list(reversed(lemmas))


if __name__ == '__main__':
    print(lemma_frequency_ranks()[:10])
