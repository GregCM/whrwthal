'''
This file is a part of whrwthal.
whrwthal is an offline bible referencing module.
Copyright (C) 2020 Gregory Caceres-Munsell <gregcaceres@gmail.com>
'''
from configparser import ConfigParser
from functools import partial
import re
import os
import signal
import sys
import time
import tkinter as tk
from tkinter import colorchooser, ttk, messagebox


class MouseHover(tk.Menu):

    def __init__(self, parent, text, command=None):
        self._com = command
        tk.Menu.__init__(self, parent, tearoff=0)
        if not isinstance(text, str):
            raise TypeError('Non-string type: ' + text.__class__.__name__)

        toktext = re.split('\n', text)
        for t in toktext:
            self.add_command(label=t)

        self._displayed = False
        self.master.bind("<Enter>", self._on_enter)
        self.master.bind("<Leave>", self._on_leave)

    def __del__(self):
        self.master.unbind("<Enter>")
        self.master.unbind("<Leave>")

    def _on_enter(self, event):
        if not self._displayed:
            self._displayed = True
            self.post(event.x_root, event.y_root)
        if self._com is not None:
            self.master.unbind_all("<Return>")
            self.master.bind_all("<Return>", self.Click)

    def _on_leave(self, event):
        if self._displayed:
            self._displayed = False
            self.unpost()
        if self._com is not None:
            self.unbind_all("<Return>")

    def click(self, event):
        self._com()


def start(self, t=7.429434566786795):
    # A simple timed progress bar out of ~7.4 seconds
    # (The average time clocked to perform the
    #  __init__ huffman decoding on my machine)
    branch = tk.Tk()
    branch.resizable(0, 0)
    branch.title('whrwthal')

    msg = 'Initializing...'
    info = tk.Label(branch, text=msg, relief='flat', font=('cambria', 14))
    progress = ttk.Progressbar(branch, orient='horizontal',
                               length=200, mode='determinate')
    info.pack(padx=10, pady=5)
    progress.pack(padx=10, pady=10)

    i = 0
    while i < t:
        progress['value'] = i / t * 100
        i += t / 200
        time.sleep(t / 200)
        branch.update()

    branch.destroy()


def _on_mousewheel(self, event):
    if (self.ispc or self.islinux):
        event.delta /= 120
    elif self.ismac:
        event.delta /= 1
    self.canvas.yview_scroll(-1*(event.delta), 'units')


def shutdown(self, event=None):
    # Exit protocol prior to the process kill at handler.kill()
    # TODO: include protocol other than LFM query?

    co = self.config_obj['FOOTPRINT']
    if (co['switch'] == 'on') and (co['transient'] == 'true'):
        msg = '\n'.join(['Would you like to disable Low Footprint Mode?',
                         'You would enjoy shorter wait times,',
                         'but sacrifice more disk space.'])

        r = messagebox.askyesno(title='Low Footprint',
                                message=msg)
        if r:
            # LFM disabled, and will not be queried again,
            # except as a Checkbox under the Options menu
            self.config_obj['FOOTPRINT']['switch'] = 'off'
            self.config_obj['FOOTPRINT']['transient'] = 'false'

            os.remove('bytes')
            with open('src.txt', 'w') as f:
                f.write(self.text)

        else:
            # LFM remains on and shutdown won't query again
            self.config_obj['FOOTPRINT']['switch'] = 'on'
            self.config_obj['FOOTPRINT']['transient'] = 'false'

        with open('config.ini', 'w') as cfg:
            self.config_obj.write(cfg)

    # End Tk environment
    self.root.destroy()
    # Kill by Process ID and exit with a vengence
    pid = os.getpid()
    os.kill(pid, signal.SIGTERM)


def info(self):
    # TODO: the "about" text under the Help menu
    return None


def settings(self):
    branch = tk.Toplevel()
    branch.attributes('-topmost', 'true')
    branch.title('Settings')
    # One third the size of the fullscreen main window
    w = self.frame.winfo_width() / 3
    h = self.frame.winfo_height() / 3
    branch.geometry('%dx%d+0+0' % (w, h))

    # Notebook lists Tabs within window.
    nb = ttk.Notebook(branch)
    nb.pack(fill='both', expand=1)

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
    # main path
    m_frame = tk.Frame(path_tab)
    m_frame.pack(fill='both', expand=1, side='top')

    m_label = tk.Label(m_frame, text='Main Path', relief='flat')
    m_label.grid(row=0, column=0, padx=6, sticky='sw')

    m_entry = tk.Entry(m_frame, relief='sunken', font=('courier', 10))
    m_entry.grid(row=1, column=0, columnspan=4, padx=5, ipadx=50,  sticky='w')
    m_entry.insert('end', config_obj['PATH']['main'])
    # TODO: bug-fix for enter-leave-enter-leave-etc... loop under mouse
    # self.m_hover = MouseHover(m_entry, m_entry.get())

    m_command = partial(self.io.browse, self, m_entry, 'main')
    m_browse = tk.Button(m_frame, text='Browse',
                         relief='groove', command=m_command)
    m_browse.grid(row=1, column=4, padx=5, sticky='w')

    # save path
    s_frame = tk.Frame(path_tab)
    s_frame.pack(fill='both', expand=1, side='top')

    s_label = tk.Label(s_frame, text='Save Path', relief='flat')
    s_label.grid(row=2, column=0, padx=5, sticky='sw')

    s_entry = tk.Entry(s_frame, relief='sunken', font=('courier', 10))
    s_entry.grid(row=3, column=0, columnspan=3, padx=5, ipadx=50, sticky='w')
    s_entry.insert('end', config_obj['PATH']['save'])
    # self.s_hover = MouseHover(s_entry, s_entry.get())

    s_command = partial(self.io.browse, self, s_entry, 'save')
    s_browse = tk.Button(s_frame, text='Browse',
                         relief='groove', command=s_command)
    s_browse.grid(row=3, column=4, padx=5, sticky='w')

    # TEXT TAB:
    x = ''
    print(x)

    # COLOR TAB:
    bg_label = tk.Label(color_tab, text='Background')
    fg_label = tk.Label(color_tab, text='Foreground')

    frame_color_label = tk.Label(color_tab, text='Main screen: ')
    gcf = partial(get_color, self, self.frame)
    fcb = tk.Button(color_tab,
                    relief='sunken',
                    bg=self.frame['bg'],
                    command=gcf)

    master_color_label = tk.Label(color_tab, text='Title Bar: ')
    gcm = partial(get_color, self, self.frame.master)
    mcb = tk.Button(color_tab,
                    relief='sunken',
                    bg=self.frame.master['bg'],
                    command=gcm)

    menubar_color_label = tk.Label(color_tab, text='Menu Bar: ')
    gcmb_bg = partial(get_color, self, self.menubar)
    mbcb_bg = tk.Button(color_tab,
                        relief='sunken',
                        bg=self.menubar['bg'],
                        command=gcmb_bg)

    gcmb_fg = partial(get_color, self, self.menubar, 'fg')
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


def toc_query(self):
    frame = tk.Frame(self.frame)
    frame.grid(row=2, rowspan=8, column=8, sticky='ns')
    i, j = 0, 0
    for book in self.bkNames:
        label = tk.Label(frame, text=book)
        if self.show_toc.get():
            label.grid(row=i, column=j)
        else:
            label.grid_forget(row=i, column=j)

        if i == 33:
            i, j = 0, 1
        else:
            i += 1


def lfm_query(self):
    # INSERT: tk evalutation on checkbox instead of ^ "co"
    if self.enable_lfm.get():
        self.config_obj['FOOTPRINT']['switch'] = 'on'
        self.config_obj['FOOTPRINT']['transient'] = 'false'
        self.io.encode_file(self)

    else:
        self.config_obj['FOOTPRINT']['switch'] = 'off'
        self.config_obj['FOOTPRINT']['transient'] = 'false'
        self.io.decode_file(self)

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


def adv_opts(self, frame, r, c, s):
    # A toggle grid/ungrid for extra options under Search Bar
    if frame.winfo_ismapped():
        frame.grid_remove()
    elif not(frame.winfo_ismapped()):
        frame.grid(row=r, column=c, sticky=s)


def regex(self):
    '''
    A method to place regular expression syntax around the Search Bar
    and enable the use of it in handler.get_in()
    '''
    if self.use_re.get():
        self.frame.leading = tk.Label(self.frame, text='r\'')
        self.frame.leading.grid(row=3, column=0, sticky='e')
        self.frame.leading.configure(bg=self.colors['header'][0],
                                     fg=self.colors['header'][1])
        self.frame.trailing = tk.Label(self.frame, text='\'')
        self.frame.trailing.grid(row=3, column=2, sticky='w')
        self.frame.trailing.configure(bg=self.colors['header'][0],
                                      fg=self.colors['header'][1])
    else:
        self.frame.leading.grid_remove()
        self.frame.trailing.grid_remove()
    # Consider regex preference housing in "config.ini"


def get_input(self, event=None):
    '''
    Takes input from tk.Entry(). Executes the following logic and returns a list and calls list_update to handle displaying results.

    If all entry contents reference a book, but none reference words / phrases:

        0:: "Genesis" Returns the entire book of Genesis

    or if entry contents reference a book, and chapter or verse:

        0:: "Rom 12:1" Returns Romans Chapter 12 verse 1.

    Else If certain entry contents reference a book and a word in text:

        1:: "romans" Returns the entire book of Romans and verses like "... if we being romans ..."

    Else If some entry contents reference a book, and some text:

        2:: "if we being romans" Returns the verse "... if we being romans ..."

    Else If entry contents only reference a number combination:

        4:: "23" Returns the 23rd chapter of every book (if such a chapter exists)
            "1:3" Returns the 3rd verse from the 1st chapter of every book (if such a verse exists)
            "1-3" Returns the 1st through 3rd verse (a subset) of every chapter of every book (if such a subset exists)
    '''
    self.frame.var.set(1)
    self.frame.entry = self.frame.SearchBar.get()
    gui_update(self.frame.header, self.frame.entry.upper())

    # Table of contents entry check, any full or abbreviated reference
    ToC = self.bkAbbrv + self.bkNames
    ToC = [C.upper() for C in ToC]

    # TODO: (1) Replace UPPER results with colorized text (tk attributes)?
    self.concordance = [w.upper() for w in self.concordance]

    if self.frame.entry is not None:
        upper = self.frame.entry.upper()
        # There exists an entry "e" referencing the ToC if its uppercase
        # form appears as either an abbreviation or word: e = "ROM/ROMAN"
        ToC_entries = [e for e in upper.split() if e in ToC]
        ToC_count = len(ToC_entries)

        conc_entries = [W for W in self.concordance if W in upper.split()]
        # SEE: "dispensation of"
        con_count = len(conc_entries)

        numeric_entries = [e for e in self.frame.entry if e.isnumeric()]
    else:
        ToC_entries = []
        ToC_count = len(ToC_entries)

        conc_entries = []
        con_count = len(conc_entries)

        numeric_entries = []

    u = self.use_re.get()
    a = any(ToC_entries)
    b = any(conc_entries)
    c = any(numeric_entries)

    vcount = pcount = 0
    # Soon to be redundant: SEE parser.phrase (lines -5:-1)
    perr, verr = None, None
    if u:
        print('get_input:: 0')
        # User specified regular expression search (phrases only)
        d, pcount, perr = self.parser.phrase(self)
    elif (a and not(b)) or (a and c):
        print('get_input:: 1')
        d, vcount, verr = self.parser.verse(self)

    elif (a and b):
        print('get_input:: 2')
        d, vcount, verr = self.parser.verse(self)
        pd, pcount, perr = self.parser.phrase(self)
        # append pout to out as a combined dict
        for key in pd:
            d[key] = pd[key]

    elif ((a and b) and (con_count > ToC_count)) or (not(a) and b):
        print('get_input:: 3')
        d, pcount, perr = self.parser.phrase(self)

    elif (c and not(any([a, b]))):
        print('get_input:: 4')
        d, vcount, verr = self.parser.verse(self)

    # Handling errors
    if perr is MemoryError:
        print('get_input ERROR:: 5')
        msg = '\n'.join(['There are too many results for "{}",',
                         'please be more specific.'])
        messagebox.showwarning('Overloaded Search', msg.format(self.frame.entry))

    elif not(any([u, a, b, c])):
        d = {}
        print('get_input ERROR:: 6')
        messagebox.showerror('Error',
                             '"{}" not found.'.format(self.frame.entry))
    else:
        count = vcount + pcount
        if count == 1:
            gui_update(self.frame.status_bar,
                       '{} RESULT MATCHING \"{}\"'.format(
                       count, self.frame.entry))
            text = [v for v in d.values()][0]
            self.textile.update(self, text)
        elif count > 1:
            gui_update(self.frame.status_bar,
                       '{} RESULTS MATCHING \"{}\"'.format(
                       count, self.frame.entry))

            # A patchy fix that amounts to awful dumb practice
            list_update(self, d)
            # FIXME I suck
            list_update(self, d)

    self.frame.go_b.wait_variable(self.frame.var)


def select(self, event=None):
    focus(self.frame.SearchBar)
    self.frame.SearchBar.select_range(0, 'end')
    self.frame.SearchBar.icursor('end')


def focus(self, event=None):
    self.focus_set()


def gui_update(self, status):
    self.configure(text=status)


def list_update(self, d, mode='w'):
    # Check that the list doesn't already exists...
    try:
        c = self.canvas
        for lb in self.blist:
            # ... if it does, destroy it.
            lb.destroy()
        c.destroy()
    except AttributeError:
        pass
    finally:
        # Ready a new list
        self.blist = []
        self.canvas = tk.Canvas(self.frame)
        c = self.canvas

    if mode == 'w':
        self.textile.cls(self.frame)
    elif mode == 'a':
        pass

    w = self.frame.SearchBar.winfo_width()
    h = self.frame.SearchBar.winfo_height() * 2

    # TODO: (1) Philemon must not return Philippians,
    # but PHM & PHIL must remain their respective abbreviations.
    # (2) Phrase labels should read -->
    # "... not TEMPT the ... ye TEMPTED him..." for DEUT 6:16, etc.
    bheight = 0
    bpress = []
    bwin = []
    for key in d:
        # Populating all the buttons, labeled as their verse reference
        # plus a few words around the searched-phrase (if applicable)
        bpress.append(partial(self.textile.update, self, d[key]))
        self.blist.append(tk.Button(c, text=key,
                                    width=w, height=h,
                                    command=bpress[-1]))
        lb = self.blist[-1]
        bwin.append(c.create_window((0, bheight),
                                    anchor='nw',
                                    width=w, height=h,
                                    window=lb))
        self.blist[-1].configure(font=('calibri', 9),
                                       activebackground='#D2D2D2')
        self.blist[-1].update()
        bheight += h

    # placing the canvas that will hold all the listed buttons / options
    c.grid(row=6, column=1, rowspan=8, columnspan=1, sticky='nsew')
    c.update()

    self.sbar = ttk.Scrollbar(self.frame,
                              orient='vertical',
                              command=self.canvas.yview)
    self.sbar.grid(row=6, column=0,
                   rowspan=8, sticky='nes')
    self.sbar.update()

    c.config(yscrollcommand=self.sbar.set, scrollregion=c.bbox('all'))
    # self.canvas.bind('<Enter>', self._bound_mouse_to_scrollbar)
    # self.canvas.bind('<Leave>', self._unbound_mouse_to_scrollbar)
