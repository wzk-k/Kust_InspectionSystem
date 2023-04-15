# -*- coding: utf-8 -*-
'''
-时间    : 2023/4/15 17:00
-作者 : 王子康
-文件    : api.py
-说明    :
'''
from fastapi import APIRouter
from api.endpoints import person,inspection,user,relative

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(person.router,tags=["人员管理"])
api_router.include_router(inspection.router,tags=["巡查任务管理"])
api_router.include_router(user.router,tags=["管理员管理"])
api_router.include_router(relative.router,tags=["亲属关系管理"])