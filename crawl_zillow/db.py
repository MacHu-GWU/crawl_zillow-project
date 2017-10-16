#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mongoengine
from .config import Config
from .ns import Model

client = mongoengine.connect(
    db=Config.MongoDB.dbname,
    host=Config.MongoDB.host,
    port=Config.MongoDB.port,
    username=Config.MongoDB.username,
    password=Config.MongoDB.password,
)
db = client.get_database(Config.MongoDB.dbname)

c_state = db.get_collection(Model.state)
c_county = db.get_collection(Model.county)
c_zipcode = db.get_collection(Model.zipcode)
c_street = db.get_collection(Model.street)
