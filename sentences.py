from functools import lru_cache
from operator import itemgetter
import os
import re
import unicodedata

from config import MORPHGNT_DIR
import frequency
import util


class Word:
    def __init__(self, word, lemma, form):
        self.word = word
        self.lemma = lemma
        self.form = form

    def __str__(self):
        return self.word

    def __repr__(self):
        return self.__str__()


class Sentence:
    def __init__(self):
        self.words = []
        self.verses = set()

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return hash(tuple(word.word for word in self.words))

    def __str__(self):
        return ' '.join([word.word for word in self.words])

    def __repr__(self):
        return self.__str__()

    def __iter__(self):
        yield from self.words


@lru_cache()
def gather_sentences():
    sentences = set()
    for book in os.listdir(MORPHGNT_DIR):
        sentence = Sentence()
        with open(os.path.join(MORPHGNT_DIR, book)) as f:
            for line in f:
                line = unicodedata.normalize('NFC', line)
                verse, pos, parse, word, _, _, lemma = line.split()

                word = word.replace('⸀', '')
                word = word.replace('⸂', '')
                word = word.replace('⸃', '')

                lemma = re.sub(r'\(.*\)', '', lemma)

                sentence.words.append(Word(word, lemma, pos+parse))
                sentence.verses.add(util.book_string(verse))

                if '.' in word or ';' in word:
                    sentences.add(sentence)
                    sentence = Sentence()

    return(sentences)


@lru_cache(maxsize=10000)
def score_sentence(sentence):
    counts = frequency.count_lemmas()
    min_count = max(counts.values())
    for word in sentence:
        min_count = min(min_count, counts[word.lemma])
    return min_count


@lru_cache(maxsize=10000)
def score_sentence_frequency_ranks(sentence):
    lemma_ranks = frequency.lemma_frequency_ranks()
    max_frequency_rank = 0
    for word in sentence:
        max_frequency_rank = max(
            max_frequency_rank, lemma_ranks.index(word.lemma))
    return max_frequency_rank


@lru_cache()
def score_sentences():
    sentences = gather_sentences()

    sentence_scores = {}
    for sentence in sentences:
        sentence_scores[sentence] = score_sentence(sentence)

    return sentence_scores


@lru_cache()
def sorted_sentences():
    sentence_scores = score_sentences()
    return [sentence for (sentence, score) in sorted(sentence_scores.items(), key=itemgetter(1))]


@lru_cache()
def sentences_under_score(score):
    scores = score_sentences()
    sentences = []
    for sentence, score in scores.items():
        if score < i:
            sentences.append(sentence)
    return sentences


@lru_cache()
def top_sentence_for_lemma(lemma):
    min_score = 10000
    min_sentence = None
    for sentence in gather_sentences():
        if lemma not in [word.lemma for word in sentence]:
            continue
        score = score_sentence(sentence)
        if score < min_score:
            min_score = score
            min_sentence = sentence
    return min_sentence, min_score


if __name__ == '__main__':
    print(sorted_sentences()[:10][0].verses)
