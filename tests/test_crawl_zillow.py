#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

def test_import():
    from crawl_zillow import zilo_urlencoder, zilo_htmlparser


if __name__ == "__main__":
    import os
    pytest.main([os.path.basename(__file__), "--tb=native", "-s", ])