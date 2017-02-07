#!/usr/bin/env python
# -*- coding: utf-8 -*-


def int_filter(text):
    """Extract integer from text.

    **中文文档**

    摘除文本内的整数。
    """
    res = list()
    for char in text:
        if char.isdigit():
            res.append(char)
    return int("".join(res))


def float_filter(text):
    """Extract float from text.

    **中文文档**

    摘除文本内的小数。
    """
    res = list()
    for char in text:
        if (char.isdigit() or (char == ".")):
            res.append(char)
    return float("".join(res))


if __name__ == "__main__":
    assert int_filter("2,154 sqft") == 2154
    assert abs(float_filter("2.5 bathroom") - 2.5) <= 0.0001
