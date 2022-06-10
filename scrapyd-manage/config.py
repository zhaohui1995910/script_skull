# -*- coding: utf-8 -*-
# @Time    : 2021/9/23 16:19
# @Author  : 10867
# @FileName: config.py
# @Software: PyCharm
import os
from sqlalchemy.engine.url import URL


class BaseConfig:
    FALLBACK_ERROR_FORMAT = 'json'
    log_config = dict(
        version=1,
        disable_existing_loggers=False,
        loggers={
            "sanic.root"  : {
                "level"   : "INFO",
                "handlers": ["generic_file"]
            },
            "sanic.error" : {
                "level"    : "INFO",
                "handlers" : ["generic_file"],
                "propagate": True,
                "qualname" : "sanic.error",
            },
            "sanic.access": {
                "level"    : "INFO",
                "handlers" : ["access_file"],
                "propagate": True,
                "qualname" : "sanic.access",
            },
        },
        handlers={
            "generic_file": {
                "class"    : "logging.handlers.RotatingFileHandler",
                "formatter": "generic",
                "filename" : "logs/generic.log",
                "encoding" : "utf-8"
            },
            "access_file" : {
                "class"    : "logging.handlers.RotatingFileHandler",
                "formatter": "access",
                "filename" : "logs/access.log",
                "encoding" : "utf-8"
            },
        },
        formatters={
            "generic": {
                "format" : "%(asctime)s [%(process)d] [%(levelname)s] %(message)s",
                "datefmt": "[%Y-%m-%d %H:%M:%S %z]",
                "class"  : "logging.Formatter",
            },
            "access" : {
                "format" : "%(asctime)s - (%(name)s)[%(levelname)s][%(host)s]: %(request)s %(message)s %(status)d %(byte)d",
                "datefmt": "[%Y-%m-%d %H:%M:%S %z]",
                "class"  : "logging.Formatter",
            },
        },
    )
    JWT_SECRET = 'wmZ4s5DAoC9yY45dxEOau5j38MW5Vy6X'


class DevConfig(BaseConfig):
    DATABASE_URI = URL.create(
        drivername='mysql+aiomysql',
        username='root',
        password='zh@852456',
        host='192.168.125.31',
        port='3306',
        database='sanic_spider'
    )


class TestConfig(BaseConfig):
    DATABASE_URI = URL.create(
        drivername='mysql+aiomysql',
        username='root',
        password='zh@852456',
        host='192.168.125.31',
        port='3306',
        database='sanic_spider'
    )


class ProdConfig(BaseConfig):
    DATABASE_URI = URL.create(
        drivername='mysql+aiomysql',
        username='root',
        password='zh@852456',
        host='192.168.125.31',
        port='3306',
        database='sanic_spider'
    )


env = os.environ.get('SPIDER_WEB_ENV', 'dev').lower()
if env == 'dev':
    config = DevConfig()
elif env == 'test':
    config = TestConfig()
elif env == 'prod':
    config = ProdConfig()
else:
    config = {}
