#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Exceptions.
"""

from requests import Timeout as TimeoutError
try:
    from .spider import NotDownloadError
    from .htmlparser import SoupError, CaptchaError, WrongHtmlError, ParseError
except:
    from crawlib.spider import NotDownloadError
    from crawlib.htmlparser import SoupError, CaptchaError, WrongHtmlError, ParseError