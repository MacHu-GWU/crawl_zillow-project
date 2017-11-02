#!/usr/bin/env python
# -*- coding: utf-8 -*-

from crawl_zillow.config import Config

Config.MongoDB.dbname = "zillowdb"
Config.MongoDB.host = "ds121535.mlab.com"
Config.MongoDB.port = 21535
Config.MongoDB.username = "admin"
Config.MongoDB.password = "e0PQ09YdUWwo"

Config.Crawler.wait_time = 2.0
Config.Crawler.browser_prepare_time = 1.0
Config.Crawler.chrome_driver_executable = r"C:\Users\shu\Documents\chromedriver.exe"
