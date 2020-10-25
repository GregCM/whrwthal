'''
This file is a part of whrwthal.
whrwthal is an offline bible referencing module.
Copyright (C) 2020 Gregory Caceres-Munsell <gregcaceres@gmail.com>
'''


def preamble():
    cross = '\n'.join([r'         _____            ',
                       r'        |     |\          ',
                       r'        |     | \         ',
                       r'        |     |  |        ',
                       r' _______|     |__|____    ',
                       r'|                     |\  ',
                       r'|                     | \ ',
                       r'|_______       _______|  |',
                       r' \      |     |\       \ |',
                       r'  \_____|     | \_______\|',
                       r'        |     |  |        ',
                       r'        |     |  |        ',
                       r'        |     |  |        ',
                       r'        |     |  |        ',
                       r'        |     |  |        ',
                       r'        |     |  |        ',
                       r'        |_____|  |        ',
                       r'        \      \ |        ',
                       r'         \______\|  v2.3.1'])
    v = '\n'.join([r' _____ _   _ _____   ____ ___ ____  _     _____ ',
                   r'|_   _| | | | ____| | __ )_ _| __ )| |   | ____|',
                   r'  | | | |_| |  _|   |  _ \| ||  _ \| |   |  _|  ',
                   r'  | | |  _  | |___  | |_) | || |_) | |___| |___ ',
                   r'  |_| |_| |_|_____| |____/___|____/|_____|_____|',
                   r'________________________________________________',
                   r'|                                                |',
                   r'|  Please rightly divide and handle with prayer  |',
                   r'|________________________________________________|'])
    AppFormat = '\n'.join(['\nA good search looks like...',
                           '-----------------------------',
                           'Romans 5:8-10     John 3:16',
                           'Psalm 119         Philemon',
                           'word              phrase'])

    return '\n'.join([cross, v, AppFormat])


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
