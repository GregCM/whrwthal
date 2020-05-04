#!/usr/share/python3

import v1


class Test:

    def test_makeBibDict(*kwargs):
        v1.Bible.__init__(v1.Bible)
        d = v1.Bible.makeBibDict(v1.Bible)
        assert len(d) == 67
        assert len(d['CONCORDANCE']) == 13673

    '''
    def test_PhraseSearch(*kwargs):
        v1.Bible.frame.entry = 'rightly divide'
        print(v1.Bible.PhraseSearch(v1.Bible))
        assert len(v1.Bible.PhraseSearch(v1.Bible)) == 1
        v1.Bible.frame.entry = 'word'
        assert len(v1.Bible.PhraseSearch(v1.Bible)) == 673
        v1.Bible.frame.entry = 'of'
        assert len(v1.Bible.PhraseSearch(v1.Bible)) == 18123
        v1.Bible.frame.entry = 'truth'
        assert len(v1.Bible.PhraseSearch(v1.Bible)) == 222
    '''
