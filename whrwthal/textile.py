'''
This file is a part of whrwthal.
whrwthal is an offline bible referencing module.
Copyright (C) 2020 Gregory Caceres-Munsell <gregcaceres@gmail.com>
'''


def preamble():
    return '\n'.join([r'          _____              ',
                      r'        |     |\            ',
                      r'        |     | \           ',
                      r'        |     |  |          ',
                      r' _______|     |__|____      ',
                      r'|                     |\    ',
                      r'|                     | \   ',
                      r'|_______       _______|  |  ',
                      r' \      |     |\       \ |  ',
                      r'  \_____|     | \_______\|  ',
                      r'        |     |  |          ',
                      r'        |     |  |          ',
                      r'        |     |  |          ',
                      r'        |     |  |          ',
                      r'        |     |  |          ',
                      r'        |     |  |          ',
                      r'        |_____|  |          ',
                      r'        \      \ |  whrwthal',
                      r'         \______\|    v2.4.0',
                       ' _____ _   _ _____   ____ ___ ____  _     _____ ',
                       '|_   _| | | | ____| | __ )_ _| __ )| |   | ____|',
                       '  | | | |_| |  _|   |  _ \| ||  _ \| |   |  _|  ',
                       '  | | |  _  | |___  | |_) | || |_) | |___| |___ ',
                       '  |_| |_| |_|_____| |____/___|____/|_____|_____|',
                       ' ________________________________________________ ',
                       '|                                                |',
                       '|  Please rightly divide and handle with prayer  |',
                       '|________________________________________________|\n'])


def update(self, text, just='left'):
    clear(self.frame)
    t = self.frame.text_widget
    t.configure(state='normal')
    t.insert('end', text)
    # Justification
    t.tag_add('just', '1.0', 'end')
    t.tag_config('just', justify=just)
    t.configure(state='disabled')


def clear(self):
    self.text_widget.configure(state='normal')
    self.text_widget.delete('1.0', 'end')
    self.text_widget.configure(state='disabled')


def keybinds(self):
    return "\n".join([" KEYBINDINGS",
                      "-----------",
                      "quit:        < q >",
                      "save:        < w >",
                      "saveas:      < W >",
                      "search:      < / >",
                      "navigate:    < ⇠ ⇡ ⇣ ⇢ > or < h j k l >"])


def about(label):
    if label == 'Whrwthal':
        version = 'v2.4.0'
        uilines = '613 tkGUI Lines of Code'
        totallines = '1367 Total Lines of Code'
        return '\n'.join(['whrwthal version %s' % (version), uilines, totallines])
    if label == 'License':
        with open('LICENSE') as f:
            return f.read()
    if label == 'Security':
        with open('SECURITY.md') as f:
            return f.read()
