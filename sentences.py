from functools import lru_cache
import os
import re
import unicodedata

from config import MORPHGNT_DIR
import frequency


class Word:
    def __init__(self, word, lemma):
        self.word = word
        self.lemma = lemma


class Sentence:
    def __init__(self):
        self.words = []

    def __str__(self):
        return ' '.join([word.word for word in self.words])

    def __repr__(self):
        return self.__str__()

    def __iter__(self):
        yield from self.words


@lru_cache()
def gather_sentences():
    sentences = []
    for book in os.listdir(MORPHGNT_DIR):
        sentence = Sentence()
        with open(os.path.join(MORPHGNT_DIR, book)) as f:
            for line in f:
                line = unicodedata.normalize('NFC', line)
                _, _, _, word, _, _, lemma = line.split()

                word = word.replace('⸀', '')
                word = word.replace('⸂', '')

                lemma = re.sub(r'\(.*\)', '', lemma)

                sentence.words.append(Word(word, lemma))

                if '.' in word:
                    sentences.append(sentence)
                    sentence = Sentence()

    return(sentences)


@lru_cache()
def score_sentences():
    lemma_ranks = frequency.lemma_frequency_ranks()
    sentences = gather_sentences()

    def score(sentence):
        max_frequency_rank = 0
        for word in sentence:
            max_frequency_rank = max(
                max_frequency_rank, lemma_ranks.index(word.lemma))
        return max_frequency_rank

    sentence_scores = {}
    for sentence in sentences:
        sentence_scores[sentence] = score(sentence)

    return sentence_scores


@lru_cache()
def sentences_under_score(score):
    scores = score_sentences()
    sentences = []
    for sentence, score in scores.items():
        if score < i:
            sentences.append(sentence)
    return sentences


if __name__ == '__main__':
    total_sentences = len(gather_sentences())
    for i in range(0, 51, 10):
        sentences = sentences_under_score(i)
        print(i, len(sentences), float(len(sentences))/float(total_sentences))
        print(sentences)
