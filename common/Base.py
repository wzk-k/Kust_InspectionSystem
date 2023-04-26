# -*- coding: utf-8 -*-
'''
-时间    : 2023/4/14 18:13
-作者 : 王子康
-文件    : Base.py
-说明    :
'''
from fastapi import FastAPI, Depends, File, UploadFile
from sqlalchemy import *
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
from pydantic import *

# mysql 配置
MYSQL_USERNAME: str = 'root'
MYSQL_PASSWORD: str = "root"
# MYSQL_PASSWORD: str = "labcloud2022!"
# 服务器
# MYSQL_HOST: Union[AnyHttpUrl, IPvAnyAddress] = "222.197.219.49:3300"
# 本地
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

inspection_group_membership = Table(
    "inspection_group_membership",
    Base.metadata,
    Column("inspection_group_id", VARCHAR(32), ForeignKey("InspectionGroup.id"), primary_key=True),
    Column("person_id", VARCHAR(32), ForeignKey("Person.id"), primary_key=True)
)
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
    talent_pool_type = Column(VARCHAR(128), nullable=True, comment="人才库类型")
    personnel_source = Column(VARCHAR(128), nullable=True, comment="人员来源")
    relatives = relationship("Relatives", foreign_keys="[Relatives.person_id]", back_populates="person")
    inspection_groups = relationship("InspectionGroup", secondary=inspection_group_membership, back_populates="members")

    def __init__(self, id=None, name=None, sex=None, phone=None, native_place=None,
                 birth_place=None, work_unit=None, unit_level=None, unit_location=None,
                 current_position=None, proposed_position=None, proposed_dismissal_position=None,
                 graduation_school=None, number=None, talent_pool_type=None, personnel_source=None):
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
        self.number = number
        self.talent_pool_type = talent_pool_type
        self.personnel_source = personnel_source
        # self.number = number


class InspectionTask(Base):
    __tablename__ = "InspectionTask"
    id = Column(VARCHAR(32), primary_key=True, comment="巡视任务ID")
    # person = relationship("Person", back_populates="inspections")
    administrative_division = Column(VARCHAR(128), comment="行政区划")
    term = Column(VARCHAR(128), comment="届次")
    round = Column(VARCHAR(128),  comment="轮次")
    inspection_start_date = Column(VARCHAR(128),  comment="巡视开始时间")
    inspection_end_date = Column(VARCHAR(128),  comment="巡视结束时间")
    standard_name = Column(VARCHAR(128),  comment="标准名称")
    # inspection_group_id = Column(VARCHAR(128),  comment="巡视组别ID")
    inspected_unit = Column(VARCHAR(128),  comment="被巡单位")
    unified_number = Column(Integer, unique=True, comment="统一编号", autoincrement=True)
    security_classification = Column(VARCHAR(128),  comment="密级标识")
    inspection_groups = relationship("InspectionGroup", back_populates="task")  # 和group建立关系
    def __init__(self, id=None,  administrative_division=None,
                 term=None, round=None, inspection_start_date=None, inspection_end_date=None,
                 standard_name=None, inspection_group=None, inspected_unit=None,
                  security_classification=None):
        self.id = id
        self.administrative_division = administrative_division
        self.term = term
        self.round = round
        self.inspection_start_date = inspection_start_date
        self.inspection_end_date = inspection_end_date
        self.standard_name = standard_name
        self.inspection_group = inspection_group
        self.inspected_unit = inspected_unit
        self.security_classification = security_classification


class User(Base):
    # 定义表名
    __tablename__ = 'User'
    # 定义字段
    # primary_key=True 设置为主键
    id = Column(
        VARCHAR(32), default=gen_uuid,
        index=True, unique=True, comment="用户id", primary_key=True)
    email = Column(VARCHAR(128), comment="用户邮箱")
    userName = Column(VARCHAR(128), comment="用户名称")
    password = Column(VARCHAR(128), comment="密码")
    userSex = Column(VARCHAR(128), comment="性别")
    phonenumber = Column(VARCHAR(128), comment="手机号码")
    dept = Column(VARCHAR(128), comment="所属部门")
    unifiedNumber = Column(Integer, unique=True, comment="编号", autoincrement=True)


    def __init__(self, userId,userName, password, userSex, userPhone,unifiedNumber, email, dept):
        self.id = userId
        self.userName = userName
        self.phonenumber = userPhone
        self.unifiedNumber = unifiedNumber
        self.password = password
        self.email = email
        self.userSex = userSex
        self.dept = dept


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

    def __init__(self, id=None, person_id=None, relative_id=None, relation=None):
        self.id = id if id is not None else gen_uuid()
        self.person_id = person_id
        self.relative_id = relative_id
        self.relation = relation


class InspectionGroup(Base):
    __tablename__ = "InspectionGroup"
    id = Column(VARCHAR(32), default=gen_uuid, primary_key=True, comment="巡视组ID")
    name = Column(VARCHAR(128), nullable=False, comment="巡视组名称")
    task_id = Column(VARCHAR(32), ForeignKey("InspectionTask.id"), comment="关联的巡视任务ID")
    members = relationship("Person", secondary=inspection_group_membership, back_populates="inspection_groups")
    task = relationship("InspectionTask", back_populates="inspection_groups")  # 和任务建立关系

    def __init__(self, id=None, name=None, task_id=None):
        self.id = id
        self.name = name
        self.task_id = task_id


class CreateInspectionTask(BaseModel):
    administrative_division: str
    term: str
    round: str
    inspection_start_date: str
    inspection_end_date: str
    standard_name: str
    # inspection_group_id: str
    inspected_unit: str
    security_classification: str


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
    talent_pool_type : str
    personnel_source : str
    graduation_school : str


class CreatInspectionTask:
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


class CreateInspectionGroup(BaseModel):
    name: str
    task_id: str


class AddPersonToGroupRequest(BaseModel):
    group_id: str
    person_ids: List[str]


# 更新人员信息的模型
class UpdatePerson(BaseModel):
    name: Optional[str] = Field(None, description="姓名")
    sex: Optional[str] = Field(None, description="性别")
    phone: Optional[str] = Field(None, description="手机号码")
    native_place: Optional[str] = Field(None, description="籍贯")
    birth_place: Optional[str] = Field(None, description="出生地")
    work_unit: Optional[str] = Field(None, description="工作单位")
    unit_level: Optional[str] = Field(None, description="单位层级")
    unit_location: Optional[str] = Field(None, description="单位所在地")
    current_position: Optional[str] = Field(None, description="现任职务")
    proposed_position: Optional[str] = Field(None, description="拟任职务")
    proposed_dismissal_position: Optional[str] = Field(None, description="拟免职务")
    graduation_school: Optional[str] = Field(None, description="毕业学校")
    talent_pool_type: Optional[str] = Field(None, description="人才库类型")
    personnel_source: Optional[str] = Field(None, description="人员来源")


# 添加亲属关系的模型
class RelativeCreate(BaseModel):
    person_id: str
    relative_id: str
    relation: str


class RelativesOut(BaseModel):
    id: str
    person_id: str
    relative_id: str
    relation: str

    class Config:
        orm_mode = True

class genTeam(BaseModel):
    inspected_unit: str
    native_place: str
    birth_place: str
    graduation_school: str