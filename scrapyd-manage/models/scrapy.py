# -*- coding: utf-8 -*-
# @Time    : 2021/9/26 11:10
# @Author  : 10867
# @FileName: scrapy.py
# @Software: PyCharm
from datetime import datetime
from copy import copy

from sqlalchemy import Column, ForeignKey, Index, String
from sqlalchemy.dialects.mysql import DATETIME, INTEGER, TINYINT, BOOLEAN
from sqlalchemy.orm import relationship

from models import Base


class BaseModel(Base):
    __abstract__ = True
    create_datetime = Column(DATETIME, doc='创建时间')
    update_datetime = Column(DATETIME, default=datetime.now(), doc='更新时间')

    def to_dict(self):
        _dict = copy(self.__dict__)
        if "_sa_instance_state" in _dict:
            del _dict["_sa_instance_state"]
        return _dict


class Server(BaseModel):
    __tablename__ = 'scrapy_server'

    id = Column(INTEGER(11), primary_key=True)
    host = Column(String(50), nullable=False)
    port = Column(String(5), nullable=False)
    auth = Column(BOOLEAN, nullable=False)
    auth_username = Column(String(50), nullable=True)
    auth_password = Column(String(50), nullable=True)

    info = relationship(
        'ServerInfo',
        uselist=False,
        cascade="all, delete",
        passive_deletes=True
    )
    project = relationship('Project', back_populates='server')


class ServerInfo(BaseModel):
    __tablename__ = 'scrapy_server_info'

    id = Column(INTEGER(11), primary_key=True)
    hostname = Column(String(50), nullable=False)
    status = Column(String(10), nullable=False)
    finished = Column(INTEGER(5), nullable=True)
    pending = Column(INTEGER(5), nullable=False)
    running = Column(INTEGER(5), nullable=False)

    server_id = Column(INTEGER, ForeignKey('scrapy_server.id', ondelete='CASCADE'))


class Project(BaseModel):
    __tablename__ = 'scrapy_project'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(100), nullable=False)
    desc = Column(String(255), default='', nullable=False)
    server_id = Column(ForeignKey('scrapy_server.id'), nullable=False)

    server = relationship('Server', back_populates='project', uselist=False)
    jobs = relationship('Job', back_populates='project')
    version = relationship(
        'ProjectVersion',
        uselist=True,
        cascade="all, delete",
        passive_deletes=True
    )
    spiders = relationship(
        'Spider',
        cascade="all, delete",
        passive_deletes=True,
        back_populates='project'
    )


class ProjectVersion(BaseModel):
    __tablename__ = 'scrapy_project_version'
    id = Column(INTEGER(11), primary_key=True)
    code = Column(String(20), nullable=False)
    is_delete = Column(BOOLEAN, nullable=False, default=False, doc='是否删除')
    is_spider = Column(BOOLEAN, nullable=False, default=False, doc='是否获取爬虫列表，写入Spider表')
    project_id = Column(INTEGER, ForeignKey('scrapy_project.id'))


class Spider(BaseModel):
    __tablename__ = 'scrapy_spider'
    id = Column(INTEGER(11), primary_key=True)

    name = Column(String(50), doc='爬虫名称')
    desc = Column(String(255), doc='爬虫简介')
    project_id = Column(INTEGER, ForeignKey('scrapy_project.id'))
    version_code = Column(String(20), nullable=False)

    project = relationship('Project', uselist=False)
    tasks = relationship('Task', back_populates='spider')


class Task(BaseModel):
    __tablename__ = 'scrapy_task'
    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(50), nullable=False, doc='任务名称')
    desc = Column(String(255), nullable=True, doc='任务简介')
    spider_id = Column(INTEGER, ForeignKey('scrapy_spider.id'), nullable=False)

    spider = relationship('Spider', uselist=False)

    task_timer = relationship(
        'TaskTimer',
        uselist=False,
        cascade="all, delete",
        passive_deletes=True
    )

    task_setting = relationship(
        'TaskSetting',
        uselist=False,
        cascade="all, delete",
        passive_deletes=True
    )


class TaskTimer(BaseModel):
    __tablename__ = 'scrapy_task_timer'
    id = Column(INTEGER(11), primary_key=True)
    year = Column(String(5))
    month = Column(String(5))
    day = Column(String(5))
    week = Column(String(20))
    day_of_week = Column(String(20))
    hour = Column(String(20))
    minute = Column(String(20))
    second = Column(String(20))
    start_date = Column(String(20))
    end_date = Column(String(20))
    timezone = Column(String(20))
    jitter = Column(String(20))
    misfire_grace_time = Column(String(20))
    coalesce = Column(String(20))
    max_instances = Column(String(20))
    task_id = Column(INTEGER, ForeignKey('scrapy_task.id', ondelete='CASCADE'))


class TaskSetting(BaseModel):
    __tablename__ = 'scrapy_task_setting'
    id = Column(INTEGER(11), primary_key=True)
    content = Column(String(1000), nullable=True)
    task_id = Column(INTEGER, ForeignKey('scrapy_task.id', ondelete='CASCADE'))


class Job(BaseModel):
    __tablename__ = "scrapy_job"
    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(100), nullable=False)
    status = Column(String(20), nullable=False, doc='状态')
    is_delete = Column(BOOLEAN, default=False)
    finish_datetime = Column(DATETIME, doc='完成时间')
    start_datetime = Column(DATETIME, doc='完成时间')
    run_time = Column(String(100), default='', doc='运行时长')
    items = Column(INTEGER(11), default=0, doc='数据条数')
    pages = Column(INTEGER(11), default=0, doc='请求数量')
    project_id = Column(INTEGER, ForeignKey('scrapy_project.id'))
    scrapyd_job_id = Column(String(100), nullable=False)  # 启动scrapyd返回的jobid

    project = relationship('Project', uselist=False)


__all__ = [
    'BaseModel',
    'Server',
    'ServerInfo',
    'Project',
    'ProjectVersion',
    'Spider',
    'Task',
    'TaskTimer',
    'TaskSetting',
]

if __name__ == '__main__':
    from sqlalchemy.engine.url import URL
    from sqlalchemy import create_engine

    drivername = 'mysql+pymysql'
    username = 'root'
    password = 'zh@852456'
    host = '192.168.125.31'
    port = '3306'
    database = 'sanic_spider'

    connect_url = URL(drivername=drivername, username=username, password=password,
                      host=host, port=port, database=database)

    engine = create_engine(connect_url, echo=True)
    Base.metadata.create_all(engine)
