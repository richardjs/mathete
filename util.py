BOOKS = [
    'Mt',
    'Mk',
    'Lk',
    'Jn',
    'Acts',
    'Rm',
    '1 Co',
    '2 Co',
    'Ga',
    'Eph',
    'Php',
    'Col',
    '1 Th',
    '2 Th',
    '1 Ti',
    '2 Ti',
    'Ti',
    'Phi',
    'Heb',
    'Jm',
    '1 Pt',
    '2 Pt',
    '1 Jn',
    '2 Jn',
    '3 Jn',
    'Jd',
    'Rev',
]

def book_string(morphgnt_string):
    book = int(morphgnt_string[0:2])
    chapter = int(morphgnt_string[2:4])
    verse = int(morphgnt_string[4:6])
    return '%s %d:%d' % (BOOKS[book - 1], chapter, verse)
