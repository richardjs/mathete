from xml.etree import ElementTree
import unicodedata

from config import STRONGS_PATH


tree = ElementTree.parse(STRONGS_PATH)


number_words = {}
for entry in tree.find('entries').findall('entry'):
    number = int(entry.find('strongs').text)
    try:
        word = entry.find('greek').attrib['unicode']
    except AttributeError:
        continue
    number_words[number] = word


definitions = {}
for entry in tree.find('entries').findall('entry'):
    try:
        word = entry.find('greek').attrib['unicode']
        word = unicodedata.normalize('NFC', word)

        # special case
        if word == 'τὶς':
            word = 'τις'

    except AttributeError as e:
        continue
    definition_e = entry.find('strongs_def')
    if definition_e == None:
        definition_e = entry.find('strongs_derivation')
    if definition_e == None:
        continue

    number = int(entry.find('strongs').text)
    definition = ''
    for e in definition_e.iter():
        if e.text:
            definition += e.text

        if e.tag == 'strongsref':
            if e.attrib['language'] == 'GREEK':
                definition += number_words[int(e.attrib['strongs'])]
            else:
                definition += '#%d' % (int(e.attrib['strongs']))
        elif e.tag == 'greek':
            definition += e.attrib['unicode']

        if e.tail:
            definition += e.tail

    definition = definition.replace('\n', '')

    definitions[word] = definition
