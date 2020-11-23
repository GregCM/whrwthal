'''
This file is a part of whrwthal.
whrwthal is an offline bible referencing module.
Copyright (C) 2020 Gregory Caceres-Munsell <gregcaceres@gmail.com>
'''

import curses

from blurses import Blurses
from whrwthal import textile


def mainmenu(window, menu, state):
    title = ['whrwthal -- Offline Bible Referencing']
    description = textile.preamble().replace('\n', ' SKIP ')
    # description = ' '.join(['whrwhtal (adverb), as in: SKIP',
    #                        'Wherewithal shall a young man',
    #                        'cleanse his way? by taking heed',
    #                        'thereto according to thy word. - Psalm 119:9 SKIP SKIP',
    #                        'Navigate using < ⇠ ⇡ ⇣ ⇢ > or < h j k l >'])
    mode = 0
    while mode == 0:
        window.clear()
        window.update()
        window.draw(title, top=2, left=2)
        window.wrap(description, width=80, vcenter=True, left=10)
        window.draw(menu(), bottom=5, left=5)
        if state:
            window.wrap(state, bottom=0, hcenter=True)
        mode = menu.input(window.getch())
    return mode


def howto(window, menu, state):
    press = 'Next page -->'
    pages = [textile.preamble(), textile.keybinds()]
    for page in pages: 
        key = 0
        while (key != 10) and (key != ord('l')) and (key != curses.KEY_RIGHT):
            window.clear()
            window.update()
            window.wrap(page.replace('\n', ' SKIP '), width=90, left=5, top=5)
            window.wrap(press, right=5, bottom=5)
            if state:
                window.wrap(state, bottom=0, hcenter=True)
            key = window.getch()
    return 0

# SUBMENU'S
# def aboutmenu(window, menu):


blurses = Blurses()
blurses.bind('', mainmenu)
blurses.bind('How-To', howto)
blurses.run()
