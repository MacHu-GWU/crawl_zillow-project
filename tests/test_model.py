#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from pytest import raises, approx

from crawl_zillow import model


class TestState(object):
    def test_url_and_key(self):
        state = model.State(href="/browse/homes/ca/", state="California")
        assert state.url == "https://www.zillow.com/browse/homes/ca"
        assert state.key == "ca"


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
