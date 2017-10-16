#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setting
from crawl_zillow.scheduler import CountyScheduler


scheduler = CountyScheduler()
input_data_queue = scheduler.get_todo(
    limit=3, get_html_kwargs={"cache_only": False})
scheduler.do(input_data_queue, multiprocess=False)
