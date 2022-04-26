# -*- coding: utf-8 -*-
# @Time    : 2022/4/25 15:00
# @Author  : 10867
# @FileName: routes.py
# @Software: PyCharm
from apps.spider import bp, ServerView, ProjectView, SpiderView, TaskView

bp.add_route(ServerView.as_view(), "/server")
bp.add_route(ProjectView.as_view(), "/project")
bp.add_route(SpiderView.as_view(), "/spider")
bp.add_route(TaskView.as_view(), "/task")