'''
This file is a part of whrwthal.
whrwthal is an offline bible referencing module.
Copyright (C) 2020 Gregory Caceres-Munsell <gregcaceres@gmail.com>
'''

from blurses import Blurses


def mainmenu(window, menu):
    title = ['whrwthal -- Offline Bible Referencing']
    description = ' '.join(['whrwhtal (adverb), as in: SKIP',
                           'Wherewithal shall a young man',
                           'cleanse his way? by taking heed',
                           'thereto according to thy word. - Psalm 119:9 SKIP SKIP',
                           'Navigate using < ⇠ ⇡ ⇣ ⇢ > or < h j k l >'])
    mode = 0
    while mode == 0:
        window.clear()
        window.update()
        window.draw(title, top=2, left=2)
        window.wrap(description, width=80, vcenter=True, left=10)
        window.draw(mainmenu(), bottom=5, left=5)
        mode = menu.input(window.getch())
    return mode


def howto(window, menu):
    press = 'Press enter to continue:'
    for page in pages: 
        key = 0
        while key != 10:
            window.clear()
            window.update()
            window.wrap(page, width=90, left=5, top=5)
            window.wrap(press, left=5, bottom=5)
            key = window.getch()
    return 0


blurses = Blurses()
blurses.bind('', mainmenu)
blurses.bind('How-To', howto)
blurses.run()
