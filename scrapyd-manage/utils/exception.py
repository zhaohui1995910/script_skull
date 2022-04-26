# -*- coding: utf-8 -*-
# @Time    : 2021/10/11 16:52
# @Author  : 10867
# @FileName: exception.py
# @Software: PyCharm
from sanic import Sanic
from sanic.response import json
from sanic.exceptions import InvalidUsage, ServerError
from utils.sanic_parser import HandleValidationError

app = Sanic.get_app('SanicSpider')


@app.exception(InvalidUsage, HandleValidationError, ServerError)
async def error_handler_sanic(request, exception):
    error = {
        "messages": str(exception)
    }
    return json(error, status=exception.status_code)


@app.exception(HandleValidationError)
async def error_handler_sanic(request, exception):
    error = {
        "messages": exception.exc.messages
    }
    return json(error, status=exception.status_code)


@app.exception(Exception)
async def error_handler_python(request, exception):
    error = {
        "messages": 'Internal Server Error',
        'error'   : str(exception)
    }
    return json(error, status=500)
