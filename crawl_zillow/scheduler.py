#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from pytq import Task, StatusFlagScheduler
import attr
from crawlib import Status

try:
    from . import config
    from .spider import get_html
    from .htmlparser import htmlparser
    from .model import BaseModel, State, County, Zipcode, Street
except:
    from crawl_zillow import config
    from crawl_zillow.spider import get_html
    from crawl_zillow.htmlparser import htmlparser
    from crawl_zillow.model import BaseModel, State, County, Zipcode, Street


@attr.s
class InputData(object):
    """
    :param doc: instance of :class:`~mongoengine.Document`.
    :param get_html_kwargs: arguments of :meth:`~crawl_zillow.spider.get_html`.
    """
    doc = attr.ib()
    get_html_kwargs = attr.ib(default=attr.Factory(dict))


primary_key = BaseModel.href.name # href field name
n_children_key = BaseModel._n_children.name #  _n_children field name


class BaseScheduler(StatusFlagScheduler):
    duplicate_flag = Status.S8_Finished.id
    update_interval = 30 * 24 * 3600  # 30 days

    model = BaseModel
    next_model = None
    next_model_col_name = None

    @property
    def collection(self):
        return self.model.col()

    def user_hash_input(self, input_data):
        return input_data.doc.href

    def user_process(self, input_data):
        """


        :param input_data:
        :return: output_data, list of next model instance. For example, if
          model is :class:`~crawl_zillow.model.State`, then next model is
          :class:`~crawl_zillow.model.County`.
        """
        url = input_data.doc.url
        html = get_html(
            url,
            wait_time=config.Crawler.wait_time,
            **input_data.get_html_kwargs)

        # some this model's attributes will also available in next model
        d = input_data.doc.to_dict()
        del d[primary_key]
        del d[self.status_key]
        del d[self.edit_at_key]
        del d[n_children_key]

        output_data = list()
        for href, name in htmlparser.get_items(html):
            data = {
                primary_key: href,
                self.next_model_col_name: name,
            }
            data.update(d)
            next_model_instance = self.next_model(**data)
            output_data.append(next_model_instance)
        output_data = output_data[:2] # COMMENT OUT IN PROD
        return output_data

    def user_post_process(self, task):
        """
        1. insert data to collection.
        2. update parent collection on ``status_key``, ``edit_at_key``,
        ``n_children_key`` fields.
        """
        # insert into next model's collection
        self.next_model.smart_insert(task.output_data)

        # update parent collection about status, edit_at, n_children
        n_children = len(task.output_data)
        self.collection.update(
            {"_id": task.id},
            {
                "$set": {
                    self.status_key: Status.S8_Finished.id,
                    self.edit_at_key: datetime.utcnow(),
                    n_children_key: n_children,
                }
            },
        )

    def get_todo(self, limit=None, get_html_kwargs=None):
        if get_html_kwargs is None:
            get_html_kwargs = dict()

        filters = {
            "$or": [  # not the finished document
                {self.status_key: {"$not": {"$gte": Status.S8_Finished.id}}},
                # now - edit_at <= update_interval
                # means now - update_interval <= edit_at
                {
                    self.edit_at_key: {
                        "$not": {
                            "$gte": datetime.utcnow() - timedelta(seconds=self.update_interval)
                        },
                    },
                },
            ]
        }
        input_data_queue = list()

        for doc in self.model.by_filter(filters=filters).limit(limit):
            input_data = InputData(
                doc=doc,
                get_html_kwargs=get_html_kwargs,
            )
            input_data_queue.append(input_data)
        return input_data_queue


class StateScheduler(BaseScheduler):
    model = State
    next_model = County
    next_model_col_name = County._meta["collection"]


class CountyScheduler(BaseScheduler):
    model = County
    next_model = Zipcode
    next_model_col_name = Zipcode._meta["collection"]


class ZipcodeScheduler(BaseScheduler):
    model = Zipcode
    next_model = Street
    next_model_col_name = Street._meta["collection"]
