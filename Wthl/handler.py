from Wthl import handler, io, parser, textile
from ast import literal_eval
from configparser import ConfigParser
import collections
from dahuffman import HuffmanCodec
from functools import partial
import json
import os
import psutil
import time
import tkinter as tk
from tkinter import colorchooser, ttk, messagebox

def start(self, t=7.429434566786795):
    branch = tk.Tk()
    branch.resizable(0,0)
    branch.title('whrwthal')

    msg = 'Initializing...'
    info = tk.Label(branch, text=msg, relief='flat', font=('cambria',14))
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
    self.root.destroy()
    frame = tk.Frame(tk.Tk())
    frame.pack()

    co = self.config_obj['FOOTPRINT']
    if (co['switch']=='on') and (co['transient']=='true'):
        # INSERT: tk evalutation on checkbox
        r = messagebox.askyesno(title='Low Footprint', message='Would you like to disable Low Footprint Mode? You would enjoy shorter wait times, but sacrifice more disk space. See the README for details.')
        frame.destroy()
        if r:
            self.config_obj['FOOTPRINT']['switch'] = 'off'
            self.config_obj['FOOTPRINT']['transient'] = 'false'

            codec = HuffmanCodec.load('.codec')
            with open ('bytes', 'rb') as f:
                b = f.read()

            for f in ['bytes','.codec']:
                os.remove(f)

            with open('.dict.json', 'w') as f:
                json.dump(self.bible_dict, f)

        else:
            self.config_obj['FOOTPRINT']['transient'] = 'false'

        with open('config.ini', 'w') as cfg:
            self.config_obj.write(cfg)

    kill()

def kill():
    pn = 'main.py'
    for proc in psutil.process_iter():
        if proc.name() == pn:
            proc.kill()

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
    m_frame = tk.Frame(path_tab)
    m_frame.pack(fill='both', expand=1, side='top')

    m_choice = tk.Entry(m_frame, relief='sunken')
    m_choice.pack(padx=10, pady=5, fill='x', expand=1, side='left')
    m_choice.insert('end', config_obj['PATH']['main'])

    m_command = partial(io.browse, self, m_choice, 'main')
    m_browse = tk.Button(m_frame, text='Browse',
                         relief='raised', command=m_command)
    m_browse.pack(padx=10, pady=5, fill='x', expand=1, side='left')

    s_frame = tk.Frame(path_tab)
    s_frame.pack(fill='both', expand=1, side='bottom')

    s_choice = tk.Entry(s_frame, relief='sunken')
    s_choice.pack(padx=10, pady=5, fill='both', expand=1, side='left')
    s_choice.insert('end', config_obj['PATH']['save'])

    s_command = partial(io.browse, self, s_choice, 'save')
    s_browse = tk.Button(s_frame, text='Browse',
                         relief='raised', command=s_command)
    s_browse.pack(padx=10, pady=5, fill='both', expand=1, side='left')

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
    frame = tk.Frame(self.root)
    frame.grid(row=2, rowspan=10, column=8, sticky='ns')
    label = tk.Label(frame, text='ToC')
    if self.show_toc.get():
        label.pack()
    else:
        label.pack_forget()

def lfm_query(self):
    co = self.config_obj['FOOTPRINT']
    # INSERT: tk evalutation on checkbox instead of ^ "co"
    if self.enable_lfm.get():
        self.config_obj['FOOTPRINT']['switch'] = 'off'
        self.config_obj['FOOTPRINT']['transient'] = 'false'

        os.remove('.dict.json')

        codec = HuffmanCodec.from_data(str(self.bible_dict))
        b = codec.encode(str(self.bible_dict))
        with open ('bytes', 'wb') as f:
            f.write(b)
            codec.save('.codec')

    else:
        self.config_obj['FOOTPRINT']['switch'] = 'off'
        self.config_obj['FOOTPRINT']['transient'] = 'false'

        for f in ['bytes','.codec']:
            os.remove(f)

        with open('.bible_dict.json', 'w') as f:
            json.dump(self.bible_dict, f)

    with open('config.ini', 'w') as cfg:
        self.config_obj.write(cfg)


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


def get_input(self, event=None):
    self.frame.var.set(1)
    self.frame.entry = self.frame.SearchBar.get()
    gui_update(self.frame.header, self.frame.entry.upper())

    # Table of contents entry check, any full or abbreviated reference
    ToC = self.bkAbbrv + self.bkNames
    ToC = [C.upper() for C in ToC]
    unique_words = self.bible_dict['CONCORDANCE']
    # TODO: (1) Upper?
    unique_words = [w.upper() for w in unique_words]

    if self.frame.entry is not None:
        upper = self.frame.entry.upper()
        # There exists an entry "e" referencing the ToC if its uppercase
        # form appears as either an abbreviation or word: e = "ROM/ROMAN"
        ToC_entries = [e for e in upper.split() if e in ToC]
        ToC_count = len(ToC_entries)

        # TODO: (2) Case sensitive search options,
        # potentially supported by the several entries
        # contained in "unique_words".
        conc_entries = [W for W in unique_words if W in upper.split()]
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
        out['VR'], vcount = self.verse(self)
    # else if certain entry contents reference a book and a word in text
    # EX: "romans" --> ROMANS(book) && "... if we being romans ..."
    elif (a and b):
        print(2)
        out['VR'], vcount = parser.verse(self)
        out['PS'], pcount = parser.phrase(self)
    # else if some entry contents reference a book, and some text
    # EX: "if we being romans" --> "... if we being romans ..."
    elif ((a and b) and (con_count > ToC_count)) or (not(a) and b):
        print(3)
        out['PS'], pcount = parser.phrase(self)
    # else if entry contents only reference a number combo
    # EX: "23", "3:23", "119:8-9"
    elif (c and not(any([a, b]))):
        print(4)
        # TODO: (3) allow number searches
        # ie "23" --> GEN 23, EXO 23 ... ACT 23
        # && "1:3" --> GEN 1:3, EXO 1:3 ... ACT 1:3
        # && "1-3" --> GEN 1:1-3, 2:1-3 ... EXO 1:1-3, 2:1-3 ... etc.
        out, vcount = parser.verse(self)
        pass

    elif not(any([a, b, c])):
        out = {}
        print(5)
        messagebox.showerror('Error',
                             '"%s" not found.' % (self.frame.entry))

    count = vcount + pcount
    if count == 0:
        gui_update(self.frame.status_bar, '{} RESULTS MATCHING \"{}\"'.format(
                   count, self.frame.entry))
    elif count == 1:
        gui_update(self.frame.status_bar, '{} RESULT MATCHING \"{}\"'.format(
                   count, self.frame.entry))
    elif count > 1:
        gui_update(self.frame.status_bar, '{} RESULTS MATCHING \"{}\"'.format(
                   count, self.frame.entry))

    list_update(self, out)
    list_update(self, out)
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
        textile.cls(self.frame)
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
        # "x" will be list of length 1 for verse dict,
        # list of length == output for phrase dict.
        label = d[key]['label']
        x = [k for k in d[key].keys() if k != 'label'][0]
        for i in range(len(d[key][x])):
            b_press.append(partial(textile.update, self, d[key][x][i]))
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

    c.grid(row=5, column=1, rowspan=8, columnspan=1, sticky='nsew')
    c.update()

    self.sbar = ttk.Scrollbar(self.frame,
                              orient='vertical',
                              command=self.canvas.yview)
    self.sbar.grid(row=5, column=0,
                   rowspan=8, sticky='nes')
    self.sbar.update()

    c.config(yscrollcommand=self.sbar.set, scrollregion=c.bbox('all'))
    '''
    self.canvas.bind('<Enter>', self._bound_mouse_to_scrollbar)
    self.canvas.bind('<Leave>', self._unbound_mouse_to_scrollbar)
    '''

