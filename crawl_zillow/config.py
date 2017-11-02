#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Config(object):
    class MongoDB(object):
        dbname = None
        username = None
        password = None
        host = None
        port = None

    class Crawler(object):
        wait_time = 1.0
        browser_prepare_time = 10.0
        chrome_driver_executable = None
