# -*- coding: utf-8 -*-
# @Time    : 2021/10/12 17:25
# @Author  : 10867
# @FileName: aiohttp_client.py
# @Software: PyCharm
import aiohttp
from functools import wraps


def aiohttp_session():
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            request.ctx.http_session = aiohttp.ClientSession()

            response = await f(request, *args, **kwargs)
            await request.ctx.http_session.close()
            return response

        return decorated_function

    return decorator
