#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
响应包装
"""


class AliResponse(object):
    """
    阿里云的相应包装
    """

    def __init__(self, status, headers=None):
        self._success_code = ("200", "201")
        self.status = str(status)
        if headers is None:
            self.headers = {}

    def success(self):
        if self.status in self._success_code:
            return True
        else:
            return False

    def __str__(self):
        return "Aliyun Response Wrapper"
