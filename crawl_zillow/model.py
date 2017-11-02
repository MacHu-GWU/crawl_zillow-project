#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mongoengine
from mongoengine_mate import ExtendedDocument
from crawlib import Status

from datetime import datetime

try:
    from . import db
except:  # pragma: no cover
    try:
        from crawl_zillow import db
    except:  # pragma: no cover
        pass

try:
    from .ns import Model
    from .urlbuilder import urlbuilder
except:  # pragma: no cover
    from crawl_zillow.ns import Model
    from crawl_zillow.urlbuilder import urlbuilder


class BaseModel(ExtendedDocument):
    href = mongoengine.StringField(primary_key=True)
    _status = mongoengine.IntField(
        default=Status.S0_ToDo.id,
    )
    _edit_at = mongoengine.DateTimeField(
        default=lambda: datetime.utcnow()
    )
    _n_children = mongoengine.IntField()

    meta = {
        "abstract": True,
    }

    @property
    def url(self):
        """
        Example::

            /browse/homes/ca/ -> https://www.zillow.com/browse/homes/ca:return:
        """
        return urlbuilder.join_all(self.href)

    @property
    def key(self):
        """
        Example::

            /browse/homes/ca/ -> ca
            /browse/homes/ca/los-angeles-county/ -> los-angeles-county
            /browse/homes/ca/los-angeles-county/91001/ -> 91001
            /browse/homes/ca/los-angeles-county/91001/tola-ave_5038895/ -> tola-ave_5038895

        :return:
        """

        return [part.strip() for part in self.href.split("/") if part.strip()][
            -1]


class State(BaseModel):
    state = mongoengine.StringField()

    meta = {
        "collection": Model.state
    }


class County(BaseModel):
    state = mongoengine.StringField()
    county = mongoengine.StringField()

    meta = {
        "collection": Model.county
    }


class Zipcode(BaseModel):
    state = mongoengine.StringField()
    county = mongoengine.StringField()
    zipcode = mongoengine.StringField()

    meta = {
        "collection": Model.zipcode
    }


class Street(BaseModel):
    state = mongoengine.StringField()
    county = mongoengine.StringField()
    zipcode = mongoengine.StringField()
    street = mongoengine.StringField()

    meta = {
        "collection": Model.street
    }


class Address(BaseModel):
    state = mongoengine.StringField()
    county = mongoengine.StringField()
    zipcode = mongoengine.StringField()
    street = mongoengine.StringField()
    address = mongoengine.StringField()
