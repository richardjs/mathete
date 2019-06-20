from collections import Counter
from operator import itemgetter
import re

import genanki

from sentences import score_sentences
from strongs import definitions

FORM_EXAMPLES_TARGET = 10


deck = genanki.Deck(
    1136510236,
    'Mathete',
)

word_model = genanki.Model(
    2097373794,
    'Mathete Word',
    fields=[
        {'name': 'Lemma'},
        {'name': 'Definition'},
    ],
    templates=[
        {
            'name': 'Word definition',
            'qfmt': 'Definition of {{Lemma}}',
            'afmt': '{{Lemma}}<hr id="answer">{{Definition}}'
        },
    ],
)

form_model = genanki.Model(
    1633583284,
    'Mathete Form',
    fields=[
        {'name': 'Word'},
        {'name': 'Form'},
    ],
    templates=[
        {
            'name': 'Word form',
            'qfmt': 'Form of {{Word}}',
            'afmt': '{{Word}}<hr id="answer">{{Form}}'
        },
    ],
)

sentence_model = genanki.Model(
    1262995617,
    'Mathete Sentence',
    fields=[
        {'name': 'Sentence'},
    ],
    templates=[
        {
            'name': 'Sentence',
            'qfmt': '{{Sentence}}',
            'afmt': '{{Sentence}}<hr id="answer">Understand it?'
        },
    ],
)


def new_word_card(word):
    deck.add_note(genanki.Note(model=word_model, fields=[
        word.lemma,
        definitions.get(word.lemma, 'Definition not found.'),
    ]))


def new_form_card(word):
    deck.add_note(genanki.Note(model=form_model, fields=[
        word.word,
        word.form,
    ]))


def new_sentence_card(sentence):
    deck.add_note(genanki.Note(model=sentence_model, fields=[
        str(sentence),
    ]))


sentences = sorted(score_sentences().items(), key=itemgetter(1), reverse=True)

learned_lemmas = set()
form_examples = Counter()
seen_form_examples = set()
for sentence, _ in sentences[:20]:
    for word in sentence:
        if word.lemma not in learned_lemmas:
            new_word_card(word)
            learned_lemmas.add(word.lemma)
        form = word.form.lower()
        if (form_examples[form] < FORM_EXAMPLES_TARGET
                and form+word.lemma not in seen_form_examples
                and not re.match(r'..--------', form)):
            new_form_card(word)
            form_examples[form] += 1
            seen_form_examples.add(form+word.lemma)
    new_sentence_card(sentence)
    print(sentence)

genanki.Package(deck).write_to_file('mathete.apkg')
