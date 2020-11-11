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
        book_tests = ['JOB', 'PROVERBS', 'PHILEMON']
        for b, i in zip(book_tests, [3445, 2932, 4248]):
            d, count = whrwthal.parser.find(whrwthal, b)
            self.assertEqual(i, len(d['%s 1' % (b)]),
                             msg='\n\n[%s] Expected length %i, got %i'
                             % (b, i, len(d['%s 1' % (b)])))

        chapter_tests = ['PSALMS 117', 'PSALMS 119', 'ROMANS 1']
        for c, i in zip(chapter_tests, [185, 14292, 4114]):
            d, count = whrwthal.parser.find(whrwthal, c)
            self.assertEqual(i, len(d[c]),
                             msg='\n\n[%s] Expected length %i, got %i'
                             % (c, i, len(d[c])))

        verse_tests = ['GENESIS 3:9', 'JOB 40:2', 'ROMANS 3:23',
                       'PHILEMON 1:3', 'REVELATION 22:21']
        for v, i in zip(verse_tests, [204, 154, 143, 153, 64]):
            d, count = whrwthal.parser.find(whrwthal, v)
            self.assertEqual(i, len(d[v]),
                             msg='\n\n[%s] Expected length %i, got %i'
                             % (v, i, len(d[v])))

        phrase_tests = ['therefore', 'wherefore', 'therewith', 'wherewithal']
        for s, i in zip(phrase_tests, [1220, 344, 36, 2]):
            d, count = whrwthal.parser.find(whrwthal, s)
            self.assertEqual(i, count,
                             msg='\n\n[%s] expected %i result(s), got %i'
                             % (s, i, count))

if __name__ == '__main__':
    unittest.main()
