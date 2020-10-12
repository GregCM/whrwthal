'''
This file is a part of whrwthal.
whrwthal is an offline bible referencing module.
Copyright (C) 2020 Gregory Caceres-Munsell <gregcaceres@gmail.com>
_______________________________________________

The Biblical translations used herein are all
in the public domain, and free to use, quote,
or share without limit.

For general support, or if you have any
questions about the app's functionality,
the content of the word of God, or
anything else related, feel free
to contact me directly.
_______________________________________________
'''

from collections import OrderedDict
import os
import json
import random as rnd
import re
import string
import whrwthal

import time


def verse(self):
    '''
    ####################################
    ##                                ##
    ## For Searching Verse References ##
    ##                                ##
    ####################################
    '''
    # Initialize 'out' for concatenation.
    out = OrderedDict({'verses': [], 'label': ''})

    err = None
    location = self.frame.entry
    loc = []

    # Saves the alphabetic part of location
    locAlph = ''.join([char for char in location if (char.isalpha() or char.isspace())])
    # Saves the numeric part of location
    locNumb = ''.join([char for char in location if
                            (not(char.isalpha()) and not(char.isspace()))])

    loc.append(locAlph)
    # Combine the alphabetic and numeric parts to loc
    loc.append(locNumb.strip())
    location = ''.join(loc)
    # 66 books!
    n = len(self.bkNames)
    # Book is empty by default, filled this loop:
    book = ''
    # LOOP THROUGH BOOKS
    for b in range(n):
        # Compare strings to see if input is in
        # Table of Contents (ignore case); accounts
        # for abbreviations of books.
        LenAbb = len(self.bkAbbrv[b])
        inToC = (self.bkAbbrv[b].upper() == locAlph.upper()[0:LenAbb])
        if inToC:
            book = self.bkAbbrv[b]
            # The following Marks for header update
            bkMark = self.bkNames[b]
            out['label'] = bkMark
            break
        # SEE <TODO (3)> in getInput
        elif not(locAlph):
            book = 'all'
            bkMark = 'Parellel References'
            out['label'] = bkMark
            self.close_window(self)
            break
        # Proceed to next book. If no match is
        # found, 'book' would remain empty.
        else:
            continue

    # This IF catches an empty numeric part
    # 0 indicates that no Chapters were specified:
    # The book will be the only output.
    if (len(loc) > 1):
        chpRef = (loc[1])
        if not chpRef:
            chpRef = '0'
    # ELSE catches the lack of numeric part
    else:
        chpRef = '0'

    # If there is a numeric part of 'loc',
    # it can be used as the chapter reference.
    if not chpRef == '0':
        loc = chpRef
        vrsRef = '0'
        firstVerse = vrsRef
        fV = int(firstVerse)
        lV = 0
        # If there is a colon, there is a verse ref.
        if ':' in loc:
            loc = re.split(':', loc)
            chpRef = loc[0]
            vrsRef = loc[1]

            severalVrs = False
            # If there is a dash, there are several verses.
            if ('-' in loc):
                vrsRef = re.split('-', vrsRef)
            elif (', ' in loc):
                vrsRef = re.split(', ', vrsRef)
            if ('-' in loc) or (', ' in loc):
                severalVrs = True
                firstVerse = vrsRef[0]
                lastVerse = vrsRef[1]
                fV = int(firstVerse)
                lV = int(lastVerse)

    try:
        outFind = self.d[book]
    except KeyError:
        return
    # If only book name is input, output whole book
    if chpRef == '0':
        cKeyList = range(len(outFind.keys()))
        # Hone in on a chapter for the verse loop sake:
        out['verses'].append('\n %s' % out['label'])
        for cKey in cKeyList:
            cKey = str(cKey+1)
            # LOOP through verses keys
            # and concatenate each verse-field's string.
            cFind = outFind[cKey]
            vKeyList = range(len(cFind.keys()))

            # Verses acquired!
            cf = '\n'.join([cFind[str(vKey + 1)]
                            for v in vKeyList if v == '1'])
            out['verses'].append('\n\n Chapter %(cKey)s\n%(cf)s' % locals())
                                 
    else:
        cKey = chpRef
        out['label'] = ' %s' % (cKey)
        try:
            cFind = outFind[cKey]
        except KeyError:
            cMax = len(outFind.keys())

            # Plural or not?
            if cMax == 1:
                noCRef = ('ortunetly, %s only has %i chapter'
                          % (bkMark, cMax))
            else:
                noCRef = ('ortunetly, %s only has %i chapters'
                          % (bkMark, cMax))
            fortunate = rnd.randint(0, 1)
            if fortunate:
                noCRef = '\n F%s' % (noCRef)
            else:
                noCRef = '\n Unf%s' % (noCRef)

        # If only chapter is input, output whole chapter
        if vrsRef == '0':
            out['label'] = '%(bkMark)s%(cKey)s' % locals()
            vKeyList = range(len(cFind.keys()))
            out['verses'].append('\n %s' % (out['label']))
            # LOOP through these verses, and
            # concatenate each verse-field's string.
            out['verses'].append('\n'.join([cFind[str(vKey + 1)]
                                           for vKey in vKeyList]))

        # Range of verses
        elif severalVrs:
            vMax = len(cFind.keys())
            try:
                out['verses'].append('\n'.join([cFind[str(vKey)] for vKey in range(fV, lV)]))
                vEnd = lV
            except KeyError:
                # Verse number larger than max number of verses in chapter
                vEnd = vMax
                out['verses'].append('\n'.join([cFind[str(vEnd)] for vKey in range(fV, vMax)]))
                # --> print only to chapter's end and cast change to label
            finally:
                out['label'] = ''.join([out['label'], ':%i-%i' % (fV, vEnd - 1)])

        # Just one verse
        else:
            vKey = vrsRef
            out['label'] = ''.join([out['label'], ':%s' % (vKey)])
            try:
                # Verse acquired!
                out['verses'].append(cFind[vKey])
            except KeyError:
                vMax = len(cFind.keys())
                noVRef = ('ortunetly, %s %s only has %i verses'
                          % (bkMark, chpRef, vMax))
                fortunate = rnd.randint(0, 1)
                if fortunate:
                    noVRef = '\n F' % (noVRef)
                else:
                    noVRef = '\n Unf' % (noVRef)
                    out = [noVRef]

    self.textile.update(self, out['label'])
    # list-ify because of bad downstream coding... on my TODO
    out['verses'] = [out['verses']]
    out['label'] = [out['label']]
    # TODO: count > 1 for instances such as many chapters containing "1-3"
    count = 1
    return out, count, err


def phrase(self):
    '''
    ###########################
    ##                       ##
    ## For Searching Phrases ##
    ##                       ##
    ###########################
    '''

    out = []

    srch = self.frame.entry
    # addOns = ''

    text = make_text(self, d=self.d)
    if self.use_re.get():
        # Whatever regular expression the user specifies!
        c = re.compile(r'%s' % (srch))
    else:
        # Case insensitive search anywhere within a word.
        # EX: srch = "tempt" -->
        # [Tempt, tempted, aTTempt, contEmpT, TEMPTATION, ...]
        c = re.compile(r'(\w*%s\w*)' % (srch), re.IGNORECASE)

    count = 0
    err = None
    for i in c.finditer(text):
        # Serves as speed / crash prevention:
        # no one wants to see a 62,000-Count word list.
        count += 1
        # TODO: out[ref] = vrsAlph
        # Every list with length greater than 2564 gets tossed
        if (count > 2564):
            err = MemoryError 
            # TODO replace with Raise MemoryError
            break
    return out, count, err
    '''
                    for item in m.finditer(vFound):
                        g = item.group(1)
                        vFound = m.sub(g.upper(), vFound)
                        # \S instead of \w to include
                        # punctuation at fringes of words

                        # pattern appears at Start Of Line
                        o = re.compile(r'^\S*%s\S* \S* \S*' % (g.upper()))
                        so = o.search(vFound)
                        # pattern appears in Middle Of Line
                        p = re.compile(r'\S* \S*%s\S* \S*' % (g.upper()))
                        sp = p.search(vFound)
                        # pattern appears at End Of Line
                        q = re.compile(r'\S* \S* \S*%s\S*$' % (g.upper()))
                        sq = q.search(vFound)

                        if so:
                            # print('o')
                            iterspan = '%s...' % (
                                       ''.join([vFound[i.start():i.end()]
                                                for i in o.finditer(vFound)]))
                        elif sp:
                            # print('p')
                            iterspan = '...%s...' % (
                                       ''.join([vFound[i.start():i.end()]
                                                for i in p.finditer(vFound)]))
                        elif sq:
                            # print('q')
                            iterspan = '...%s...' % (
                                       ''.join([vFound[i.start():i.end()]
                                                for i in q.finditer(vFound)]))

                        vrsNumb = ''.join([c for c in vFound if c.isdigit()])
                        vrsAlph = ''.join([c for c in vFound
                                           if not(c.isdigit())])
                        ref = ''.join([' ', b,
                                       ' ', c,
                                       ':', vrsNumb,
                                       '\n%(iterspan)s' % locals()])
                        out[ref] = vrsAlph
    '''


def make_json(**kwargs):
    '''
    Returns a nested dictionary:

        d = {book: {chapter: {verse: text }}}

    Key-word arguments consist of 'self' and 'filename'.

    Use:

        Return the dictionary, don't write to file:

            d = make_json()

        Return the dictionary and write it to file ``f``:

            d = make_json(filename=f)

        Return the dictionary as an attribute of the parent object, and write it to file ``f``:

            d = make_json(self='whrwthal', filename='f')

    '''
    # ===================================================
    # Handling key word arguments:
    try:
        keys, values = kwargs.items()
        if 'self' in keys:
            if 'whrwthal' in values:
                self = kwargs['self']
        if 'filename' in keys:
            filename = kwargs['filename']
    except ValueError:
        # dummy object to stand in for whrwthal...
        # for use in make_json call from shell / interpreter
        self = whrwthal
        # dummy filename to signify no file output
        filename = ''

    # ===================================================
    # Import source text:
    with open('src.txt') as f:
        text = f.read()

    # ===================================================
    # Dictionary Table of Contents:
    self.bkNames = ['GENESIS', 'EXODUS', 'LEVITICUS', 'NUMBERS', 'DEUTERONOMY',
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
                    'I TIMOTHY', 'IITIMOTHY', 'TITUS', 'PHILEMON', 'HEBREWS',
                    'JAMES', 'IPETER', 'IIPETER', 'IJOHN', 'IIJOHN',
                    'IIIJOHN', 'JUDE', 'REVELATION']
    self.bkAbbrv = ['GEN', 'EXO', 'LEV', 'NUM', 'DEUT',
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

    # OderedDict()
    d = OrderedDict()
    # Table of Contents
    d['ToC'] = [self.bkNames, self.bkAbbrv]
    # ===================================================
    # Dictionary Verse Number / Text Pairs:

    # Book Title Group
    g1 = '([A-Z]{2,})'
    # Chapter Number Group
    g2 = '(\d+)'
    # Verse Number Group
    g3 = '(\d+)'
    # SubText Group
    g4 = '((?:[^\dA-Z]+(?!:\d)|[A-Z](?![A-Z]+ \d+:\d))*)'
    match = re.finditer(r'(?:%s(?= \d+:\d)|(?!^))(?:%s:%s)?\s*%s'
                        % (g1, g2, g3, g4), text)
    for m in match:
        if m.group(1):
            # Book Title
            b = m.group(1)
        else:
            # Chapter Number
            c = m.group(2)
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

    # Exclude punctuation & numerberation
    words = []
    alpha = string.ascii_letters + ' '
    trim = ''.join([char for char in text if char in alpha])
    words.extend([w for w in set(re.split(' ', trim))])
    # No space
    words.remove('')
    # Alphabetize
    words.sort()
    d['CONCORDANCE'] = words
    # ===================================================
    # Handle file output:
    if os.path.exists(filename):
        with open('src.json', 'w') as f:
            json.dump(d, f)
    # ===================================================
    return d


# Consider adding url request to whrwthal-text raw source
# TODO: Ensure make_json compatibility && add parser.make_* to whrwthal methods
def make_text(self, **kwargs):
    '''
    Returns a str():

        text = "Alpha ... Omega"

    Key-word arguments consist of 'd', and 'filename'.

    Use:

        Return the string, don't write to file:

            text = make_text()

        Return the string and write it to plain-text file ``f``:

            text = make_text(filename='f')

        Return the string as an attribute of the parent object, and write it to plain-text file ``f``:

            text = make_text(self='whrwthal', filename='f')

        Return the string as an attribute of the parent object, and write it to plain-text file ``f``,
        using dictionary ``dict()`` as the source instead of default ``./src.json``:

            text = make_text(self='whrwthal', d=dict(), filename='f')

    Alternative source texts @ https://github.com/GregCM/whrwthal/tree/texts
    '''
    # ===================================================
    # Handling key word arguments:
    try:
        keys, values = kwargs.items()
        if 'd' in keys:
            d = kwargs['d']
        if 'filename' in keys:
            filename = kwargs['filename']
            print(filename)
    except ValueError:
        # dummy filename to signify no file output
        filename = ''
        # dummy dictionary to signify the dictionary
        # is coming from file, not namespace
        d = None

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
                    # ('Book Chapter:Verse')
                    first = ''.join(['{} {}:{}'.format(b, c, d[b][c][v])
                                     for v in d[b][c] if v == '1'])
                    text.append(first)
                    # remaining verses (' Chapter:Verse')
                    remains = ''.join([' {}:{}'.format(c, d[b][c][v])
                                       for v in d[b][c] if v != '1'])
                    text.append(remains)
                else:
                    # remaining verses (' Chapter:Verse')
                    remains = ''.join([' {}:{}'.format(c, d[b][c][v]) for v in d[b][c]])
                    text.append(remains)

    text = ''.join(text)
    # ===================================================
    # Handle file output:
    if os.path.exists(filename):
        with open('src.txt', 'w') as f:
            f.write(text)
    # ===================================================
    return text