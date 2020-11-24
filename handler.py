#!/usr/bin/python

'''
This file is a part of whrwthal.
whrwthal is an offline bible referencing module.
Copyright (C) 2020 Gregory Caceres-Munsell <gregcaceres@gmail.com>
'''

import curses
import time

from blurses import Blurses
import whrwthal
from whrwthal import textile


def start(self, t=5.0):
    # A simple timed progress bar ~5.0 seconds
    time.sleep(t)

def mainmenu(window, menu):
    title = ['whrwthal -- Offline Bible Referencing']
    preamble = ''.join([textile.preamble(),
                        '\n\nwhrwhtal (adverb), as in:\n\n',
                        'Wherewithal shall a young man ',
                        'cleanse his way? by taking heed ',
                        'thereto according to thy word. - Psalm 119:9'])
    mode = 0
    while mode == 0:
        window.clear()
        window.update()
        window.draw(title, top=2, left=2)
        window.wrap(preamble, width=80, vcenter=True, hcenter=True)
        window.draw(menu(), bottom=5, left=5)
        mode = menu.input(window.getch())
    return mode


def howto(window, menu):
    pageup = ['<-']
    pagedown = ['->']
    pages = [textile.keybinds(whrwthal),
            '\n'.join([' A good search looks like...',
                       '---------------------------',
                       'Romans 5:8-10     John 3:16',
                       'Psalm 119         Philemon',
                       'phrase            word'])]
    i = 0
    while 0 <= i < len(pages):
        window.clear()
        window.update()
        window.wrap(pages[i], width=90, vcenter=True, hcenter=True)
        window.draw(pagedown, right=5, bottom=5)
        window.draw(pageup, top=5, left=5)
        key = window.getch()
        if (key == 10) or (key == ord('l')) or (key == curses.KEY_RIGHT):
            i += 1
        elif (key == ord('h')) or (key == curses.KEY_LEFT):
            i -= 1
    return 0


# SUBMENU'S
# def aboutmenu(window, menu):

blurses = Blurses()
blurses.bind('', mainmenu)
blurses.bind('How-To', howto)
blurses.run()
