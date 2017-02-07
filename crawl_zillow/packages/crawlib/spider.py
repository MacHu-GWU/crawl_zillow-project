#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import sys
import time
import requests

try:
    from urlparse import urlparse
except:
    from urllib.parse import urlparse

try:
    from .decoder import smart_decode
except:
    from crawlib.decoder import smart_decode


def get_domain_name(url):
    """Get root domain name of an url.

    For example: https://www.python.org/doc/ => www.python.org
    """
    parse_result = urlparse(url)
    domain_name = parse_result.netloc
    return domain_name


class NotDownloadError(Exception):

    """Error that an content of url are not successfully downloaded.
    """


class Spider(object):

    """A minimal spider class. Two useful method are provided:

    - :meth:`Spider.get_html`
    - :meth:`Spider.download`

    :param default_timeout: in any method making http request, if timeout 
      keyword is not explicitly given, then use default value.
    :param default_sleeptime: in any method making http request, sleep for 
      short period of time before making request.
    """

    def __init__(self, default_headers=None, default_timeout=None, default_sleeptime=0.0, ):
        self.default_headers = default_headers
        self.default_timeout = default_timeout
        self.default_sleeptime = default_sleeptime
        self.domain_encoding_table = dict()

    def i_am_browser(self):
        self.default_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, sdch",
            "Accept-Language": "en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4",
            "Content-Type": "text/html; charset=UTF-8",
            "Connection": "close",
            "Referer": None,
        }

    def get_binary(self, url, headers=None, timeout=None):
        """Get binary data of an url.
        """
        if headers is None:
            headers = self.default_headers
        if timeout is None:
            timeout = self.default_timeout
        time.sleep(self.default_sleeptime)

        # Exception may raises
        response = requests.get(url, headers=headers, timeout=timeout)
        binary = response.content
        return binary

    def get_html(self, url, headers=None, timeout=None, encoding=None, errors="strict"):
        """Get html source in text.

        :param url: url you want to crawl
        :param timeout: time out time in second
        :param encoding: if not given, the encoding will be auto-detected
        :param strict: options "ignore", "strict"; encoding error parameter
        """
        binary = self.get_binary(url, headers=headers, timeout=timeout)
        if encoding is None:
            domain_name = get_domain_name(url)
            if domain_name in self.domain_encoding_table:
                encoding = self.domain_encoding_table[domain_name]
                html = binary.decode(encoding, errors=errors)
            else:
                html, encoding, confidence = smart_decode(
                    binary, errors=errors)
                # cache domain name and encoding
                self.domain_encoding_table[domain_name] = encoding

        else:
            html = binary.decode(encoding, errors=errors)

        return html

    def download(self, url, dst, timeout=None,
                 minimal_size=-1, maximum_size=1024**3):
        """Download binary content to destination.

        :param url: binary content url
        :param dst: path to the 'save_as' file
        :param timeout: time out time in second
        :param minimal_size: default -1, if response content smaller than 
          minimal_size, then delete what just download.
        :param maximum_size: default 1GB, if response content greater than
          maximum_size, then delete what just download.
        """
        if not timeout:
            timeout = self.default_timeout
        time.sleep(self.default_sleeptime)

        response = requests.get(url, timeout=timeout, stream=True)
        chunk_size = 1024
        downloaded = 0
        with open(dst, "wb") as f:
            for chunk in response.iter_content(chunk_size):
                if not chunk:
                    break
                f.write(chunk)
                downloaded += chunk_size

        if downloaded < minimal_size or downloaded > maximum_size:
            try:
                os.remove(dst)
            except:
                pass
            raise NotDownloadError(url)

spider = Spider()

#--- Unittest ---


def test_get_domain_name():
    url = "https://www.python.org/doc/"
    assert get_domain_name(url) == "www.python.org"


def test_get_html():
    url = "https://www.python.org/"
    html = spider.get_html(url)
    sys.stderr.write(html)


def test_download():
    url = "http://www.planwallpaper.com/static/images/Nature-Wallpaper-29.jpg"
    dst = "image.jpg"
    spider.download(url, dst)


if __name__ == "__main__":
    test_get_domain_name()
    test_get_html()
    test_download()
