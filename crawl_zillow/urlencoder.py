#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from .packages.crawlib.urlencoder import BaseUrlEncoder
except:
    from crawl_zillow.packages.crawlib.urlencoder import BaseUrlEncoder


class UrlEncoder(BaseUrlEncoder):
    domain = "http://www.zillow.com"
    domain_browse_homes = "http://www.zillow.com/browse/homes"

    def browse_home_listpage_url(self,
                                 state=None,
                                 county=None,
                                 zipcode=None,
                                 street=None,
                                 **kwargs):
        """Construct an url of home list page by state, county, zipcode, street. 
        """
        url = self.domain_browse_homes
        for item in [state, county, zipcode, street]:
            if item:
                url = url + "/%s" % item
        url = url + "/"
        return url

    def browse_home_listpage_url_by_href(self, href):
        """http://www.zillow.com/browse/homes + surfix.
        """
        if not href.startswith("/"):
            href = "/" + href
        if not href.startswith("/browse/homes"):
            href = "/browse/homes" + href
        return self.url_join(href)


urlencoder = UrlEncoder()

if __name__ == "__main__":
    import webbrowser

    def test_all():
        webbrowser.open(urlencoder.browse_home_listpage_url())
        webbrowser.open(urlencoder.browse_home_listpage_url("md"))
        webbrowser.open(urlencoder.browse_home_listpage_url(
            "md", "montgomery-county"))
        webbrowser.open(urlencoder.browse_home_listpage_url(
            "md", "montgomery-county", "20878"))
        webbrowser.open(urlencoder.browse_home_listpage_url(
            "md", "montgomery-county", "20878", "case-st_949815"))

        webbrowser.open(urlencoder.browse_home_listpage_url_by_href(
            "/browse/homes/md/montgomery-county/20875/"))
        webbrowser.open(urlencoder.browse_home_listpage_url_by_href(
            "/md/montgomery-county/20876/"))
        webbrowser.open(urlencoder.browse_home_listpage_url_by_href(
            "md/montgomery-county/20877/"))

    test_all()
