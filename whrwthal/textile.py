'''
This file is a part of whrwthal.
whrwthal is an offline bible referencing module.
Copyright (C) 2020 Gregory Caceres-Munsell <gregcaceres@gmail.com>
'''


def mini_preamble():
    cross = '\n'.join(['\n',
                       '         _____            ',
                       '        |     |\          ',
                       '        |     | \         ',
                       '        |     |  |        ',
                       ' _______|     |__|____    ',
                       '|                     |\  ',
                       '|                     | \ ',
                       '|_______       _______|  |',
                       ' \      |     |\       \ |',
                       '  \_____|     | \_______\|',
                       '        |     |  |        ',
                       '        |     |  |        ',
                       '        |     |  |        ',
                       '        |     |  |        ',
                       '        |     |  |        ',
                       '        |     |  |        ',
                       '        |_____|  |        ', 
                       '        \      \ |        ',
                       '         \______\|        '])

    version = '\n'.join([' _____ _   _ _____   ____ ___ ____  _     _____ ',
                         '|_   _| | | | ____| | __ )_ _| __ )| |   | ____|',
                         '  | | | |_| |  _|   |  _ \| ||  _ \| |   |  _|  ',
                         '  | | |  _  | |___  | |_) | || |_) | |___| |___ ',
                         '  |_| |_| |_|_____| |____/___|____/|_____|_____|',
                         '________________________________________________',
                         '|                                                |',
                         '|  Please rightly divide and handle with prayer  |',
                         '|________________________________________________|'])
    return '\n'.join([cross, version])
def preamble():
    cross = '\n'.join([r'-   \              /  +',
                       r'+    \     _      /   -',
                       r'-         | |         +',
                       r'+         | |         -',
                       r'-    _____| |_____    +',
                       r'+   |_____   _____|   -',
                       r'-         | |         +',
                       r'+         | |         -',
                       r'-         | |         +',
                       r'+         | |         -',
                       r'-         | |         +',
                       r'+         | |         -',
                       r'-         |_|         +',
                       r'+ _______/   \_______ -'])
    version = '\n'.join(['______________________',
                         '\n',
                         ' THE KING JAMES BIBLE ',
                         '______________________',
                         '\n',
                         ' Please rightly divide and handle with prayer.'])

    AppFormat = ''' The format: \n\n When queried "Where To?", a good
response would be one of the following...

To find a verse-to-verse passage --
"Book Chapter:Verse-Verse"
    EX: "Romans 5:8-10"

To find only one verse --
"Book Chapter:Verse"
    EX: "John 3:16"
To find full chapters --
"Book Chapter"
    EX: "Psalm 119"
To find full books --
"Book"
    EX: "Philemon"\n
______________________________________________________________\n
'''

    return '\n'.join([cross, version, AppFormat])


def update(self, text, just='left'):
    cls(self.frame)
    t = self.frame.text_widget
    t.configure(state='normal')
    t.insert('end', text)
    # Justification
    t.tag_add('just', '1.0', 'end')
    t.tag_config('just', justify=just)
    t.configure(state='disabled')


def cls(self):
    self.text_widget.configure(state='normal')
    self.text_widget.delete('1.0', 'end')
    self.text_widget.configure(state='disabled')
