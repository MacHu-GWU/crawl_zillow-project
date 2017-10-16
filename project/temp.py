#!/usr/bin/env python
# -*- coding: utf-8 -*-


import setting
from crawl_zillow.db import (
    c_state, c_county, c_street, c_zipcode,
)
from crawl_zillow.model import State, County, Zipcode, Street
from crawl_zillow.spider import get_html

url = "https://www.zillow.com/browse/homes/ca/los-angeles-county/"
html = get_html(url, cache_only=True)

pattern = "was not found on this server."
print(pattern in html)

# c_state.update({}, {"$rename": {"finished": "status"}}, multi=True)
# print(c_state)
# for doc in c_state.find():
#     print(doc)
