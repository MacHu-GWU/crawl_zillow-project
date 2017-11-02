#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from random import randint
from crawlib import (
    requests_spider as spider,
    Headers, exc
)
try:
    from .config import Config
except:
    from crawl_zillow.config import Config


prefix = "http://webcache.googleusercontent.com/search?q=cache:"


# This will appear in html when google cache haven't seen a url
not_found_pattern = "was not found on this server."

captcha_patterns = [
    "https://www.google.com/recaptcha/api.js", "I'm not a robot"]


def if_captcha_then_raise(html):
    for captcha_pattern in captcha_patterns:
        if captcha_pattern in html:
            raise exc.CaptchaError("Found %r in html!" % captcha_pattern)


server_side_error_page_pattern = "Oops – no one seems to be home."


def _get_html(url,
              headers=None,
              timeout=None,
              errors="strict",
              wait_time=None,
              driver=None,
              **kwargs):
    """

    :param url:
    :param headers:
    :param timeout:
    :param errors:
    :param wait_time:
    :param driver:
    :param kwargs:
    :return:

    :raises exc.WrongHtmlError:
    :raises exc.CaptchaError:
    :raises exc.ServerSideWrongPageError:
    """
    if driver:  # selenium spider
        html = driver.get_html(url=url, wait_time=wait_time)
    else:  # requests spider
        if headers is None:
            if url.startswith(prefix):
                headers = {
                    Headers.UserAgent.KEY: Headers.UserAgent.chrome,
                    Headers.Referer.KEY: "http://cachedview.com/",
                }
            else:
                referer_url = "/".join(url.split("/")[:-1])
                headers = {
                    Headers.UserAgent.KEY: Headers.UserAgent.chrome,
                    Headers.Referer.KEY: referer_url,
                }
        html = spider.get_html(
            url, headers=headers, timeout=timeout,
            encoding="utf-8", errors=errors, wait_time=wait_time,
            **kwargs)

    if not_found_pattern in html:
        raise exc.WrongHtmlError
    if_captcha_then_raise(html)
    if server_side_error_page_pattern in html:
        raise exc.ServerSideError
    return html


def get_html(url,
             headers=None,
             timeout=None,
             errors="strict",
             wait_time=None,
             driver=None,
             zillow_only=False,
             cache_only=False,
             zillow_first=False,
             cache_first=False,
             random=False,
             **kwargs):
    """
    Use Google Cached Url.

    :param cache_only: if True, then real zillow site will never be used.
    :param driver: selenium browser driver。
    """
    if wait_time is None:
        wait_time = Config.Crawler.wait_time

    # prepare url
    cache_url1 = prefix + url + "/"
    cache_url2 = prefix + url
    zillow_url = url

    only_flags = [zillow_only, cache_only]
    if sum(only_flags) == 0:
        first_flags = [zillow_first, cache_first]
        if sum(first_flags) == 0:
            if random:
                if randint(0, 1):
                    all_url = [zillow_url, cache_url1, cache_url2]
                else:
                    all_url = [cache_url1, cache_url2, zillow_url]
            else:
                all_url = [zillow_url, cache_url1, cache_url2]
        elif sum(first_flags) == 1:
            if zillow_first:
                all_url = [zillow_url, cache_url1, cache_url2]
            elif cache_first:
                all_url = [cache_url1, cache_url2, zillow_url]
        else:
            raise ValueError(
                "Only zero or one `xxx_first` argument could be `True`!")

    elif sum(only_flags) == 1:
        if zillow_only:
            all_url = [zillow_url, ]
        elif cache_only:
            all_url = [cache_url1, cache_url2]

    else:
        raise ValueError(
            "Only zero or one `xxx_only` argument could be `True`!")

    for url in all_url:
        try:
            html = _get_html(url, headers, timeout, errors,
                             wait_time, driver, **kwargs)
            return html
        except Exception as e:
            pass
    raise e


if __name__ == "__main__":
    url = "https://www.zillow.com/browse/homes/la/jefferson-parish/"
    html = get_html(url, zillow_first=True, cache_only=False)
    print(html)
