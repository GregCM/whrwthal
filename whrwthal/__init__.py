'''
This file is a part of whrwthal.
whrwthal is an offline bible referencing module.
Copyright (C) 2020 Gregory Caceres-Munsell <gregcaceres@gmail.com>
'''

from configparser import ConfigParser
import os
import sys
from threading import Thread

from dahuffman.huffmancodec import HuffmanCodec
from whrwthal import parser


def __init__(self):
    if sys.platform.startswith('linux'):
        self.homeDirectory = '~/'
        self.pathPart = '/'
    elif sys.platform.startswith('win'):
        os.remove(f for f in ['*/*sh', 'Makefile'])
        self.homeDirectory = '%userprofile%'
        self.pathPart = '\\'
    elif sys.platform.startswith('darwin'):
        os.remove(f for f in ['*/*sh', 'Makefile'])
        self.homeDirectory = '~/'
        self.pathPart = '/'
    try:
        self.config_obj = ConfigParser()
        self.config_obj.read('config.ini')
        _ = self.config_obj['PATH']['main']
    except KeyError:
        fd = os.getcwd()
        # Defaults:
        self.config_obj['PATH'] = {'main': fd, 'save': ''}
        self.config_obj['FONT'] = {'font': 'roman',
                                   'text': '12',
                                   'title': '25'}
        self.config_obj['COLORS'] = {'frame': 'gray18,',
                                     'master': 'gray18,',
                                     'menubar': 'gray20,ghost white',
                                     'header': 'gray18,ghost white',
                                     'text_widget': 'gray26,ghost white'}
        self.config_obj['LOWFOOTPRINT'] = {'switch': 'true',
                                        'transient': 'true'}
        self.config_obj['KEYS'] = {'save': '<Control-s>',
                                   'saveas': '<Control-Shift-S>',
                                   'quit': '<Control-q>',
                                   'select_search': '<Control-l>',
                                   'pageup': '<Control-k>',
                                   'pagedown': '<Control-j>'}
        self.colors = {}
        for key in self.config_obj['COLORS'].keys():
            self.colors[key] = self.config_obj['COLORS'][key].split(',')

        # Change to Defaults available in Settings menubar
        with open('config.ini', 'w') as cfg:
            self.config_obj.write(cfg)
    finally:
        self.fileLocation = self.config_obj['PATH']['main']
        self.font = self.config_obj['FONT']['font']
        self.font_size = self.config_obj['FONT']['text']
        self.colors = dict(self.config_obj['COLORS'])
        for key in self.colors.keys():
            self.colors[key] = self.colors[key].split(',')
        self.LFM = bool(self.config_obj['LOWFOOTPRINT']['switch'])
        self.key = self.config_obj['KEYS']

    # LOW FOOTPRINT MODE
    if self.LFM:
        thread = Thread(target=self.tkhandler.start, args=(self,))
        thread.start()
        # Decode bible string
        with open('bytes', 'rb') as f:
            # comes as bytes
            b = f.read()
        codec = HuffmanCodec.load('.codec')
        self.text = codec.decode(b)
    else:
        # Import bible dictionary
        with open('src.txt') as f:
            self.text = f.read()

    # Table of Contents
    self.bkNames, self.bkAbbrv = parser.toc()
    # Concordance
    self.concordance = parser.make_concord(self, self.text)
    # By default, don't use regular expressions
    self.use_re = False
    # Consider regex preference housing in "config.ini"
