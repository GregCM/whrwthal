#!/usr/share/python3

import v1

class Test:
    def test_makeBibDict(*kwargs):
        v1.Bible.__init__(v1.Bible)
        d = v1.Bible.makeBibDict(v1.Bible)
        assert len(d) == 67
        assert len(d['CONCORDANCE']) == 13673
