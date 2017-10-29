#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This is monkey patch to lively edit ``crawl_zillow.config.Config``.
"""

from crawl_zillow.config import Config

Config.MongoDB.dbname = "zillowdb"
Config.MongoDB.host = "ds121535.mlab.com"
Config.MongoDB.port = 21535
Config.MongoDB.username = "admin"
Config.MongoDB.password = "e0PQ09YdUWwo"
