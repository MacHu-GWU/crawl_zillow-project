#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setting
from crawl_zillow.scheduler import StateScheduler

scheduler = StateScheduler()
input_data_queue = scheduler.get_todo(
    limit=3, get_html_kwargs={"cache_only": True})
scheduler.do(input_data_queue, multiprocess=False)
