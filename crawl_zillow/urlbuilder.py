#!/usr/bin/env python
# -*- coding: utf-8 -*-


from crawlib import BaseUrlBuilder


class UrlBuilder(BaseUrlBuilder):
    domain = "https://www.zillow.com"
    domain_browse_homes = "https://www.zillow.com/browse/homes"

    def browse_home_listpage_url(self,
                                 state=None,
                                 county=None,
                                 zipcode=None,
                                 street=None,
                                 **kwargs):
        """
        Construct an url of home list page by state, county, zipcode, street.

        Example:

        - https://www.zillow.com/browse/homes/ca/
        - https://www.zillow.com/browse/homes/ca/los-angeles-county/
        - https://www.zillow.com/browse/homes/ca/los-angeles-county/91001/
        - https://www.zillow.com/browse/homes/ca/los-angeles-county/91001/tola-ave_5038895/
        """
        url = self.domain_browse_homes
        for item in [state, county, zipcode, street]:
            if item:
                url = url + "/%s" % item
        url = url + "/"
        return url

    # def browse_home_listpage_url_by_href(self, href):
    #     """
    #     http://www.zillow.com/browse/homes + surfix.
    #     """
    #     if not href.startswith("/"):
    #         href = "/" + href
    #     if not href.startswith("/browse/homes"):
    #         href = "/browse/homes" + href
    #     return self.url_join(href)


urlbuilder = UrlBuilder()

# if __name__ == "__main__":
#     import webbrowser
#
#     def test_all():
#         webbrowser.open(urlencoder.browse_home_listpage_url())
#         webbrowser.open(urlencoder.browse_home_listpage_url("md"))
#         webbrowser.open(urlencoder.browse_home_listpage_url(
#             "md", "montgomery-county"))
#         webbrowser.open(urlencoder.browse_home_listpage_url(
#             "md", "montgomery-county", "20878"))
#         webbrowser.open(urlencoder.browse_home_listpage_url(
#             "md", "montgomery-county", "20878", "case-st_949815"))
#
#         webbrowser.open(urlencoder.browse_home_listpage_url_by_href(
#             "/browse/homes/md/montgomery-county/20875/"))
#         webbrowser.open(urlencoder.browse_home_listpage_url_by_href(
#             "/md/montgomery-county/20876/"))
#         webbrowser.open(urlencoder.browse_home_listpage_url_by_href(
#             "md/montgomery-county/20877/"))
#
#     test_all()
