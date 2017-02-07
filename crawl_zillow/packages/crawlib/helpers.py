#!/usr/bin/env python
# -*- coding: utf-8 -*-


def url_join(domain, *parts):
    """Construct url from domain and parts.
    """
    if " " in [domain,] + list(parts):
        raise Exception("empty string is not allowed in url!")
    
    l = list()
    
    if domain.endswith("/"):
        domain = domain[:-1]
    l.append(domain)
    
    for part in parts:
        for i in part.split("/"):
            if i.strip():
                l.append(i)
    return "/".join(l)
