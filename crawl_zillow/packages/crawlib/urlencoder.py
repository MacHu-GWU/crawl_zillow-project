#!/usr/bin/env python
# -*- coding: utf-8 -*-

from requests.compat import urlparse
try:
    from .helpers import url_join
except:
    from crawlib.helpers import url_join


class BaseUrlEncoder(object):

    """Base Url Encoder. Provide functional interface to create url.
    """
    domain = None
    
    def __init__(self):
        result = urlparse(self.domain)
        self.domain = "%s://%s" % (result.scheme, result.netloc)        
    
    def url_join(self, *parts):
        return url_join(self.domain, *parts)

    def get_url(self, *args, **kwargs):
        """An example method, takes argument and return url.
        """
        return self.domain


if __name__ == "__main__":
    def test_urlencoder():
        class PythonOrgUrlEncoder(BaseUrlEncoder):
            domain = "https://www.python.org"

        urlencoder = PythonOrgUrlEncoder()
        assert urlencoder.url_join("/about/") == "https://www.python.org/about"

    test_urlencoder()
