#!/usr/bin/env python
# -*- coding: utf-8 -*-

from crawl_zillow.config import Config

Config.MongoDB.dbname = "crawl_zillow"
Config.MongoDB.host = "localhost"
Config.MongoDB.port = 27017
Config.MongoDB.username = None
Config.MongoDB.password = None

Config.Crawler.wait_time = 2.0
Config.Crawler.browser_prepare_time = 1.0
Config.Crawler.chrome_driver_executable = r"C:\Users\shu\Documents\chromedriver.exe"
