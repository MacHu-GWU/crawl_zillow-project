#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup


class SoupError(Exception):

    """Failed to convert html to beatifulsoup.

    **中文文档**

    html成功获得了, 但是格式有错误, 不能转化为soup。
    """


class CaptchaError(Exception):

    """Encounter a captcha page.

    **中文文档**

    遭遇反爬虫验证页面。
    """


class WrongHtmlError(Exception):

    """The html is not the one we desired.

    **中文文档**

    页面不是我们想要的页面, 很可能被redirect到其他页面了。
    """


class ParseError(Exception):

    """Failed to parse data from html, may due to bug in your method.

    **中文文档**

    由于函数的设计失误, 解析页面信息发生了错误。
    """


class BaseHtmlParser(object):

    """Base Html Parser. Able to get useful data from html.
    """

    def get_soup(self, html):
        try:
            return BeautifulSoup(html, "html.parser")
        except Exception as e:
            raise SoupError()

    def get_data(self, html, *args, **kwargs):
        """An example method, takes argument and return parsed data.

        Make sure every possible errors is properly raised. 
        """
        if "http://www.google.com/recaptcha/api.js" in html:
            raise CaptchaError

        soup = self.get_soup(html)
        data = dict()

        try:
            a = soup.find("a", class_="header")
            if a is None:
                raise WrongHtmlError
            name = a.text
            data["name"] = name
        except Exception as e:
            raise ParseError(str(e))

        if len(data) == 0:
            data = None
        return data

if __name__ == "__main__":
    def test_htmlparser():
        htmlparser = BaseHtmlParser()
        html = '<a class="header" href="www.python.org">Python</a>'
        data = htmlparser.get_data(html)
        assert data == {"name": "Python"}

    test_htmlparser()
