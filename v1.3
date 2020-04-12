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

try:

    import bs4
    import collections
    import curses.ascii
    import datetime as dt
    from functools import partial
    import json
    import os
    import pandas
    import random as rnd
    import re
    import subprocess
    import sys
    import tkinter as tk
    from tkinter import filedialog
    import traceback
    import time
    import urllib


    class bible:

            def __init__(self):

                ##################
                ##              ##
                ## Initializing ##
                ##              ##
                ##################

                #Create & Configure root
                self.root = tk.Tk()
                tk.Grid.rowconfigure(self.root, 0, weight=1)
                tk.Grid.columnconfigure(self.root, 0, weight=1)

                #Create & Configure frame
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
                fileMenu.add_command(label='Save', accelerator='Ctrl+S', command=self.sv_Button)
                self.frame.master.bind('<Control-s>', self.sv_Button)

                optionsMenu.add_cascade(label='Color Preferences', command=self.getColor())
                self.frame.master.config(menu=menubar)

                self.w, self.h = self.frame.winfo_screenwidth(), self.frame.winfo_screenheight()
                self.frame.master.geometry('%dx%d+0+0' %(self.w, self.h))

                self.frame.entry = '...'                                         # For any entry field, ensures one time only call.
                self.getIN = partial(self.getInput, self)
                self.frame.master.bind('<Return>', self.getIN)

                self.qvar = tk.IntVar()
                self.frame.var = tk.IntVar()
                self.frame.SearchBar = tk.Entry(self.frame)
                self.frame.SearchBar.grid(row=2, column=1, sticky='ew')
                self.fc = partial(self.focus, self)
                self.frame.master.bind('<Control-l>', self.fc)

                self.getIN = partial(self.getInput, self)
                self.frame.go_b = tk.Button(self.frame, text='ENTER ↵', command=self.getIN, relief='flat')
                self.frame.go_b.grid(row=3, column=1, sticky='new')

                self.frame.listFrame = tk.Frame(self.frame)
                self.frame.listFrame.grid(row=4, column=1, rowspan=6, sticky='new')
                #FIXME
                #self.frame.listFrame.config(scrollregion=self.frame.bbox('all'))
                #self.lbox_h = (self.frame.listFrame.config()['height'][-1])
                #self.lbox_w = (self.frame.listFrame.config()['width'][-1])

                #self.frame.scrollbar = tk.Scrollbar(self.frame, orient='vertical')
                #self.frame.scrollbar.bind_all('<MouseWheel>', self._on_mousewheel)
                #self.frame.scrollbar.config(command=self.frame.listFrame.yview_scroll)

                #self.frame.listFrame = tk.Frame(self.frame.listFrame)
                #self.frame.listFrame.config(width=self.lbox_w, height=self.canvas_h)
                #self.frame_h= self.frame.listFrame.config()['height'][-1]
                #self.frame_w = self.frame.listFrame.config()['width'][-1]
                #self.frame.listFrame.create_window((4,4), window=self.frame.listFrame, anchor="nw", tags='self.frame.listFrame')

                ## Populated in listUpdate
                self.b_press = list()              # List of event handlers for button presses
                self.frame.listed_button = list()  # List of buttons to be pressed
                ##

                self.frame.statusBar = tk.Label(self.frame, text='Welcome!', relief='flat')
                self.frame.statusBar.grid(row=1, column=7, sticky='sew')

                self.frame.textWidget = tk.Text(self.frame, relief='sunken', wrap='word')
                self.frame.textWidget.grid(row=2, rowspan=10, column=7, sticky='nsew')
                self.cls(self.frame)

                self.textUpdate(self, self.miniPreamble())                      # Welcome message!

                #self.frame.master.bind('<Enter>', self.enter)
                #self.frame.master.bind('<Leave>', self.leave)
                #self.frame.master.bind('<ButtonPress>', self.leave)

                self.qt_Button = partial(self.close_window, self)
                self.frame.master.bind('<Control-q>', self.qt_Button)
                self.frame.quitButton = tk.Button(self.frame, text='Quit', command=self.qt_Button, relief='raised')
                self.frame.quitButton.grid(row=11, column=10, columnspan=2, sticky='sew')

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
                menubar.config(background='gray20', foreground='ghost white', relief='flat')
                self.frame.listFrame.configure(background='gray18', relief='sunken')
                self.frame.quitButton.configure(background='gray26', foreground='ghost white')
                self.frame.statusBar.configure(background='gray18', foreground='ghost white', font=('times', 25))
                self.frame.textWidget.configure(background='gray26', foreground='ghost white')#, font=(self.font, self.font_size))
                self.frame.Tpadding.configure(background='gray18', foreground='ghost white', state='disabled')
                self.frame.Bpadding.configure(background='gray18', foreground='ghost white', state='disabled')
                self.frame.Lpadding.configure(background='gray18', foreground='ghost white', state='disabled')
                self.frame.Rpadding.configure(background='gray18', foreground='ghost white', state='disabled')

                ispc = sys.platform.startswith('win')
                ismac = sys.platform.startswith('darwin')                                  # Platform name for Mac OS X.
                islinux = sys.platform.startswith('linux')

                if ispc:
                    self.pathPart = '\\'
                elif (ismac or islinux):
                    self.pathPart = '/'

                wd = os.getcwd()
                try:
                    with open('.fileLocation.json', 'r+') as fileLoc:
                        self.fileLocation = json.load(fileLoc)
                    os.chdir(self.fileLocation)
                except:
                    self.fileLocation = filedialog.askopenfilename(                  # Manual input required if searchpath isn't
                                        initialdir=self.pathPart,                    # already defined. This will then be saved for
                                        title="Select file",                         # next time and used as the working directory.
                                        filetypes=(("json file", "*.json"), ("all files", "*.*")))
                    os.chdir(self.fileLocation)                                      # This directory contains BIBLE.txt & the
                    with open('.fileLocation.json', 'w+') as fileLoc:                # the directory's name itself.
                        json.dump(self.fileLocation, fileLoc, ensure_ascii=True)

                try:
                    with open('.bibPreferences.json', 'r+') as Pref:
                        [self.language, self.font, self.font_size] = json.load(Pref)
                except:
                    self.language = 'en'; self.font = 'roman'; self.font_size = '12' # defaults
                    with open('.bibPreferences.json', 'w+') as Pref:
                        json.dump([self.language, self.font, self.font_size], Pref, ensure_ascii=True)

                    # FIXME {
                    #sett_root = tk.Tk()
                    #query_list = ['Language? [el/he/en/es]','Font?','Font Size?']
                    #self.pref_to_dump = []
                    #settings_list = []
                    #for q in query_list:
                    #    query = tk.Label(sett_root,text=q)
                    #    setting = tk.Entry(sett_root)
                    #    query.pack(), setting.pack()
                    #    settings_list.append(setting)


                    #gqi = partial(self.getQueryInput, settings_list, self)
                    #input_button = tk.Button(sett_root, text='ENTER ↵', command=gqi)
                    #input_button.pack()

                    #sett_root.destroy()
                    #with open('.bibPreferences.json', '+w') as Pref:
                    #    json.dump([self.language, self.font, self.font_size], Pref, ensure_ascii=True)
                    # FIXME }
                try:
                    fileName = ''.join(['.ToC_', self.language, '.json'])
                    with open(fileName, 'r+') as TableCont:                          # path for the full bible text.
                        [self.bkNames, self.bkAbbrv] = json.load(TableCont)
                except:
                    with open(fileName, 'r+') as TableCont:                         # Fall-back import Table of Contents
                        [self.bkNames, self.bkAbbrv] = json.load(TableCont)         # as "bkAbbrv" & "bkNames".
                                                                                    # (Instance variables based on "language")
                try:                                                                # Attempt to import bible dictionary
                    fileName = ''.join(['.BibDict_', self.language, '.json'])                   # as "BibDict".
                    with open(fileName, 'r+') as Bib:
                        self.BibDict = json.load(Bib, object_pairs_hook=collections.OrderedDict)
                except:                                                              # Make "BibDict" if it doesn't already exist,
                    self.BibDict = self.makeBibDict(self)                            # or isn't found in the specified searchpath

            def focus(self, event=None):
                self.frame.SearchBar.focus_set()
                self.select(self)

            def select(self, event=None):
                self.frame.SearchBar.select_range(0,'end')
                self.frame.SearchBar.icursor('end')

            def _on_mousewheel(self, event=None):
                self.frame.listFrame.yview_scroll(-1*(event.delta/120),'units')

            #def enter(self, event=None):
            #        self.schedule()

            #def leave(self, event=None):
            #        self.unschedule()
            #        self.hidetip()

            #def schedule(self):
            #    self.unschedule()
            #    self.id = self.widget.after(self.waittime, self.showtip)

            #def unschedule(self):
            #    ids = self.id
            #    self.id = None
            #    if ids:
            #        self.widget.after_cancel(ids)

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
                                 background="#ffffff", relief='solid',
                                 borderwidth=1, wraplength=self.wraplength)
                label.pack(ipadx=1)

            def hidetip(self):
                tw = self.tw
                self.tw = None
                if tw:
                    tw.destroy()

            def getColor():
                return
                #color = tk.tkColorChooser.askcolor()
                #print(color)

            def createToolTip(self, widget, text):
                self.showtip(self, widget, text)

            def close_window(self, event=None):
                self.root.destroy()

            def getInput(self, event=None):
                self.frame.var.set(1)
                self.frame.entry = self.frame.SearchBar.get()
                self.statusUpdate(self.frame, self.frame.entry)
                self.VerseRef(self)

            def getQueryInput(setting_list, self,event=None):
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
                    self.frame.listed_button.append(tk.Button(self.frame.listFrame,
                                        text=l[i][0:50], command=self.b_press[i]))
                    self.frame.listed_button[i].grid(row=i, column=0, sticky='ew')
                self.frame.scrollbar.grid(column=1, sticky='ns')
                lgsize = self.frame.listFrame.grid_size()
                for row in range(lgsize[0]):
                    tk.Grid.rowconfigure(self.frame.listFrame, row, weight=1)
                    for col in range(lgsize[1]):
                        tk.Grid.columnconfigure(self.frame.listFrame, col, weight=1)
                self.frame.listFrame.config(width=self.lbox_w, height=self.canvas_h)
                self.b_press,self.frame.listed_button = [],[]

            def calendarUpdate(self):
                url = 'https://www.blueletterbible.org/dailyreading/index.cfm'
                netloc = urllib.request.urlparse(url).netloc
                html = urllib.request.urlopen(url).read()
                soup = bs4.BeautifulSoup(html)
                pdfs = soup.find_all('span')
                links = [l.get('onclick') for l in pdfs]
                hrefs = [l for l in links if l != None]
                for r in range(len(hrefs)):
                    hrefs[r] = hrefs[r].split('=')[1].replace(';','').replace("'",'')
                    hrefs[r] = netloc + hrefs[r]

                #TODO HREFS TO PDFS
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
                    with open('%s.txt' %(log_time), 'w+') as saved:
                        saved.write(text)                                            #save file found and amended
                except:
                    self.saveas(self)                                                #save file not found, saveas
                finally:
                    os.chdir(wd)

            def saveas(self):
                text = self.frame.textWidget.get('1.0', 'end')
                fileName = filedialog.asksaveasfilename(
                            initialdir=self.pathPart, title="Save as",
                            filetypes=(("text file", "*.txt"), ("all files", "*.*")))
                with open(fileName, 'w+') as saved_as:
                    saved_as.write(text)
                self.save_directory = re.split('.', fileName)[0]
                os.chdir(self.fileLocation)
                with open('.save_directory.json', 'w+') as save_dir:
                    json.drump(self.save_directory, save_dir, ensure_ascii=True)

            ####################################
            ##                                ##
            ## For Searching Verse References ##
            ##                                ##
            ####################################

            # TODO: Hide files for closed country safety

            def VerseRef(self, toShow='None'):
                verses_out = list()                                                       # Initialize 'verses_out' for concatenation.
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
                    if char.isalpha():                                               # Saves the alphabetic part of location
                        locAlph += char
                    else:                                                            # Saves the numeric part of location
                        locNumb += char
                loc.append(locAlph)
                loc.append(locNumb.strip())                                          # Combine the alphabetic and numeric parts to loc
                location = ''.join(loc)
                n = len(self.bkNames)                                                # 66 books!
                book = ''                                                            # Book is empty by default, filled this loop:
                for b in range(n):                                                   # LOOP THROUGH BOOKS
                    LenAbb = len(self.bkAbbrv[b])                                    # Compare strings to see if input is in
                    inToC = (self.bkAbbrv[b].upper() == locAlph.upper()[0:LenAbb])   # Table of Contents (ignore case); accounts
                    if inToC:                                                        # for abbreviations of books.
                        book = self.bkAbbrv[b]
                        bkMark = self.bkNames[b]                                     # The following Marks for statusUpdate
                        status += bkMark
                        break
                    elif b == 65:
                        return self.PhraseSearch(self)
                    else:                                                            # Proceed to next book. If no match is
                        continue                                                     # found, 'book' would remain empty.
                if (len(loc) > 1):                                                   # parts (Lines 101-102 )...
                    chpRef = (loc[1])                                                # <- This IF catches an empty numeric part ---
                    if not chpRef:                                                   # 0 indicates that no Chapters were specified:
                        chpRef = '0'                                                 # The book will be the only output.
                                                                                     # <- ELSE catches the lack of numeric part ---
                else:
                    chpRef = '0'

                if not chpRef == '0':                                                # If there is a numeric part of 'loc',
                    loc = chpRef                                                     # it can be used as the chapter reference.
                    vrsRef = '0'
                    for char in loc:
                        if char == ':':                                              # If there is a colon, there is a verse ref.
                            loc = re.split(char, loc)
                            chpRef = loc[0]
                            vrsRef = loc[1]

                    severalVrs = False
                    for char in vrsRef:
                        if char == '-':                                              # If there's a dash, there are multiple verses.
                            severalVrs = True
                            vrsStart2Fin = re.split('-', vrsRef)
                            firstVerse = vrsStart2Fin[0]
                            lastVerse = vrsStart2Fin[1]
                            fV = int(firstVerse)
                            lV = int(lastVerse) + 1

                    if not severalVrs:
                        firstVerse = vrsRef
                        fV = int(firstVerse)
                        lV = 0

                if not location:
                    next
                elif location.upper() == 'ABOUT':
                        toShow = 'Long'
                        self.textUpdate(self, '\n'.join([
                                     ' _______________________________________________\n',

                                     ' This text-based app was written by Greg Caceres',
                                     ' It is free to use, access, or edit. It is open',
                                     ' source, free as in beer and speech. The King',
                                     ' James Bible has its publishing and usage rights',
                                     ' vested in the Crown within the UK. Everywhere',
                                     ' else it is in the public domain, and is free',
                                     ' to use, quote, or share without limit provided',
                                     ' no changes are made to the content therein.',
                                     ' For support, or if you have any questions',
                                     ' about the app\'s functionality, the content',
                                     ' of the word of God, or anything else related, ',
                                     ' contact at\n',
                                     ' gregcaceres@gmail.com',
                                     ' _______________________________________________']))
                elif location.upper() == 'OPTIONS':
                        toShow = 'None'
                        self.cls(self.frame)
                        ToC[0] = '_________________________'
                        ToC[1] = '                         '
                        ToC[2] = 'Table of Contents --- ToC'
                        ToC[3] = '_________________________'
                        ToC[4] = '                         '
                        for i in range(5, (n+4)):
                            ToC[i] = self.bkNames[i-4] + ' ... ' + self.bkAbbrv[i-4]

                        ToC[66+5] = self.bkNames[66] + ' ... ' + self.bkAbbrv[66]
                        self.textUpdate(self, ToC)
                elif location.upper() == 'HELP':
                        toShow = 'Long'

                verses_outFind = self.BibDict[book]                                  # according to input if it was found
                verses_out = list()                                                  # in the table of contents.

                ## If only book name is input, output whole book ##
                if chpRef is '0':
                    cKeyList = range(len(verses_outFind.keys()))
                    for cKey in cKeyList:                                            # Hone in on a chapter for the verse loop sake:
                        cKey = str(cKey+1)
                        cFind = verses_outFind[cKey]                                 # LOOP through verses keys
                        vKeyList = range(len(cFind.keys()))
                        verses_out_collect = ''
                        for vKey in vKeyList:                                        # and concatenate each verse-field's string.
                            vKey = str(vKey+1)
                            if vKey == '1':
                                cPrint = '\n\n Chapter %s \n\n' %(cKey)
                            else:
                                cPrint = '\n'

                            verses_out_collect += (cPrint + cFind[vKey])             # TODO: BASED ON LANGUAGE, PRINT BACKWARDS
                    verses_out.append(verses_out_collect)                            # <- Verses acquired!

                else:
                    cKey = chpRef
                    status += ' %s' %(cKey)
                    try:
                        cFind = verses_outFind[cKey]
                    except:
                        cMax = len(verses_outFind.keys())

                        ## Plural or not? ##
                        if cMax is 1:
                            noCRef = 'ortunetly, %s only has %i chapter' %(bkMark, cMax)
                        else:
                            noCRef = 'ortunetly, %s only has %i chapters' %(bkMark, cMax)
                        fortunate = rnd.randint(0, 1)
                        if fortunate:
                            noCRef = '\n F' + noCRef
                        else:
                            noCRef = '\n Unf' + noCRef

                        verses_out_list = [noCRef]

                    ## If only chapter is input, output whole chapter ##
                    if vrsRef is '0':
                        vKeyList = range(len(cFind.keys()))
                        verses_out_collect = ''
                        for vKey in vKeyList:                                        # LOOP through these verses, and
                            vKey = str(vKey+1)                                       # concatenate each verse-field's string.
                            verses_out_collect += '\n' + cFind[vKey]
                        verses_out.append(verses_out_collect)

                    ## Range of verses ##
                    elif severalVrs:
                        vMax = len(cFind.keys())
                        e_raised = False
                        for verseNum in range(fV, lV):
                            vKey = str(verseNum)
                            try:
                                verses_out.append('\n' + cFind[vKey])                # <- Verses acquired!
                            except:
                                e_raised = True
                            finally:
                                if e_raised:
                                    vEnd = vMax
                                else:
                                    vEnd = lV

                        status += ':%s-%s' %(str(fV), str(vEnd-1))

                    ## Just one verse ##
                    else:
                        vKey = vrsRef
                        status += ':%s' %(vKey)
                        try:
                            verses_out.append('\n' + cFind[vKey])                    # <- Verse acquired!
                        except:
                            vMax = len(cFind.keys())
                            noVRef = ('ortunetly, %s %s only has %i verses'
                                      %(bkMark, chpRef, vMax))
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

            ###########################
            ##                       ##
            ## For Searching Phrases ##
            ##                       ##
            ###########################

            def PhraseSearch(self, toShow='None'):
                verses_out = list()
                if not toShow == 'None':
                    self.textUpdate(self, self.miniPreamble())
                    self.frame.go_b.wait_variable(self.frame.var)
                else:
                    self.cls(self.frame)

                Srch = self.frame.entry
                sLine = '\n\n'
                addOns = ''
                m = re.compile('(?i)'+Srch)
                if Srch.isnumeric():
                    self.frame.entry.delete(0, 'end')
                    self.statusUpdate(self.frame, 'Non-numeric Input Please')
                    self.textUpdate(self, self.miniPreamble())


            #    try:
            #        cmd  = re.split(' ', Srch)[0]
            #        Srch = re.split(' ', Srch)[1:] #
            #        if   cmd.upper() == 'VB':
            #            addons = ''.join(['(?-i)', addons])
            #
            #        elif cmd.upper() == 'BW':
            #            addons = ''.join(['(\<)', addons])
            #
            #        elif cmd.upper() == 'MW':
            #            addons = ''.join(['(\>)', addons])
            #
            #        elif cmd.upper() == 'EW':
            #            addons = ''.join(['(\b)', addons])
            #
            #    except:
            #        continue

                #if Srch.upper() == 'ARBITRA':
                #    self.cls(self.frame)
                #    self.textUpdate(self,
                #                    '\n'.join(['',
                #                          ' By default, the search will return',
                #                          ' exact words and phrases. It is case-',
                #                          ' insensitive and inclusive.',
                #                          ' EX: \"hope\" will return \"Hopeful\".\n',

                #                          ' By default, whole phrases can only be searched',
                #                          ' in sequence (i.e. \"the God LORD\" will not',
                #                          ' return \"the God LORD\"... \"he lord go\" will).',

                #                          '\n For extra options, type the following',
                #                          ' in front of the the word or phrase.',
                #                          ' [Separate all options with a space]\n',

                #                          '   VB -- Verbose (Exactly as you type it)',
                #                          '   (i.e. \"VB hope\" will only return \"hope\", excluding \"Hope\", \"hopeful\", etc.)\n',

                #                          '   BW -- Beginning of a word',
                #                          '   (i.e. \"BW wh\" will return \"who\", \"where\", \"whence\", etc.)\n',

                #                          '   MW -- Middle of a word',
                #                          '   (i.e. \"MW id\" will return \"middle\", \"midst\", \"tide\", etc.)\n',

                #                          '   EW -- End of a word',
                #                          '   (i.e. \"EW el\" will return \"Michael\", \"Gabriel\", \"Abel\", etc.)\n']))

                #elif Srch.upper() == 'FINITO':
                #    exit()
                #elif Srch.upper() == 'REFERENCE':
                #    self.VerseRef('Long')
                count = 0
                verses = []
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
                                vFound.append(m.sub(Srch.upper(), vrsList[-1]))  # Precompiled - pattern.sub(replacement, str)

                        vLen = len(vFound)
                        count += vLen
                        if vLen > 0:
                            for v in range(vLen):
                                if not (vFound[v])[0].isnumeric():
                                    ref = ''.join([bKeySpaced, ' ', cKey, ':1 '])
                                    verses_out.append('\n '.join(['', ref, vFound[v]]))
                                else:
                                    vrsAlph, vrsNumb = '', ''
                                    for char in vFound[v]:
                                        if char.isdigit():                       # Saves the numeric part of the verse.
                                            vrsNumb += char
                                        else:
                                            vrsAlph += char

                                    ref = ''.join([' ', bKeySpaced, ' ', cKey, ':', vrsNumb])
                                    verses_out.append('\n'.join(['', ref, '', vrsAlph]))
                            del vFound[0]

                if count == 0:
                    self.statusUpdate(self.frame, '%i VERSES CONTAINING %s' %(count, Srch.upper()))
                elif count == 1:
                    self.statusUpdate(self.frame, '%i VERSE CONTAINING %s' %(count, Srch.upper()))
                elif count > 1:
                    self.statusUpdate(self.frame, '%i VERSES CONTAINING %s' %(count, Srch.upper()))

                self.listUpdate(self, verses_out)
                self.frame.go_b.wait_variable(self.frame.var)

            def preamble():
                cross = '\n'.join(['\n\n                 ',
                                    '    \\             /  ',
                                    '     \\     _     /   ',
                                    '          | |        ',
                                    '          | |        ',
                                    '     _____| |_____   ',
                                    '    |_____   _____|  ',
                                    '          | |        ',
                                    '          | |        ',
                                    '          | |        ',
                                    '          | |        ',
                                    '          | |        ',
                                    '          | |        ',
                                    '          |_|        ',
                                    '  _______/   \\_______\n\n'])

                version = '\n'.join([' ______________________\n',

                                     '  THE KING JAMES BIBLE   ',
                                     ' ______________________\n',

                                     ' Please rightly divide and handle with prayer. \n\n'])

                AppFormat = '\n'.join([' The format: \n\n When queried "Where To?", a good response would be one of the following...\n',

                                        ' To find a verse-to-verse passage -- "Book Chapter:Verse-Verse".',
                                        '         EX: "Romans 5:8-10"\n',

                                        ' To find only one verse -- "Book Chapter:Verse".',
                                        '         EX: "John 3:16"\n',
                                        ' To find full chapters -- "Book Chapter".',
                                        '         EX: "Psalm 119"\n',
                                        ' To find full books -- "Book".',
                                        '         EX: "Philemon"\n\n',
                                        ' ______________________________________________________________ \n',

                                        ' Type "Help" to display this page again.',
                                        ' Type "About" for information about the app.',
                                        ' Type "Options" for a list of recognized book names.',
                                        ' Type "Phrase" to switch over to phrase searching.',
                                        ' Type "Done" to finish searching and quit.\n'])

                return ''.join([cross, version, AppFormat])

            def miniPreamble():
                cross = '\n'.join(['\n                 ',
                                    '    \\             /  ',
                                    '     \\     _     /   ',
                                    '          | |        ',
                                    '          | |        ',
                                    '     _____| |_____   ',
                                    '    |_____   _____|  ',
                                    '          | |        ',
                                    '          | |        ',
                                    '          | |        ',
                                    '          | |        ',
                                    '          | |        ',
                                    '          | |        ',
                                    '          |_|        ',
                                    '  _______/   \\_______\n\n'])

                version = '\n'.join([' ______________________\n',

                                     '  THE KING JAMES BIBLE   ',
                                     ' ______________________\n',

                                     ' Please rightly divide and handle with prayer.\n'])

                return ''.join([cross, version])

            def makeBibDict(self):
                with open('.fileLocation.json', 'r+') as fileLoc:
                    self.fileLocation = json.load(fileLoc)

                fileName = ''.join(['.ToC_', self.language, '.json'])
                with open(fileName, 'r+') as ToC:
                    [self.bkNames, self.bkAbbrv] = json.load(ToC)

                fileBible = self.pathPart.join([self.fileLocation, 'BIBLE.txt'])
                with open(fileBible, 'r+') as Bfile:                             # Imports full bible text and
                    bib = Bfile.read()                                           # books as "bib".

                n = len(self.bkNames)
                books = list()
                for b in range(n):                                               # Populate "books" to be placed
                    populated = re.split(self.bkNames[b], bib)[0]
                    if b == 0:
                        GEN = re.split(bkNames[b+1], bib)[0]                     # Removes special case GENESIS title from text
                        books.append(GEN.replace(bkNames[b],'')[1:-1])

                    elif b == 65:
                        books.append(re.split(self.bkNames[b], bib)[1])

                    elif populated:
                        books.append(populated)

                    bkToWipe = populated
                    bkWiper = ''                                                 # Speeds up For loop and keeps books
                    bib = bib.replace(bkToWipe, bkWiper)                         # from being populated with prior books.

                del bib                                                          # Toss "bib", takes up memory.
                self.BibDict = collections.OrderedDict()
                for b in range(n):                                               # Loops to populate the book structure.
                    chapters = re.split(':1 ', books[b])[1:]                    # Chapters marked uniquely (":1 " = verse 1).
                    cLen = len(chapters)                                    # re.split()[0] is garbage... excluded by [1:]
                    chpDict = collections.OrderedDict()
                    for c in range(cLen):                                            # Loops to populate the chapter structure.
                        chapters[c] = ':1 ' + chapters[c]                          # Add the verse 1 marker again for verse indexing:
                        idx = chapters[c].find(':')                        # Indexes the places where verses MAY appear.
                        for x in [idx]:
                            if (chapters[c])[x+1].isnumeric():                       # Python counts from 0, Bible from 1 -> "c+1"
                                delim = str(c+1) + ':'                           # Only the numeral indexed places are retained
                                verses = re.split(delim, chapters[c])             # (i.e. "1:2" retained, "Behold: Stuff" is not).
                        vLen = len(verses)
                        vrsDict = collections.OrderedDict()
                        for v in range(vLen):                                        # Loops to populate the verse structure.
                            if v is 0:
                                vv = (verses[v])[1:]                           # Removes the extra colon left in each verse 1.
                            else:
                                vv = verses[v]                                 # Other verses don't have the extra colon.

                            chars = ' '.join([chr(k) for k in [10, 13, 10]])         # Newline whitespace strip.
                            verses[v] = re.split(chars, vv)[0]                       # --------------------------
                            if (verses[v])[-1].isnumeric():                          # Strips out chapter numbers
                                verses[v] = (verses[v])[:-1]                         # at the end of the verse.
                            elif self.ismember(chr(10), verses[v]):                  # --------------------
                                for s in range(len(verses[v])):                      # Strips out remaining
                                    char = (verses[v])[s]                            # whitespace.
                                    ischr10 = char is chr(10)
                                    ischr13 = char is chr(13)                        # Replaces the void space
                                    if ischr10 or ischr13:                           # produced by newline deletion
                                        verses[v].replace(char, chr(32))             # with a space between words.

                            tplSpace = chr(32) + chr(32) + chr(32)
                            dblSpace = chr(32) + chr(32)                             # Deletes any redundant spaces
                            snglSpace = chr(32)                                      # produced by the void white
                            vv = verses[v].replace(dblSpace, snglSpace)              # space replacement.

                            vvv = vv.replace(tplSpace, snglSpace)
                            verses[v] = vvv.strip()                                  # Trims off lead/trail whitespace.
                            vrsKey = str(v+1)                                        # Structure field names cannot or
                            vrsDict[vrsKey] = verses[v]                              # should not start with numbers.

                        chpKey = str(c+1)                                            # Structure field names cannot or
                        chpDict[chpKey] = vrsDict                                    # should not start with numbers.
                    bkKey = (self.bkAbbrv[b]).replace(' ', '')                       # Dictionary field names cannot
                    self.BibDict[bkKey] = chpDict                                    # contain spaces (I SAM is ISAM).

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
        bible.__init__(bible)
        gsize = bible.frame.grid_size()
        for row in range(gsize[0]):
            tk.Grid.rowconfigure(bible.frame, row, weight=1)
            for col in range(gsize[1]):
                tk.Grid.columnconfigure(bible.frame, col, weight=1)
        main = tk.mainloop()

    with open('log', '+w') as elog:
        log_time = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        elog.write(log_time + ' -- Executed without error\n')

except:
    eror = traceback.format_exc()
    with open('log', '+w') as elog:
        log_time = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        elog.write(log_time + '\n' + error)

