#!/usr/bin/python3

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# _______________________________________________
#
# This app was written by Greg Caceres.
# It is free to use, access, or edit. It is open
# source, free as in beer and as in speech.
# Comprehensive license pending.
#
# The Biblical translations used herein are all
# in the public domain, and free to use, quote,
# or share without limit, provided no changes
# are made to the content therein.
#
# If you are running on MicroSoft Windows,
# see the install support for Python at
#
# https://docs.python.org/3/using/windows.html
#
# For other support, or if you have any
# questions about the app's functionality,
# the content of the word of God, or
# anything else related, contact at
#
# gregcaceres@gmail.com
# _______________________________________________

import bs4
import collections
import datetime as dt
from functools import partial
import json
import os
import random as rnd
import re
import sys
import tkinter as tk
from tkinter import filedialog
import urllib


class Bible:

    def __init__(self):

        '''
        # ################
        #              ##
        # Initializing ##
        #              ##
        # ################
        '''

        # Create & Configure root
        self.root = tk.Tk()
        tk.Grid.rowconfigure(self.root, 0, weight=1)
        tk.Grid.columnconfigure(self.root, 0, weight=1)

        # Create & Configure frame
        self.frame = tk.Frame(self.root)
        self.frame.tk_focusFollowsMouse()
        self.frame.master.title('The Bible')
        self.frame.grid(row=0, column=0, sticky='NSEW')

        menubar = tk.Menu(self.frame)
        fileMenu = tk.Menu(menubar, tearoff=0)
        optionsMenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='File', menu=fileMenu)
        menubar.add_cascade(label='Options', menu=optionsMenu)

        self.sv_Button = partial(self.save, self)
        fileMenu.add_command(label='Save',
                             accelerator='Ctrl+S',
                             command=self.sv_Button)
        self.frame.master.bind('<Control-s>', self.sv_Button)

        optionsMenu.add_cascade(label='Color Preferences',
                                command=self.getColor())
        self.frame.master.config(menu=menubar)

        self.w = self.frame.winfo_screenwidth()
        self.h = self.frame.winfo_screenheight()
        self.frame.master.geometry('%dx%d+0+0' % (self.w, self.h))

        # For any entry field, ensures one time only call.
        self.frame.entry = '...'
        self.getIN = partial(self.getInput, self)
        self.frame.master.bind('<Return>', self.getIN)

        self.qvar = tk.IntVar()
        self.frame.var = tk.IntVar()
        self.frame.SearchBar = tk.Entry(self.frame)
        self.frame.SearchBar.grid(row=2, column=1, sticky='ew')
        self.fc = partial(self.focus, self)
        self.frame.master.bind('<Control-l>', self.fc)

        self.getIN = partial(self.getInput, self)
        self.frame.go_b = tk.Button(self.frame,
                                    text='ENTER ↵',
                                    command=self.getIN,
                                    relief='flat')
        self.frame.go_b.grid(row=3, column=1, sticky='new')

        self.frame.listFrame = tk.Frame(self.frame)
        self.frame.listFrame.grid(row=4, column=1, rowspan=6, sticky='new')
        # FIXME
        '''
        # elf.frame.listFrame.config(scrollregion=self.frame.bbox('all'))
        # elf.lbox_h = (self.frame.listFrame.config()['height'][-1])
        # elf.lbox_w = (self.frame.listFrame.config()['width'][-1])

        # elf.frame.scrollbar = tk.Scrollbar(self.frame, orient='vertical')
        # elf.frame.scrollbar.bind_all('<MouseWheel>', self._on_mousewheel)
        # elf.frame.scrollbar.config(command=self.frame.listFrame.yview_scroll)

        # elf.frame.listFrame = tk.Frame(self.frame.listFrame)
        # elf.frame.listFrame.config(width=self.lbox_w, height=self.canvas_h)
        # elf.frame_h= self.frame.listFrame.config()['height'][-1]
        # elf.frame_w = self.frame.listFrame.config()['width'][-1]
        # elf.frame.listFrame.create_window((4,4),
                                            window=self.frame.listFrame,
                                            anchor="nw",
                                            tags='self.frame.listFrame')
        '''

        # Populated in listUpdate
        # List of event handlers for button presses
        self.b_press = list()
        # List of buttons to be pressed
        self.frame.listed_button = list()

        self.frame.statusBar = tk.Label(self.frame,
                                        text='Welcome!',
                                        relief='flat')

        self.frame.statusBar.grid(row=1, column=7, sticky='sew')

        self.frame.textWidget = tk.Text(self.frame,
                                        relief='sunken',
                                        wrap='word')
        self.frame.textWidget.grid(row=2,
                                   rowspan=10,
                                   column=7,
                                   sticky='nsew')
        self.cls(self.frame)

        # Welcome message!
        self.textUpdate(self, self.miniPreamble())

        # elf.frame.master.bind('<Enter>', self.enter)
        # elf.frame.master.bind('<Leave>', self.leave)
        # elf.frame.master.bind('<ButtonPress>', self.leave)

        self.qt_Button = partial(self.close_window, self)
        self.frame.master.bind('<Control-q>', self.qt_Button)
        self.frame.quitButton = tk.Button(self.frame,
                                          text='Quit',
                                          command=self.qt_Button,
                                          relief='raised')
        self.frame.quitButton.grid(row=11,
                                   column=10,
                                   columnspan=2,
                                   sticky='sew')

        self.frame.Tpadding = tk.Label(self.frame, text='', relief='flat')
        self.frame.Tpadding.grid(row=0, column=0, columnspan=14, sticky='ew')

        self.frame.Bpadding = tk.Label(self.frame, text='', relief='flat')
        self.frame.Bpadding.grid(row=14, column=0, columnspan=14, sticky='ew')

        self.frame.Lpadding = tk.Label(self.frame, text='', relief='flat')
        self.frame.Lpadding.grid(row=0, column=0, rowspan=14, sticky='ns')

        self.frame.Rpadding = tk.Label(self.frame, text='', relief='flat')
        self.frame.Rpadding.grid(row=0, column=14, rowspan=14, sticky='ns')

        self.frame.configure(background='gray18')
        self.frame.master.configure(background='gray18')
        menubar.config(background='gray20',
                       foreground='ghost white',
                       relief='flat')
        self.frame.listFrame.configure(background='gray18', relief='sunken')
        self.frame.quitButton.configure(background='gray26',
                                        foreground='ghost white')
        self.frame.statusBar.configure(background='gray18',
                                       foreground='ghost white',
                                       font=('times', 25))
        self.frame.textWidget.configure(background='gray26',
                                        foreground='ghost white')
        self.frame.Tpadding.configure(background='gray18',
                                      foreground='ghost white',
                                      state='disabled')
        self.frame.Bpadding.configure(background='gray18',
                                      foreground='ghost white',
                                      state='disabled')
        self.frame.Lpadding.configure(background='gray18',
                                      foreground='ghost white',
                                      state='disabled')
        self.frame.Rpadding.configure(background='gray18',
                                      foreground='ghost white',
                                      state='disabled')

        ispc = sys.platform.startswith('win')
        # Platform name for Mac OS X.
        ismac = sys.platform.startswith('darwin')
        islinux = sys.platform.startswith('linux')

        if ispc:
            self.pathPart = '\\'
        elif (ismac or islinux):
            self.pathPart = '/'

        try:
            with open('.fileLocation.json', 'r+') as fileLoc:
                self.fileLocation = json.load(fileLoc)
            os.chdir(self.fileLocation)
        except:
            # Manual input required if searchpath isn't
            # already defined. This will then be saved for
            # next time and used as the working directory.
            self.fileLocation = filedialog.askdirectory(
                                initialdir=self.pathPart,
                                title="Select directory")
            # This directory contains BIBLE.txt & the directory's name itself.
            os.chdir(self.fileLocation)
            with open('.fileLocation.json', 'w+') as fileLoc:
                json.dump(self.fileLocation, fileLoc, ensure_ascii=True)

        try:
            with open('.bibPreferences.json', 'r+') as Pref:
                [self.language, self.font, self.font_size] = json.load(Pref)
        except:
            # Defaults:
            self.language = 'en'
            self.font = 'roman'
            self.font_size = '12'

            with open('.bibPreferences.json', 'w+') as Pref:
                json.dump([self.language, self.font, self.font_size],
                          Pref, ensure_ascii=True)

            # FIXME
            '''
            # ett_root = tk.Tk()
            # uery_list = ['Language? [el/he/en/es]','Font?','Font Size?']
            # elf.pref_to_dump = []
            # ettings_list = []
            # or q in query_list:
            #   query = tk.Label(sett_root,text=q)
            #   setting = tk.Entry(sett_root)
            #   query.pack(), setting.pack()
            #   settings_list.append(setting)


            # qi = partial(self.getQueryInput, settings_list, self)
            # nput_button = tk.Button(sett_root, text='ENTER ↵', command=gqi)
            # nput_button.pack()

            # ett_root.destroy()
            # ith open('.bibPreferences.json', '+w') as Pref:
            #   json.dump([self.language, self.font, self.font_size],
                          Pref, ensure_ascii=True)
            '''
        try:
            fileName = ''.join(['.ToC_', self.language, '.json'])
            # Path for the full bible text.
            with open(fileName, 'r+') as TableCont:
                [self.bkNames, self.bkAbbrv] = json.load(TableCont)
        except:
            # Fall-back import Table of Contents
            # as "bkAbbrv" & "bkNames".
            # (Instance variables based on "language")
            with open(fileName, 'r+') as TableCont:
                [self.bkNames, self.bkAbbrv] = json.load(TableCont)
        try:
            # Attempt to import bible dictionary
            # as "BibDict".
            fileName = ''.join(['.BibDict_', self.language, '.json'])
            with open(fileName, 'r+') as Bib:
                d = collections.OrderedDict
                self.BibDict = json.load(Bib,
                                         object_pairs_hook=d)
        except:
            # Make "BibDict" if it doesn't already exist,
            # or isn't found in the specified searchpath
            self.BibDict = self.makeBibDict(self)

    def focus(self, event=None):
        self.frame.SearchBar.focus_set()
        self.select(self)

    def select(self, event=None):
        self.frame.SearchBar.select_range(0, 'end')
        self.frame.SearchBar.icursor('end')

    def on_mousewheel(self, event=None):
        self.frame.listFrame.yview_scroll(-1*(event.delta/120), 'units')

        '''
        # ef enter(self, event=None):
        #       self.schedule()

        # ef leave(self, event=None):
        #       self.unschedule()
        #       self.hidetip()

        # ef schedule(self):
        #   self.unschedule()
        #   self.id = self.widget.after(self.waittime, self.showtip)

        # ef unschedule(self):
        #   ids = self.id
        #   self.id = None
        #   if ids:
        #       self.widget.after_cancel(ids)
        '''

    def showtip(self, widget, txt='', event=None):
        x = y = 0
        x, y, cx, cy = widget.bbox("insert")
        x += widget.winfo_rootx() + 25
        y += widget.winfo_rooty() + 20
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

    def getColor():
        return
        # color = tk.tkColorChooser.askcolor()
        # rint(color)

    def createToolTip(self, widget, text):
        self.showtip(self, widget, text)

    def close_window(self, event=None):
        self.root.destroy()

    def getInput(self, event=None):
        self.frame.var.set(1)
        self.frame.entry = self.frame.SearchBar.get()
        self.statusUpdate(self.frame, self.frame.entry)
        self.VerseRef(self)

    def getQueryInput(setting_list, self, event=None):
        self.qvar.set(1)
        for i in range(len(setting_list)):
            self.pref_to_dump.append(setting_list[i].get())

    def statusUpdate(self, status):
        self.statusBar.configure(text=status)

    def cls(self):
        self.textWidget.configure(state='normal')
        self.textWidget.delete('1.0', 'end')
        self.textWidget.configure(state='disabled')

    def textUpdate(self, text):
        self.cls(self.frame)
        self.frame.textWidget.configure(state='normal')
        self.frame.textWidget.insert('end', text)
        self.frame.textWidget.configure(state='disabled')

    # TODO (L.115)
    def listUpdate(self, l):
        for i in range(len(l)):
            self.b_press.append(partial(self.textUpdate, self, l[i]))
            b = self.b_press[i]
            self.frame.listed_button.append(tk.Button(self.frame.listFrame,
                                                      text=l[i][0:50],
                                                      command=b))
            self.frame.listed_button[i].grid(row=i, column=0, sticky='ew')
        self.frame.scrollbar.grid(column=1, sticky='ns')
        lgsize = self.frame.listFrame.grid_size()
        for row in range(lgsize[0]):
            tk.Grid.rowconfigure(self.frame.listFrame, row, weight=1)
            for col in range(lgsize[1]):
                tk.Grid.columnconfigure(self.frame.listFrame,
                                        col,
                                        weight=1)
        self.frame.listFrame.config(width=self.lbox_w,
                                    height=self.canvas_h)
        self.b_press, self.frame.listed_button = [], []

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

        # ODO HREFS TO PDFS
        self.calendar = ''

    def save(self):
        text = self.frame.textWidget.get('1.0', 'end')
        log_time = dt.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        try:
            wd = os.getcwd()
            os.chdir(self.fileLocation)
            with open('.save_directory.json', 'r+') as save_dir:
                self.save_directory = json.load(save_dir)
            os.chdir(self.save_directory)
            with open('%s.txt' % (log_time), 'w+') as saved:
                # Save file found and amended
                saved.write(text)
        except:
            # Save file not found, saveas:
            self.saveas(self)
        finally:
            os.chdir(wd)

    def saveas(self):
        text = self.frame.textWidget.get('1.0', 'end')
        fileName = filedialog.asksaveasfilename(
                    initialdir=self.pathPart, title="Save as",
                    filetypes=(("text file", "*.txt"),
                               ("all files", "*.*")))
        with open(fileName, 'w+') as saved_as:
            saved_as.write(text)
        self.save_directory = re.split('.', fileName)[0]
        os.chdir(self.fileLocation)
        with open('.save_directory.json', 'w+') as save_dir:
            json.drump(self.save_directory, save_dir, ensure_ascii=True)

    '''
    # ##################################
    #                                ##
    # For Searching Verse References ##
    #                                ##
    # ##################################
    '''

    def VerseRef(self, toShow='None'):
        # Initialize 'verses_out' for concatenation.
        verses_out = list()
        status = ''
        self.cls(self.frame)
        if toShow == 'Short':
            self.textUpdate(self, self.miniPreamble())
            self.frame.go_b.wait_variable(self.frame.var)
        elif toShow == 'None':
            pass

        location = self.frame.entry
        loc = list()
        locAlph = ''
        locNumb = ''
        for char in location:
            # Saves the alphabetic part of location
            if char.isalpha():
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
            if inToC:
                book = self.bkAbbrv[b]
                # The following Marks for statusUpdate
                bkMark = self.bkNames[b]
                status += bkMark
                break
            elif b == 65:
                return self.PhraseSearch(self)
            # Proceed to next book. If no match is
            # found, 'book' would remain empty.
            # parts (Lines 101-102 )...
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
            for char in loc:
                # If there is a colon, there is a verse ref.
                if char == ':':
                    loc = re.split(char, loc)
                    chpRef = loc[0]
                    vrsRef = loc[1]

                # If there is a dash, there are several verses.
                if (char == '-') or (char == ','):
                    severalVrs = True
                    vrsRef = re.split(char, vrsRef)
                    firstVerse = vrsRef[0]
                    lastVerse = vrsRef[1]
                    fV = int(firstVerse)
                    lV = int(lastVerse)
                else:
                    severalVrs = False
                    firstVerse = vrsRef
                    fV = int(firstVerse)
                    lV = 0

        if not location:
            next
        elif location.upper() == 'ABOUT':
            toShow = 'Long'
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
        elif location.upper() == 'OPTIONS':
            toShow = 'None'
            self.cls(self.frame)
            ToC = ['_________________________',
                   '                         ',
                   'Table of Contents --- ToC',
                   '_________________________',
                   '                         ']
            for i in range(5, (n+4)):
                ToC.append(self.bkNames[i-4] + ' ... ' + self.bkAbbrv[i-4])

            ToC[66+5] = self.bkNames[66] + ' ... ' + self.bkAbbrv[66]
            self.textUpdate(self, ToC)
        elif location.upper() == 'HELP':
            toShow = 'Long'

        verses_outFind = self.BibDict[book]
        verses_out = list()

        # If only book name is input, output whole book ##
        if chpRef == '0':
            cKeyList = range(len(verses_outFind.keys()))
            # Hone in on a chapter for the verse loop sake:
            for cKey in cKeyList:
                cKey = str(cKey+1)
                # LOOP through verses keys
                # and concatenate each verse-field's string.
                cFind = verses_outFind[cKey]
                vKeyList = range(len(cFind.keys()))
                verses_out_collect = ''
                for vKey in vKeyList:
                    vKey = str(vKey+1)
                    if vKey == '1':
                        cPrint = '\n\n Chapter %s \n\n' % (cKey)
                    else:
                        cPrint = '\n'

                    # TODO: BASED ON LANGUAGE, PRINT BACKWARDS
                    verses_out_collect += (cPrint + cFind[vKey])
            # Verses acquired!
            verses_out.append(verses_out_collect)

        else:
            cKey = chpRef
            status += ' %s' % (cKey)
            try:
                cFind = verses_outFind[cKey]
            except:
                cMax = len(verses_outFind.keys())

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

            # If only chapter is input, output whole chapter ##
            if vrsRef == '0':
                vKeyList = range(len(cFind.keys()))
                verses_out_collect = ''
                # LOOP through these verses, and
                # concatenate each verse-field's string.
                for vKey in vKeyList:
                    vKey = str(vKey+1)
                    verses_out_collect += '\n' + cFind[vKey]
                verses_out.append(verses_out_collect)

            # Range of verses ##
            elif severalVrs:
                vMax = len(cFind.keys())
                e_raised = False
                for verseNum in range(fV, lV):
                    vKey = str(verseNum)
                    try:
                        # Verses acquired!
                        verses_out.append('\n' + cFind[vKey])
                    except:
                        e_raised = True
                    finally:
                        if e_raised:
                            vEnd = vMax
                        else:
                            vEnd = lV

                status += ':%s-%s' % (str(fV), str(vEnd-1))

            # Just one verse
            else:
                vKey = vrsRef
                status += ':%s' % (vKey)
                try:
                    # Verse acquired!
                    verses_out.append('\n' + cFind[vKey])
                except:
                    vMax = len(cFind.keys())
                    noVRef = ('ortunetly, %s %s only has %i verses'
                              % (bkMark, chpRef, vMax))
                    fortunate = rnd.randint(0, 1)
                    if fortunate:
                        noVRef = '\n F' + noVRef
                    else:
                        noVRef = '\n Unf' + noVRef
                        verses_out = [noVRef]

        self.statusUpdate(self.frame, status)
        self.cls(self.frame)
        self.listUpdate(self, verses_out)
        self.frame.go_b.wait_variable(self.frame.var)

    '''
    # #########################
    #                       ##
    # For Searching Phrases ##
    #                       ##
    # #########################
    '''

    def PhraseSearch(self, toShow='None'):
        verses_out = list()
        if not toShow == 'None':
            self.textUpdate(self, self.miniPreamble())
            self.frame.go_b.wait_variable(self.frame.var)
        else:
            self.cls(self.frame)

        Srch = self.frame.entry
        addOns = ''
        m = re.compile('(?i)'+Srch)
        if Srch.isnumeric():
            self.frame.entry.delete(0, 'end')
            self.statusUpdate(self.frame, 'Non-numeric Input Please')
            self.textUpdate(self, self.miniPreamble())

        count = 0
        vFound = list()
        vrsList = list()
        for bKeySpaced in self.bkAbbrv:
            bKey = bKeySpaced.replace(' ', '')
            chpDict = self.BibDict[bKey]
            chpIter = chpDict.keys()
            for cKey in chpIter:
                vrsDict = chpDict[cKey]
                vrsIter = vrsDict.keys()
                for vKey in vrsIter:
                    lines = vrsDict[vKey]
                    vrsList.append(lines)
                    if re.search(addOns+Srch, vrsList[-1]):
                        # Precompiled - pattern.sub(replacement, str)
                        vFound.append(m.sub(Srch.upper(), vrsList[-1]))

                vLen = len(vFound)
                count += vLen
                if vLen > 0:
                    for v in range(vLen):
                        if not (vFound[v])[0].isnumeric():
                            ref = ''.join([bKeySpaced, ' ', cKey, ':1 '])
                            verses_out.append('\n '.join(['',
                                                          ref,
                                                          vFound[v]]))
                        else:
                            vrsAlph, vrsNumb = '', ''
                            for char in vFound[v]:
                                # Saves the numeric part of the verse.
                                if char.isdigit():
                                    vrsNumb += char
                                else:
                                    vrsAlph += char

                            ref = ''.join([' ',
                                           bKeySpaced,
                                           ' ',
                                           cKey,
                                           ':',
                                           vrsNumb])
                            verses_out.append('\n'.join(['',
                                                         ref,
                                                         '',
                                                         vrsAlph]))
                    del vFound[0]

        if count == 0:
            self.statusUpdate(self.frame, ('%i VERSES CONTAINING %s'
                                           % (count, Srch.upper())))
        elif count == 1:
            self.statusUpdate(self.frame, ('%i VERSE CONTAINING %s'
                                           % (count, Srch.upper())))
        elif count > 1:
            self.statusUpdate(self.frame, ('%i VERSES CONTAINING %s'
                                           % (count, Srch.upper())))

        self.listUpdate(self, verses_out)
        self.frame.go_b.wait_variable(self.frame.var)

    def preamble():
        cross = '''\n\n
                   |        \\              /        |
                   |         \\     _      /         |
                   |              | |               |
                   |              | |               |
                   |         _____| |_____          |
                   |        |_____   _____|         |
                   |              | |               |
                   |              | |               |
                   |              | |               |
                   |              | |               |
                   |              | |               |
                   |              | |               |
                   |              |_|               |
                   |      _______/   \\_______       |\n\n
                '''

        version = '''______________________

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
                   |        \\              /        |
                   |         \\     _      /         |
                   |              | |               |
                   |              | |               |
                   |         _____| |_____          |
                   |        |_____   _____|         |
                   |              | |               |
                   |              | |               |
                   |              | |               |
                   |              | |               |
                   |              | |               |
                   |              | |               |
                   |              |_|               |
                   |      _______/   \\_______       |\n\n
                '''

        version = '''______________________\n

                       THE KING JAMES BIBLE
                      ______________________\n

                      Please rightly divide and handle with prayer. \n\n
                  '''

        return ''.join([cross, version])

    def makeBibDict(self):
        with open('.fileLocation.json', 'r+') as fileLoc:
            self.fileLocation = json.load(fileLoc)

        fileName = ''.join(['.ToC_', self.language, '.json'])
        with open(fileName, 'r+') as ToC:
            [self.bkNames, self.bkAbbrv] = json.load(ToC)

        fileBible = self.pathPart.join([self.fileLocation, 'BIBLE.txt'])
        # Imports full bible text and books as "bib".
        with open(fileBible, 'r+') as Bfile:
            bib = Bfile.read()

        n = len(self.bkNames)
        books = list()
        # Populate "books" to be placed
        for b in range(n):
            populated = re.split(self.bkNames[b], bib)[0]
            if b == 0:
                # Removes special case GENESIS title from text
                GEN = re.split(self.bkNames[b+1], bib)[0]
                books.append(GEN.replace(self.bkNames[b], '')[1:-1])

            elif b == 65:
                books.append(re.split(self.bkNames[b], bib)[1])

            elif populated:
                books.append(populated)

            bkToWipe = populated
            # Speeds up For loop and keeps books
            # from being populated with prior books.
            bkWiper = ''
            bib = bib.replace(bkToWipe, bkWiper)

        del bib
        self.BibDict = collections.OrderedDict()
        # Loops to populate the book structure.
        for b in range(n):
            # Chapters marked uniquely (":1 " = verse 1).
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
                        vv = (verses[v])[1:]
                    else:
                        # Other verses don't have the extra colon.
                        vv = verses[v]

                    # Newline whitespace strip.
                    chars = ' '.join([chr(k) for k in [10, 13, 10]])
                    verses[v] = re.split(chars, vv)[0]
                    # Strips out chapter numbers at the end of the verse.
                    if (verses[v])[-1].isnumeric():
                        verses[v] = (verses[v])[:-1]
                    # Strips out remaining whitespace.
                    elif self.ismember(chr(10), verses[v]):
                        for s in range(len(verses[v])):
                            char = (verses[v])[s]
                            # Replaces the void space
                            # produced by newline deletion
                            # with a space between words.
                            ischr10 = char is chr(10)
                            ischr13 = char is chr(13)
                            if ischr10 or ischr13:
                                verses[v].replace(char, chr(32))

                    # Deletes any redundant spaces produced by the void
                    # white space replacement.
                    tplSpace = chr(32) + chr(32) + chr(32)
                    dblSpace = chr(32) + chr(32)
                    snglSpace = chr(32)
                    vv = verses[v].replace(dblSpace, snglSpace)

                    # Trims off lead/trail whitespace.
                    # Structure field names cannot or
                    # should not start with numbers.
                    vvv = vv.replace(tplSpace, snglSpace)
                    verses[v] = vvv.strip()
                    vrsKey = str(v+1)
                    vrsDict[vrsKey] = verses[v]

                # Structure field names cannot or
                # should not start with numbers.
                # Dictionary field names cannot
                # contain spaces (I SAM is ISAM).
                chpKey = str(c+1)
                chpDict[chpKey] = vrsDict
            bkKey = (self.bkAbbrv[b]).replace(' ', '')
            self.BibDict[bkKey] = chpDict

        fileName = ''.join(['.BibDict_', self.language, '.json'])
        with open(fileName, 'w+') as bDict:
            json.dump(self.BibDict, bDict, ensure_ascii=True)

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
