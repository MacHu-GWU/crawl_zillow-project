#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setting
from crawl_zillow.scheduler import CountyScheduler

scheduler = CountyScheduler()
input_data_queue = scheduler.get_todo(
    limit=2, get_html_kwargs={"zillow_only": True})
scheduler.do(input_data_queue, multiprocess=False, use_browser=True)
