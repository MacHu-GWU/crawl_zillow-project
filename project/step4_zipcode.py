#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setting
from crawl_zillow.scheduler import ZipcodeScheduler


scheduler = ZipcodeScheduler()
input_data_queue = scheduler.get_todo(
    limit=2, get_html_kwargs={"cache_only": False})
scheduler.do(input_data_queue, multiprocess=False)
