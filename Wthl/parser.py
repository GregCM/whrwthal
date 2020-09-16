import collections
import random as rnd
import re
import tkinter as tk
from tkinter import ttk
import string

def verse(self):
    # TODO: (1) Languages
    # (2) Trim fat code
    '''
    ####################################
    ##                                ##
    ## For Searching Verse References ##
    ##                                ##
    ####################################
    '''
    # Initialize 'out' for concatenation.
    out = collections.OrderedDict({'verses': '', 'label': ''})

    location = self.frame.entry
    loc = []
    locAlph = ''
    locNumb = ''
    for char in location:
        # Saves the alphabetic part of location
        if char.isalpha() or char.isspace():
            locAlph += char
        # Saves the numeric part of location
        else:
            locNumb += char

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
        print(self.bkAbbrv[b], inToC)
        if inToC:
            print('IF (L774)')
            book = self.bkAbbrv[b]
            # The following Marks for headerUpdate
            bkMark = self.bkNames[b]
            out['label'] += bkMark
            print(bkMark)
            break
        # SEE <TODO (3)> in getInput
        elif not(locAlph):
            print('ELIF (L783)')
            book = 'all'
            bkMark = 'Parellel References'
            out['label'] += bkMark
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
            loc = re.split(char, loc)
            chpRef = loc[0]
            vrsRef = loc[1]

            severalVrs = False
            # If there is a dash, there are several verses.
            if ('-' in loc) or (',' in loc):
                severalVrs = True
                vrsRef = re.split(char, vrsRef)
                firstVerse = vrsRef[0]
                lastVerse = vrsRef[1]
                fV = int(firstVerse)
                lV = int(lastVerse)

    if not location:
        next
    elif location.upper() == 'ABOUT':
        self.textUpdate(self,
                        '''
                        ____________________________________________
                        ___\n This text-based app was written by
                         Greg Caceres\n It is free to use, access,
                         or edit. It is open\n source, free as in
                         beer and speech. The King\n James Bible has
                         its publishing and usage rights\n vested in
                         the Crown within the United Kingdom.\n
                         Everywhere else it is in the public domain,
                        \n and is free to use, quote, or share
                         without\n limit, provided no changes are
                         made to the\n content therein. For
                         support, or if you\n have any questions
                         about the app\'s functionality,\n the content
                         of the word of God, or anything else\n
                         related, feel free to contact me at\n
                         gregcaceres@gmail.com\n
                        ____________________________________________
                        ___\n
                        ''')

    try:
        outFind = self.bible_dict[book]
    except KeyError:
        return
    # If only book name is input, output whole book
    if chpRef == '0':
        cKeyList = range(len(outFind.keys()))
        # Hone in on a chapter for the verse loop sake:
        out['verses'] = '\n %s' % (out['label'])
        for cKey in cKeyList:
            cKey = str(cKey+1)
            # LOOP through verses keys
            # and concatenate each verse-field's string.
            cFind = outFind[cKey]
            vKeyList = range(len(cFind.keys()))
            for vKey in vKeyList:
                vKey = str(vKey+1)
                if vKey == '1':
                    cPrint = '\n\n Chapter %s\n\n' % (cKey)
                else:
                    cPrint = '\n'

                # Verses acquired!
                out['verses'] += (cPrint + cFind[vKey])

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
                noCRef = '\n F' + noCRef
            else:
                noCRef = '\n Unf' + noCRef

        # If only chapter is input, output whole chapter
        if vrsRef == '0':
            out['label'] = bkMark + cKey
            vKeyList = range(len(cFind.keys()))
            out['verses'] = '\n %s' % (out['label'])
            # LOOP through these verses, and
            # concatenate each verse-field's string.
            for vKey in vKeyList:
                vKey = str(vKey+1)
                out['verses'] += '\n' + cFind[vKey]

        # Range of verses
        elif severalVrs:
            vMax = len(cFind.keys())
            for verseNum in range(fV, lV):
                vKey = str(verseNum)
                try:
                    # Verses acquired!
                    out['verses'] += '\n%s' % (cFind[vKey])
                    vEnd = lV
                # Verse number larger than max number of verses in chapter
                # --> print only to chapter's end and cast change to label
                except KeyError:
                    vEnd = vMax
                    out['verses'] += '\n%s' % (cFind[vEnd])

            out['label'] += ':%s-%s' % (str(fV), str(vEnd-1))

        # Just one verse
        else:
            vKey = vrsRef
            out['label'] += ':%s' % (vKey)
            try:
                # Verse acquired!
                out['verses'] += '\n%s' % (cFind[vKey])
            except KeyError:
                vMax = len(cFind.keys())
                noVRef = ('ortunetly, %s %s only has %i verses'
                          % (bkMark, chpRef, vMax))
                fortunate = rnd.randint(0, 1)
                if fortunate:
                    noVRef = '\n F' + noVRef
                else:
                    noVRef = '\n Unf' + noVRef
                    out = [noVRef]

    self.headerUpdate(self.frame, out['label'])
    out['verses'] = [out['verses']]
    out['label'] = [out['label']]
    # TODO: count > 1 for instances such as many chapters containing "1-3"
    count = 1
    return out, count

def phrase(self):
    '''
    ###########################
    ##                       ##
    ## For Searching Phrases ##
    ##                       ##
    ###########################
    '''

    out = collections.OrderedDict({'phrases': [], 'label': []})

    Srch = r'%s' % (self.frame.entry)
    # addOns = ''

    # Case insensitive search anywhere within a word.
    # EX: Srch = "tempt" -->
    # [Tempt, tempted, aTTempt, contEmpT, TEMPTATION, ...]
    m = re.compile(r'(?i)(\w*%s\w*)' % (Srch))

    count = 0
    for bKey in self.bkAbbrv:
        chpDict = self.bible_dict[bKey]
        chpIter = chpDict.keys()
        for cKey in chpIter:
            vrsDict = chpDict[cKey]
            vrsIter = vrsDict.keys()
            for vKey in vrsIter:
                lines = vrsDict[vKey]
                s = m.search(lines)
                if s:
                    # Precompiled - pattern.sub(replacement, str)
                    vFound = lines
                    for item in m.finditer(vFound):
                        g = item.group(1)
                        n = re.compile(r'(?i)%s' % (g))
                        vFound = n.sub(g.upper(), vFound)

                    # \S instead of \w to include
                    # punctuation at fringes of words
                    o = re.compile(r'(?i)^\S*%s\S* \S* \S*' % (g))
                    p = re.compile(r'(?i)\S* \S*%s\S* \S*' % (g))
                    q = re.compile(r'(?i)\S* \S* \S*%s\S*$' % (g))
                    iterspan = ''

                    ocond = o.search(vFound)
                    pcond = p.search(vFound)
                    qcond = q.search(vFound)
                    if ocond:
                        # print('o')
                        for item in o.finditer(vFound):
                            s = item.start()
                            e = item.end()
                            iterspan += '%s...' % (vFound[s:e])

                    if pcond:
                        # print('p')
                        for item in p.finditer(vFound):
                            s = item.start()
                            e = item.end()
                            iterspan += '... %s...' % (vFound[s:e])

                    if qcond:
                        # print('q')
                        for item in q.finditer(vFound):
                            s = item.start()
                            e = item.end()
                            iterspan += '... %s' % (vFound[s:e])

                    vrsAlph, vrsNumb = '', ''
                    for char in vFound:
                        if char.isdigit():
                            vrsNumb += char
                        else:
                            vrsAlph += char

                    ref = ''.join([' ', bKey,
                                   ' ', cKey,
                                   ':', vrsNumb])
                    out['phrases'].append(vrsAlph)
                    out['label'].append('%s\n%s' % (ref, iterspan))
                    count += 1

    return out, count

# DEPRECATED
'''
def make_bibdict(self):
    with open('BIBLE.txt', 'r') as f:
        bib = f.read()

    # TODO: Add verbal details to progress bar status updates
    child = tk.Tk()
    child.title('Importing')
    msg = 'Please wait while the text is compiled...'
    info = tk.Label(child, text=msg, relief='flat')
    progress = ttk.Progressbar(child, orient='horizontal',
                               length=100, mode='determinate')
    info.pack(padx=5, pady=5)
    progress.pack(padx=5, pady=5)

    progress['value'] = 1
    child.update()

    # Letters and space for Concordance compilation
    alpha_space = string.ascii_letters + ' '

    n = len(self.bkNames)
    books = []
    trim_books = []
    trim_text = ''
    for b in range(n):
        m = re.compile(r'^(%s)' % (self.bkNames[b]))
        if b < 65:
            text = re.split(self.bkNames[b+1], bib)[0]
            # Exclude titles from text.
            bib = m.sub('', bib)
            text = m.sub('', text)

        elif b == 65:
            text = bib

        # Clear books already coverd.
        bkWiper = ''
        bkToWipe = text
        bib = bib.replace(bkToWipe, bkWiper)

        books.append(text)
        trim_text += ''.join([l for l in text if l in alpha_space])
        trim_books.append(trim_text)

        progress['value'] = b / n * 100
        child.update()

    trim_bible = ''.join(trim_books)
    # Whole Bible excluding punctuation and book titles.
    bib_letters = ''.join([l for l in trim_bible])
    bib_words = re.split(' ', bib_letters)
    bib_words = [w for w in bib_words if w != '']
    # Concordance equivalent
    unique_words = [s for s in set(bib_words) if s not in self.bkNames]

    progress['value'] = 1
    child.update()

    bible_dict = collections.OrderedDict()
    # Loops to populate the book structure.
    for b in range(n):
        # Chapters marked uniquely (":1 " =  c.x:v.1)
        chapters = re.split(':1 ', books[b])[1:]
        cLen = len(chapters)
        chpDict = collections.OrderedDict()
        # Loops to populate the chapter structure.
        for c in range(cLen):
            # Add the verse 1 marker again for verse indexing:
            chapters[c] = ':1 ' + chapters[c]
            # Indexes the places where verses MAY appear.
            idx = chapters[c].find(':')
            for x in [idx]:
                if (chapters[c])[x+1].isnumeric():
                    # Only the numeral indexed places are retained
                    # (i.e. "1:2" retained, "Behold: Foo" is not).
                    delim = str(c+1) + ':'
                    verses = re.split(delim, chapters[c])
            vLen = len(verses)
            vrsDict = collections.OrderedDict()
            # Loops to populate the verse structure.
            for v in range(vLen):
                if v == 0:
                    # Removes the extra colon left in each verse 1.
                    m = re.compile(':1 ')
                    verses[v] = m.sub('1 ', verses[v])

                # Beginning of line whitespace strip
                m = re.compile(r'(^\s*)')
                verses[v] = m.sub('', verses[v])

                # End of line whitespace / misc. strip
                # EX: "Amen. I" / "Amen. 1" / "Amen.  "
                m = re.compile(r'([\s\dI]{1,}$)')
                verses[v] = m.sub('', verses[v])

                vrsKey = str(v + 1)
                vrsDict[vrsKey] = verses[v]

            # Structure field names cannot or
            # should not start with numbers.
            chpKey = str(c+1)
            chpDict[chpKey] = vrsDict

        bkKey = self.bkAbbrv[b]
        bible_dict[bkKey] = chpDict

        progress['value'] = b / n * 100
        child.update()

    child.destroy()

    bible_dict['CONCORDANCE'] = unique_words
    return bible_dict
'''
