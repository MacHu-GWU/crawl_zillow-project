#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from pytest import raises, approx

from crawl_zillow.spider import get_html
from crawl_zillow.urlbuilder import urlbuilder
from crawl_zillow.htmlparser import htmlparser


class TestHtmlParser(object):
    def test_get_items(self):
        urls = [
            urlbuilder.browse_home_listpage_url(),
            urlbuilder.browse_home_listpage_url(state="ca"),
            urlbuilder.browse_home_listpage_url(
                state="ca", county="los-angeles-county"
            ),
            urlbuilder.browse_home_listpage_url(
                state="ca", county="los-angeles-county", zipcode="91001"
            ),
            urlbuilder.browse_home_listpage_url(
                state="ca", county="los-angeles-county", zipcode="91001",
                street="tola-ave_5038895"
            ),
        ]
        for url in urls:
            html = get_html(url)
            data = htmlparser.get_items(html)
            assert len(data[:3]) == 3


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
