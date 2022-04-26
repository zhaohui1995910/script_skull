# -*- coding: utf-8 -*-
# @Time    : 2021/10/11 16:26
# @Author  : 10867
# @FileName: middleware.py
# @Software: PyCharm
from sanic import Sanic
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from utils.response import Response
from models import bind, base_model_session_ctx
from apps.spider import scheduler_update_job

app: Sanic = Sanic.get_app('SanicSpider')


@app.listener('before_server_start')
async def initialize_scheduler(_app, loop):
    _app.ctx.scheduler = AsyncIOScheduler({'event_loop': loop, 'apscheduler.timezone': 'UTC'})
    # _app.ctx.scheduler.add_job(scheduler_update_job, trigger='interval', seconds=60)
    _app.ctx.scheduler.start()


@app.middleware('request')
async def vialdate_user_token(request):
    """验证用户状态"""
    no_require_token = {
        '/user/login',
        '/user/test',
        '/user/signin'
    }
    if request.path in no_require_token:
        return None

    token = request.token
    if not token:
        return Response.fail(code=403, data='not find tokne')


# 配置数据库ORM会话Session
@app.middleware("request")
async def inject_session(request):
    """注入数据库回话"""
    request.ctx.session = sessionmaker(bind, AsyncSession, expire_on_commit=False, future=True)()
    request.ctx.session_ctx_token = base_model_session_ctx.set(request.ctx.session)


@app.middleware("response")
async def close_session(request, response):
    if hasattr(request.ctx, "session_ctx_token"):
        base_model_session_ctx.reset(request.ctx.session_ctx_token)
        await request.ctx.session.close()
