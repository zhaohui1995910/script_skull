# -*- coding: utf-8 -*-
# @Time    : 2021/9/23 15:40
# @Author  : 10867
# @FileName: __init__.py.py
# @Software: PyCharm
from sqlalchemy.orm import declarative_base
from contextvars import ContextVar
from sqlalchemy.ext.asyncio import create_async_engine

from config import config

Base = declarative_base()
bind = create_async_engine(config.DATABASE_URI, echo=True)
base_model_session_ctx = ContextVar("session")
