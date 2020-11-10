'''
This file is a part of whrwthal.
whrwthal is an offline bible referencing module.
Copyright (C) 2020 Gregory Caceres-Munsell <gregcaceres@gmail.com>
_______________________________________________

The Biblical translations used herein are all
in the public domain, and free to use, quote,
modify, or share without limit.

For general support, or if you have any
questions about whrwthal's functionality,
the content of the word of God, or
anything else related, feel free
to contact me directly.
_______________________________________________
'''

from collections import OrderedDict
import os
import json
import re
import string


def find(self, srch):
    d = OrderedDict()
    b, r, f = regex(self, srch)
    book = re.split(b, self.text, flags=re.MULTILINE | re.DOTALL)[1:]
    pattern = re.compile(r, flags=f)
    for i in range(0, len(book), 2):
        b = book[i]
        match = pattern.finditer(book[i+1])
        for m in match:
            ref = ' '.join([b, m.group(2)])
            d[ref] = m.group(1)
    return d, len(d)


def regex(self, srch):
    '''
    Takes input and executes the following logic to determine a regular
    expression to assign. Returns a string which is used for both phrase
    and verse srches.

    If entry contents reference a book, and chapter or verse:

        1:: "ROM 16:1-3" Returns a regex matching Romans chapter 12 verses
            "Rom 12:1" Returns a regex matching Romans chapter 12 verse 1.
                1 through 3.
            "romans 1" Returns a regex matching Romans chapter 1.

        1.5:: "rom" Returns a regex matching Romans chapter 1.

    Else If entry contents only reference a number combination:

        2:: "1:3" Returns any 3rd verse from any 1st chapter (if it exists)
            "23" Returns the 23rd chapter of every book (if it exists)
            

    Else:
        3:: "phrase of words" Returns a regex matching "phrase of words"
            "word" Returns a regex matching "word"
    '''
    # Table of contents entry check, any full or abbreviated reference
    ToC = self.bkAbbrv + self.bkNames
    uconcord = [w.upper() for w in self.concordance]

    upper = srch.upper()
    # There exists an entry "e" referencing the ToC if its uppercase
    # form appears as either an abbreviation or word: e = "ROM/ROMAN"
    usplit = upper.split()
    ToC_entries = [e for e in usplit if e in ToC]
    ToC_count = len(ToC_entries)

    conc_entries = [W for W in uconcord if W in usplit]
    conc_count = len(conc_entries)

    numeric_entries = [e for e in srch if e.isnumeric()]

    u = self.use_re
    a = any(ToC_entries)
    b = any(numeric_entries)
    c = any(conc_entries)
    count = 0
    if u:
        print('0::')
        # User specified regular expression
        alph = r'^([A-Z]+)$'
        return alph, srch
    # TODO: It looks like unique cases may be needed for Chapters & for Verses
    # CHAPTER
    elif a and b:
        print('1:: %s' % (srch))
        alph = ''.join([char.upper() for char in srch if char.isalpha()])
        numb = ''.join([char for char in srch if (not(char.isalpha())
                        and not(char.isspace()))])
        return('(%s)' % (alph),
               r'^(({}):1 .*?)(?={}:1 ).*(?=^[A-Z]+$).*(?=\Z)'.format(numb, str(int(numb)+1)),
               re.DOTALL | re.MULTILINE)
    # VERSE
    # elif...:
        # print('1.X:: %s' % (srch))
    elif (a and not b):
        print('1.5:: %s' % (srch))
        alph = r''.join([char.upper() for char in srch if char.isalpha()])
        return alph, r'({})\n(1:\d+) (.*?)(?=2:1 )'.format(upper)
    elif b:
        print('2:: %s' % (srch))
        alph = r'^([A-Z]+)$'
        numb = ''.join([char for char in srch if (not(char.isalpha())
                        and not(char.isspace()))])
        return(alph,
               r'^(({}).*)$'.format(numb),
               None)
    elif (c and not(any([a, b]))):
        print('3:: %s' % (srch))
        alph = r'^([A-Z]+)$'
        return(alph,
               r'^((\d+:\d+).*\b{}\b.*?)$'.format(srch),
               re.IGNORECASE | re.MULTILINE)
    if not(any([u, a, b, c])):
        raise KeyError


def navigate(self, vector, event=None):
    ref = self.frame.header.cget('text')
    _, _, numb, nref = numbeval(ref)
    srch = ref.replace(numb, str(nref + vector))
    try:
        d, count = find(self, srch)
        h = [k for k in d.keys()][0]
        t = [v for v in d.values()][0]
        self.handler.gui_update(self, head=h, text=t,
                                status='{} RESULT MATCHING \"{}\"'.format(
                                    count, srch))
    except IndexError:
        # FIXME: See "Romans 17"
        _, book = alpheval(srch)
        idx = self.bkNames.index(book)
        if numb == 1:
            # <Ctl-k> on "romans 1" should return "Acts 28"
            book = self.bkNames[idx - 1]
        else:
            # <Ctl-j> on "romans 16" should return "i corinthians 1"
            book = self.bkNames[idx + 1]


def toc():
    # Table of Contents
    bkNames = ['GENESIS', 'EXODUS', 'LEVITICUS', 'NUMBERS', 'DEUTERONOMY',
               'JOSHUA', 'JUDGES', 'RUTH', 'ISAMUEL', 'IISAMUEL',
               'IKINGS', 'IIKINGS', 'ICHRONICLES', 'IICHRONICLES',
               'EZRA', 'NEHEMIAH', 'ESTHER', 'JOB', 'PSALMS', 'PROVERBS',
               'ECCLESIASTES', 'SONG OF SONGS', 'ISAIAH', 'JEREMIAH',
               'LAMENTATIONS', 'EZEKIEL', 'DANIEL', 'HOSEA', 'JOEL',
               'AMOS', 'OBADIAH', 'JONAH', 'MICAH', 'NAHUM', 'HABAKKUK',
               'ZEPHANIAH', 'HAGGAI', 'ZECHARIAH', 'MALACHI', 'MATTHEW',
               'MARK', 'LUKE', 'JOHN', 'ACTS', 'ROMANS', 'ICORINTHIANS',
               'IICORINTHIANS', 'GALATIANS', 'EPHESIANS', 'PHILIPPIANS',
               'COLOSSIANS', 'ITHESSALONIANS', 'IITHESSALONIANS',
               'ITIMOTHY', 'IITIMOTHY', 'TITUS', 'PHILEMON', 'HEBREWS',
               'JAMES', 'IPETER', 'IIPETER', 'IJOHN', 'IIJOHN',
               'IIIJOHN', 'JUDE', 'REVELATION']
    bkAbbrv = ['GEN', 'EXO', 'LEV', 'NUM', 'DEUT',
               'JOSH', 'JUD', 'RU', 'ISA', 'IISA',
               'IKI', 'IIKI', 'ICHRON', 'IICHRON',
               'EZR', 'NEH', 'EST', 'JOB', 'PSA', 'PRO',
               'ECC', 'SONG', 'ISA', 'JER',
               'LAM', 'EZE', 'DAN', 'HOS', 'JOE', 'AMO',
               'OBAD', 'JON', 'MIC', 'NAH', 'HAB', 'ZEP',
               'HAG', 'ZEC', 'MAL', 'MATT', 'MAR', 'LUK',
               'JOH', 'ACT', 'ROM', 'ICOR', 'IICOR',
               'GAL', 'EPH', 'PHLP', 'COL',
               'ITHESS', 'IITHESS', 'ITIM',
               'IITIM', 'TIT', 'PHM', 'HEB', 'JAM',
               'IPE', 'IIPE', 'IJO', 'IIJO', 'IIIJO', 'JU',
               'REV']
    return bkNames, bkAbbrv


def make_text(**kwargs):
    '''
    Returns a str():

        text = "Alpha ... Omega"

    Key-word arguments consist of 'd' and 'filename'.

    Use:

        Return the string, don't write to file:

            text = make_text()

        Return the string and write it to plain-text file ``f``:

            text = make_text(filename='f')

        Return the string and write it to plain-text file ``f``:

            text = make_text(filename='f')

        Return the string and write it to plain-text file ``f`` using namespace
        dictionary ``dict()`` as the source instead of default ``./src.json``:

            text = make_text(d=dict(), filename='f')

    Alternative source texts @ https://github.com/GregCM/whrwthal/tree/texts
    '''
    # ===================================================
    # Handling key word arguments:
    keys = kwargs.keys()
    if 'd' in keys:
        d = kwargs['d']
    else:
        # dummy dictionary to signify read from file
        d = None
    if 'filename' in keys:
        filename = kwargs['filename']
    else:
        # dummy filename to signify no file output
        filename = ''
    # ===================================================
    # Import dictionary:
    if not(d):
        with open('src.json') as f:
            d = json.load(f, object_pairs_hook=OrderedDict)
    # ===================================================
    # Parse text from dictionary:
    text = []
    for b in d:
        if (b != 'CONCORDANCE') and (b != 'ToC'):
            for c in d[b]:
                if c == '1':
                    # grabs the first verse of the first chapter in a book
                    # (' Book Chapter:Verse')
                    if b == 'GENESIS':
                        form = '{} {}:{} {}'
                    else:
                        form = ' {} {}:{} {}'
                    first = ''.join([form.format(b, c, v, d[b][c][v])
                                     for v in d[b][c] if v == '1'])
                    text.append(first)
                    # remaining verses (' Chapter:Verse')
                    remains = ''.join([' {}:{} {}'.format(c, v, d[b][c][v])
                                       for v in d[b][c] if v != '1'])
                    text.append(remains)
                else:
                    # remaining verses (' Chapter:Verse')
                    remains = ''.join([' {}:{} {}'.format(c, v, d[b][c][v])
                                       for v in d[b][c]])
                    text.append(remains)

    text = ''.join(text)
    # ===================================================
    # Handle file output:
    if os.path.exists(filename):
        with open('src.txt', 'w') as f:
            f.write(text)
    # ===================================================
    return text


def make_concord(self, text):
    # Exclude punctuation & numerberation
    words = []
    alpha = string.ascii_letters + ' '
    trim = ''.join([char for char in text if char in alpha])
    words.extend([w for w in set(re.split(' ', trim))
                  if w not in self.bkNames])
    # No space
    words.remove('')
    # Alphabetize
    words.sort()
    return words


def _make_json(**kwargs):
    '''
    Returns a nested dictionary:

        d = {book: {chapter: {verse: text }}}

    Key-word arguments consist of 'self', 'text', and 'filename'.

    Use:

        Return the dictionary, don't write to file:

            d = _make_json()

        Return the dictionary and write it to file ``f``:

            d = _make_json(filename=f)
    '''
    # ===================================================
    # Handling key word arguments:
    keys = kwargs.keys()
    if 't' in keys:
        text = kwargs['t']
    else:
        # dummy string to signify read from file
        text = None
    if 'filename' in keys:
        filename = kwargs['filename']
    else:
        # dummy filename to signify no file output
        filename = ''
    # ===================================================
    # Import source text:
    if not(text):
        with open('src.txt') as f:
            text = f.read()

    # ===================================================
    # Dictionary:
    d = OrderedDict()
    # Table of Contents
    d['ToC'] = toc()

    # PATTERN
    # ===============================================================
    # Book Title Group -- captures more than 2 capitals before a digit
    g1 = r'([A-Z]+)'
    # Chapter Number Group -- captures digit before a colon
    g2 = r'(\d+)'
    # Verse Number Group -- captures digit after a colon
    g3 = r'(\d+)'
    # SubText Group -- captures verse between digits/title, no trailing \s
    g4 = r'((?:[A-Z](?![A-Z]+ \d)|[^\dA-Z](?!(?:[A-Z]+ \d|\d)))*)'
    match = re.finditer(r'(?:%s(?= \d+:)|(?!^))(?:%s:%s)? %s'
                        % (g1, g2, g3, g4), text)
    # The full pattern is expressed:
    r'''
     (?:([A-Z]+)(?= \d+:)|(?!^))...
     ...(?:(\d+):(\d+))? ...
     ...((?:[A-Z](?![A-Z]+ \d)|[^\dA-Z](?![A-Z]+ \d|\d))*)
     '''
    # ===================================================
    # Dictionary Verse Number / Text Pairs:
    for m in match:
        if m.group(1):
            # Book Title
            b = m.group(1)
        else:
            # Chapter Number
            c = m.group(2)
            if m.group(3):
                # Verse Number
                v = m.group(3)
                # SubText
                st = m.group(4)
                # Initialize dict
                if b not in d:
                    d[b] = OrderedDict({c: OrderedDict({v: st})})
                # Initialize subdict
                elif c not in d[b]:
                    d[b][c] = OrderedDict({v: st})
                # Populate subdict
                else:
                    d[b][c][v] = st

    # ===================================================
    # Dictionary Concordance:
    # (uncomment and add self to _make_json's arguments if dict needs concord)
    # d['CONCORDANCE'] = make_concord(self, text)
    # ===================================================
    # Handle file output:
    if os.path.exists(filename):
        with open('src.json', 'w') as f:
            json.dump(d, f)
    # ===================================================
    return d
