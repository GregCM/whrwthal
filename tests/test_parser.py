#!/usr/bin/python

import unittest
import whrwthal
import re


class TestParser(unittest.TestCase):
    whrwthal.__init__(whrwthal)

    def test_phrase(self):
        search_tests = ['therefore', 'wherefore', 'therewith', 'wherewithal']
        for s, i in zip(search_tests, [1220, 344, 36, 2]):
            out, count, err = whrwthal.parser.phrase(whrwthal, s)
            self.assertEqual(count, i, msg='%s: Should be %i, Was %i'
                             % (s, i, count))
    

if __name__ == '__main__':
    unittest.main()
