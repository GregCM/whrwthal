'''
Blurses is a simple framework to make curses-based applications.
The original module may be found at

https://github.com/bajaco/Blurses

Copyright (c) 2020 bajaco
'''

import curses


class Window:
    
    def __init__(self,stdscr):
        curses.use_default_colors()
        curses.curs_set(0) 
        self.stdscr = stdscr
        self.bottom = stdscr.getmaxyx()[0]
        self.right = stdscr.getmaxyx()[1]
        self.top = 0
        self.left = 0
        self.width = self.right - self.left
        self.height = self.bottom - self.top

    def update(self):
        self.bottom = self.stdscr.getmaxyx()[0]
        self.right = self.stdscr.getmaxyx()[1]
        self.top = 0
        self.left = 0
        self.width = self.right - self.left
        self.height = self.bottom - self.top

    def pause(self): 
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()

    def resume(self):
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)
        
    def refresh(self):
        self.stdscr.refresh()
    
    def clear(self):
        self.stdscr.clear()

    def getch(self):
        return self.stdscr.getch()
    
    def getkey(self):
        return self.stdscr.getkey()

    def get_wch(self):
        return self.stdscr.get_wch()

    # Draw based on percentages from borders and centering
    def draw(self, lines, **kwargs):
        x = 0
        y = 0
        flines = []
        for line in lines:
            if isinstance(line, tuple):
                flines.append(line)
            else:
                flines.append((line, curses.A_NORMAL))

        lw = len(max(flines, key=lambda l: len(l[0]))[0])
        lh = len(flines)

        for key, value in kwargs.items():
            if key == 'vcenter' and value:
                y = int(round(self.height / 2))
                y = int(round(y - (len(flines)/2)))
            elif key == 'hcenter' and value:
                x = int(round(self.width / 2))
                x = int(round(x - (lw / 2)))
            elif key == 'top' and y == 0:
                y += int(round(value / 100 * self.height))
            elif key == 'bottom' and y == 0:
                y += self.height - int(round(value / 100 * self.height)) - lh
            elif key == 'left' and x == 0:
                x = int(round(value / 100 * self.width))
            elif key == 'right' and x == 0:
                x = self.width - int(round(value / 100 * self.width)) - lw - 1
        if self.width > lw and self.height > lh:
            for l in flines:
                self.stdscr.addstr(y, x, l[0], l[1])
                y += 1
    
    def wrap(self, text, width=100, **kwargs):
        mode = curses.A_NORMAL
        if isinstance(text, tuple):
            mode = text[1]
        max_width = int(round(width / 100 * self.width))
        words = text.split()
        lines = []
        line = ''
        for word in words:
            if word == 'SKIP':
                lines.append(line)
                line = ''
            else:
                if line == '':
                    line = word
                else:
                    line += ' ' + word
                    if len(line) > max_width - 1:
                        line = line[:- len(word) - 1]
                        lines.append((line,mode))
                        line = word
        lines.append((line, mode))
        self.draw(lines, **kwargs)

class Menu:
    def __init__(self):
        self.options = ['Exit']
        self.active = 1
    
    def __call__(self):
        lines = []
        for i, option in enumerate(self.options[1:]):
            mode = curses.A_NORMAL
            if i == self.active - 1:
                mode = curses.A_REVERSE
            lines.append((f'{i+1}. {option}', mode))
        return lines
        
    # Options
    def get_quit(self):
        return len(self.options) - 1

    def add(self, name):
        self.options.insert(-1, name)

    def input(self, key):
        if (key == curses.KEY_UP) or (key == ord('k')):
            if self.active - 1 >= 1:
                self.active -= 1
        elif (key == curses.KEY_DOWN) or (key == ord('j')):
            if self.active < len(self.options) - 1:
                self.active += 1
        elif key == curses.KEY_ENTER or key == 10: 
            return self.active
        elif key == ord('q'):
            # Quit
            return 3
        return 0
            
class Blurses:
    def __init__(self):
        self.menu = Menu()
        self.functions = []
        self.mode = 0
        self.state = None
    
    def bind(self, name, func):
        self.menu.add(name)
        self.functions.append(func)

    def run(self):
        while self.mode != self.menu.get_quit():
            curses.wrapper(self.main)
    
    def main(self, stdscr):
        func = self.functions[self.mode]
        window = Window(stdscr)
        res = func(window, self.menu, self.state)
        self.mode = res[0]
        self.state = res[1]
        
