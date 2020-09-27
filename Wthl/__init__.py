from ast import literal_eval
from configparser import ConfigParser
import collections
from dahuffman import HuffmanCodec
from functools import partial
import json
import os
import sys
from threading import Thread
import tkinter as tk
from tkinter import ttk


def __init__(self, configfile='config.ini'):

    '''
    ##################
    ##              ##
    ## Initializing ##
    ##              ##
    ##################
    '''

    self.ispc = sys.platform.startswith('win')
    self.ismac = sys.platform.startswith('darwin')
    self.islinux = sys.platform.startswith('linux')
    # FIXME: MACOSX ERROR
    # xcrun: error: invalid active developer path
    # (/Library/Developer/CommandLineTools), missing xcrun at:
    # /Library/Developer/CommandLineTools/usr/bin/xcrun

    if self.ispc:
        self.homeDirectory = '%userprofile%'
        self.pathPart = '\\'
    elif (self.ismac or self.islinux):
        self.homeDirectory = '/home'
        self.pathPart = '/'

    self.config_obj = ConfigParser()
    try:
        self.config_obj.read(configfile)
        self.fileLocation = self.config_obj['PATH']['main']
        self.language = self.config_obj['LANGUAGE']['current']
        self.font = self.config_obj['FONT']['font']
        self.font_size = self.config_obj['FONT']['text size']
        self.colors = dict(self.config_obj['COLORS'])
        for key in self.colors.keys():
            self.colors[key] = self.colors[key].split(',')

        # Low Footprint Mode:
        LFM = self.config_obj['FOOTPRINT']['switch']

    except KeyError:
        # This directory contains the text source & the configuration file.
        # This will then be saved for next time
        # and used as the working directory.
        fd = os.getcwd()
        os.chdir(fd)

        self.config_obj['PATH'] = {'main': fd, 'save': ''}
        self.fileLocation = self.config_obj['PATH']['main']

        self.config_obj['LANGUAGE'] = {'current': 'eng',
                                       'options':
                                       'eng,spa,fre,ger,heb,gre'}
        self.config_obj['FONT'] = {'font': 'times',
                                   'text size': '12',
                                   'title size': '25',
                                   'font options':
                                   'roman,calibri,courier',
                                   'size options':
                                   '9,10,11,12,13,14,15'}
        self.config_obj['COLORS'] = {'frame': 'gray18,',
                                     'master': 'gray18,',
                                     'menubar': 'gray20,ghost white',
                                     'header': 'gray18,ghost white',
                                     'text_widget': 'gray26,ghost white'}
        # Low Footprint Mode:
        self.config_obj['FOOTPRINT'] = {'switch': 'on',
                                        'transient': 'true'}
        # Low Footprint Mode:
        LFM = self.config_obj['FOOTPRINT']['switch']

        # Defaults:
        self.language = self.config_obj['LANGUAGE']['current']
        self.font = self.config_obj['FONT']['font']
        self.font_size = self.config_obj['FONT']['text size']
        self.colors = dict(self.config_obj['COLORS'])
        for key in self.colors.keys():
            self.colors[key] = self.colors[key].split(',')

        # Change to Defaults available in Settings menubar
        with open(configfile, 'w') as cfg:
            self.config_obj.write(cfg)

    # Create & Configure root
    self.root = tk.Tk()
    tk.Grid.rowconfigure(self.root, 0, weight=1)
    tk.Grid.columnconfigure(self.root, 0, weight=1)

    # Create & Configure frame
    self.frame = tk.Frame(self.root, name='frame')
    self.frame.tk_focusFollowsMouse()
    self.frame.grid(row=0, column=0, sticky='nsew')

    # Configure frame master
    self.w = self.frame.winfo_screenwidth()
    self.h = self.frame.winfo_screenheight()
    self.frame.master.geometry('%dx%d+0+0' % (self.w, self.h))
    self.frame.master.title('whrwthal')

    # Create & Configure menubar
    self.menubar = tk.Menu(self.frame, name='menubar')
    self.frame.master.config(menu=self.menubar)

    file_menu = tk.Menu(self.menubar, tearoff=0)
    edit_menu = tk.Menu(self.menubar, tearoff=0)
    options_menu = tk.Menu(self.menubar, tearoff=0)
    help_menu = tk.Menu(self.menubar, tearoff=0)

    self.menubar.add_cascade(label='File', menu=file_menu, underline=0)
    self.menubar.add_cascade(label='Edit', menu=edit_menu, underline=0)
    self.menubar.add_cascade(label='Options', menu=options_menu,
                             underline=0)
    self.menubar.add_cascade(label='Help', menu=help_menu, underline=0)

    # File menu choices:
    self.sv_button = partial(self.io.save, self)
    self.frame.master.bind('<Control-s>', self.sv_button)
    file_menu.add_command(label='Save',
                          accelerator='Ctrl+S',
                          command=self.sv_button,
                          underline=0)

    self.svas_button = partial(self.io.saveas, self)
    self.frame.master.bind('<Control-Shift-S>', self.svas_button)
    file_menu.add_command(label='SaveAs',
                          accelerator='Ctrl+Shift+S',
                          command=self.svas_button,
                          underline=0)

    self.qt_Button = partial(self.handler.shutdown, self)
    self.frame.master.bind('<Control-q>', self.qt_Button)
    file_menu.add_command(label='Quit',
                          accelerator='Ctrl+Q',
                          command=self.qt_Button,
                          underline=0)

    # Options menu choices:
    sett = partial(self.handler.settings, self)
    options_menu.add_command(label='Settings',
                             command=sett,
                             underline=0)

    self.show_toc = tk.BooleanVar()
    tocq = partial(self.handler.toc_query, self)
    options_menu.add_checkbutton(label='Display Table of Contents',
                                 onvalue=1, offvalue=0,
                                 variable=self.show_toc,
                                 command=tocq)

    self.enable_lfm = tk.BooleanVar()
    self.enable_lfm.set(LFM)
    lfmq = partial(self.handler.lfm_query, self)
    options_menu.add_checkbutton(label='Low Footprint Mode',
                                 onvalue=1, offvalue=0,
                                 variable=self.enable_lfm,
                                 command=lfmq)

    # Status Bar
    self.frame.status_bar = tk.Label(self.frame,
                                     text='Awaiting input...',
                                     relief='flat',
                                     name='status_bar')

    self.frame.status_bar.grid(row=2, column=1, sticky='s')

    # Search Bar placement
    self.qvar = tk.IntVar()
    self.frame.var = tk.IntVar()
    self.frame.SearchBar = tk.Entry(self.frame)
    self.frame.SearchBar.grid(row=3, column=1, sticky='ew')
    slSB = partial(self.handler.select, self)
    self.frame.master.bind('<Control-l>', slSB)

    # Dropdown search options
    # FIXME: finish toggle button and frame placement / padding... then more opts
    self.frame.drop_frame = tk.Frame(self.frame, relief='sunken')
    dfgrid = partial(self.frame.drop_frame.grid,
                     row=5, column=1, sticky='ew')
    self.frame.drop_button = tk.Button(self.frame,
                                       relief='flat',
                                       text=' ᐯ ',
                                       command=dfgrid)
    self.frame.drop_button.grid(row=4, column=1, sticky='ew')

    self.frame.regex_check = ttk.Checkbutton(self.frame.drop_frame)
    self.frame.regex_check.pack(side='left', fill='both')
    s = 'Use regular expressions (advanced)'
    self.frame.regex_label = ttk.Label(self.frame.drop_frame,
                                       text=s)
    self.frame.regex_label.pack(side='left', fill='x')

    # For any entry field, ensures one time only call.
    self.frame.entry = 'Search'
    self.frame.SearchBar.insert('end', self.frame.entry)

    get = partial(self.handler.get_input, self)
    self.frame.master.bind('<Return>', get)
    self.frame.go_b = tk.Button(self.frame,
                                text='ENTER',
                                comman=get,
                                relief='raised')
    self.frame.go_b.grid(row=4, column=1, sticky='new')

    self.list_button = []

    self.frame.header = tk.Label(self.frame,
                                 text='Welcome!',
                                 relief='flat',
                                 name='header')

    self.frame.header.grid(row=1, column=7, sticky='sew')

    self.frame.text_widget = tk.Text(self.frame,
                                     relief='sunken',
                                     wrap='word',
                                     name='text_widget')
    self.frame.text_widget.grid(row=2,
                                rowspan=10,
                                column=7,
                                sticky='nsew')

    # Welcome message!
    self.textile.update(self, self.textile.preamble())

    '''
    TOOL-TIPS
    self.frame.bind('<ButtonPress>', self.leave)
    # 3 second pause before tooltip appears
    self.waittime = 3000
    '''

    self.frame.Bpadding = tk.Label(self.frame, text='', relief='flat')
    self.frame.Bpadding.grid(row=14, column=0,
                             columnspan=14, sticky='ew')

    self.frame.configure(bg=self.colors['frame'][0])
    self.frame.master.configure(bg=self.colors['master'][0])
    self.menubar.config(bg=self.colors['menubar'][0],
                        fg=self.colors['menubar'][1],
                        relief='flat')
    self.frame.header.configure(bg=self.colors['header'][0],
                                fg=self.colors['header'][1],
                                font=(self.font,
                                      self.config_obj[
                                              'FONT'][
                                                  'title size']))
    self.frame.status_bar.configure(bg=self.colors['header'][0],
                                    fg=self.colors['header'][1],
                                    font=(self.font,
                                          self.config_obj[
                                              'FONT'][
                                                  'text size']))
    self.frame.text_widget.configure(bg=self.colors['text_widget'][0],
                                     fg=self.colors['text_widget'][1])
    self.frame.Bpadding.configure(bg=self.colors['frame'][0],
                                  state='disabled')

    if LFM == 'on':
        LFM = 1
        # First time decode of bible data
        with open('bytes', 'rb') as f:
            # comes as bytes
            b = f.read()

        thread = Thread(target=self.handler.start, args=(self,))
        thread.start()

        # b decoded with json delimiters as strings objects
        codec = HuffmanCodec.load('.codec')
        # literal_eval interprets the delimiters into type=dict
        self.bible_dict = literal_eval(codec.decode(b))
        [self.bkNames, self.bkAbbrv] = self.bible_dict['ToC']

    else:
        LFM = 0
        # Import bible dictionary as "bible_dict"
        with open('.dict.json', 'r') as b:
            d = collections.OrderedDict
            self.bible_dict = json.load(b, object_pairs_hook=d)

        # Parse Table of Contents
        [self.bkNames, self.bkAbbrv] = self.bible_dict['ToC']
