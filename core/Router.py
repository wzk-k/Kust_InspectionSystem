# -*- coding: utf-8 -*-
'''
-时间    : 2023/4/15 16:41
-作者 : 王子康
-文件    : Router.py
-说明    : 路由聚合
'''

from fastapi import APIRouter
from api.api import *

router = APIRouter()
#API路由
router.include_router(api_router)

