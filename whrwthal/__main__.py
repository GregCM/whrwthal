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

import sys

import whrwthal
import handler

# Interpreter refresh every 10 milisec.
sys.setswitchinterval(0.01)
whrwthal.__init__(whrwthal)
handler.mainloop()
