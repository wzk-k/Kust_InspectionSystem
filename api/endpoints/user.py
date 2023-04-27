# -*- coding: utf-8 -*-
'''
-时间    : 2023/4/15 17:19
-作者 : 王子康
-文件    : user.py
-说明    :
'''

from common.Base import *
from fastapi import *
from pymysql.err import OperationalError
import time
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
        # session.commit()
        # session.close()
    except ArithmeticError:
        return {"code": "0002", "message": "数据库异常"}
    finally:
        session.commit()
        session.close()
    return {"code": 200, "id": user_id}


class LoginUser(BaseModel):
    userName: str
    password: str


# @router.post("/login", summary="管理员登录")
# async def login_user(
#     user: LoginUser
# ):
#     try:
#         user = session.query(User).filter(User.userName == user.userName).first()
#         if user and user.password == user.password:
#             session.close()
#             return {"code": 200, "message": "登录成功"}
#     except ArithmeticError:
#         return {"code": "0002", "message": "数据库异常"}
#     return {"code": 400, "message": "登录失败,密码错误或不存在用户！"}

@router.post("/login", summary="管理员登录")
async def login_user(user: LoginUser):
    # max_retries = 3

    # for attempt in range(max_retries):
        try:
            user1 = session.query(User).filter(User.userName == user.userName).first()
            # if user and User.password == user.password:
            if user1 and user1.password == user.password:
                return {"code": 200, "message": "登录成功"}
        except OperationalError as e:
            # if e.args[0] == 1213 and attempt < max_retries - 1:  # Deadlock error
            #     time.sleep(0.1)  # Wait for a short time before retrying
            session.rollback()
            return {"code": "0002", "message": "数据库异常"}
            # else:
            #     return {"code": "0002", "message": "数据库异常"}
        except ArithmeticError:
            session.rollback()
            return {"code": "0002", "message": "数据库异常"}
        finally:
            session.close()
            print("关闭了连接...")

        return {"code": 400, "message": "登录失败,密码错误或不存在用户！"}





@router.get("/getAmin", summary="管理员登录")
async def get_admin():
    try:
        user = session.query(User).first()

        if user:
            print(user)
            return {"code": 200, "data": user}
            print("2")
    except ArithmeticError:
        session.rollback()
        return {"code": "0002", "message": "数据库异常"}
    finally:
        session.close()
        print("关闭了连接...")

    return {"code": 400, "message": "获取失败" }