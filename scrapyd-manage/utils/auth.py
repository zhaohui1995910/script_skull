# -*- coding: utf-8 -*-
# @Time    : 2021/9/30 10:44
# @Author  : 10867
# @FileName: auth.py
# @Software: PyCharm
import datetime
from typing import Union

import jwt
from jwt.exceptions import ExpiredSignatureError

from config import config

token_set = set()


def gen_token(data: dict) -> str:
    """生成token"""
    data['exp'] = datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    encoded = jwt.encode(data, config.JWT_SECRET, algorithm='HS256')
    return encoded


def verify_token(token: str) -> Union[bool, dict]:
    """解析token"""
    try:
        token = jwt.decode(token, config.JWT_SECRET, algorithms='HS256')
    except ExpiredSignatureError as e:
        print('token ExpiredSignatureError %s' % e)
        return False
    except Exception as e:
        print('token fial %s' % e)
        return False
    else:
        return token


def vaildate_login(request) -> bool:
    """验证用户登录状态"""

    token = request.headers.get('token', '')
    if verify_token(token):
        if token in token_set:
            return True

    return False
