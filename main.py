import time
from http.client import HTTPException

import pymysql
from fastapi import FastAPI, Depends, File, UploadFile

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, load_only, relationship

from typing import Union, List, Optional
from pydantic import AnyHttpUrl, IPvAnyAddress, BaseModel

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Column, VARCHAR, TEXT, DateTime, and_, or_, ForeignKey
from sqlalchemy.sql import text
from sqlalchemy.sql import func

import datetime

import uvicorn

from db.base_class import gen_uuid

import random

from fastapi.responses import FileResponse

app = FastAPI(title="昆工巡查系统测试文档",
              description="后台接口详情")

# mysql 配置
MYSQL_USERNAME: str = 'root'
MYSQL_PASSWORD: str = "root"
MYSQL_HOST: Union[AnyHttpUrl, IPvAnyAddress] = "127.0.0.1:3306"
MYSQL_DATABASE: str = 'kust_inspection'

# 配置数据库地址：数据库类型+数据库驱动名称://用户名:密码@机器地址:端口号/数据库名
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@" \
                          f"{MYSQL_HOST}/{MYSQL_DATABASE}?charset=utf8mb4"

engine = create_engine(SQLALCHEMY_DATABASE_URL, encoding='utf-8')

# 把当前的引擎绑定给这个会话；
# autocommit：是否自动提交 autoflush：是否自动刷新并加载数据库 bind：绑定数据库引擎
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# 实例化
session = Session()

Base = declarative_base()

class Person(Base):
    __tablename__ = "Person"
    id = Column(
        VARCHAR(32), default=gen_uuid,
        index=True, unique=True, comment="用户id", primary_key=True)
    name = Column(VARCHAR(128),  comment="姓名")
    sex = Column(VARCHAR(128), comment="性别")
    phone = Column(VARCHAR(128),comment="手机号码")
    native_place = Column(VARCHAR(128), nullable=True, comment="籍贯")
    number = Column(Integer, unique=True, comment="编号", autoincrement=True)
    birth_place = Column(VARCHAR(128), nullable=True, comment="出生地")
    work_unit = Column(VARCHAR(128), nullable=True, comment="工作单位")
    unit_level = Column(VARCHAR(128), nullable=True, comment="单位层级")
    unit_location = Column(VARCHAR(128), nullable=True, comment="单位所在地")
    current_position = Column(VARCHAR(128), nullable=True, comment="现任职务")
    proposed_position = Column(VARCHAR(128), nullable=True, comment="拟任职务")
    proposed_dismissal_position = Column(VARCHAR(128), nullable=True, comment="拟免职务")
    graduation_school = Column(VARCHAR(128), nullable=True, comment="毕业学校")
    inspections = relationship("InspectionTask", back_populates="person")
    relatives = relationship("Relatives", foreign_keys="[Relatives.person_id]", back_populates="person")

    def __init__(self, id=None, name=None, sex=None, phone=None, native_place=None,
                 birth_place=None, work_unit=None, unit_level=None, unit_location=None,
                 current_position=None, proposed_position=None, proposed_dismissal_position=None,
                 graduation_school=None):
        self.id = id if id is not None else gen_uuid()
        self.name = name
        self.sex = sex
        self.phone = phone
        self.native_place = native_place
        self.birth_place = birth_place
        self.work_unit = work_unit
        self.unit_level = unit_level
        self.unit_location = unit_location
        self.current_position = current_position
        self.proposed_position = proposed_position
        self.proposed_dismissal_position = proposed_dismissal_position
        self.graduation_school = graduation_school
        # self.number = number
class InspectionTask(Base):
    __tablename__ = "InspectionTask"
    id = Column(VARCHAR(32), primary_key=True, comment="巡视任务ID")
    person_id = Column(VARCHAR(32), ForeignKey("Person.id"), comment="关联的人员ID")
    person = relationship("Person", back_populates="inspections")
    administrative_division = Column(VARCHAR(128), nullable=False, comment="行政区划")
    term = Column(VARCHAR(128), nullable=False, comment="届次")
    round = Column(VARCHAR(128), nullable=False, comment="轮次")
    inspection_start_date = Column(VARCHAR(128), nullable=False, comment="巡视开始时间")
    inspection_end_date = Column(VARCHAR(128), nullable=False, comment="巡视结束时间")
    standard_name = Column(VARCHAR(128), nullable=False, comment="标准名称")
    inspection_group = Column(VARCHAR(128), nullable=False, comment="巡视组别")
    inspected_unit = Column(VARCHAR(128), nullable=False, comment="被巡单位")
    unified_number = Column(Integer, unique=True, comment="统一编号", autoincrement=True)
    talent_pool_type = Column(VARCHAR(128), nullable=True, comment="人才库类型")
    personnel_source = Column(VARCHAR(128), nullable=True, comment="人员来源")
    security_classification = Column(VARCHAR(128), nullable=True, comment="密级标识")

    def __init__(self, id=None, person_id=None, administrative_division=None,
                 term=None, round=None, inspection_start_date=None, inspection_end_date=None,
                 standard_name=None, inspection_group=None, inspected_unit=None,
                 talent_pool_type=None, personnel_source=None, security_classification=None):
        self.id = id
        self.person_id = person_id
        self.administrative_division = administrative_division
        self.term = term
        self.round = round
        self.inspection_start_date = inspection_start_date
        self.inspection_end_date = inspection_end_date
        self.standard_name = standard_name
        self.inspection_group = inspection_group
        self.inspected_unit = inspected_unit
        # self.unified_number = unified_number
        self.talent_pool_type = talent_pool_type
        self.personnel_source = personnel_source
        self.security_classification = security_classification
class User(Base):
    # 定义表名
    __tablename__ = 'User'
    # 定义字段
    # primary_key=True 设置为主键
    id = Column(
        VARCHAR(32), default=gen_uuid,
        index=True, unique=True, comment="用户id", primary_key=True)
    userName = Column(VARCHAR(128), comment="姓名")
    password = Column(VARCHAR(128), comment="密码")
    userSex = Column(VARCHAR(128), comment="性别")
    userPhone = Column(VARCHAR(128), comment="手机号码")
    unifiedNumber = Column(Integer, unique=True, comment="编号", autoincrement=True)


    def __init__(self, userId,userName, password, userSex, userPhone,unifiedNumber):
        self.id = userId
        self.userName = userName
        self.userSex = userSex
        self.userPhone = userPhone
        self.unifiedNumber = unifiedNumber
        self.password = password

class Relatives(Base):
    __tablename__ = 'Relatives'

    id = Column(
        VARCHAR(32), default=gen_uuid,
        index=True, unique=True, comment="id", primary_key=True)
    person_id = Column(VARCHAR(32), ForeignKey('Person.id'), comment="关联的人员ID")
    relative_id = Column(VARCHAR(32), ForeignKey('Person.id'), comment="关联的亲属ID")
    relation = Column(VARCHAR(128), comment="关系")
    person = relationship("Person", foreign_keys="[Relatives.person_id]", back_populates="relatives")
    relative = relationship("Person", foreign_keys="[Relatives.relative_id]")

    def __init__(self, id, person_id, relative_id,relation):
        self.id = id
        self.person_id = person_id
        self.relative_id = relative_id
        self.relation = relation


Base.metadata.create_all(bind=engine)


class CreatPerson(BaseModel):
    name : str
    sex : str
    phone : str
    native_place : str
    # number : str
    birth_place : str
    work_unit : str
    unit_level : str
    unit_location : str
    current_position : str
    proposed_position : str
    proposed_dismissal_position : str
    graduation_school : str
class CreatInspectionTask:
    person_id = str
    person = str
    administrative_division = str
    term = str
    round = str
    inspection_start_date = str
    inspection_end_date = str
    standard_name = str
    inspection_group = str
    inspected_unit = str
    unified_number = str
    talent_pool_type = str
    personnel_source = str
    security_classification = str
class CreatUser(BaseModel):
    userName : str
    password : str
    userSex : str
    userPhone : str
    unifiedNumber : str
class CreatRelatives(BaseModel):
    person_id = str
    relative_id = str
    relation = str

@app.post("/person/addPerson")
async def add_person(person : CreatPerson ):

    try:
        # user1 = session.query(Person).filter(Person.number== person.number).first()
        # if user1:
        #     return {"code": "0002", "message": "该人员已经添加！"}
        # else:
        person_id = gen_uuid()
        data_person = Person(
               id = person_id,
                name=person.name,
                sex=person.sex,
                phone=person.phone,
                native_place=person.native_place,
                # number=person.number,
                birth_place=person.birth_place,
                work_unit=person.work_unit,
                unit_level=person.unit_level,
                unit_location=person.unit_location,
                current_position=person.current_position,
                proposed_position=person.proposed_position,
                proposed_dismissal_position=person.proposed_dismissal_position,
                graduation_school=person.graduation_school
            )
        session.add(data_person)
        session.commit()
        session.close()
    except ArithmeticError:
        return {"code": "0002", "message": "数据库异常"}
    return {"code": 200, "id": person_id}
@app.get("/person/getPersonlist")
async def get_person(number1: Optional[str] = None ):

    try:
        if number1 is not None:
            person = session.query(Person).filter(Person.number == number1).first()
            for relative in person.relatives:
                relative_person = session.query(Person).filter(Person.id == relative.relative_id).first()
                print(session.query(Person).filter(Person.id == relative.relative_id).first().work_unit)
                # if relative_person:
                #     print(f"亲属姓名：{relative_person.name}, 工作单位：{relative_person.work_unit}")

            # person.relatives
            # print(person.relatives)
            return {"code": 200, "data": person}
        else:
            persons = session.query(Person).all()
            return {"code": 200, "data": persons}
        session.commit()
        session.close()
    except ArithmeticError:
        return {"code": "0002", "message": "数据库异常"}
@app.delete("/person/deletePerson")
async def delete_person(person_id:str):
    try:
        # 先查询要删除的记录
        person = session.query(Person).filter(Person.id == person_id).first()
        if not person:
            # 如果记录不存在，抛出 HTTPException 异常
            return {"code": "0002", "message": "该人员未找到！"}
        # 删除记录
        session.delete(person)
        session.commit()
        return {"code": 200, "message": "Person deleted successfully"}
    except Exception as e:
        # 捕获异常，并返回错误信息
        return {"code": "0002", "message": "未知错误"}


# 添加一个新的接口，生成巡视组成员列表
@app.post("/inspection/generate_team")
async def generate_inspection_team(inspected_unit: Optional[str] = "任职单位",native_place:Optional[str] = "籍贯",birth_place:Optional[str] = "出生地",graduation_school:Optional[str] = "毕业院校",
                                   ):
    # 获取所有候选人
    print(inspected_unit,native_place,birth_place,graduation_school)
    candidates = session.query(Person).all()

    print(candidates)
    # 定义一个空列表，用于存储符合条件的巡视组成员
    inspection_team = []
    try:
        for candidate in candidates:
            # 检查回避条件
            avoid_unit = (inspected_unit is not None) and \
                         ((candidate.work_unit == inspected_unit) or
                          any(relative_person.work_unit == inspected_unit
                              for relative in candidate.relatives
                              for relative_person in session.query(Person).filter(Person.id == relative.relative_id)))
            # print(inspected_unit)
            # print(candidate.work_unit)
            avoid_native_place = (native_place is not None) and (candidate.native_place == native_place)
            # print(native_place is not None)
            # print(candidate.native_place == native_place)
            # print(candidate.native_place)
            # print(avoid_native_place)
            avoid_birth_place = (birth_place is not None) and (candidate.birth_place == birth_place)
            avoid_graduation_school = (graduation_school is not None) and (candidate.graduation_school == graduation_school)
            # 如果满足所有回避条件，将候选人添加到巡视组
            if not (avoid_unit or avoid_native_place or avoid_birth_place or avoid_graduation_school):
                inspection_team.append(candidate)
        # print(inspection_team)

        return {"code": 200, "data": [team_member.id for team_member in inspection_team]}
    except ArithmeticError:
        return {"code": "0002", "message": "发生错误"}

# 添加管理员
@app.post("/User/addUser")
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





if __name__ == "__main__":
    # 启动服务，因为我们这个文件叫做 main.py
    # 所以需要启动 main.py 里面的 app
    # 第一个参数 "main:app" 就表示这个含义
    # 然后是 host 和 port 表示监听的 ip 和端口
    uvicorn.run("main:app", host="0.0.0.0", port=8000)

