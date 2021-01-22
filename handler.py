#!/usr/bin/python

'''
For Windows users:
    python -m pip install windows-curses
'''


import collections
import curses
from functools import partial
import textwrap

import whrwthal
from config import books, info, sample


# TODO:
# (1) replace STATEVAR with Class Object
# (2) vcenter, hcenter
def main(stdscr):
    curses.curs_set(0)
    curses.set_escdelay(1)
    active = tab = 0
    statevar = mainmenu(stdscr)
    char = ''
    while char != 'q' and statevar != None:
        scrsize = (curses.LINES - 1, curses.COLS - 1)
        char = stdscr.getkey()
        # searches
        if char == '/':
            # cursor to bottom left corner
            stdscr.move(scrsize[0], 0)
            curses.curs_set(1)
            while char != '\n' and char != '':
                stdscr.refresh()
                if char == '' and stdscr.getyx()[1] != 1:
                    y, x = stdscr.getyx()
                    stdscr.delch(y, x - 1)
                elif char != '':
                    stdscr.addch(char)
                elif char == '' and stdscr.getyx()[1] == 1:
                    break
                char = stdscr.getkey()
            stdscr.deleteln()
            stdscr.move(scrsize[0], 0)
            curses.curs_set(0)
        # ===================================================================
        # navigation
        elif (char == 'h' or char == 'KEY_LEFT' or char == '') and tab > 0:
            tab -= 1
            # reset active until a more dynamic way of saving the previous selection is found
            active = 0
            try:
                statevar = statevar[tab](statevar, stdscr, active)
            except TypeError:
                statevar = statevar[tab](stdscr, active)
        elif (char == 'j' or char == 'KEY_DOWN') and active > 0:
            active -= 1
            if type(statevar[2]) == str:
                statevar = read(statevar, stdscr, vector=-1)
            else:
                statevar[tab](stdscr, active)
        elif (char == 'k' or char == 'KEY_UP') and active < len([x for x in statevar if type(x) == list][0]) - 1:
            active += 1
            if type(statevar[2]) == str:
                statevar = read(statevar, stdscr, vector=1)
            else:
                statevar[tab](stdscr, active)
        elif (char == 'l' or char == 'KEY_RIGHT' or char == '\n') and tab < 3:
            tab += 1
            statevar = statevar[tab][active](statevar, stdscr)
        # ===================================================================
        stdscr.refresh()

def mainmenu(stdscr, active=0):
    stdscr.clear()
    # 70% of the screen height
    line0 = round(0.30 * curses.LINES)
    line1 = round(0.70 * curses.LINES)
    # 85% of the screen width
    col0 = round(0.15 * curses.COLS)
    col1 = round(0.75 * curses.LINES)
    idx = [0, line0, col0]
    span = [(line1 - line0) * (col1 - col0), line0, col0]

    title = 'whrwthal -- Offline Bible Referencing'
    description = 'whrwhtal (adverb), as in:\n\nWherewithal shall a young man cleanse his way? by taking heed thereto according to thy word. - Psalm 119:9'
    opts = ['Exit', 'About', 'Table of Contents']
    # Right justify menu statevar
    trailing = max([len(opt) for opt in opts])
    lines = curses.LINES - 2
    for lidx, opt in enumerate(opts):
        if lidx == active:
            stdscr.addstr(lines - lidx, trailing - len(opt), opt, curses.A_REVERSE)
        else:
            stdscr.addstr(lines - lidx, trailing - len(opt), opt, curses.A_NORMAL)

    # Print title
    stdscr.addstr(round(0.05 * lines), round(0.025 * curses.COLS), title)
    # Wrap description
    wrap(stdscr, idx, span, description) 
    statevar = [mainmenu, [exit, about, toc], None, None, None, None]
    return statevar

def toc(statevar, stdscr, active=0):
    stdscr.clear()
    statevar = [mainmenu, toc, [partial(read, prior=toc, txt=partial(whrwthal.parser.find, whrwthal, b)) for b in books], None, None, None]
    # Right justify menu statevar
    trailing = max([len(opt) for opt in books]) + 2
    lines = curses.LINES - 2
    y, x = stdscr.getyx()
    lidx = o = 0
    while o < 66:
        # Wrap statevar to next column if they overflow past max lines
        if lidx == lines:
            x += trailing
            lidx = 0
        else:
            lidx += 1

        if o == active:
            stdscr.addstr(lines - lidx, x + (trailing - len(books[o])),
                          books[o], curses.A_REVERSE)
        else:
            stdscr.addstr(lines - lidx, x + (trailing - len(books[o])),
                          books[o], curses.A_NORMAL)
        o += 1

    stdscr.move(y, x)
    return statevar

def about(statevar, stdscr, active=0):
    stdscr.clear()
    opts = ['How-To', 'Whrwthal', 'Security', 'License']
    opts.reverse()
    statevar = [mainmenu, about, [partial(read, prior=about, txt=info[o]) for o in opts], None, None, None]
    lines = curses.LINES - 2
    y, x = stdscr.getyx()
    for lidx, opt in enumerate(opts):
        if lidx == active:
            stdscr.addstr(lines - lidx, x, opt, curses.A_REVERSE)
        else:
            stdscr.addstr(lines - lidx, x, opt, curses.A_NORMAL)

    stdscr.move(y, x)
    return statevar

def read(statevar, stdscr, prior=mainmenu, txt='', vector=None):
    if type(txt) != str:
        txt = textify(txt)

    # FIXME: j/k while reading (def scroll?)
    # needed to use wrap for anything decent.
    stdscr.clear()
    # 90% of the screen height
    line0 = round(0.10 * curses.LINES)
    line1 = round(0.90 * curses.LINES)
    linespan = line1 - line0
    # 95% of the screen width
    col0 = round(0.05 * curses.COLS)
    col1 = round(0.95 * curses.COLS)
    colspan = col1 - col0

    if vector:
        statevar = scroll(statevar, stdscr, vector)
    else:
        idx = [0, line0, col0]
        span = [linespan * colspan, linespan, colspan]
        txt = wrap(stdscr, idx, span, txt, box=True) 
        statevar = [mainmenu, prior, txt, idx, span]

    # Cursor in top-left corner
    stdscr.move(line0, col0)
    return statevar

def wrap(stdscr, idx, span, txt, box=False):
    # Wrap string to next line if it overflows past max cols
    sidx, lidx, cidx = idx
    strspan, linespan, colspan = span
    wrapbox = stdscr.derwin(linespan, colspan, lidx, cidx)
    wrapbox.immedok(True)
    if box:
        boundbox = stdscr.derwin(linespan + 2, colspan + 2, lidx - 1, cidx - 1)
        boundbox.box()
    txt = textwrap.fill(txt, width=colspan, break_long_words=True, replace_whitespace=False)
    ''' 
    # Someday, something like this will be usefull...
    wraplist = textwrap.wrap(s, width=colspan, break_long_words=True, replace_whitespace=False)
    if len(wraplist) > linespan:
        txtlist = wraplist[:linespan - 1]
        txt = '\n'.join(txtlist)
        wraplist = wraplist[linespan:]
    else:
        txt = '\n'.join(wraplist)
        wraplist = []
    '''
    # TODO: truncate TXT to the amount that fits in span, indexed by an initial position
    wrapbox.addstr(txt[sidx:strspan - sidx])
    return txt

def scroll(statevar, stdscr, vector):
    # Mainloop (j/k) scrolls,
    # Calls WRAP() recursively to move wrapped text up or down
    txt = statevar[2]
    idx = statevar[3]
    span = statevar[4]
    if 0 <= statevar[3][0] <= span[0] - idx[0]:
        idx[0] += vector
        txt = wrap(stdscr, idx, span, txt, box=True) 
        # As with a non-vector READ()
        statevar = [statevar[:2], txt, idx, span]
    return statevar

def textify(partial):
    txt = ''
    p = partial()
    if type(p) == collections.OrderedDict:
        for key in p:
            txt = ''.join([txt, p[key]])
    elif type(p) == list:
        for item in p:
            txt = ''.join([txt, item])
    return txt

def exit(*args):
    return None

'''
def report(stdscr, active, tab, statevar, char=''):
    stdscr.move(0, 0)
    stdscr.deleteln()
    stdscr.deleteln()
    stdscr.deleteln()
    stdscr.insertln()
    stdscr.insertln()
    stdscr.insertln()
    stdscr.addstr(f'key pressed: {char}\ntab: {tab}\nactive: {active}\nstatevar: {statevar}')
'''

def mainloop():
    curses.wrapper(main)
