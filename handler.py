'''
This file is a part of whrwthal.
whrwthal is an offline bible referencing module.
Copyright (C) 2020 Gregory Caceres-Munsell <gregcaceres@gmail.com>
'''

import curses

from blurses import Blurses
import whrwthal
from whrwthal import textile


def mainmenu(window, menu):
    title = ['whrwthal -- Offline Bible Referencing']
    preamble = ' '.join(['whrwhtal (adverb), as in: SKIP',
                         'Wherewithal shall a young man',
                         'cleanse his way? by taking heed',
                         'thereto according to thy word. - Psalm 119:9 SKIP SKIP',
                         'Navigate using < ⇠ ⇡ ⇣ ⇢ > or < h j k l >'])
    mode = 0
    while mode == 0:
        window.clear()
        window.update()
        window.draw(title, top=2, left=2)
        window.wrap(preamble, width=80, left=10,
                    vcenter=True, hcenter=True)
        window.draw(menu(), bottom=5, left=5)
        mode = menu.input(window.getch())
    return mode


def howto(window, menu):
    press = 'Next page -->'
    pages = [textile.preamble(), textile.keybinds(whrwthal)]
    for page in pages: 
        key = 0
        while (key != 10) and (key != ord('l')) and (key != curses.KEY_RIGHT):
            window.clear()
            window.update()
            window.wrap(press, right=5, bottom=5)
            window.wrap(page.replace('\n', ' SKIP '), width=90, left=5, top=5)
            key = window.getch()
    return 0


# SUBMENU'S
# def aboutmenu(window, menu):

blurses = Blurses()
blurses.bind('', mainmenu)
blurses.bind('How-To', howto)
blurses.run()
