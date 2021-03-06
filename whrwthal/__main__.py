#!/usr/bin/python

'''
This file is a part of whrwthal.
whrwthal is an offline bible referencing module.
Copyright (C) 2020 Gregory Caceres-Munsell <gregcaceres@gmail.com>

whrwthal is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

whrwthal is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with whrwthal.  If not, see <https://www.gnu.org/licenses/>.
'''

import tkinter as tk
import sys

import whrwthal
from whrwthal import tkhandler

# Interpreter refresh every 10 milisec.
sys.setswitchinterval(0.01)
# base
whrwthal.__init__(whrwthal)
# ui
tkhandler.Reader.__init__(whrwthal)
gsize = whrwthal.frame.grid_size()
for row in range(gsize[0]):
    tk.Grid.rowconfigure(whrwthal.frame, row, weight=1)
    for col in range(gsize[1]):
        tk.Grid.columnconfigure(whrwthal.frame, col, weight=1)
main = tk.mainloop()
