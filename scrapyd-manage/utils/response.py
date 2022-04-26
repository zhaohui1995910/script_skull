# -*- coding: utf-8 -*-
# @Time    : 2021/9/30 10:43
# @Author  : 10867
# @FileName: utils.py
# @Software: PyCharm
from typing import Union
from sanic.response import json, HTTPResponse


class Response:

    @staticmethod
    def success(
            code: int = 200,
            data: Union[str, list, dict] = None,
    ) -> HTTPResponse:
        data = {
            'code': code,
            'data': data,
        }
        return json(data, status=code)

    @staticmethod
    def fail(
            code: int = 500,
            data: Union[str, list, dict] = None,
            error: Union[dict, str] = None
    ) -> HTTPResponse:
        data = {
            'code' : code,
            'data' : data,
            'error': error,
        }
        return json(data, status=code)
