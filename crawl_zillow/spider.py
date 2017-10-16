#!/usr/bin/env python
# -*- coding: utf-8 -*-

from crawlib import (
    requests_spider as spider,
    Headers,
)

prefix = "http://webcache.googleusercontent.com/search?q=cache:"


def get_html(url,
             headers=None,
             timeout=None,
             errors="strict",
             wait_time=None,
             cache_only=False,
             **kwargs):
    """
    Use Google Cached Url.

    :param cache_only: if True, then real zillow site will never be used.
    """
    cache_url = prefix + url
    if headers is None:
        headers = {
            Headers.UserAgent.KEY: Headers.UserAgent.chrome,
            Headers.Referer.KEY: "http://cachedview.com/",
        }
    html = spider.get_html(
        cache_url, headers=headers, timeout=timeout,
        encoding="utf-8", errors=errors, wait_time=wait_time,
        **kwargs)

    if cache_only:
        return html

    # not available in google cache
    # crawl real zillow site, with wait_time 1.0
    if "was not found on this server." in html:
        referer_url = "/".join(url.split("/")[:-1])
        headers = {
            Headers.UserAgent.KEY: Headers.UserAgent.chrome,
            Headers.Referer.KEY: referer_url,
        }
        return spider.get_html(
            url, headers=headers, timeout=timeout,
            encoding="utf-8", errors=errors, wait_time=1.0,
            **kwargs)
    else:
        return html


# if __name__ == "__main__":
#     url = "https://www.zillow.com/browse/homes/ca/los-angeles-county"
#     html = get_html(url)
#     print(html)
