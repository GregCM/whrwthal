#!/usr/bin/python3

# FIXME: MACOSX ERROR
# xcrun: error: invalid active developer path (/Library/Developer/CommandLineTools), missing xcrun at: /Library/Developer/CommandLineTools/usr/bin/xcrun


'''
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
_______________________________________________

This app was written by Greg Caceres.
It is free to use, access, or edit. It is open
source, free as in beer and as in speech.
Comprehensive license pending.

The Biblical translations used herein are all
in the public domain, and free to use, quote,
or share without limit, provided no changes
are made to the content therein.

For general support, or if you have any
questions about the app's functionality,
the content of the word of God, or
anything else related, contact at

gregcaceres@gmail.com
_______________________________________________

'''

import bs4
import collections
from configparser import ConfigParser
import datetime as dt
from functools import partial
import json
import os
import psutil
import random as rnd
import re
import string
import sys
import tkinter as tk
from tkinter import colorchooser
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
import urllib


class Bible:

    def __init__(self, configfile='config.ini'):

        '''
        ##################
        ##              ##
        ## Initializing ##
        ##              ##
        ##################
        '''

        self.pytesting = False
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
            self.fileLocation = self.config_obj['PATH']['main']
            self.language = self.config_obj['LANGUAGE']['current']
            self.font = self.config_obj['FONT']['font']
            self.font_size = self.config_obj['FONT']['text size']
            self.footprint = self.config_obj['FOOTPRINT']['weight']
            self.colors = dict(self.config_obj['COLORS'])
            for key in self.colors.keys():
                self.colors[key] = self.colors[key].split(',')

        except KeyError:
            # This directory contains BIBLE_***.txt & the configuration file.
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
            self.config_obj['FOOTPRINT'] = {'weight': 'normal',
                                            'options': 'normal,low'}
            # FIXME
            self.config_obj['COLORS'] = {'frame': 'gray18,',
                                         'master': 'gray18,',
                                         'menubar': 'gray20,ghost white',
                                         'status_bar': 'gray18,ghost white',
                                         'text_widget': 'gray26,ghost white'}

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

        fileName = ''.join(['.ToC_', self.language, '.json'])
        # Path for the full bible text.
        try:
            with open(fileName, 'r') as TableCont:
                [self.bkNames, self.bkAbbrv] = json.load(TableCont)
        except FileNotFoundError:
            messagebox.showerror('Error', 'Table of Contents not found.')

        # Attempt to import bible dictionary as "BibDict".
        fileName = ''.join(['.BibDict_', self.language, '.json'])
        try:
            with open(fileName, 'r') as b:
                d = collections.OrderedDict
                self.BibDict = json.load(b, object_pairs_hook=d)
        except FileNotFoundError:
            # Make "BibDict" if it doesn't already exist,
            # or isn't found in the specified searchpath
            self.BibDict = self.makeBibDict(self)
            with open(fileName, 'w') as b:
                json.dump(self.BibDict, b, ensure_ascii=True)

        try:
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
            self.menubar.add_cascade(label='File', menu=file_menu)
            self.menubar.add_cascade(label='Edit', menu=edit_menu)
            self.menubar.add_cascade(label='Options', menu=options_menu)
            self.menubar.add_cascade(label='Help', menu=help_menu)

            # File menu choices:
            self.sv_button = partial(self.save, self)
            self.frame.master.bind('<Control-s>', self.sv_button)
            file_menu.add_command(label='Save',
                                  accelerator='Ctrl+S',
                                  command=self.sv_button)

            self.svas_button = partial(self.saveas, self)
            self.frame.master.bind('<Control-Shift-S>', self.svas_button)
            file_menu.add_command(label='SaveAs',
                                  accelerator='Ctrl+Shift+S',
                                  command=self.svas_button)

            self.qt_Button = partial(self.close_window, self)
            self.frame.master.bind('<Control-q>', self.qt_Button)
            file_menu.add_command(label='Quit',
                                  accelerator='Ctrl+Q',
                                  command=self.qt_Button)

            # Options menu choices:
            sett = partial(self.settings, self)
            options_menu.add_command(label='Settings',
                                     command=sett)

            self.show_toc = tk.BooleanVar()
            tocq = partial(self.toc_query, self)
            options_menu.add_checkbutton(label='Display Table of Contents',
                                         onvalue=1, offvalue=0,
                                         variable=self.show_toc,
                                         command=tocq)

            # Search Bar placement
            self.qvar = tk.IntVar()
            self.frame.var = tk.IntVar()
            self.frame.SearchBar = tk.Entry(self.frame)
            self.frame.SearchBar.grid(row=2, column=1, sticky='ew')
            slSB = partial(self.select, self)
            self.frame.master.bind('<Control-l>', slSB)

            # For any entry field, ensures one time only call.
            self.frame.entry = 'Search'
            self.frame.SearchBar.insert('end', self.frame.entry)

            self.getIN = partial(self.getInput, self)
            self.frame.master.bind('<Return>', self.getIN)
            self.frame.go_b = tk.Button(self.frame,
                                        text='ENTER',
                                        command=self.getIN,
                                        relief='raised')
            self.frame.go_b.grid(row=3, column=1, sticky='new')

            self.list_button = []

            self.frame.status_bar = tk.Label(self.frame,
                                             text='Welcome!',
                                             relief='flat',
                                             name='status_bar')

            self.frame.status_bar.grid(row=1, column=7, sticky='sew')

            self.frame.text_widget = tk.Text(self.frame,
                                             relief='sunken',
                                             wrap='word',
                                             name='text_widget')
            self.frame.text_widget.grid(row=2,
                                        rowspan=10,
                                        column=7,
                                        sticky='nsew')
            self.cls(self.frame)

            # Welcome message!
            self.textUpdate(self, self.miniPreamble(), 'center')

            '''
            TOOL-TIPS
            self.frame.bind('<ButtonPress>', self.leave)
            # 3 second pause before tooltip appears
            self.waittime = 3000
            '''

            self.frame.Tpadding = tk.Label(self.frame, text='', relief='flat')
            self.frame.Tpadding.grid(row=0, column=0,
                                     columnspan=14, sticky='ew')

            self.frame.Bpadding = tk.Label(self.frame, text='', relief='flat')
            self.frame.Bpadding.grid(row=14, column=0,
                                     columnspan=14, sticky='ew')

            self.frame.Lpadding = tk.Label(self.frame, text='', relief='flat')
            self.frame.Lpadding.grid(row=0, column=0, rowspan=14, sticky='ns')

            self.frame.Rpadding = tk.Label(self.frame, text='', relief='flat')
            self.frame.Rpadding.grid(row=0, column=14, rowspan=14, sticky='ns')

            self.frame.configure(bg=self.colors['frame'][0])
            self.frame.master.configure(bg=self.colors['master'][0])
            self.menubar.config(bg=self.colors['menubar'][0],
                                fg=self.colors['menubar'][1],
                                relief='flat')
            self.frame.status_bar.configure(bg=self.colors['status_bar'][0],
                                            fg=self.colors['status_bar'][1],
                                            font=(self.font,
                                                  self.config_obj[
                                                      'FONT'][
                                                          'title size']))
            self.frame.text_widget.configure(bg=self.colors['text_widget'][0],
                                             fg=self.colors['text_widget'][1])
            self.frame.Tpadding.configure(bg=self.colors['frame'][0],
                                          state='disabled')
            self.frame.Bpadding.configure(bg=self.colors['frame'][0],
                                          state='disabled')
            self.frame.Lpadding.configure(bg=self.colors['frame'][0],
                                          state='disabled')
            self.frame.Rpadding.configure(bg=self.colors['frame'][0],
                                          state='disabled')

        except tk._tkinter.TclError:
            self.pytesting = True

    def _on_mousewheel(self, event):
        if (self.ispc or self.islinux):
            event.delta /= 120
        elif self.ismac:
            event.delta /= 1
        self.canvas.yview_scroll(-1*(event.delta), 'units')

    '''
    def _bound_mouse_to_scrollbar(self, event):
        self.canvas.bind_all('<MouseWheel>', self._on_mousewheel)

    def _unbound_mouse_to_scrollbar(self, event):
        self.canvas.unbind_all('<MouseWheel>')
    '''

    def focus(self, event=None):
        self.focus_set()

    def select(self, event=None):
        self.focus(self.frame.SearchBar)
        self.frame.SearchBar.select_range(0, 'end')
        self.frame.SearchBar.icursor('end')

    '''
    def enter(self, event=None):

    def leave(self, event=None):

    def schedule(self, child):
        self.unschedule()
        st = partial(self.showtip, self, child)
        self.id = self.widget.after(self.waittime, st)

    def unschedule(self):
        ids = self.id
        self.id = None
        if ids:
            self.widget.after_cancel(ids)

    def showtip(self, child, event=None):
        try:
            widget = child
            txt = child.about
            x, y, cx, cy = widget.bbox("insert")
            x += widget.winfo_rootx() + 25
            y += widget.winfo_rooty() + 20
        except NameError:
            return None

        # creates a toplevel window
        self.tw = tk.Toplevel(widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tw, text=txt, justify='left',
                         background="# fffff", relief='solid',
                         borderwidth=1, wraplength=self.wraplength)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw = None
        if tw:
            tw.destroy()

    def createToolTip(self, widget, text):
        self.showtip(self, widget, text)
    '''

    def close_window(self, event=None):
        self.root.destroy()
        pn = 'v1.py'
        for proc in psutil.process_iter():
            if proc.name() == pn:
                proc.kill()

    def settings(self):
        branch = tk.Tk()
        branch.title('Settings')
        # One third the size of the fullscreen main window
        w = self.frame.winfo_width() / 3
        h = self.frame.winfo_height() / 3
        branch.geometry('%dx%d+0+0' % (w, h))

        # Notebook lists Tabs within window.
        nb = ttk.Notebook(branch)
        nb.grid(row=0, column=0, sticky='nsew')

        # Tabs each show component of config.ini
        config_obj = ConfigParser()
        config_obj.read('config.ini')

        path_tab = tk.Frame(nb)
        nb.add(path_tab, text='Path')

        text_tab = tk.Frame(nb)
        nb.add(text_tab, text='Text')

        color_tab = tk.Frame(nb)
        nb.add(color_tab, text='Colors')

        # PATH TAB:
        main = config_obj['PATH']['main']
        m_choice = tk.Entry(path_tab, relief='sunken')
        m_choice.grid(row=1, column=0, columnspan=2)
        m_choice.configure(state='normal')
        m_choice.insert('end', main)

        save = config_obj['PATH']['save']
        s_choice = tk.Entry(path_tab, relief='sunken')
        s_choice.grid(row=2, column=0, columnspan=2)
        s_choice.configure(state='normal')
        s_choice.insert('end', save)

        # TEXT TAB:
        x = ''
        print(x)

        # COLOR TAB:
        bg_label = tk.Label(color_tab, text='Background')
        fg_label = tk.Label(color_tab, text='Foreground')

        frame_color_label = tk.Label(color_tab, text='Main screen: ')
        gcf = partial(self.get_color, self, self.frame)
        fcb = tk.Button(color_tab,
                        relief='sunken',
                        bg=self.frame['bg'],
                        command=gcf)

        master_color_label = tk.Label(color_tab, text='Title Bar: ')
        gcm = partial(self.get_color, self, self.frame.master)
        mcb = tk.Button(color_tab,
                        relief='sunken',
                        bg=self.frame.master['bg'],
                        command=gcm)

        menubar_color_label = tk.Label(color_tab, text='Menu Bar: ')
        gcmb_bg = partial(self.get_color, self, self.menubar)
        mbcb_bg = tk.Button(color_tab,
                            relief='sunken',
                            bg=self.menubar['bg'],
                            command=gcmb_bg)

        gcmb_fg = partial(self.get_color, self, self.menubar, 'fg')
        mbcb_fg = tk.Button(color_tab,
                            relief='sunken',
                            bg=self.menubar['fg'],
                            command=gcmb_fg)

        bg_label.grid(row=0, column=1)
        fg_label.grid(row=0, column=2)

        frame_color_label.grid(row=1, column=0)
        fcb.grid(row=1, column=1)

        master_color_label.grid(row=2, column=0)
        mcb.grid(row=2, column=1)

        menubar_color_label.grid(row=3, column=0)
        mbcb_bg.grid(row=3, column=1)
        mbcb_fg.grid(row=3, column=2)

    def get_color(self, tk_obj, ground='bg'):
        # Queries a color choice
        c = colorchooser.askcolor()[1]
        # Color is applied to tkinter object in the background or foreground
        tk_obj[ground] = c

        # Object's name is used to change its configuration file color value
        n = tk_obj.winfo_name()
        if ground == 'bg':
            self.config_obj['COLORS'][n] = ','.join([c, self.colors[n][1]])
        elif ground == 'fg':
            self.config_obj['COLORS'][n] = ','.join([self.colors[n][0], c])

        with open('config.ini', 'w') as cfg:
            self.config_obj.write(cfg)

    def toc_query(self):
        print(self.show_toc.get())

    def getInput(self, event=None):
        self.frame.var.set(1)
        self.frame.entry = self.frame.SearchBar.get()
        self.statusUpdate(self.frame, self.frame.entry)

        # Table of contents entry check, any full or abbreviated reference
        ToC = self.bkAbbrv + self.bkNames
        ToC = [C.upper() for C in ToC]
        unique_words = self.BibDict['CONCORDANCE']
        # TODO: (1) Upper?
        unique_words = [W.upper() for W in unique_words]

        if self.frame.entry is not None:
            upper = self.frame.entry.upper()
            ToC_entries = [e for e in ToC if e in upper]
            ToC_count = len(ToC_entries)

            words = self.frame.entry.upper().split(' ')
            # TODO: (2) Case sensitive search options,
            # potentially supported by the several entries
            # contained in "unique_words".
            conc_entries = [w for w in unique_words if w in words]
            # SEE: "dispensation of"
            con_count = len(conc_entries)

            numeric_entries = [e for e in self.frame.entry if e.isnumeric()]
        else:
            ToC_entries = []
            ToC_count = len(ToC_entries)

            conc_entries = []
            con_count = len(conc_entries)

            numeric_entries = []

        a = any(ToC_entries)
        b = any(conc_entries)
        c = any(numeric_entries)

        # if all entry contents reference a book, but none of the text
        # EX: "Genesis" --> GENESIS(book)
        # or if entry contents reference a book, and chapter or verse
        # EX: "Rom 12:1"
        out = collections.OrderedDict()
        vcount = pcount = 0
        if (a and not(b)) or (a and c):
            print(1)
            out['VR'], vcount = self.VerseRef(self)
        # else if certain entry contents reference a book and a word in text
        # EX: "romans" --> ROMANS(book) && "... if we being romans ..."
        elif (a and b):
            print(2)
            out['VR'], vcount = self.VerseRef(self)
            out['PS'], pcount = self.PhraseSearch(self)
        # else if some entry contents reference a book, and some text
        # EX: "if we being romans" --> "... if we being romans ..."
        elif ((a and b) and (con_count > ToC_count)) or (not(a) and b):
            print(3)
            out['PS'], pcount = self.PhraseSearch(self)
        # else if entry contents only reference a number combo
        # EX: "23", "3:23", "119:8-9"
        elif (c and not(any([a, b]))):
            print(4)
            # TODO: (3) allow number searches
            # ie "23" --> GEN 23, EXO 23 ... ACT 23
            # && "1:3" --> GEN 1:3, EXO 1:3 ... ACT 1:3
            # && "1-3" --> GEN 1:1-3, 2:1-3 ... EXO 1:1-3, 2:1-3 ... etc.
            out, vcount = self.VerseRef(self)
            pass

        elif not(any([a, b, c])):
            out = []
            print(5)
            messagebox.showerror('Error',
                                 '"%s" not found.' % (self.frame.entry))

        count = vcount + pcount
        if count == 0:
            self.statusUpdate(self.frame, ('%i RESULTS MATCHING %s'
                                           % (count, upper)))
        elif count == 1:
            self.statusUpdate(self.frame, ('%i RESULT MATCHING %s'
                                           % (count, upper)))
        elif count > 1:
            self.statusUpdate(self.frame, ('%i RESULTS MATCHING %s'
                                           % (count, upper)))

        self.listUpdate(self, out)
        self.listUpdate(self, out)
        self.frame.go_b.wait_variable(self.frame.var)

    def getQueryInput(setting_list, self, event=None):
        self.qvar.set(1)
        for i in range(len(setting_list)):
            self.pref_to_dump.append(setting_list[i].get())

    def statusUpdate(self, status):
        self.status_bar.configure(text=status)

    def cls(self):
        self.text_widget.configure(state='normal')
        self.text_widget.delete('1.0', 'end')
        self.text_widget.configure(state='disabled')

    def textUpdate(self, text, just='left'):
        self.cls(self.frame)
        t = self.frame.text_widget
        t.configure(state='normal')
        t.insert('end', text)
        # Justification
        t.tag_add('just', '1.0', 'end')
        t.tag_config('just', justify=just)
        t.configure(state='disabled')

    def listUpdate(self, d, mode='w'):
        try:
            c = self.canvas
            for lb in self.list_button:
                lb.destroy()
            c.destroy()
        except AttributeError:
            pass
        finally:
            self.list_button = []
            self.canvas = tk.Canvas(self.frame)
            c = self.canvas

        if mode == 'w':
            self.cls(self.frame)
        elif mode == 'a':
            pass

        w = self.frame.SearchBar.winfo_width()
        h = self.frame.SearchBar.winfo_height() * 2

        butt_height = 0
        b_press = []
        button_windows = []
        # TODO: (1) Philemon must not return Philippians,
        # but PHM & PHIL must remain their respective abbreviations.
        # (2) Phrase labels should read -->
        # "... not TEMPT the ... ye TEMPTED him..." for DEUT 6:16, etc.
        for key in d.keys():
            # "x" will be list of length 1 for VerseRef dict,
            # list of length == output for PhraseSearch dict.
            label = d[key]['label']
            x = [k for k in d[key].keys() if k != 'label'][0]
            for i in range(len(d[key][x])):
                b_press.append(partial(self.textUpdate, self, d[key][x][i]))
                self.list_button.append(tk.Button(c, text=label[i],
                                                  width=w, height=h,
                                                  command=b_press[-1]))
                lb = self.list_button[-1]
                button_windows.append(c.create_window((0, butt_height),
                                                      anchor='nw',
                                                      width=w, height=h,
                                                      window=lb))
                self.list_button[-1].configure(font=('calibri', 9),
                                               activebackground='#D2D2D2')
                self.list_button[-1].update()
                butt_height += h

        c.grid(row=4, column=1, rowspan=8, columnspan=1, sticky='nsew')
        c.update()

        self.sbar = ttk.Scrollbar(self.frame,
                                  orient='vertical',
                                  command=self.canvas.yview)
        self.sbar.grid(row=4, column=0,
                       rowspan=8, sticky='nes')
        self.sbar.update()

        c.config(yscrollcommand=self.sbar.set, scrollregion=c.bbox('all'))
        '''
        self.canvas.bind('<Enter>', self._bound_mouse_to_scrollbar)
        self.canvas.bind('<Leave>', self._unbound_mouse_to_scrollbar)
        '''

    def calendarUpdate(self):
        url = 'https://www.blueletterbible.org/dailyreading/index.cfm'
        netloc = urllib.request.urlparse(url).netloc
        html = urllib.request.urlopen(url).read()
        soup = bs4.BeautifulSoup(html)
        pdfs = soup.find_all('span')
        links = [l.get('onclick') for l in pdfs]
        hrefs = [l for l in links if l is not None]
        for r in range(len(hrefs)):
            hrefs[r] = hrefs[r].split('=')[1].replace(';', '')
            hrefs[r] = netloc + hrefs[r].replace("'", '')

        # TODO HREFS TO PDFS
        self.calendar = ''

    def save(self, event=None):
        text = self.frame.text_widget.get('1.0', 'end')
        log_time = dt.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        wd = os.getcwd()
        try:
            os.chdir(self.fileLocation)
            self.config_obj.read('config.ini')
            self.save_directory = self.config_obj['PATH']['save']
            # Technical necessity in the case of accessing
            # settings from the menubar, before saving manually:
            if self.save_directory == '':
                raise KeyError

            with open('config.ini', 'w') as cfg:
                self.config_obj.write(cfg)

            os.chdir(self.save_directory)
            with open('%s.txt' % (log_time), 'w') as saved:
                # Save file found and amended
                saved.write(text)

        except (KeyError, FileNotFoundError):
            # Save file not found, saveas:
            self.saveas(self)

        finally:
            os.chdir(wd)

    def saveas(self, event=None):
        text = self.frame.text_widget.get('1.0', 'end')
        dirName = filedialog.askdirectory(
                   initialdir=self.homeDirectory, title="SaveAs")

        try:
            os.chdir(dirName)
        except OSError:
            return None
        log_time = dt.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        with open(log_time, 'w') as saved_as:
            saved_as.write(text)

        os.chdir(self.fileLocation)
        self.config_obj = ConfigParser()
        self.config_obj.read('config.ini')
        self.config_obj['PATH']['save'] = dirName
        with open('config.ini', 'w') as cfg:
            self.config_obj.write(cfg)

    '''
    ####################################
    ##                                ##
    ## For Searching Verse References ##
    ##                                ##
    ####################################
    '''

    # TODO: (1) Languages
    # (2) Trim fat code
    def VerseRef(self):
        # Initialize 'out' for concatenation.
        out = collections.OrderedDict({'verses': '', 'label': ''})

        location = self.frame.entry
        loc = []
        locAlph = ''
        locNumb = ''
        for char in location:
            # Saves the alphabetic part of location
            if char.isalpha() or char.isspace():
                locAlph += char
            # Saves the numeric part of location
            else:
                locNumb += char

        loc.append(locAlph)
        # Combine the alphabetic and numeric parts to loc
        loc.append(locNumb.strip())
        location = ''.join(loc)
        # 66 books!
        n = len(self.bkNames)
        # Book is empty by default, filled this loop:
        book = ''
        # LOOP THROUGH BOOKS
        for b in range(n):
            # Compare strings to see if input is in
            # Table of Contents (ignore case); accounts
            # for abbreviations of books.
            LenAbb = len(self.bkAbbrv[b])
            inToC = (self.bkAbbrv[b].upper() == locAlph.upper()[0:LenAbb])
            print(self.bkAbbrv[b], inToC)
            if inToC:
                print('IF (L774)')
                book = self.bkAbbrv[b]
                # The following Marks for statusUpdate
                bkMark = self.bkNames[b]
                out['label'] += bkMark
                print(bkMark)
                break
            # SEE <TODO (3)> in getInput
            elif not(locAlph):
                print('ELIF (L783)')
                book = 'all'
                bkMark = 'Parellel References'
                out['label'] += bkMark
                self.close_window(self)
                break
            # Proceed to next book. If no match is
            # found, 'book' would remain empty.
            else:
                continue

        # This IF catches an empty numeric part
        # 0 indicates that no Chapters were specified:
        # The book will be the only output.
        if (len(loc) > 1):
            chpRef = (loc[1])
            if not chpRef:
                chpRef = '0'
        # ELSE catches the lack of numeric part
        else:
            chpRef = '0'

        # If there is a numeric part of 'loc',
        # it can be used as the chapter reference.
        if not chpRef == '0':
            loc = chpRef
            vrsRef = '0'
            firstVerse = vrsRef
            fV = int(firstVerse)
            lV = 0
            # If there is a colon, there is a verse ref.
            if ':' in loc:
                loc = re.split(char, loc)
                chpRef = loc[0]
                vrsRef = loc[1]

                severalVrs = False
                # If there is a dash, there are several verses.
                if ('-' in loc) or (',' in loc):
                    severalVrs = True
                    vrsRef = re.split(char, vrsRef)
                    firstVerse = vrsRef[0]
                    lastVerse = vrsRef[1]
                    fV = int(firstVerse)
                    lV = int(lastVerse)

        if not location:
            next
        elif location.upper() == 'ABOUT':
            self.textUpdate(self,
                            '''
                            ____________________________________________
                            ___\n This text-based app was written by
                             Greg Caceres\n It is free to use, access,
                             or edit. It is open\n source, free as in
                             beer and speech. The King\n James Bible has
                             its publishing and usage rights\n vested in
                             the Crown within the United Kingdom.\n
                             Everywhere else it is in the public domain,
                            \n and is free to use, quote, or share
                             without\n limit, provided no changes are
                             made to the\n content therein. For
                             support, or if you\n have any questions
                             about the app\'s functionality,\n the content
                             of the word of God, or anything else\n
                             related, feel free to contact me at\n
                             gregcaceres@gmail.com\n
                            ____________________________________________
                            ___\n
                            ''')

        outFind = self.BibDict[book]
        # If only book name is input, output whole book
        if chpRef == '0':
            cKeyList = range(len(outFind.keys()))
            # Hone in on a chapter for the verse loop sake:
            out['verses'] = '\n %s' % (out['label'])
            for cKey in cKeyList:
                cKey = str(cKey+1)
                # LOOP through verses keys
                # and concatenate each verse-field's string.
                cFind = outFind[cKey]
                vKeyList = range(len(cFind.keys()))
                for vKey in vKeyList:
                    vKey = str(vKey+1)
                    if vKey == '1':
                        cPrint = '\n\n Chapter %s\n\n' % (cKey)
                    else:
                        cPrint = '\n'

                    # Verses acquired!
                    out['verses'] += (cPrint + cFind[vKey])

        else:
            cKey = chpRef
            out['label'] = ' %s' % (cKey)
            try:
                cFind = outFind[cKey]
            except KeyError:
                cMax = len(outFind.keys())

                # Plural or not?
                if cMax == 1:
                    noCRef = ('ortunetly, %s only has %i chapter'
                              % (bkMark, cMax))
                else:
                    noCRef = ('ortunetly, %s only has %i chapters'
                              % (bkMark, cMax))
                fortunate = rnd.randint(0, 1)
                if fortunate:
                    noCRef = '\n F' + noCRef
                else:
                    noCRef = '\n Unf' + noCRef

            # If only chapter is input, output whole chapter
            if vrsRef == '0':
                out['label'] = bkMark + cKey
                vKeyList = range(len(cFind.keys()))
                out['verses'] = '\n %s' % (out['label'])
                # LOOP through these verses, and
                # concatenate each verse-field's string.
                for vKey in vKeyList:
                    vKey = str(vKey+1)
                    out['verses'] += '\n' + cFind[vKey]

            # Range of verses
            elif severalVrs:
                vMax = len(cFind.keys())
                for verseNum in range(fV, lV):
                    vKey = str(verseNum)
                    try:
                        # Verses acquired!
                        out['verses'] += '\n%s' % (cFind[vKey])
                        vEnd = lV
                    # Verse number larger than max number of verses in chapter
                    # --> print only to chapter's end and cast change to label
                    except KeyError:
                        vEnd = vMax
                        out['verses'] += '\n%s' % (cFind[vEnd])

                out['label'] += ':%s-%s' % (str(fV), str(vEnd-1))

            # Just one verse
            else:
                vKey = vrsRef
                out['label'] += ':%s' % (vKey)
                try:
                    # Verse acquired!
                    out['verses'] += '\n%s' % (cFind[vKey])
                except KeyError:
                    vMax = len(cFind.keys())
                    noVRef = ('ortunetly, %s %s only has %i verses'
                              % (bkMark, chpRef, vMax))
                    fortunate = rnd.randint(0, 1)
                    if fortunate:
                        noVRef = '\n F' + noVRef
                    else:
                        noVRef = '\n Unf' + noVRef
                        out = [noVRef]

        self.statusUpdate(self.frame, out['label'])
        out['verses'] = [out['verses']]
        out['label'] = [out['label']]
        # TODO: count > 1 for instances such as many chapters containing "1-3"
        count = 1
        return out, count

    '''
    ###########################
    ##                       ##
    ## For Searching Phrases ##
    ##                       ##
    ###########################
    '''

    def PhraseSearch(self, toShow='None'):
        out = collections.OrderedDict({'phrases': [], 'label': []})

        Srch = r'%s' % (self.frame.entry)
        # addOns = ''

        # Case insensitive search anywhere within a word.
        # EX: Srch = "tempt" -->
        # [Tempt, tempted, aTTempt, contEmpT, TEMPTATION, ...]
        m = re.compile(r'(?i)(\w*%s\w*)' % (Srch))

        count = 0
        for bKey in self.bkAbbrv:
            chpDict = self.BibDict[bKey]
            chpIter = chpDict.keys()
            for cKey in chpIter:
                vrsDict = chpDict[cKey]
                vrsIter = vrsDict.keys()
                for vKey in vrsIter:
                    lines = vrsDict[vKey]
                    s = m.search(lines)
                    if s:
                        # Precompiled - pattern.sub(replacement, str)
                        vFound = lines
                        for item in m.finditer(vFound):
                            g = item.group(1)
                            n = re.compile(r'(?i)%s' % (g))
                            vFound = n.sub(g.upper(), vFound)

                        # \S instead of \w to include
                        # punctuation at fringes of words
                        o = re.compile(r'(?i)^\S*%s\S* \S* \S*' % (g))
                        p = re.compile(r'(?i)\S* \S*%s\S* \S*' % (g))
                        q = re.compile(r'(?i)\S* \S* \S*%s\S*$' % (g))
                        iterspan = ''

                        ocond = o.search(vFound)
                        pcond = p.search(vFound)
                        qcond = q.search(vFound)
                        if ocond:
                            # print('o')
                            for item in o.finditer(vFound):
                                s = item.start()
                                e = item.end()
                                iterspan += '%s...' % (vFound[s:e])

                        if pcond:
                            # print('p')
                            for item in p.finditer(vFound):
                                s = item.start()
                                e = item.end()
                                iterspan += '... %s...' % (vFound[s:e])

                        if qcond:
                            # print('q')
                            for item in q.finditer(vFound):
                                s = item.start()
                                e = item.end()
                                iterspan += '... %s' % (vFound[s:e])

                        vrsAlph, vrsNumb = '', ''
                        for char in vFound:
                            if char.isdigit():
                                vrsNumb += char
                            else:
                                vrsAlph += char

                        ref = ''.join([' ', bKey,
                                       ' ', cKey,
                                       ':', vrsNumb])
                        out['phrases'].append(vrsAlph)
                        out['label'].append('%s\n%s' % (ref, iterspan))
                        count += 1

        return out, count

    def preamble():
        cross = '''\n\n
                         \\              /
                          \\     _      /
                               | |
                               | |
                          _____| |_____
                         |_____   _____|
                               | |
                               | |
                               | |
                               | |
                               | |
                               | |
                               |_|
                       _______/   \\_______        \n\n
                '''

        version = '''   ______________________

                      THE KING JAMES BIBLE
                      ______________________

                      Please rightly divide and handle with prayer. \n\n
                  '''

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
                        ______________________________________________________________

                        Type "Help" to display this page again.
                        Type "About" for information about the app.
                        Type "Options" for a list of recognized book names.
                        Type "Phrase" to switch over to phrase searching.
                        Type "Done" to finish searching and quit.\n
                    '''

        return ''.join([cross, version, AppFormat])

    def miniPreamble():
        cross = '''\n\n
-   \\              /  +
+    \\     _      /   -
-         | |         +
+         | |         -
-    _____| |_____    +
+   |_____   _____|   -
-         | |         +
+         | |         -
-         | |         +
+         | |         -
-         | |         +
+         | |         -
-         |_|         +
+ _______/   \\_______ -
'''

        version = '''
______________________

 THE KING JAMES BIBLE
______________________

Please rightly divide and handle with prayer.
\n\n'''

        return ''.join([cross, version])

    def makeBibDict(self):
        bfile = self.pathPart.join([self.fileLocation, 'BIBLE_%s.txt' % (self.language)])
        with open(bfile, 'r') as f:
            bib = f.read()

        # TODO: Add verbal details to progress bar status updates
        try:
            child = tk.Tk()
            child.title('Importing')
            msg = 'Please wait while the text is compiled...'
            info = tk.Label(child, text=msg, relief='flat')
            progress = ttk.Progressbar(child, orient='horizontal',
                                       length=100, mode='determinate')
            info.pack(padx=5, pady=5)
            progress.pack(padx=5, pady=5)

            progress['value'] = 1
            child.update()
        except tk._tkinter.TclError:
            self.pytesting = True

        # Letters and space for Concordance compilation
        alpha_space = string.ascii_letters + ' '

        n = len(self.bkNames)
        books = []
        trim_books = []
        trim_text = ''
        for b in range(n):
            m = re.compile(r'^(%s)' % (self.bkNames[b]))
            if b < 65:
                text = re.split(self.bkNames[b+1], bib)[0]
                # Exclude titles from text.
                bib = m.sub('', bib)
                text = m.sub('', text)

            elif b == 65:
                text = bib

            # Clear books already coverd.
            bkWiper = ''
            bkToWipe = text
            bib = bib.replace(bkToWipe, bkWiper)

            books.append(text)
            trim_text += ''.join([l for l in text if l in alpha_space])
            trim_books.append(trim_text)

            if self.pytesting:
                pass
            else:
                progress['value'] = b / n * 100
                child.update()

        trim_bible = ''.join(trim_books)
        # Whole Bible excluding punctuation and book titles.
        bib_letters = ''.join([l for l in trim_bible])
        bib_words = re.split(' ', bib_letters)
        bib_words = [w for w in bib_words if w != '']
        # Concordance equivalent
        unique_words = [s for s in set(bib_words) if s not in self.bkNames]

        if self.pytesting:
            pass
        else:
            progress['value'] = 1
            child.update()

        BibDict = collections.OrderedDict()
        # Loops to populate the book structure.
        for b in range(n):
            # Chapters marked uniquely (":1 " =  c.x:v.1)
            chapters = re.split(':1 ', books[b])[1:]
            cLen = len(chapters)
            chpDict = collections.OrderedDict()
            # Loops to populate the chapter structure.
            for c in range(cLen):
                # Add the verse 1 marker again for verse indexing:
                chapters[c] = ':1 ' + chapters[c]
                # Indexes the places where verses MAY appear.
                idx = chapters[c].find(':')
                for x in [idx]:
                    if (chapters[c])[x+1].isnumeric():
                        # Only the numeral indexed places are retained
                        # (i.e. "1:2" retained, "Behold: Foo" is not).
                        delim = str(c+1) + ':'
                        verses = re.split(delim, chapters[c])
                vLen = len(verses)
                vrsDict = collections.OrderedDict()
                # Loops to populate the verse structure.
                for v in range(vLen):
                    if v == 0:
                        # Removes the extra colon left in each verse 1.
                        m = re.compile(':1 ')
                        verses[v] = m.sub('1 ', verses[v])

                    # Beginning of line whitespace strip
                    m = re.compile(r'(^\s*)')
                    verses[v] = m.sub('', verses[v])

                    # End of line whitespace / misc. strip
                    # EX: "Amen. I" / "Amen. 1" / "Amen.  "
                    m = re.compile(r'([\s\dI]{1,}$)')
                    verses[v] = m.sub('', verses[v])

                    vrsKey = str(v + 1)
                    vrsDict[vrsKey] = verses[v]

                # Structure field names cannot or
                # should not start with numbers.
                chpKey = str(c+1)
                chpDict[chpKey] = vrsDict

            bkKey = self.bkAbbrv[b]
            BibDict[bkKey] = chpDict

            if self.pytesting:
                pass
            else:
                progress['value'] = b / n * 100
                child.update()

        if self.pytesting:
            pass
        else:
            child.destroy()

        BibDict['CONCORDANCE'] = unique_words
        return BibDict

    def ismember(a, b):
        bind = {}
        for i, elt in enumerate(b):
            if elt not in bind:
                bind[elt] = i
                return [bind.get(itm, None) for itm in a]


if __name__ == '__main__':
    Bible.__init__(Bible)
    gsize = Bible.frame.grid_size()
    for row in range(gsize[0]):
        tk.Grid.rowconfigure(Bible.frame, row, weight=1)
        for col in range(gsize[1]):
            tk.Grid.columnconfigure(Bible.frame, col, weight=1)
    main = tk.mainloop()
