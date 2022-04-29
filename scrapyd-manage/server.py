# -*- coding: utf-8 -*-
# @Time    : 2021/9/23 15:37
# @Author  : 10867
# @FileName: server.py
# @Software: PyCharm
from sanic import Sanic
from sanic_cors import CORS
from aiocache import Cache, caches
# from aiocache.serializers import PickleSerializer

from config import config
from utils.autodiscover import auto_discover

# 创建应用
app = Sanic(
    'SanicSpider',
    log_config=config.log_config
)
# 配置文件
app.update_config(config)
# 配置跨域
CORS(app, automatic_options=True)
# 配置缓存
cache = Cache(Cache.MEMORY)
app.ctx.cache = cache

auto_discover(
    app,
    'middleware',
    'routes',
    'apps.user',
    'apps.spider',
    # 'utils.exception',
    recursive=False,
)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, access_log=True, workers=4)




