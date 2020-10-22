'''
This file is a part of whrwthal.
whrwthal is an offline bible referencing module.
Copyright (C) 2020 Gregory Caceres-Munsell <gregcaceres@gmail.com>
'''

from configparser import ConfigParser
from functools import partial
import os
import signal
import time
import tkinter as tk
from tkinter import colorchooser, ttk, messagebox


class Reader():
    def __init__(self):
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
        self.enable_lfm.set(self.LFM)
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
        # self.frame.SearchFrame = tk.Frame(self.frame)
        # self.frame.SearchFrame.grid(row=3, column=1, sticky='ew')

        self.qvar = tk.IntVar()
        self.frame.var = tk.IntVar()
        self.frame.SearchBar = tk.Entry(self.frame)
        # Gridified in SearchFrame (alongside potential lead/trail regex)
        self.frame.SearchBar.grid(row=3, column=1, sticky='ew')
        slSB = partial(self.handler.select, self)
        self.frame.master.bind('<Control-l>', slSB)

        # Dropdown search options
        # FIXME: finish toggle button and frame placement / padding...
        # ... then more opts
        self.frame.drop_frame = tk.Frame(self.frame, relief='flat')
        ao_gridify = partial(self.handler.adv_opts, self,
                             frame=self.frame.drop_frame,
                             r=5, c=1, s='new')
        self.frame.drop_button = tk.Button(self.frame,
                                           relief='flat',
                                           text='Advanded Options ▼',
                                           command=ao_gridify)
        self.frame.drop_button.grid(row=4, column=1, sticky='ew')

        # Regular Expression Input:
        s = 'Use regular expressions'
        self.use_re = tk.BooleanVar()
        reg_pref = partial(self.handler.regex, self)
        self.frame.regex_check = tk.Checkbutton(self.frame.drop_frame,
                                                text=s,
                                                onvalue=1, offvalue=0,
                                                variable=self.use_re,
                                                command=reg_pref)
        self.frame.regex_check.pack(side='top', fill='both')

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
        self.textile.update(self, self.textile.preamble(), just='center')

        '''
        TOOL-TIPS
        self.frame.bind('<ButtonPress>', self.leave)
        # 3 second pause before tooltip appears
        self.waittime = 3000
        '''

        self.frame.Bpadding = tk.Label(self.frame, text='', relief='flat')
        self.frame.Bpadding.grid(row=14, column=0,
                                 columnspan=14, sticky='ew')

        # COLORS:
        self.frame.configure(bg=self.colors['frame'][0])
        self.frame.master.configure(bg=self.colors['master'][0])
        self.menubar.config(bg=self.colors['menubar'][0],
                            fg=self.colors['menubar'][1],
                            relief='flat')
        f = self.frame
        # Alias for line readability
        f.header.configure(bg=self.colors['header'][0],
                           fg=self.colors['header'][1],
                           font=(self.font,
                                 self.config_obj[
                                     'FONT'][
                                         'title']))
        f.status_bar.configure(bg=self.colors['header'][0],
                               fg=self.colors['header'][1],
                               font=(self.font,
                                     self.config_obj[
                                         'FONT'][
                                             'text']))
        f.text_widget.configure(bg=self.colors['text_widget'][0],
                                fg=self.colors['text_widget'][1])
        f.Bpadding.configure(bg=self.colors['frame'][0],
                             state='disabled')
        f.drop_button.configure(bg=self.colors['header'][0],
                                fg=self.colors['header'][1])
        f.drop_frame.configure(bg=self.colors['header'][0])
        f.regex_check.configure(bg=self.colors['header'][0],
                                fg=self.colors['header'][1])
        # f.SearchFrame.configure(bg=self.colors['header'][0])


def start(self, t=5.0):
    # A simple timed progress bar ~5.0 seconds
    branch = tk.Tk()
    branch.resizable(0, 0)
    branch.title('whrwthal')

    msg = 'Initializing...'
    info = tk.Label(branch, text=msg, relief='flat', font=('roman', 14))
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
    if (co['switch']) and (co['transient']):
        msg = '\n'.join(['Would you like to disable Low Footprint Mode?',
                         'You would enjoy shorter wait times,',
                         'but sacrifice more disk space.'])

        r = messagebox.askyesno(title='Low Footprint',
                                message=msg)
        if r:
            # LFM disabled, and will not be queried again,
            # except as a Checkbox under the Options menu
            self.config_obj['FOOTPRINT']['switch'] = ''
            self.config_obj['FOOTPRINT']['transient'] = ''

            os.remove('bytes')
            with open('src.txt', 'w') as f:
                f.write(self.text)

        else:
            # LFM remains on and shutdown won't query again
            self.config_obj['FOOTPRINT']['switch'] = 'true'
            self.config_obj['FOOTPRINT']['transient'] = ''

        with open('config.ini', 'w') as cfg:
            self.config_obj.write(cfg)

    # End Tk environment
    self.root.destroy()
    # Kill by Process ID and exit with a vengence
    pid = os.getpid()
    os.kill(pid, signal.SIGTERM)


def info(self):
    # TODO: the "about" text under the Help menu
    book =  "\n".join([r"    ,   ,",
                       r"   /////|",
                       r"  ///// |",
                       r" /////  |",
                       r"|~~~| | |",
                       r"|===| |/|",
                       r"| B |/| |",
                       r"| I | | |",
                       r"| B | | |",
                       r"| L |  / ",
                       r"| E | /  ",
                       r"|===|/   ",
                       r"'---'    "])

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

    m_entry = tk.Entry(m_frame, relief='sunken', font=('roman', 10))
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

    s_entry = tk.Entry(s_frame, relief='sunken', font=('roman', 10))
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

    or If entry contents reference a book, and chapter or verse:

        0:: "Rom 12:1" Returns Romans Chapter 12 verse 1.

    Else If certain entry contents reference a book and a word in text:

        1:: "romans" Returns the entire book of Romans and verses like "... if we being romans ..."

    Else If some entry contents reference a book, and some text:

        2:: "if we being romans" Returns the verse "... if we being romans ..."

    Else If entry contents only reference a number combination:

        3:: "23" Returns the 23rd chapter of every book (if such a chapter exists)
            "1:3" Returns the 3rd verse from the 1st chapter of every book (if such a verse exists)
            "1-3" Returns the 1st through 3rd verse (a subset) of every chapter of every book (if such a subset exists)

    Else:
        4:: "word" Returns every verse containing "word"
    '''
    self.frame.var.set(1)
    self.frame.entry = self.frame.SearchBar.get()

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
        d, pcount, perr = self.parser.phrase(self, self.frame.entry,
                                             self.use_re.get())
    elif (a and not(b)) or (a and c):
        print('get_input:: 1')
        d, vcount, verr = self.parser.verse(self, self.frame.entry)

    elif (a and b):
        print('get_input:: 2')
        d, vcount, verr = self.parser.verse(self, self.frame.entry)
        pd, pcount, perr = self.parser.phrase(self, self.frame.entry,
                                              self.use_re.get())
        # append pout to out as a combined dict
        for key in pd:
            d[key] = pd[key]

    elif (c and not(any([a, b]))):
        print('get_input:: 3')
        d, vcount, verr = self.parser.verse(self, self.frame.entry)

    elif ((a and b) and (con_count > ToC_count)) or (not(a) and b):
        print('get_input:: 4')
        d, pcount, perr = self.parser.phrase(self, self.frame.entry,
                                             self.use_re.get())

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
            h = [k for k in d.keys()][0]
            t = [v for v in d.values()][0]
            gui_update(self, status='{} RESULT MATCHING \"{}\"'.format(
                           count, self.frame.entry), head=h, text=t)
        elif count > 1:
            # OPINIONPOLL: what's a good header to
            # show while waiting for a selection?
            h = '...'
            gui_update(self, status='{} RESULTS MATCHING \"{}\"'.format(
                           count, self.frame.entry), head=h)

            # FIXME this frame sucks
            list_update(self, d)

    self.frame.go_b.wait_variable(self.frame.var)


def select(self, event=None):
    focus(self.frame.SearchBar)
    self.frame.SearchBar.select_range(0, 'end')
    self.frame.SearchBar.icursor('end')


def focus(self, event=None):
    self.focus_set()


def gui_update(self, **kwargs):
    '''
    Key-word arguments consist of 'status', 'head' and 'text'
    '''
    keys = kwargs.keys()
    values = kwargs.values()
    if 'status' in keys:
        status = kwargs['status']
        self.frame.status_bar.configure(text=status)
    if 'head' in keys:
        head = kwargs['head']
        self.frame.header.configure(text=head)
    if 'text' in keys:
        text = kwargs['text']
        self.textile.update(self, text)

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
        self.textile.clear(self.frame)
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
        bpress.append(partial(gui_update, self, head=key, text=d[key]))
        self.blist.append(tk.Button(c, text=key,
                                    width=w, height=h,
                                    command=bpress[-1]))
        lb = self.blist[-1]
        bwin.append(c.create_window((0, bheight),
                                    anchor='nw',
                                    width=w, height=h,
                                    window=lb))
        self.blist[-1].configure(font=('roman', 9),
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
