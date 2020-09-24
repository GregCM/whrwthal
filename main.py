#!/usr/bin/python3

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

import Wthl

# By convention, any method call of "self" will be self=Wthl
Wthl.__init__(Wthl)
gsize = Wthl.frame.grid_size()
for row in range(gsize[0]):
    Wthl.tk.Grid.rowconfigure(Wthl.frame, row, weight=1)
    for col in range(gsize[1]):
        Wthl.tk.Grid.columnconfigure(Wthl.frame, col, weight=1)
main = Wthl.tk.mainloop()
