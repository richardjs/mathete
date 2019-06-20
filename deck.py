import frequency
import sentences
import strongs

N = 100

class Entry:
    pass

def main():
    entries = []
    seen = set()
    for lemma in frequency.lemma_frequency_ranks()[:N]:
        sentence, _ = sentences.top_sentence_for_lemma(lemma)
        for word in sentence:
            entries.append(word.lemma, sentence)
            seen.add(word.lemma)

if __name__ == '__main__':
    main()
