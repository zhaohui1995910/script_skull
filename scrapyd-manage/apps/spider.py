# -*- coding: utf-8 -*-
# @Time    : 2021/10/14 13:31
# @Author  : 10867
# @FileName: spider.py
# @Software: PyCharm
import json
import datetime
import time

import requests
import aiohttp
from aiohttp.payload import BytesIOPayload
from aiohttp.formdata import FormData
from webargs import fields
from sanic import Blueprint, text, Request, Sanic, log
from sanic.views import HTTPMethodView
from sanic.exceptions import InvalidUsage
from sqlalchemy import select, update, func, insert, delete, exc
from sqlalchemy.orm import selectinload, Session, sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from marshmallow import Schema

from models import bind
from models.scrapy import Server, Project, ProjectVersion, Job, Spider, Task, TaskTimer, TaskSetting
from utils.sanic_parser import parse_args as params_parse
from utils.response import Response

app = Sanic.get_app('SanicSpider')
bp = Blueprint("scrapy", url_prefix='/scrapy')


class ServerView(HTTPMethodView):
    """服务器模块"""
    _fields: dict = {
        'host'         : fields.Str(required=True, validate=lambda x: len(x) < 15),
        'port'         : fields.Str(required=True),
        'auth'         : fields.Boolean(required=False, load_default=False),
        'auth_username': fields.Str(required=False, validate=lambda x: len(x) < 16),
        'auth_password': fields.Str(required=False, validate=lambda x: len(x) < 16),
        'hostname'     : fields.Str(default=None, attribute='info.hostname'),
        'id'           : fields.Integer()
    }

    async def get(self, request: Request):
        session: Session = request.ctx.session
        async with session.begin():
            stmt = select(Server).options(selectinload(Server.info))
            result = await session.execute(stmt)
            servers = result.scalars().all()

        result_schema = Schema.from_dict(self._fields)(many=True)
        data = result_schema.dump(servers)

        return Response.success(code=200, data=data)

    @params_parse(_fields, location='json')
    async def post(self, request, kwargs):

        # todo 验证是否有效，并且获取hostname

        server = Server(**kwargs)
        server.create_datetime = datetime.datetime.now()

        session = request.ctx.session
        async with session.begin():
            session.add(server)

        return Response.success(data='success')

    async def delete(self, request):
        sid = request.json.get('id')
        if not sid:
            raise InvalidUsage('`id` not null')
        session = request.ctx.session

        select_server_stmt = select(Server).where(Server.id == sid)
        result = await session.execute(select_server_stmt)
        server = result.scalars().first()

        if not server:
            return Response.fail(error=f'sid:{sid} no exist')

        # todo 同时删除所属server_info, project,

        await session.delete(server)

        await session.commit()

        return Response.success(data='删除成功')


class ProjectView(HTTPMethodView):
    """项目模块"""
    _limit = 18
    _fields = {
        'page'      : fields.Integer(required=False, default=1),
        'project'   : fields.Str(required=False, default=None),
        'project_id': fields.Integer(required=False, default=None),
        'desc'      : fields.Str(required=False, default=None, validate=lambda x: len(x) < 255),
    }

    result_fields = {
        'id'             : fields.Str(),
        'name'           : fields.Str(),
        'desc'           : fields.Str(),
        'create_datetime': fields.DateTime(),
        'update_datetime': fields.DateTime(),
        'versions'       : fields.List(fields.Nested(Schema.from_dict({
            'code'           : fields.Str(attribute='code'),
            'create_datetime': fields.DateTime()
        })), attribute='version'),
        'server_id'      : fields.Str(default=None, attribute='server.id'),
    }

    @params_parse(_fields, location="query")
    async def get(self, request, kwargs):
        page: int = kwargs.get('page')
        project: str = kwargs.get('project')
        session = request.ctx.session

        async with session.begin():
            # 查询项目总数
            count_stmt = select(func.count()).select_from(Project).where(Project.is_delete == 0)
            count_result = await session.execute(count_stmt)
            project_count = count_result.scalar()

            if project:
                stmt = select(Project).where(Project.name.like("%{}%".format(project)))
            else:
                stmt = select(Project)
            stmt = stmt.where(Project.is_delete == 0)
            # 加载子表
            stmt = stmt.options(selectinload(Project.server), selectinload(Project.version))
            # 分页查询
            stmt = stmt.offset((page - 1) * self._limit).limit(self._limit)

            result = await session.execute(stmt)
            project_list = result.scalars().all()

        result_schema = Schema.from_dict(self.result_fields)(many=True)
        data = result_schema.dump(project_list)
        result_data = {'total': project_count, 'projects': data}

        return Response.success(data=result_data)

    async def post(self, request):
        # 发布项目或发布新版本, scrapyd服务器信息（地址，端口），egg文件，项目信息（名称、版本）
        # 发布成功后，获取项目信息，及爬虫列表
        # 若新发布的项目名称数据库中已存在并is_delete为true，需要is_delete改为false
        # todo 若scrapyd因意外等，导致项目历史的版本已不存在，但是数据库仍饭存在
        project_name = request.form.get('name')
        project_desc = request.form.get('desc')
        server_id = request.form.get('server_id')

        version = int(time.time() * 1000)

        db_session = request.ctx.session
        select_stmt = select(Server).where(Server.id == int(server_id))
        result = await db_session.execute(select_stmt)
        server_item = result.scalars().first()

        file = request.files.get('file') if request.files.get('file') else b''
        host = server_item.host
        port = server_item.port

        select_stmt = select(Project).where(Project.name == project_name)
        result = await db_session.execute(select_stmt)
        project = result.scalars().first()

        if project:
            project.is_delete = False
            await db_session.commit()

        # 发布项目 -> scrapyd
        data = {
            'project': project_name,
            'version': version,
            'egg'    : file.body,
        }
        add_project_url = f'http://{host}:{port}/addversion.json'
        response = requests.post(url=add_project_url, data=data)
        result = response.json()

        if result.get('status') == 'ok':

            if not project:

                insert_stmt = insert(Project).values(
                    name=project_name,
                    desc=project_desc,
                    server_id=server_id,
                    is_delete=False
                )
                insert_result = await db_session.execute(insert_stmt)
                project_id = insert_result.inserted_primary_key[0]

                version_insert_stmt = insert(ProjectVersion).values(
                    code=version,
                    project_id=project_id,
                    create_datetime=datetime.datetime.now()
                )
                await db_session.execute(version_insert_stmt)

            else:
                project_id = project.id
                version_insert_stmt = insert(ProjectVersion).values(
                    code=version,
                    project_id=project.id,
                    create_datetime=datetime.datetime.now()
                )
                await db_session.execute(version_insert_stmt)
                await db_session.commit()
        else:
            return Response.fail(data="发布失败")

        # 获取爬虫列表
        get_spider_url = f'http://{host}:{port}/listspiders.json'
        params = {'project': project_name, '_version': version}
        response = requests.get(get_spider_url, params=params)
        result = response.json()

        for spider_name in result.get('spiders'):
            insert_spider_stmt = insert(Spider).values(
                name=spider_name,
                desc='',
                project_id=project_id,
                version_code=version,
                create_datetime=datetime.datetime.now()
            )
            await db_session.execute(insert_spider_stmt)

        await db_session.commit()
        return Response.success(data='发布成功')

    @params_parse(_fields, location="json")
    async def put(self, request, kwargs):
        session = request.ctx.session

        project_id = kwargs.get('project_id')
        desc = kwargs.get('desc')

        if not kwargs.get('project_id') or not kwargs.get('desc'):
            return Response.fail(data='请检查参数')

        async with session.begin():
            update_stmt = update(Project).where(Project.id == project_id).values(desc=desc)
            await session.execute(update_stmt)

        return Response.success(data='更新成功')

    @params_parse(_fields, location="json")
    async def delete(self, request, body):
        project_id = body.get('project_id')

        session = request.ctx.session

        select_project_stmt = select(Project).where(
            Project.id == project_id
        ).options(
            selectinload(Project.server)
        )
        result = await session.execute(select_project_stmt)
        project = result.scalars().first()
        host = project.server.host
        port = project.server.port

        delete_version_stmt = delete(ProjectVersion).where(ProjectVersion.project_id == project_id)
        delete_spider_stmt = delete(Spider).where(Spider.project_id == project_id)
        delete_stmt = delete(Project).where(Project.id == project_id)

        await session.execute(delete_version_stmt)
        await session.execute(delete_spider_stmt)
        await session.execute(delete_stmt)

        async with aiohttp.ClientSession() as http_session:
            url = f'http://{host}:{port}/delproject.json'
            data = {'project': project.name}
            response = await http_session.post(url, data=data)
            result = await response.json()

            print('result', result)

            if result.get('status') == 'error':
                return Response.fail(data='删除失败', error=result.get('message'))

        await session.commit()

        return Response.success(data='删除成功')


class SpiderView(HTTPMethodView):
    _limit = 18
    get_fields = {
        'page'   : fields.Integer(required=False, default=1),
        'spider' : fields.Str(required=False, default=None),
        'project': fields.Integer(required=False, default=None),
        'version': fields.Str(required=False, default=None),
    }
    put_fields = {
        'id'  : fields.Integer(required=True),
        'desc': fields.Str(required=False, default=None, validate=lambda x: len(x) < 255),
    }
    post_fields = {
        'id'      : fields.Integer(required=True),
        'version' : fields.Str(required=True),
        'settings': fields.Dict(required=True),
    }
    result_fields = {
        'id'             : fields.Str(),
        'name'           : fields.Str(),
        'desc'           : fields.Str(),
        'version'        : fields.Str(attribute='version_code'),
        'create_datetime': fields.DateTime(),
    }

    @params_parse(get_fields, location="query")
    async def get(self, request, kwargs):
        """爬虫列表"""
        page = kwargs.get('page')
        session = request.ctx.session
        async with session.begin():
            count_stmt = select(func.count()).select_from(Spider)
            select_stmt = select(Spider)

            if kwargs.get('spider'):
                count_stmt = count_stmt.where(Spider.name == kwargs['spider'])
                select_stmt = select_stmt.where(Spider.name == kwargs['spider'])

            if kwargs.get('version'):
                count_stmt = count_stmt.where(Spider.version_code == kwargs['version'])
                select_stmt = select_stmt.where(Spider.version_code == kwargs['version'])

            if kwargs.get('project'):
                count_stmt = count_stmt.where(Spider.project_id == kwargs['project'])
                select_stmt = select_stmt.where(Spider.project_id == kwargs['project'])

            count_result = await session.execute(count_stmt)
            spider_count = count_result.scalar()

            select_stmt = select_stmt.order_by(Spider.version_code.desc())
            select_stmt = select_stmt.offset((page - 1) * self._limit).limit(self._limit)
            result = await session.execute(select_stmt)
            item_list = result.scalars().all()

        result_schema = Schema.from_dict(self.result_fields)(many=True)
        data = result_schema.dump(item_list)
        result_data = {'total': spider_count, 'spiders': data}

        return Response.success(data=result_data)

    @params_parse(post_fields, location="json")
    async def post(self, request, kwargs):
        """启动爬虫"""
        session = request.ctx.session
        async with session.begin():
            select_stmt = select(Spider).options(
                selectinload(Spider.project).options(
                    selectinload(Project.server)
                )
            ).where(
                Spider.id == kwargs['id'],
                Spider.version_code == kwargs['version']
            )
            result = await session.execute(select_stmt)
            item = result.scalar()
            if not item:
                log.logger.error('未查询到爬虫，sql： %s' % select_stmt)
                return Response.fail(data='启动失败', code=200)
        url = 'http://{}:{}/schedule.json'.format(
            item.project.server.host,
            item.project.server.port
        )
        post_json = {
            'project' : item.project.name,
            'spider'  : item.name,
            '_version': item.version_code,
            'setting' : kwargs['settings'],
        }
        http_session = aiohttp.ClientSession()
        async with http_session.post(url, json=post_json) as response:
            result_json = await response.json()
            if result_json.get('jobid'):
                job_item = Job(
                    name=result_json.get('jobid'),
                    status='pending',
                    project_id=item.project.id,
                    create_datetime=datetime.datetime.now(),
                )
                async with session.begin():
                    session.add(job_item)
        await http_session.close()

        return Response.success(data='启动成功')

    @params_parse(put_fields, location="json")
    async def put(self, request, kwargs):
        """更新爬虫简介"""
        session = request.ctx.session
        update_stmt = update(Spider).where(
            Spider.id == kwargs['id']
        ).values(desc=kwargs['desc'])

        async with session.begin():
            await session.execute(update_stmt)

        return Response.success(data='更新成功')


class TaskView(HTTPMethodView):
    _limit = 18
    get_fields = {
        'page'   : fields.Integer(required=False, default=1),
        'project': fields.Integer(required=False, default=None),
    }
    post_fields = {
        'name'     : fields.Str(required=True),
        'desc'     : fields.Str(required=False),
        'spider_id': fields.Integer(required=True),
        'trigger'  : fields.Str(required=True),
        'timer'    : fields.Dict(required=True),
        'settings' : fields.Dict(required=True),
    }
    result_fields = {
        'id'       : fields.Integer(),
        'name'     : fields.Str(),
        'desc'     : fields.Str(),
        'spider_id': fields.Integer(),
        'settings' : fields.Str(attribute='task_setting.content'),
        'timer'    : {
            'year'              : fields.Str(attribute='task_timer.year'),
            'month'             : fields.Str(attribute='task_timer.month'),
            'day'               : fields.Str(attribute='task_timer.day'),
            'week'              : fields.Str(attribute='task_timer.week'),
            'day_of_week'       : fields.Str(attribute='task_timer.day_of_week'),
            'hour'              : fields.Str(attribute='task_timer.hour'),
            'minute'            : fields.Str(attribute='task_timer.minute'),
            'second'            : fields.Str(attribute='task_timer.second'),
            'start_date'        : fields.Str(attribute='task_timer.start_date'),
            'end_date'          : fields.Str(attribute='task_timer.end_date'),
            'timezone'          : fields.Str(attribute='task_timer.timezone'),
            'jitter'            : fields.Str(attribute='task_timer.jitter'),
            'misfire_grace_time': fields.Str(attribute='task_timer.misfire_grace_time'),
            'coalesce'          : fields.Str(attribute='task_timer.coalesce'),
            'max_instances'     : fields.Str(attribute='task_timer.max_instances'),
        }
    }

    @params_parse(get_fields, location="query")
    async def get(self, request, kwargs):
        """定时任务列表"""
        print(kwargs)
        session = request.ctx.session
        select_stmt = select(Task).options(
            selectinload(Task.task_timer),
            selectinload(Task.task_setting)
        )
        select_stmt = select_stmt.offset((kwargs['page'] - 1) * self._limit).limit(self._limit)
        print('sql', select_stmt)
        result = await session.execute(select_stmt)
        item_data: list = result.scalars().all()
        print('item data', item_data)

        result_schema = Schema.from_dict(self.result_fields)(many=True)
        data = result_schema.dump(item_data)

        return Response.success(data={'data': data})

    @params_parse(post_fields, location="json")
    async def post(self, request, kwargs):
        """添加定时任务"""

        session = request.ctx.session
        async with session.begin():
            insert_stmt = insert(Task).values(
                name=kwargs.get('name'),
                desc=kwargs.get('desc'),
                spider_id=kwargs.get('spider_id'),
            )

            insert_result = await session.execute(insert_stmt)
            task_id = insert_result.inserted_primary_key[0]

            task_timer = TaskTimer(**kwargs.get('timer'))
            task_timer.create_datetime = datetime.datetime.now()
            task_timer.task_id = task_id

            task_setting = TaskSetting(**kwargs.get('settings'))
            task_setting.create_datetime = datetime.datetime.now()
            task_setting.task_id = task_id

            session.add(task_timer)
            session.add(task_setting)

            scheduler = app.ctx.scheduler
            scheduler.add_job(
                id=kwargs.get('name'),
                func=schedule_task_spider,
                trigger=kwargs.get('trigger'),
                **kwargs.get('timer'),
                kwargs={'task_id': task_id},
            )

        return Response.success(data='创建成功')


class LogView(HTTPMethodView):

    def get(self, request, kwargs):
        pass


async def scheduler_update_job():
    """更新JOB状态"""
    print('scheduler_update_job')
    session = sessionmaker(bind, AsyncSession, expire_on_commit=False, future=True)()
    http_session = aiohttp.ClientSession()
    # 处理逻辑
    # 查询状态pending或running的job
    # noinspection PyUnresolvedReferences
    job_select = select(Job).options(
        selectinload(Job.project).options(
            selectinload(Project.server)
        ),
    ).where(
        Job.status.in_(['running', 'pending'])
    )
    result = await session.execute(job_select)
    job_list = result.scalars()
    for job in job_list:
        host = job.project.server.host
        port = job.project.server.host
        project_name = job.project.name
        url = f'http://{host}:{port}/listjobs.json?project={project_name}'
        async with http_session.get(url) as response:
            job_result = await response.json()

            for job_run in job_result.get('running'):
                if job.scrapyd_job_id == job_run['id']:
                    job.status = 'running'
                    start_datetime = job_run['start_time'].split('.')[0]
                    start_datetime = datetime.datetime.strptime(start_datetime, '%Y-%m-%d %H:%M:%S')
                    job.start_datetime = start_datetime
                    # 计算运行时间
                    now_datetime = datetime.datetime.now()
                    run_time = now_datetime - start_datetime
                    days = run_time.days
                    hours, remainder = divmod(run_time.seconds, 3600)
                    minutes, seconds = divmod(remainder, 60)
                    job.run_time = f'{days}:{hours}:{minutes}.{seconds}'
                    await session.commit()

            for job_fin in job_result.get('finished'):
                if job.scrapyd_job_id == job_fin['id']:
                    start_datetime = job_fin['start_time'].split('.')[0]
                    start_datetime = datetime.datetime.strptime(start_datetime, '%Y-%m-%d %H:%M:%S')
                    job.start_datetime = start_datetime
                    fin_datetime = job_fin['end_time'].split('.')[0]
                    fin_datetime = datetime.datetime.strptime(fin_datetime, '%Y-%m-%d %H:%M:%S')
                    job.finish_datetime = fin_datetime
                    # 计算运行时间
                    run_time = fin_datetime - start_datetime
                    days = run_time.days
                    hours, remainder = divmod(run_time.seconds, 3600)
                    minutes, seconds = divmod(remainder, 60)
                    job.run_time = f'{days}:{hours}:{minutes}.{seconds}'

                    await session.commit()

    # 如果状态为running，更新start_time,status,days,runtime
    # 如果状态为finished，更新start_time,finish_time,status,days,runtime
    # 更新job状态
    await http_session.close()
    await session.commit()
    await session.close()


async def schedule_task_spider(task_id: int):
    """启动爬虫定时任务"""
    print('schedule_task_spider', task_id)
    session = sessionmaker(bind, AsyncSession, expire_on_commit=False, future=True)()
    http_session = aiohttp.ClientSession()

    # 根据task_id查询爬虫对象
    select_task_stmt = select(Task).where(Task.id == task_id).options(
        selectinload(Task.task_timer), selectinload(Task.task_setting)
    )
    task_result = await session.execute(select_task_stmt)
    task = task_result.scalars().first()
    # 根据爬虫对象查询项目对象
    spider_id = task.spider_id
    select_spider_stmt = select(Spider).where(Spider.id == spider_id).options(
        selectinload(Spider.project).options(Project.server)
    )
    spider_result = await session.execute(select_spider_stmt)
    spider = spider_result.scalars().first()

    # 启动爬虫
    host = spider.project.server.host
    port = spider.project.server.port
    url = f'http://{host}:{port}/schedule.json'
    post_data = {
        'project' : spider.project.name,
        'spider'  : spider.name,
        '_version': spider.project.version,
        # 'jobid'   : str(time.time() * 1000),  # 不传递，scrapyd会自动生成jobid  例如："6487ec79947edab326d6db28a2d86511e8247444"
        'settings': json.loads(task.task_setting.content),
        'priority': 0,
    }

    async with session.begin():
        async with http_session.post(url, json=post_data) as response:
            schedule_result = await response.json()
            job_id = schedule_result.get('jobid')

            job_insert_stmt = insert(Job).values(
                name=task.name + job_id,
                static='pending',
                project_id=spider.project.id,
                scrapyd_job_id=job_id,
                create_datetime=datetime.datetime.now()
            )
            await session.execute(job_insert_stmt)

    await http_session.close()
    await session.close()
