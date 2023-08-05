#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging

logger = logging.getLogger(__name__)


class BaseApi(object):
    def __init__(self, account, service=None):
        """
        service 为签名用到的如  OSS MNS 等等服务的名字
        :param account:
        :param service:
        """
        self._account = account
        self._service = service

    def get_request(self, resource):
        raise NotImplementedError
