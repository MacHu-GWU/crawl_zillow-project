#!/usr/bin/env python
# -*- coding: utf-8 -*-

is_prod = False  # False, using cloud test database, True, using local prod database

if is_prod:
    import setting_prod
else:
    import setting_dev
