#!/usr/bin/python

import unittest
import whrwthal


class TestParser(unittest.TestCase):
    '''
    Any changes made to parser.py are best evaulated by
    calling `python -m unittest tests/test_parser.py`

    If some result was other than expected, likely something
    having to do with regular expression matching was modified
    in any of phrase(), verse(), alpheval(), or numbeval();

    It may also indicate a change in the bible translation used.
    If this change is intentional, simply modify the
    numbers below to match your expected case.
    '''
    whrwthal.__init__(whrwthal)

    def test_find(self):
        phrase_tests = ['therefore', 'wherefore', 'therewith', 'wherewithal']
        for s, i in zip(phrase_tests, [1220, 344, 36, 2]):
            d, count = whrwthal.parser.find(whrwthal, s)
            self.assertEqual(count, i, msg='[%s] expected %i result(s), got %i'
                             % (s, i, count))

        chapter_tests = ['PSALM 117', 'PSALM 119', 'ROMANS 1']
        for c, i in zip(chapter_tests, [178, 14285, 4109]):
            d, count = whrwthal.parser.find(whrwthal, l)
            self.assertEqual(len(d[c]), i, msg='[%s] Expected length %i, got %i'
                             % (c, len(d[c]), i))


if __name__ == '__main__':
    unittest.main()
