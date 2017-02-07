#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module provide extended power to decode HTML you crawled.
"""

import chardet


def smart_decode(binary, errors="strict"):
    d = chardet.detect(binary)
    encoding = d["encoding"]
    confidence = d["confidence"]
    text = binary.decode(encoding, errors=errors)
    return text, encoding, confidence


#--- Unittest ---
if __name__ == "__main__":
    def test_handle_errors():
        utf8_text = "欢迎来到Python-CN。本社区主要讨论Python和Web开发技术。"
        utf8 = utf8_text.encode("utf-8")

    test_handle_errors()
