'''
This file is a part of whrwthaal.
whrwthal is an offline bible referencing module.
Copyright (C) 2020 Gregory Caceres-Munsell <gregcaceres@gmail.com>
'''

from configparser import ConfigParser
from dahuffman.huffmancodec import HuffmanCodec
import os
import sys
import tkinter as tk
from threading import Thread
from whrwthal import handler, io, parser, textile


def __init__(self, configfile='config.ini'):
    self.ispc = sys.platform.startswith('win')
    self.ismac = sys.platform.startswith('darwin')
    self.islinux = sys.platform.startswith('linux')
    if self.ispc:
        self.homeDirectory = '%userprofile%'
        self.pathPart = '\\'
    elif (self.ismac or self.islinux):
        self.homeDirectory = '/home'
        self.pathPart = '/'

    self.config_obj = ConfigParser()
    try:
        self.config_obj.read(configfile)
    except KeyError:
        fd = os.getwd()
        # Defaults:
        self.config_obj['PATH'] = {'main': fd, 'save': ''}
        self.fileLocation = self.config_obj['PATH']['main']
        self.config_obj['FONT'] = {'font': 'roman',
                                   'text': '12',
                                   'title': '25'}
        self.config_obj['COLORS'] = {'frame': 'gray18,',
                                     'master': 'gray18,',
                                     'menubar': 'gray20,ghost white',
                                     'header': 'gray18,ghost white',
                                     'text_widget': 'gray26,ghost white'}
        # Low Footprint Mode:
        self.config_obj['FOOTPRINT'] = {'switch': 'true',
                                        'transient': 'true'}
        for key in self.colors.keys():
            self.colors[key] = self.colors[key].split(',')

        # Change to Defaults available in Settings menubar
        with open(configfile, 'w') as cfg:
            self.config_obj.write(cfg)
    finally:
        self.fileLocation = self.config_obj['PATH']['main']
        self.font = self.config_obj['FONT']['font']
        self.font_size = self.config_obj['FONT']['text']
        self.colors = dict(self.config_obj['COLORS'])
        for key in self.colors.keys():
            self.colors[key] = self.colors[key].split(',')
        # Low Footprint Mode:
        self.LFM = bool(self.config_obj['FOOTPRINT']['switch'])

    # LOW FOOTPRINT MODE
    if self.LFM:
        # Decode bible string
        with open('bytes', 'rb') as f:
            # comes as bytes
            b = f.read()

        thread = Thread(target=self.handler.start, args=(self,))
        thread.start()

        codec = HuffmanCodec.load('.codec')
        self.text = codec.decode(b)
    else:
        # Import bible dictionary
        with open('src.txt') as f:
            self.text = f.read()

    # Table of Contents
    self.bkNames = ['GENESIS', 'EXODUS', 'LEVITICUS', 'NUMBERS', 'DEUTERONOMY',
                    'JOSHUA', 'JUDGES', 'RUTH', 'ISAMUEL', 'IISAMUEL',
                    'IKINGS', 'IIKINGS', 'ICHRONICLES', 'IICHRONICLES',
                    'EZRA', 'NEHEMIAH', 'ESTHER', 'JOB', 'PSALMS', 'PROVERBS',
                    'ECCLESIASTES', 'SONG OF SONGS', 'ISAIAH', 'JEREMIAH',
                    'LAMENTATIONS', 'EZEKIEL', 'DANIEL', 'HOSEA', 'JOEL',
                    'AMOS', 'OBADIAH', 'JONAH', 'MICAH', 'NAHUM', 'HABAKKUK',
                    'ZEPHANIAH', 'HAGGAI', 'ZECHARIAH', 'MALACHI', 'MATTHEW',
                    'MARK', 'LUKE', 'JOHN', 'ACTS', 'ROMANS', 'ICORINTHIANS',
                    'IICORINTHIANS', 'GALATIANS', 'EPHESIANS', 'PHILIPPIANS',
                    'COLOSSIANS', 'ITHESSALONIANS', 'IITHESSALONIANS',
                    'I TIMOTHY', 'IITIMOTHY', 'TITUS', 'PHILEMON', 'HEBREWS',
                    'JAMES', 'IPETER', 'IIPETER', 'IJOHN', 'IIJOHN',
                    'IIIJOHN', 'JUDE', 'REVELATION']
    self.bkAbbrv = ['GEN', 'EXO', 'LEV', 'NUM', 'DEUT',
                    'JOSH', 'JUD', 'RU', 'I SA', 'II SA',
                    'I KI', 'II KI', 'I CHRON', 'II CHRON',
                    'EZR', 'NEH', 'EST', 'JOB', 'PSA', 'PRO',
                    'ECC', 'SONG', 'ISA', 'JER',
                    'LAM', 'EZE', 'DAN', 'HOS', 'JOE', 'AMO',
                    'OBAD', 'JON', 'MIC', 'NAH', 'HAB', 'ZEP',
                    'HAG', 'ZEC', 'MAL', 'MATT', 'MAR', 'LUK',
                    'JOH', 'ACT', 'ROM', 'I COR', 'II COR',
                    'GAL', 'EPH', 'PHLP', 'COL',
                    'I THESS', 'II THESS', 'I TIM',
                    'II TIM', 'TIT', 'PHM', 'HEB', 'JAM',
                    'I PE', 'II PE', 'I JO', 'II JO', 'III JO', 'JU',
                    'REV']

    # Concordance
    self.concordance = parser.make_concord(self, self.text)
