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

from whrwthal import io, textile


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
        # ===============================================
        # MENU
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
        self.frame.master.bind(self.key['save'], self.sv_button)
        file_menu.add_command(label='Save',
                              accelerator='Ctrl+S',
                              command=self.sv_button,
                              underline=0)
        self.svas_button = partial(self.io.saveas, self)
        self.frame.master.bind(self.key['saveas'], self.svas_button)
        file_menu.add_command(label='SaveAs',
                              accelerator='Ctrl+Shift+S',
                              command=self.svas_button,
                              underline=0)
        qt_Button = partial(shutdown, self)
        self.frame.master.bind(self.key['quit'], qt_Button)
        file_menu.add_command(label='Quit',
                              accelerator='Ctrl+Q',
                              command=qt_Button,
                              underline=0)
        # Options menu choices:
        sett = partial(settings, self)
        options_menu.add_command(label='Settings',
                                 command=sett,
                                 underline=0)
        self.show_toc = tk.BooleanVar()
        tocq = partial(toc_query, self)
        options_menu.add_checkbutton(label='Display Table of Contents',
                                     onvalue=1, offvalue=0,
                                     variable=self.show_toc,
                                     command=tocq,
                                     underline=8)
        self.enable_lfm = tk.BooleanVar()
        self.enable_lfm.set(self.LFM)
        lfmq = partial(lfm_query, self)
        options_menu.add_checkbutton(label='Low Footprint Mode',
                                     onvalue=1, offvalue=0,
                                     variable=self.enable_lfm,
                                     command=lfmq,
                                     underline=0)
        # Help menu choices:
        about_submenu = tk.Menu(help_menu, tearoff=0)
        help_menu.add_cascade(label='About',
                              menu=about_submenu,
                              underline=0)

        # about whrwthal
        w_about = partial(textile.update, self,
                          textile.about('Whrwthal'), just='center')
        about_submenu.add_command(label='Whrwthal', command=w_about,
                                  underline=0)
        # about license
        l_about = partial(textile.update, self,
                          textile.about('License'), just='left')
        about_submenu.add_command(label='License', command=l_about,
                                  underline=0)
        # about security
        s_about = partial(textile.update, self,
                          textile.about('Security'), just='left')
        about_submenu.add_command(label='Security', command=s_about,
                                  underline=0)

        # keybinds
        kb = partial(textile.update, self,
                     textile.keybinds(self), just='right')
        help_menu.add_command(label='Keybindings',
                              command=kb,
                              underline=0)
        # ===============================================
        # MAIN LAYOUT
        # Status Bar
        self.frame.status_bar = tk.Label(self.frame,
                                         text='Awaiting input...',
                                         relief='flat',
                                         name='status_bar')
        self.frame.status_bar.grid(row=2, column=1, padx=5, pady=5, sticky='s')

        self.qvar = tk.IntVar()
        self.frame.var = tk.IntVar()
        self.frame.SearchBar = tk.Entry(self.frame)
        # Gridified in SearchFrame (alongside potential lead/trail regex)
        self.frame.SearchBar.grid(row=3, column=1, padx=5, pady=5, sticky='ew')
        selsbar = partial(select, self)
        self.frame.master.bind(self.key['select_search'], selsbar)

        # Dropdown search options
        self.frame.drop_frame = tk.Frame(self.frame, relief='flat')
        # TODO: more opts
        ao_gridify = partial(adv_opts, self,
                             frame=self.frame.drop_frame,
                             r=5, c=1, s='new')
        self.frame.drop_button = tk.Button(self.frame,
                                           relief='flat',
                                           text='Advanded Options ▼',
                                           command=ao_gridify)
        self.frame.drop_button.grid(row=4, column=1, padx=5,
                                    pady=5, sticky='sew')

        # Regular Expression Input:
        s = 'Use regular expressions'
        self.use_re = tk.BooleanVar()
        self.frame.regex_check = tk.Checkbutton(self.frame.drop_frame,
                                                text=s,
                                                onvalue=1, offvalue=0,
                                                variable=self.use_re)
        self.frame.regex_check.pack(side='top', fill='both')

        # For any entry field, ensures one time only call.
        self.frame.entry = 'Search'
        self.frame.SearchBar.insert('end', self.frame.entry)

        get = partial(get_input, self)
        self.frame.master.bind('<Return>', get)
        self.frame.go_b = tk.Button(self.frame,
                                    text='ENTER',
                                    command=get,
                                    relief='raised')
        self.frame.go_b.grid(row=4, column=1, padx=5, pady=5, sticky='new')
        self.frame.header = tk.Label(self.frame,
                                     text='Welcome!',
                                     relief='flat',
                                     name='header')
        self.frame.header.grid(row=1, column=7, pady=5, sticky='sew')

        self.frame.text_widget = tk.Text(self.frame,
                                         relief='sunken',
                                         wrap='word',
                                         name='text_widget')
        self.frame.text_widget.grid(row=2,
                                    rowspan=10,
                                    column=7,
                                    padx=5, pady=10,
                                    sticky='nsew')
        # ===============================================
        # Welcome message!
        self.textile.update(self, self.textile.preamble(), just='center')
        '''
        TOOL-TIPS
        self.frame.bind('<ButtonPress>', self.leave)
        # 3 second pause before tooltip appears
        self.waittime = 3000
        '''
        # ===============================================
        # NAVIGATION:
        navs = tk.Frame(self.frame)
        navs.grid(row=12, column=7, padx=5, pady=0, sticky='new')
        # Up
        pageup = partial(self.parser.navigate, self, -1)
        self.frame.master.bind(self.key['pageup'], pageup)
        nl = tk.Button(navs, text='▲',
                       command=pageup,
                       relief='raised')
        nl.grid(row=0, column=0, sticky='nw')
        # Down
        pagedown = partial(self.parser.navigate, self, 1)
        self.frame.master.bind(self.key['pagedown'], pagedown)
        nr = tk.Button(navs, text='▼',
                       command=pagedown,
                       relief='raised')
        nr.grid(row=0, column=1, sticky='ne')
        # ===============================================
        # COLORS:
        self.frame.configure(bg=self.colors['frame'][0])
        self.frame.master.configure(bg=self.colors['master'][0])
        self.menubar.config(bg=self.colors['menubar'][0],
                            fg=self.colors['menubar'][1],
                            relief='flat')
        f = self.frame
        f.header.configure(bg=self.colors['header'][0],
                           fg=self.colors['header'][1],
                           font=(self.font,
                                 self.config_obj[
                                     'FONT'][
                                         'title']))
        f.status_bar.configure(bg=self.colors['header'][0],
                               fg=self.colors['header'][1],
                               font=(self.font,
                                     self.config_obj['FONT']['text']))
        f.text_widget.configure(bg=self.colors['text_widget'][0],
                                fg=self.colors['text_widget'][1])
        f.drop_button.configure(bg=self.colors['header'][0],
                                fg=self.colors['header'][1])
        f.drop_frame.configure(bg=self.colors['header'][0])
        f.regex_check.configure(bg=self.colors['header'][0],
                                fg=self.colors['header'][1])
        navs.configure(bg=self.colors['header'][0])
        nl.configure(bg=self.colors['header'][0],
                     fg=self.colors['header'][1])
        nr.configure(bg=self.colors['header'][0],
                     fg=self.colors['header'][1])
        # ===============================================


def start(self, t=5.0):
    # A simple timed progress bar ~5.0 seconds
    branch = tk.Tk()
    branch.resizable(0, 0)
    branch.title('whrwthal')

    msg = 'Initializing...'
    label = tk.Label(branch, text=msg, relief='flat', font=('roman', 14))
    progress = ttk.Progressbar(branch, orient='horizontal',
                               length=200, mode='determinate')
    label.pack(padx=10, pady=5)
    progress.pack(padx=10, pady=10)

    i = 0
    while i < t:
        progress['value'] = i / t * 100
        i += t / 200
        time.sleep(t / 200)
        branch.update()

    branch.destroy()


def focus(self, event=None):
    self.focus_set()


def _on_mousewheel(self, event):
    if (sys.platform.startswith('win') or sys.platform.startswith('linux')):
        event.delta /= 120
    elif sys.platform.startswith('darwin'):
        event.delta /= 1
    self.canvas.yview_scroll(-1*(event.delta), 'units')


def shutdown(self, event=None):
    # Exit protocol prior to the process kill at tktkhandler.kill()
    # TODO: include protocol other than LFM query?
    co = self.config_obj['LOWFOOTPRINT']
    if (co['switch']) and (co['transient']):
        msg = '\n'.join(['Would you like to disable Low Footprint Mode?',
                         'You would enjoy shorter wait times,',
                         'but sacrifice more disk space.'])

        r = messagebox.askyesno(title='Low Footprint',
                                message=msg)
        if r:
            # LFM disabled, and will not be queried again,
            # except as a Checkbox under the Options menu
            self.config_obj['LOWFOOTPRINT']['switch'] = ''
            self.config_obj['LOWFOOTPRINT']['transient'] = ''

            os.remove('bytes')
            with open('src.txt', 'w') as f:
                f.write(self.text)

        else:
            # LFM remains on and shutdown won't query again
            self.config_obj['LOWFOOTPRINT']['switch'] = 'true'
            self.config_obj['LOWFOOTPRINT']['transient'] = ''

        with open('config.ini', 'w') as cfg:
            self.config_obj.write(cfg)

    # End Tk environment
    self.root.destroy()
    # Kill by Process ID and exit with a vengence
    pid = os.getpid()
    os.kill(pid, signal.SIGTERM)


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
    tocframe = tk.Frame(self.frame)
    tocframe.grid(row=2, rowspan=8, column=8, sticky='w',
                  padx=5, pady=5, ipadx=2)
    tocframe.configure(bg=self.colors['header'][0])
    i, j = 0, 0
    for book, bk in zip(self.bkNames, self.bkAbbrv):
        label = tk.Label(tocframe, text='%s (%s)' % (book, bk))
        if self.show_toc.get():
            label.grid(row=i, column=j, sticky='nw')
            label.configure(bg=self.colors['header'][0],
                            fg=self.colors['header'][1])
        else:
            label.grid_forget()

        if i == 32:
            i, j = 0, 1
        else:
            i += 1


def lfm_query(self):
    # INSERT: tk evalutation on checkbox instead of ^ "co"
    if self.enable_lfm.get():
        self.config_obj['LOWFOOTPRINT']['switch'] = 'on'
        self.config_obj['LOWFOOTPRINT']['transient'] = 'false'
        self.io.encode_file(self)

    else:
        self.config_obj['LOWFOOTPRINT']['switch'] = 'off'
        self.config_obj['LOWFOOTPRINT']['transient'] = 'false'
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
        frame.grid(row=r, column=c, padx=5, pady=5, sticky=s)


def select(self, event=None):
    focus(self.frame.SearchBar)
    self.frame.SearchBar.select_range(0, 'end')
    self.frame.SearchBar.icursor('end')


def get_input(self, event=None):
    '''
    Takes input from tk.Entry() and returns a list with matches,
    calls list_update() to handle displaying the results.
    '''
    self.frame.var.set(1)
    try:
        self.use_re = self.use_re.get()
    except AttributeError:
        pass
    srch = self.frame.SearchBar.get()
    try:
        d, count = self.parser.find(self, srch)
    # Handling errors
    except MemoryError:
        msg = '\n'.join(['There are too many results for "{}",',
                         'please be more specific.'])
        messagebox.showwarning('Overloaded Search',
                               msg.format(self.frame.entry))
        count = 0
    except KeyError:
        messagebox.showerror('Error',
                             '\"{}\" not found.'.format(self.frame.entry))
        d = {}
        count = 0

    list_destroy(self)
    if count == 1:
        h = [k for k in d.keys()][0]
        t = [v for v in d.values()][0]
        gui_update(self, status='{} RESULT MATCHING \"{}\"'.format(
                       count, self.frame.entry), head=h, text=t)
    elif count > 1:
        h = 'Awaiting selection...'
        gui_update(self, status='{} RESULTS MATCHING \"{}\"'.format(
                       count, self.frame.entry), head=h)
        # FIXME this list frame sucks
        list_update(self, d)
    self.frame.go_b.wait_variable(self.frame.var)


def gui_update(self, **kwargs):
    '''
    Key-word arguments consist of 'status', 'head' and 'text'
    '''
    keys = kwargs.keys()
    if 'status' in keys:
        status = kwargs['status']
        self.frame.status_bar.configure(text=status)
    if 'head' in keys:
        head = kwargs['head']
        self.frame.header.configure(text=head)
    if 'text' in keys:
        text = kwargs['text']
        if 'just' in keys:
            just = kwargs['just']
            self.textile.update(self, text, just)
        else:
            self.textile.update(self, text)


def list_destroy(self):
    # Check that the list doesn't already exists...
    try:
        c = self.canvas
        for lb in self.blist:
            # ... if it does, destroy it.
            lb.destroy()
        c.destroy()
    except AttributeError:
        pass


def list_update(self, d, mode='w'):
    # Ready a new list
    self.blist = []
    append_bl = self.blist.append
    cframe = tk.Frame(self.frame)
    cframe.grid(row=6, column=1, padx=5, pady=5)
    c = tk.Canvas(cframe)

    if mode == 'w':
        self.textile.clear(self.frame)
    elif mode == 'a':
        pass

    w = self.frame.go_b.winfo_width()
    h = round(self.frame.go_b.winfo_height() * 1.25)

    # TODO: (1) Philemon must not return Philippians,
    # but PHM & PHIL must remain their respective abbreviations.
    # (2) Phrase labels should read -->
    # "... not TEMPT the ... ye TEMPTED him..." for DEUT 6:16, etc.
    bheight = 0
    bpress = []
    bwin = []
    append_bp = bpress.append
    append_bw = bwin.append
    for key in d:
        # Populating all the buttons, labeled as their verse reference
        # plus a few words around the searched-phrase (if applicable)
        append_bp(partial(gui_update, self, head=key, text=d[key]))
        append_bl(tk.Button(c, text=key,
                            width=w, height=h,
                            command=bpress[-1]))
        append_bw(c.create_window((0, bheight),
                                  anchor='nw',
                                  width=w, height=h,
                                  window=self.blist[-1]))
        self.blist[-1].configure(font=('roman', 9),
                                 activebackground='#D2D2D2')
        bheight += h
    self.sbar = ttk.Scrollbar(cframe,
                              orient='vertical',
                              command=c.yview)
    self.sbar.grid(row=0, column=0, sticky='ns')
    self.sbar.update()

    # placing the canvas that will hold all the listed buttons / options
    c.grid(row=0, column=1, sticky='ns')
    c.config(yscrollcommand=self.sbar.set, scrollregion=c.bbox('all'))
    c.update()
    # self.canvas.bind('<Enter>', self._bound_mouse_to_scrollbar)
    # self.canvas.bind('<Leave>', self._unbound_mouse_to_scrollbar)
