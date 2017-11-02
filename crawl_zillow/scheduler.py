#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import attr
from datetime import datetime, timedelta
from pymongo_mate.crud.insert import smart_insert
from crawlib.spider.selenium_spider import ChromeSpider
from crawlib import exc, Status
from pytq import StatusFlagScheduler

try:
    from .config import Config
    from .spider import get_html
    from .htmlparser import htmlparser
    from .model import BaseModel, State, County, Zipcode, Street, Address
    from .db import all_state, address_col_mapper
except:
    from crawl_zillow.config import Config
    from crawl_zillow.spider import get_html
    from crawl_zillow.htmlparser import htmlparser
    from crawl_zillow.model import BaseModel, State, County, Zipcode, Street, Address
    from crawl_zillow.db import all_state, address_col_mapper


@attr.s
class InputData(object):
    """
    :param doc: instance of :class:`~mongoengine.Document`.
    :param get_html_kwargs: arguments of :meth:`~crawl_zillow.spider.get_html`.
    """
    doc = attr.ib()
    get_html_kwargs = attr.ib(default=attr.Factory(dict))


@attr.s
class OutputData(object):
    """
    :param doc: instance of :class:`~mongoengine.Document`.
    :param get_html_kwargs: arguments of :meth:`~crawl_zillow.spider.get_html`.

    """
    data = attr.ib()
    errors = attr.ib(default=None)
    status = attr.ib(default=Status.S0_ToDo.id)


primary_key = BaseModel.href.name
status_key = BaseModel._status.name
edit_at_key = BaseModel._edit_at.name
n_children_key = BaseModel._n_children.name
primary_key = BaseModel.href.name  # href field name
n_children_key = BaseModel._n_children.name  # _n_children field name


class BaseScheduler(StatusFlagScheduler):
    duplicate_flag = Status.S50_Finished.id
    update_interval = 30 * 24 * 3600  # 30 days

    status_key = status_key
    edit_at_key = edit_at_key
    n_children_key = n_children_key

    model = BaseModel
    next_model = None
    next_model_col_name = None

    _use_browser = None
    _selenium_driver = None

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

        self.logger.info("Crawl %s ." % url, 1)

        output_data = OutputData(data=list())
        try:
            html = get_html(
                url,
                wait_time=Config.Crawler.wait_time,
                driver=self._selenium_driver,
                **input_data.get_html_kwargs)

            # some this model's attributes will also available in next model
            d = input_data.doc.to_dict()
            del d[primary_key]
            del d[status_key]
            del d[edit_at_key]
            del d[n_children_key]

            try:
                for href, name in htmlparser.get_items(html):
                    data = {
                        primary_key: href,
                        self.next_model_col_name: name,
                    }
                    data.update(d)
                    next_model_instance = self.next_model(**data)
                    output_data.data.append(next_model_instance)
                self.logger.info(Status.S50_Finished.description, 1)
                output_data.status = Status.S50_Finished.id
            except Exception as e:
                raise exc.ParseError
        except exc.CaptchaError as e:
            time.sleep(10.0)  # Wait for 10 seconds to solve Captcha
            self.logger.info(Status.S20_WrongPage.description, 1)
            output_data.status = Status.S20_WrongPage.id
            output_data.errors = e
        except exc.WrongHtmlError as e:
            self.logger.info(Status.S20_WrongPage.description, 1)
            output_data.status = Status.S20_WrongPage.id
            output_data.errors = e
        except exc.ParseError as e:
            self.logger.info(Status.S30_ParseError.description, 1)
            output_data.status = Status.S30_ParseError.id
            output_data.errors = e
        except exc.ServerSideError as e:
            self.logger.info(Status.S60_ServerSideError.description, 1)
            output_data.status = Status.S60_ServerSideError.id
            output_data.errors = e
        except Exception as e:
            self.logger.info(Status.S10_HttpError.description, 1)
            output_data.status = Status.S10_HttpError.id
            output_data.errors = e
        # output_data.data = output_data.data[:2] # COMMENT OUT IN PROD

        return output_data

    def user_post_process(self, task):
        """

        :param task:
        :return:
        """
        # insert into next model's collection
        output_data = task.output_data

        parent_to_set = {
            self.status_key: output_data.status,
            self.edit_at_key: datetime.utcnow(),
        }
        if output_data.status == Status.S50_Finished.id:
            n_children = len(output_data.data)

            if n_children:
                self.next_model.smart_insert(output_data.data)

            parent_to_set[self.n_children_key] = n_children

        self.collection.update({"_id": task.id}, {"$set": parent_to_set})

        if output_data.status < Status.S50_Finished.id:
            raise output_data.errors

    def get_todo(self, filters=None, limit=None, get_html_kwargs=None):
        if filters is None:
            filters = {
                "$or": [  # not the finished document
                    {status_key: {"$not": {"$gte": Status.S50_Finished.id}}},
                    # now - edit_at <= update_interval
                    # means now - update_interval <= edit_at
                    {
                        edit_at_key: {
                            "$not": {
                                "$gte": datetime.utcnow() - timedelta(seconds=self.update_interval)
                            },
                        }
                    }
                ]
            }

        if get_html_kwargs is None:
            get_html_kwargs = dict()

        input_data_queue = list()

        for doc in self.model.by_filter(filters=filters).limit(limit):
            input_data = InputData(
                doc=doc,
                get_html_kwargs=get_html_kwargs,
            )
            input_data_queue.append(input_data)
        return input_data_queue

    def do(self,
           input_data_queue,
           pre_process=None,
           multiprocess=False,
           debug_mode=False,
           use_browser=False):
        self._use_browser = use_browser
        if self._use_browser:
            self._selenium_driver = ChromeSpider(
                driver_executable_path=Config.Crawler.chrome_driver_executable,
                default_timeout=5.0,
                default_wait_time=Config.Crawler.wait_time,
            )
            # Wait 10 seconds to initiate something, like log-in.
            time.sleep(Config.Crawler.browser_prepare_time)
            with self._selenium_driver as driver:
                super(BaseScheduler, self).do(
                    input_data_queue,
                    pre_process=pre_process,
                    multiprocess=False,
                    debug_mode=debug_mode,
                )
        else:
            self._selenium_driver = None
            super(BaseScheduler, self).do(
                input_data_queue,
                pre_process=pre_process,
                multiprocess=multiprocess,
                debug_mode=debug_mode,
            )


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


class StreetScheduler(BaseScheduler):
    model = Street
    next_model = Address
    next_model_col_name = Address._meta["collection"]

    def user_post_process(self, task):
        # insert into next model's collection
        output_data = task.output_data

        if output_data.status == Status.S50_Finished.id:
            n_children = len(output_data.data)

            if n_children:
                state = output_data.data[0].state
                next_model_col = address_col_mapper[state]

                to_insert = list()
                for doc in output_data.data:
                    d = doc.to_dict()
                    d["_id"] = d["href"]
                    del d["href"]
                    to_insert.append(d)

                smart_insert(next_model_col, to_insert)

            # update parent collection about status, edit_at, n_children
            self.collection.update(
                {"_id": task.id},
                {
                    "$set": {
                        status_key: Status.S50_Finished.id,
                        edit_at_key: datetime.utcnow(),
                        n_children_key: n_children,
                    }
                },
            )
        else:
            self.collection.update(
                {"_id": task.id},
                {
                    "$set": {
                        status_key: output_data.status,
                        edit_at_key: datetime.utcnow(),
                    }
                },
            )
            raise output_data.errors
