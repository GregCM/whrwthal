'''
This file is a part of whrwthal.
whrwthal is an offline bible referencing module.
Copyright (C) 2020 Gregory Caceres-Munsell <gregcaceres@gmail.com>
'''

import os
import sys
from threading import Thread

from dahuffman.huffmancodec import HuffmanCodec
from whrwthal import parser
from config import settings
import handler


def __init__(self):
    if sys.platform.startswith('linux'):
        self.homeDirectory = '~/'
        self.pathPart = '/'
    elif sys.platform.startswith('win'):
        os.remove('*/*sh')
        self.homeDirectory = '%userprofile%'
        self.pathPart = '\\'
    elif sys.platform.startswith('darwin'):
        os.remove('*/*sh')
        self.homeDirectory = '~/'
        self.pathPart = '/'

    self.fileLocation = settings['path.main']
    self.lfm = settings['lowfootprint.switch']

    # LOW FOOTPRINT MODE
    if self.lfm:
        thread = Thread(target=handler.start, args=(self,))
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
