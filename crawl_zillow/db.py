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
if Config.MongoDB.password:
    db.authenticate(Config.MongoDB.username, Config.MongoDB.password)

c_state = db.get_collection(Model.state)
c_county = db.get_collection(Model.county)
c_zipcode = db.get_collection(Model.zipcode)
c_street = db.get_collection(Model.street)

address_col_mapper = dict()
all_state = list()
for doc in c_state.find():
    href = doc["_id"]
    state = doc["state"]
    state_abbr = href.split("/")[-2]
    all_state.append(state)
    col_name = "{prefix}_{state_abbr}".format(
        prefix=Model.address, state_abbr=state_abbr)
    col = db.get_collection(col_name)
    address_col_mapper[state] = col
