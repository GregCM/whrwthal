#!/usr/bin/python

import unittest
import whrwthal


class TestParser(unittest.TestCase):
    whrwthal.__init__(whrwthal)

    def test_phrase(self):
        search_tests = ['therefore', 'wherefore', 'therewith', 'wherewithal']
        for s, i in zip(search_tests, [1220, 344, 36, 2]):
            out, count, err = whrwthal.parser.phrase(whrwthal, s)
            self.assertEqual(count, i, msg='[%s] Expected %i result(s), got %i'
                             % (s, i, count))

    def test_verse(self):
        count_tests = ['Gen 3', '1:3']
        for c, i in zip(count_tests, [1, 66]):
            out, count, err = whrwthal.parser.verse(whrwthal, c)
            self.assertEqual(count, i, msg='[%s] Expected %i result(s), got %i'
                             % (c, i, count))

        length_tests = ['PSALM 117', 'PSALM 119', 'ROMANS']
        for l, i in zip(length_tests, [178, 14285, 52422]):
            out, count, err = whrwthal.parser.verse(whrwthal, l)
            self.assertEqual(len(out[l]), i, msg='[%s] Expected length %i, got %i'
                             % (l, len(out[l]), i))


if __name__ == '__main__':
    unittest.main()
