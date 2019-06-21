from collections import Counter
from operator import itemgetter
import os
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
        {'name': 'Sentence'},
        {'name': 'Recording'},
    ],
    templates=[
        {
            'name': 'Word definition',
            'qfmt': 'Definition of {{Lemma}} {{Recording}}',
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
        {'name': 'Lemma'},
        {'name': 'Recording'},
    ],
    templates=[
        {
            'name': 'Word form',
            'qfmt': 'Form of {{Word}} {{Recording}}',
            'afmt': '{{Word}}<hr id="answer">{{Form}}<br>{{Lemma}}'
        },
    ],
)

sentence_model = genanki.Model(
    1262995617,
    'Mathete Sentence',
    fields=[
        {'name': 'Sentence'},
        {'name': 'Recording'},
    ],
    templates=[
        {
            'name': 'Sentence',
            'qfmt': '{{Sentence}} {{Recording}}',
            'afmt': '{{Sentence}}<hr id="answer">Understand it?'
        },
    ],
)

media_files = []


def speak(text):
    filename = str(hash(text))+'.wav'
    if not os.path.exists(os.path.join('media', filename)):
        os.system('espeak -v grc -s 100 -w %s "%s"' %
                  (os.path.join('media', filename), text))
    media_files.append(filename)
    return '[sound:%s]' % filename


def new_word_card(word, sentence):
    deck.add_note(genanki.Note(model=word_model, fields=[
        word.lemma,
        definitions.get(word.lemma, 'Definition not found.'),
        str(sentence),
        speak(word.lemma),
    ]))


def new_form_card(word):
    deck.add_note(genanki.Note(model=form_model, fields=[
        word.word,
        word.form,
        word.lemma,
        speak(word.word),
    ]))


def new_sentence_card(sentence):
    deck.add_note(genanki.Note(model=sentence_model, fields=[
        str(sentence),
        speak(str(sentence)),
    ]))


try:
    os.mkdir('media')
except FileExistsError:
    pass

sentences = sorted(score_sentences().items(), key=itemgetter(1), reverse=True)

learned_lemmas = set()
form_examples = Counter()
seen_form_examples = set()
for sentence, _ in sentences[:50]:
    for word in sentence:
        if word.lemma not in learned_lemmas:
            new_word_card(word, sentence)
            learned_lemmas.add(word.lemma)
        form = word.form.lower()
        if (form_examples[form] < FORM_EXAMPLES_TARGET
                and form+word.lemma not in seen_form_examples
                and not re.match(r'..--------', form)):
            new_form_card(word)
            form_examples[form] += 1
            seen_form_examples.add(form+word.lemma)
    new_sentence_card(sentence)

os.chdir('media')
package = genanki.Package(deck)
package.media_files = media_files
package.write_to_file('../mathete.apkg')
