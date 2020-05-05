#!/usr/bin/python3

import v1
from v1 import Bible


class Test:

    def test_makeBibDict(*kwargs):
        Bible.__init__(Bible, configfile='config_test.ini')
        d = Bible.makeBibDict(Bible)
        assert len(d) == 67
        assert len(d['CONCORDANCE']) == 13664

    def test_PhraseSearch(*kwargs):
        Bible.frame.entry = 'rightly dividing'
        print(Bible.PhraseSearch(Bible))
        assert len(Bible.PhraseSearch(Bible)) == 1
        v1.Bible.frame.entry = 'of'
        assert len(Bible.PhraseSearch(Bible)) == 18906
        v1.Bible.frame.entry = 'truth'
        assert len(Bible.PhraseSearch(Bible)) == 222
