# -*- coding: utf-8 -*-
# @Time    : 2021/9/23 16:00
# @Author  : 10867
# @FileName: user.py
# @Software: PyCharm
import datetime
import asyncio

from sanic import Sanic, Blueprint, text, log
from webargs import fields
from sqlalchemy import select
from sanic.exceptions import InvalidUsage, ServerError

from models.user import AuthUser
from utils.sanic_parser import parse_args as params_parse
from utils.auth import gen_token, token_set, vaildate_login
from utils.response import Response
from utils.aiohttp_client import aiohttp_session

app = Sanic.get_app('SanicSpider')
bp = Blueprint('user', url_prefix='/user')

user_fields = {
    'username'  : fields.Str(required=True, validate=lambda x: len(x) < 16),
    'password'  : fields.Str(required=True, validate=lambda x: len(x) < 16),
    'first_name': fields.Str(required=False, validate=lambda x: len(x) < 16),
    'last_name' : fields.Str(required=False, validate=lambda x: len(x) < 16),
    'email'     : fields.Str(required=False, validate=lambda x: len(x) < 16),
}


async def io_task(_app):
    await asyncio.sleep(5)
    print(_app.name)


@app.route('/cache/set')
async def test_cache_set(request):
    await app.ctx.cache.set('name', 'abcd')
    return text('ok')


@app.route('/cache/get')
async def test_cache_get(request):
    result = await app.ctx.cache.get('name')
    print(result)
    return text(result)


@bp.route('/test', methods=['GET'])
@aiohttp_session()
async def test(request):
    # app.add_task(io_task)
    # session = request.ctx.session
    # async with session.begin():
    #     stmt = select(AuthUser).where(AuthUser.username == 'admin')
    #     result = await session.execute(stmt)
    #     person = result.scalar()
    #
    # async with request.ctx.http_session.get('http://www.baidu.com') as response:
    #     print(response.status)
    #     print(response.text)

    return text('ok')


@bp.post('/create')
@params_parse(user_fields, location='json')
async def create_user(request):
    """创建用户: 只有超级用户有权限"""
    pass


@bp.route('/login', methods=['POST'])
@params_parse(user_fields, location='json')
async def login(request, args):
    """用户登录"""
    username = args.get('username')
    password = args.get('password')

    # 验证用户账号密码
    session = request.ctx.session
    async with session.begin():
        stmt = select(AuthUser).where(AuthUser.username == username)
        result = await session.execute(stmt)
        user = result.scalar()

        if not user:
            return Response.fail(
                code=201,
                message='',
                error='"%s" 用户名不存在' % username
            )
        # 验证密码
        status: bool = user.verify_password(password)
        # 更新登录时间
        user.last_login = datetime.datetime.now()

        if status:
            token = gen_token({'username': user.username})
            token_set.add(token)
            data = {
                'username': username,
                'token'   : token
            }
            return Response.success(
                code=200,
                data=data,

            )
        else:
            error = '密码错误'
            return Response.fail(
                code=201,
                error=error,
                data='',
            )


@bp.route('/info', methods=['GET'])
async def user_data(request):
    result = {
        'name'        : 'admin',
        'avatar'      : 'static/img/admin-header.jpg',
        'introduction': '',
        'roles'       : ['Spider'],
    }
    return Response.success(data=result)


@bp.route('/verify_token', methods=['POST'])
@params_parse({'token': fields.Str(required=True)}, location='json')
async def user_token(request, args):
    """验证token是否有效"""
    if vaildate_login(request):
        return Response.success(code=200, data={'result': True})
    else:
        return Response.success(code=403, data={'result': False})


@bp.route('/logout', methods=['POST'])
async def logout(request):
    """退出登录"""
    token = request.headers.get('token')

    log.logger.info('token %s' % token)
    if vaildate_login(request):
        token_set.remove(token)

    return Response.success(
        code=200,
        data={'result': '退出成功'}
    )


@bp.route('/lumi/signin', methods=['POST'])
@aiohttp_session()
@params_parse(user_fields, location='json')
async def user_signin(request, args):
    """渠成授权登录"""
    sign_in_url = app.config.get('LUMI_SIGNIN_URL')
    data = {
        "clientId"    : "Default",
        "clientSecret": "erp_secret",
        "signName"    : int(args.get('username')),
        "password"    : args.get('password')
    }
    async with request.ctx.http_session.post(sign_in_url, json=data) as response:
        if response.status != 200:
            return Response.fail(code=201, data='sign failed')

        result_json = await response.json()
        if result_json.get('success'):
            access_token = result_json.get('data', {}).get('access_token')
            return Response.success(code=200, data=access_token)
        else:
            result = result_json.get('result')
            return Response.success(code=200, data=result)


@bp.route('/lumi/info')
@aiohttp_session()
async def user_info(request):
    token = request.token
    headers = {'Authorization': f'Bearer {token}'}
    # 1 请求渠成认证接口，获取用户信息
    user_info_url = app.config.get('LUMI_USERINFO_URL')

    async with request.ctx.http_session.get(user_info_url, headers=headers) as response:
        result_json = await response.json()
        _user_info: dict = result_json.get('result', {})

    # 2 请求渠成权限中心，获取用户权限列表
    permission_url = app.config.get('LUMI_PERMISSION_URL')
    _json = {
        "applicationName": "Spider",
        "moduleName"     : "string",
        "specUserName"   : _user_info['userName']
    }
    async with request.ctx.http_session.post(permission_url, json=_json, headers=headers) as response:
        result_json = await response.json()
        items = result_json.get('result').get('items')
        permission: list = [i['name'] for i in items]

    # 3 构建用户信息（user_info)
    user = dict()
    user['roles'] = permission
    user['introduction'] = ''
    user['avatar'] = 'static/img/admin-header.jpg'
    user['name'] = _user_info['displayName']
    return Response.success(code=200, data=user)
