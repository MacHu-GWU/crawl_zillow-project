#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

try:
    from .helpers import int_filter, float_filter
    from .packages.crawlib import exc
    from .packages.crawlib.htmlparser import BaseHtmlParser
except:
    from crawl_zillow.helpers import int_filter, float_filter
    from crawl_zillow.packages.crawlib import exc
    from crawl_zillow.packages.crawlib.htmlparser import BaseHtmlParser


class HTMLParser(BaseHtmlParser):

    def get_items(self, html, url="unknown url"):
        """Get state, county, zipcode, address code from lists page.
        
        Example: http://www.zillow.com/browse/homes/md/
        """
        if "I'm not a robot" in html:
            raise exc.CaptchaError(url)

        data = list()
        soup = self.get_soup(html)
        try:
            div = soup.find("div", class_="zsg-lg-1-2 zsg-sm-1-1")
            for li in div.find_all("li"):
                a = li.find_all("a")[0]
                link = a["href"].replace("/browse/homes/", "")
                name = a.text.strip()
                data.append((link, name))
            return data
        except Exception as e:
            raise exc.ParseError("%s: %s" % (url, e))

    def get_house_detail(self, html):
        """Get bedroom, bathroom, sqft and more information.
        
        Example: http://www.zillow.com/homedetails/8510-Whittier-Blvd-Bethesda-MD-20817/37183103_zpid/
        """
        if "I'm not a robot" in html:
            raise exc.CaptchaError(url)

        data = {"errors": dict()}
        soup = self.get_soup(html)

        # header part, bedroom, bathroom, sqft
        header = soup.find("header", class_="zsg-content-header addr")
        if header is None:
            raise exc.ParseError(url)

        try:
            h3 = header.find("h3")
            if h3 is None:
                raise exc.ParseError

            span_list = h3.find_all("span", class_="addr_bbs")
            if len(span_list) != 3:
                raise exc.ParseError

            text = span_list[0].text
            try:
                bedroom = float_filter(text)
                data["bedroom"] = bedroom
            except:
                data["errors"][
                    "bedroom"] = "can't parse bedroom from %r" % text

            text = span_list[1].text
            try:
                bathroom = float_filter(text)
                data["bathroom"] = bathroom
            except:
                data["errors"][
                    "bathroom"] = "can't parse bathroom from %r" % text

            text = span_list[2].text
            try:
                sqft = int_filter(text)
                data["sqft"] = sqft
            except:
                data["errors"]["sqft"] = "can't parse sqft from %r" % text
        except:
            pass

        # Facts, Features, Construction, Other (FFCO)
        div_list = soup.find_all(
            "div", class_=re.compile("fact-group-container zsg-content-component"))

        for div in div_list:
            h3 = div.find("h3")
            if h3.text == "Facts":
                try:
                    facts = list()
                    for li in div.find_all("li"):
                        facts.append(li.text.strip())
                    data["facts"] = facts
                except Exception as e:
                    data["errors"]["facts"] = str(e)

            if h3.text == "Features":
                features = list()
                try:
                    for li in div.find_all("li"):
                        if '"targetDiv"' not in li.text:
                            features.append(li.text.strip())
                    data["features"] = features
                except Exception as e:
                    data["errors"]["features"] = repr(e)

            if h3.text == "Appliances Included":
                appliances = list()
                try:
                    for li in div.find_all("li"):
                        appliances.append(li.text.strip())
                    data["appliances"] = appliances
                except Exception as e:
                    data["errors"]["appliances"] = repr(e)

            if h3.text == "Additional Features":
                additional_features = list()
                try:
                    for li in div.find_all("li"):
                        additional_features.append(li.text.strip())
                    data["additional_features"] = additional_features
                except Exception as e:
                    data["errors"]["additional_features"] = repr(e)

            if h3.text == "Construction":
                construction = list()
                try:
                    for li in div.find_all("li"):
                        construction.append(li.text.strip())
                    data["construction"] = construction
                except Exception as e:
                    data["errors"]["construction"] = repr(e)

            if h3.text == "Other":
                other = list()
                try:
                    for li in div.find_all("li"):
                        other.append(li.text.strip())
                    data["other"] = other
                except Exception as e:
                    data["errors"]["other"] = repr(e)

        if len(data["errors"]) == 0:
            del data["errors"]

        if data:
            return data
        else:
            return None

htmlparser = HTMLParser()


if __name__ == "__main__":
    import os
    from pprint import pprint as ppt
    from dataIO import textfile
    from pathlib_mate import Path

    from crawlib.spider import spider
    from crawl_zillow.urlencoder import urlencoder

    testdata = [
        ("listpage", None, None, None, None),
        ("state", "md", None, None, None),
        ("county", "md", "montgomery-county", None, None),
        ("zipcode", "md", "montgomery-county", "20878", None),
        ("street", "md", "montgomery-county", "20878", "case-st_949815"),
    ]

    zillow_house_url_list = [
        "/homedetails/5504-Griffith-Rd-Gaithersburg-MD-20882/37074305_zpid/",
        "/homedetails/524-19th-St-Richmond-CA-94801/18535709_zpid/",
        "/homedetails/3341-P-St-NW-Washington-DC-20007/429739_zpid/",
        "/homedetails/3333-Q-St-NW-Washington-DC-20007/119083145_zpid/",
        "/homedetails/244-W-23rd-St-APT-5C-New-York-NY-10011/2097514248_zpid/",
        "/homedetails/450-7th-St-APT-1N-Hoboken-NJ-07030/52962322_zpid/",
    ]

    def get_testdata():
        """

        **中文文档**

        下载测试数据。
        """
        for page, state, county, zipcode, street in testdata:
            url = urlencoder.browse_home_listpage_url(
                state, county, zipcode, street)
            filepath = Path("testdata", "%s.html" % page)
            if not filepath.exists():
                html = spider.get_html(url, encoding="utf-8")
                textfile.write(html, filepath.abspath)

        for href in zillow_house_url_list:
            url = urlencoder.url_join(href)
            zid = href.split("/")[-2]
            filepath = Path("testdata", "%s.html" % zid)
            if not filepath.exists():
                html = spider.get_html(url, encoding="utf-8")
                textfile.write(html, filepath.abspath)

    get_testdata()

    def test_get_items():
        for page, state, county, zipcode, street in testdata:
            filepath = Path("testdata", "%s.html" % page)
            data = htmlparser.get_items(textfile.read(filepath.abspath))
            ppt(data)

#     test_get_items()

    def test_get_house_detail():
        for p in Path("testdata").select_by_pattern_in_fname("zpid"):
            html = textfile.read(p.abspath)
            data = htmlparser.get_house_detail(html)
            ppt(data)

#     test_get_house_detail()

    def test_single_house():
        """Test with one address.
        """
        html = textfile.read(Path("testdata", "119083145_zpid.html").abspath)
        data = htmlparser.get_house_detail(html)
        ppt(data)

#     test_single_house()
