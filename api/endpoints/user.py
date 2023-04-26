# -*- coding: utf-8 -*-
'''
-时间    : 2023/4/15 17:19
-作者 : 王子康
-文件    : user.py
-说明    :
'''

from common.Base import *
from fastapi import *
router = APIRouter(prefix='/user')
# 添加管理员
@router.post("/addUser",summary="添加管理员")
async def add_user(user : CreatUser ):

    try:
        user1 = session.query(User).filter(User.unifiedNumber == user.unifiedNumber).first()
        if user1:
            return {"code": "0002", "message": "该人员已经注册！"}
        else:
            userid = gen_uuid()
            user_id = userid
            data_user = User(
                userId=userid,
                userName=user.userName,
                password=user.password,
                userSex=user.userSex,
                userPhone=user.userPhone,
                unifiedNumber=user.unifiedNumber
            )
            session.add(data_user)
        session.commit()
        session.close()
    except ArithmeticError:
        return {"code": "0002", "message": "数据库异常"}
    return {"code": 200, "id": user_id}


class LoginUser(BaseModel):
    userName: str
    password: str


@router.post("/login", summary="管理员登录")
async def login_user(
    user: LoginUser
):
    try:
        user = session.query(User).filter(User.userName == user.userName).first()
        session.close()
        if user and user.password == user.password:
            return {"code": 200, "message": "登录成功"}
    except ArithmeticError:
        return {"code": "0002", "message": "数据库异常"}
    return {"code": 400, "message": "登录失败,密码错误或不存在用户！"}


@router.get("/getAmin", summary="管理员登录")
async def get_admin():
    try:
        user = session.query(User).first()
        if user:
            return {"code": 200, "data": user}
    except ArithmeticError:
        return {"code": "0002", "message": "数据库异常"}
    return {"code": 400, "message": "获取失败" }