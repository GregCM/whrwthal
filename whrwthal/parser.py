'''
This file is a part of whrwthal.
whrwthal is an offline bible referencing module.
Copyright (C) 2020 Gregory Caceres-Munsell <gregcaceres@gmail.com>
_______________________________________________

The Biblical translations used herein are all
in the public domain, and free to use, quote,
or share without limit.

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


def phrase(self, srch, use_re=False):
    out = OrderedDict()

    # PATTERN
    # Book Title Group -- captures more than 2 capitals before a digit
    g1 = r'([A-Z]+)'
    # Chapter Number Group -- captures digit before a colon
    g2 = r'(\d+)'
    # Verse Number Group -- captures digit after a colon
    g3 = r'(\d+)'
    # SubText Group -- captures verse between digits/title, no trailing \s
    g4 = r'((?:[A-Z](?![A-Z]+ \d)|[^\dA-Z](?!(?:[A-Z]+ \d|\d)))*)'
    match = re.finditer(r'(?:%s(?= \d+:)|(?!^))(?:%s:%s)? %s'
                        % (g1, g2, g3, g4), self.text)
    # SearchMatch
    if use_re:
        sm = re.compile(r'%(srch)s' % locals())
    else:
        # Case insensitive search, anywhere in a word.
        # --> "the" Returns "these", "anthem", "THE", etc.
        sm = re.compile(r'[^\d]*%(srch)s[^\d]*' % locals(), re.IGNORECASE)
    # Count serves as speed / crash prevention:
    # no one wants to see a 62,000-Count word list.
    count = 0
    err = None
    for m in match:
        if m.group(1):
            b = m.group(1)
        else:
            # Chapter
            c = m.group(2)
            # Verse
            v = m.group(3)
            # SubText
            st = m.group(4)
            # Search in st?
            if sm.match(st):
                ref = ''.join([b, ' ', c, ':', v])
                out[ref] = st
                # Every list with length greater than 2564 gets tossed
                count += 1
                if (count > 2564):
                    err = MemoryError
                    # TODO replace with Raise MemoryError
                    break
    return out, count, err


def verse(self, srch):
    out = OrderedDict()
    # ===============================================================
    # Alphabetic part of user's input
    alph, aref = alpheval(srch)
    # ===============================================================
    # Numeric part of user's input
    numb, trail, _, _ = numbeval(srch)
    lead = r'%(alph)s%(numb)s' % locals()
    match = re.finditer(r'%(lead)s(.+?)%(trail)s' % locals(), self.text)
    # ===============================================================
    # Sort the groups for dictionary and return
    count = 0
    err = None
    for m in match:
        if m.group(1):
            b = m.group(1)
        # No book was specified (or found)
        else:
            # Try every book with the verse specified
            b = self.bkNames[count]
        # Reference group
        r = m.group(2)
        st = m.group(3)
        if r:
            ref = ' '.join([b, r])
        else:
            ref = b
        if (':' in srch) and ('-' in srch):
            ref = ''.join([ref, '-', str(lv)])
        out[ref] = st
        # Every list with length greater than 2564 gets tossed
        count += 1
        if (count > 2564):
            err = MemoryError
            # TODO replace with Raise MemoryError
            break
    # ===============================================================
    return out, count, err


def alpheval(ref):
    alph = ''.join([char.upper() for char in ref
                    if char.isalpha()])
    aref = alph
    bkNames, bkAbbrv = toc()
    # Specified book
    if (alph) and (alph not in bkAbbrv):
        alph = r'(%(alph)s).*?' % locals()
    # Alias
    elif alph in bkAbbrv:
        alph = [bkNames[i] for i in range(66)
                if alph == bkAbbrv[i]][0]
        alph = r'(%(alph)s).*?' % locals()
    # Unspecifed
    else:
        alph = r'()'
    return alph, aref


def numbeval(ref):
    numb = ''.join([char for char in ref
                    if (not(char.isalpha()) and not(char.isspace()))])
    # Specified chapter/verse number (logic from least to most specific)
    # A book
    if not(numb):
        # Grab the whole book
        numeric = r'()'
        trail = r'(?= [A-Z]+ \d|$)'
        nref = None
    # A chapter
    # FIXME: See "Romans 17"
    elif ('-' not in numb) and (':' not in numb):
        nref = int(numb)
        trail = r'(?= %i:| [A-Z]+ \d|$)' % (nref + 1)
        numeric = r'(?<= (%(numb)s)):\d+ ' % locals()
    # Some verses
    elif (':' in numb) and ('-' in numb):
        chp = int(numb.split(':')[0])
        nref = int(numb.split('-')[1])
        trail = r'(?= %i:%i| %i:1| [A-Z]+ \d|$)' % (chp, nref + 1, chp + 1)
        numeric = r'(?<= (%s) )' % (numb.split('-')[0])
    # A verse
    elif (':' in numb) and ('-' not in numb):
        nref = int(numb.split(':')[1])
        trail = r'(?= \d| [A-Z]+ \d|$)'
        numeric = r'(?<= (%(numb)s) )' % locals()

    return numeric, trail, numb, nref


def navigate(self, vector, event=None):
    ref = self.frame.header.cget('text')
    _, _, numb, nref = numbeval(ref)
    srch = ref.replace(numb, str(nref + vector))
    d, count, _= verse(self, srch)
    h = [k for k in d.keys()][0]
    t = [v for v in d.values()][0]
    self.handler.gui_update(self, head=h, text=t,
                            status='{} RESULT MATCHING \"{}\"'.format(
                                count, srch))


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
    # Dictionary Table of Contents:
    bkNames = ['GENESIS', 'EXODUS', 'LEVITICUS', 'NUMBERS', 'DEUTERONOMY',
               'JOSHUA', 'JUDGES', 'RUTH', 'ISAMUEL', 'IISAMUEL',
               'IKINGS', 'IIKINGS', 'ICHRONICLES', 'IICHRONICLES',
               'EZRA', 'NEHEMIAH', 'ESTHER', 'JOB', 'PSALMS', 'PROVERBS',
               'ECCLESIASTES', 'SONGOFSONGS', 'ISAIAH', 'JEREMIAH',
               'LAMENTATIONS', 'EZEKIEL', 'DANIEL', 'HOSEA', 'JOEL',
               'AMOS', 'OBADIAH', 'JONAH', 'MICAH', 'NAHUM', 'HABAKKUK',
               'ZEPHANIAH', 'HAGGAI', 'ZECHARIAH', 'MALACHI', 'MATTHEW',
               'MARK', 'LUKE', 'JOHN', 'ACTS', 'ROMANS', 'ICORINTHIANS',
               'IICORINTHIANS', 'GALATIANS', 'EPHESIANS', 'PHILIPPIANS',
               'COLOSSIANS', 'ITHESSALONIANS', 'IITHESSALONIANS',
               'I TIMOTHY', 'IITIMOTHY', 'TITUS', 'PHILEMON', 'HEBREWS',
               'JAMES', 'IPETER', 'IIPETER', 'IJOHN', 'IIJOHN',
               'IIIJOHN', 'JUDE', 'REVELATION']
    bkAbbrv = ['GEN', 'EXO', 'LEV', 'NUM', 'DEUT',
               'JOSH', 'JUD', 'RU', 'I SA', 'II SA',
               'I KI', 'II KI', 'I CHRON', 'II CHRON',
               'EZR', 'NEH', 'EST', 'JOB', 'PSA', 'PRO',
               'ECC', 'SONG', 'ISA', 'JER',
               'LAM', 'EZE', 'DAN', 'HOS', 'JOE', 'AMO',
               'OBAD', 'JON', 'MIC', 'NAH', 'HAB', 'ZEP',
               'HAG', 'ZEC', 'MAL', 'MATT', 'MAR', 'LUK',
               'JOH', 'ACT', 'ROM', 'I COR', 'II COR',
               'GAL', 'EPH', 'PHLP', 'COL',
               'I THESS', 'II THESS', 'I TIM',
               'II TIM', 'TIT', 'PHM', 'HEB', 'JAM',
               'I PE', 'II PE', 'I JO', 'II JO', 'III JO', 'JU',
               'REV']

    d = OrderedDict()
    # Table of Contents
    d['ToC'] = [bkNames, bkAbbrv]

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
    '''
    (?:([A-Z]+)(?= \\d+:)|(?!^))\
    (?:(\\d+):(\\d+))? \
    ((?:[A-Z](?![A-Z]+ \\d)|[^\\dA-Z](?![A-Z]+ \\d|\\d))*)
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
