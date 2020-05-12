#!/usr/bin/python3

import v1
from v1 import Bible


class Test:

    def test_makeBibDict(*kwargs):
        Bible.__init__(Bible, configfile='config_test.ini')
        d = Bible.BibDict
        assert len(d) == 67
        assert len(d['CONCORDANCE']) == 13664

    # If you experience weird search output, uncomment the following
    # test function and run "pytest" to confirm basic search parameters.
    '''
    def test_PhraseSearch(*kwargs):
        Bible.__init__(Bible, configfile='config_test.ini')
        Bible.frame.entry = 'rightly dividing'
        assert len(Bible.PhraseSearch(Bible)['phrases']) == 1
        v1.Bible.frame.entry = 'word'
        assert len(Bible.PhraseSearch(Bible)['phrases']) == 1581
        v1.Bible.frame.entry = 'of'
        assert len(Bible.PhraseSearch(Bible)['phrases']) == 18940
        v1.Bible.frame.entry = 'truth'
        assert len(Bible.PhraseSearch(Bible)['phrases']) == 224
    '''
