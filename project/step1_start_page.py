#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setting
from crawl_zillow.urlbuilder import urlbuilder
from crawl_zillow.htmlparser import htmlparser
from crawl_zillow.spider import get_html
from crawl_zillow.model import State


def crawl():
    url = urlbuilder.browse_home_listpage_url()
    html = get_html(url)

    state_list = list()
    for href, name in htmlparser.get_items(html):
        if "district-of-columbia-county" not in href:
            state = State(href=href, state=name)
            state_list.append(state)

    # state_list = state_list[:2]  # COMMENT OUT IN PROD

    State.smart_insert(state_list)


if __name__ == "__main__":
    crawl()
