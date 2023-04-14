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
    number = Column(VARCHAR(128), nullable=False, unique=True, comment="编号")
    birth_place = Column(VARCHAR(128), nullable=True, comment="出生地")
    work_unit = Column(VARCHAR(128), nullable=True, comment="工作单位")
    unit_level = Column(VARCHAR(128), nullable=True, comment="单位层级")
    unit_location = Column(VARCHAR(128), nullable=True, comment="单位所在地")
    current_position = Column(VARCHAR(128), nullable=True, comment="现任职务")
    proposed_position = Column(VARCHAR(128), nullable=True, comment="拟任职务")
    proposed_dismissal_position = Column(VARCHAR(128), nullable=True, comment="拟免职务")
    graduation_school = Column(VARCHAR(128), nullable=True, comment="毕业学校")
    inspections = relationship("InspectionTask", back_populates="person")

    def __init__(self, id=None, name=None, sex=None, phone=None, native_place=None,number = None,
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
        self.number = number
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
    unified_number = Column(VARCHAR(128), nullable=False, unique=True, comment="统一编号")
    talent_pool_type = Column(VARCHAR(128), nullable=True, comment="人才库类型")
    personnel_source = Column(VARCHAR(128), nullable=True, comment="人员来源")
    security_classification = Column(VARCHAR(128), nullable=True, comment="密级标识")

    def __init__(self, id=None, person_id=None, administrative_division=None,
                 term=None, round=None, inspection_start_date=None, inspection_end_date=None,
                 standard_name=None, inspection_group=None, inspected_unit=None, unified_number=None,
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
        self.unified_number = unified_number
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
    unifiedNumber = Column(VARCHAR(128), comment="统一编号")


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
    number : str
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
        user1 = session.query(Person).filter(Person.number== person.number).first()
        if user1:
            return {"code": "0002", "message": "该人员已经添加！"}
        else:
            person_id = gen_uuid()
            data_person = Person(
                id = person_id,
                name=person.name,
                sex=person.sex,
                phone=person.phone,
                native_place=person.native_place,
                number=person.number,
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
            person = session.query(Person).filter(Person.number == number1).all()
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
"""
# 更新巡检人员信息
@app.post("/insPerson/updatePerson")
async def update_insp_person(update_person: UpdatePerson):
    try:
        # 查找要更新的Inspection_personnel对象
        user_to_update = session.query(Inspection_personnel).filter(Inspection_personnel.unifiedNumber == update_person.unifiedNumber).first()

        # 如果找到了对象，则更新其属性
        if user_to_update:
            if update_person.userName is not None:
                user_to_update.userName = update_person.userName
            if update_person.userSex is not None:
                user_to_update.userSex = update_person.userSex
            if update_person.userPhone is not None:
                user_to_update.userPhone = update_person.userPhone
            if update_person.nativePlace is not None:
                user_to_update.nativePlace = update_person.nativePlace
            if update_person.birthPlace is not None:
                user_to_update.birthPlace = update_person.birthPlace
            if update_person.workUnit is not None:
                user_to_update.workUnit = update_person.workUnit
            if update_person.UnitLevel is not None:
                user_to_update.UnitLevel = update_person.UnitLevel
            if update_person.UnitPlace is not None:
                user_to_update.UnitPlace = update_person.UnitPlace
            if update_person.currentPosition is not None:
                user_to_update.currentPosition = update_person.currentPosition
            if update_person.administrativeDivision is not None:
                user_to_update.administrativeDivision = update_person.administrativeDivision
            if update_person.term is not None:
                user_to_update.term = update_person.term
            if update_person.round is not None:
                user_to_update.round = update_person.round
            if update_person.inspectionStartDate is not None:
                user_to_update.inspectionStartDate = update_person.inspectionStartDate
            if update_person.inspectionEndDate is not None:
                user_to_update.inspectionEndDate = update_person.inspectionEndDate
            if update_person.standardName is not None:
                user_to_update.standardName = update_person.standardName
            if update_person.inspectionGroup is not None:
                user_to_update.inspectionGroup = update_person.inspectionGroup
            if update_person.inspectedUnit is not None:
                user_to_update.inspectedUnit = update_person.inspectedUnit
            if update_person.talentPoolType is not None:
                user_to_update.talentPoolType = update_person.talentPoolType
            if update_person.personnelSource is not None:
                user_to_update.personnelSource = update_person.personnelSource
            if update_person.securityClassification is not None:
                user_to_update.securityClassification = update_person.securityClassification

            if update_person.currentPosition is not None:
                user_to_update.currentPosition = update_person.currentPosition

            if update_person.level is not None:
                user_to_update.level = update_person.level
            if update_person.proposedPosition is not None:
                user_to_update.proposedPosition = update_person.proposedPosition
            if update_person.proposedDismissalPosition is not None:
                user_to_update.proposedDismissalPosition = update_person.proposedDismissalPosition
            if update_person.appointmentDismissionReason is not None:
                user_to_update.appointmentDismissionReason = update_person.appointmentDismissionReason
            if update_person.graduationSchool is not None:
                user_to_update.graduationSchool = update_person.graduationSchool
            # 将更改提交到数据库
            session.commit()
        else:
            raise HTTPException(status_code=404, detail="Person not found")

    except Exception as e:
        return {"code": "0002", "message": f"Database exception: {str(e)}"}

    return {"code": 200, "message": "Person updated successfully"}
"""


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



"""


@app.post("/user/authLogin")
async def auth_login(user: CreatUser):
    user_id = ""
    try:
        user1 = session.query(User).filter(User.userName == user.nickName).first()
        if user1:
            user_id = user1.id
        else:
            userid = gen_uuid()
            user_id = userid
            data_user = User(
                userid=userid,
                username=user.nickName,
                vi=user.vi
            )
            session.add(data_user)
        session.commit()
        session.close()
    except ArithmeticError:
        return {"code": "0002", "message": "数据库异常"}
    return {"code": 200, "id": user_id}


@app.post("/bwClass/addNewClass")
async def add_new_class(new_class: CreatClass):
    cid = random.randint(10000, 100000).__str__()
    try:
        data_class = Class(
            cid=cid,
            c_name=new_class.cname,
            s_name=new_class.sname,
            id=new_class.id
        )
        data_student = Student(
            sid=gen_uuid(),
            id=new_class.id,
            cid=cid,
            srole='1',
            sname=new_class.sname
        )
        session.add(data_class)
        session.add(data_student)
        session.commit()
        session.close()
    except ArithmeticError:
        return {"code": "0002", "message": "数据库异常"}
    return {"code": 200, "cid": cid}


@app.post("/bwClass/joinNewClass")
async def join_new_class(join_class: JoinClass):
    try:
        data_student = Student(
            sid=gen_uuid(),
            id=join_class.id,
            cid=join_class.cid,
            srole=join_class.srole,
            sname=join_class.sname
        )
        session.add(data_student)
        session.commit()
        session.close()
    except ArithmeticError:
        return {"code": "0002", "message": "数据库异常"}
    return {"code": 200, "cid": join_class.cid }


@app.get("/bwClass/getClassList")
async def get_task_list(
    id: Optional[str] = None
):
    try:
        query_class = session.query(Class).all()
        query_student = session.query(Student).filter(Student.id == id).all()
        data_class = list(query_class)
        data_lists = []
        for i in query_student:
            for item in data_class:
                if item.cid == i.cid:
                    item_len = session.query(Student).filter(Student.cid == item.cid).all()
                    pnumber = len(list(item_len))
                    item.pnumber = pnumber
                    data_lists.append(item)
        session.close()
    except ArithmeticError:
        return {"code": "0002", "message": "数据库异常"}
    return {"code": 200, "data": data_lists}


@app.get("/bwClass/getStudentList")
async def get_student_list(
    cid: Optional[str] = None
):
    try:
        query_student = session.query(Student).all()
        session.close()
    except ArithmeticError:
        return {"code": "0002", "message": "数据库异常"}
    return {"code": 200, "data": list(query_student)}


# 上传文件
@app.post('/uploadFile')
async def get_file(
    file: UploadFile = File(...)
):
    contents = await file.read()
    with open("file/" + file.filename, "wb") as f:
        f.write(contents)
    return ({
            'file_name': file.filename})


# 上传作业任务
@app.post('/uploadFinishFile/{cid}/{userId}')
async def upload_file(
    file: UploadFile = File(...),
    cid: Optional[str] = None,
    userId: Optional[str] = None
):
    contents = await file.read()
    with open("file/" + file.filename, "wb") as f:
        f.write(contents)
    try:
        data_upload = Upload(
            up_id=gen_uuid(),
            tid=cid,
            sid=userId,
            fileName=file.filename
        )
        session.add(data_upload)
        session.commit()
        session.close()
    except ArithmeticError:
        return {"code": "0002", "message": "数据库异常"}
    return ({
            'file_name': file.filename})


@app.get('/bwThings/getFinishFile')
async def get_finish_file(
        id: Optional[str] = None,
):
    try:
        file_list = session.query(Upload).filter(Upload.tid == id).all()
    except ArithmeticError:
        return {"code": "0002", "message": "数据库异常"}
    return ({
        "code": 200,
        'data': list(file_list)})


@app.get("/{some_file_path}")
async def preview_img(
    some_file_path: str
):
    return FileResponse("file/" + some_file_path)


# 新增任务
@app.post("/bwThings/addNewTask")
async def add_new_task(
        task: CreatTask
):
    try:
        data_task = Tasks(
            tid=gen_uuid(),
            cid=task.cid,
            sid=task.sid,
            title=task.title,
            detail=task.detail,
            endtime=task.endtime,
            files=task.files,
        )
        session.add(data_task)
        session.commit()
        session.close()
        return {"code": 200, "message": "新增任务成功！"}
    except ArithmeticError:
        return {"code": "0002", "message": "数据库异常"}


# 新增作业
@app.post("/bwThings/addNewWork")
async def add_new_work(
        work: CreatWork
):
    try:
        data_work = Works(
            wid=gen_uuid(),
            cid=work.cid,
            sid=work.sid,
            title=work.title,
            detail=work.detail,
            endtime=work.endtime,
            files=work.files,
        )
        session.add(data_work)
        session.commit()
        session.close()
        return {"code": 200, "message": "新增任务成功！"}
    except ArithmeticError:
        return {"code": "0002", "message": "数据库异常"}


# 获取任务
@app.get("/bwThings/getTaskList")
async def get_task_list(
    cid: Optional[str] = None,
    sid: Optional[str] = None
):
    try:
        task_list = session.query(Tasks).filter(Tasks.cid == cid).all()
        return {"code": 200, "data": list(task_list)}
    except ArithmeticError:
        return {"code": "0002", "message": "数据库异常"}


#  获取作业
@app.get("/bwThings/getWorkList")
async def get_work_list(
    cid: Optional[str] = None,
    sid: Optional[str] = None
):
    try:
        work_list = session.query(Works).filter(Works.cid == cid).all()
        return {"code": 200, "data": list(work_list)}
    except ArithmeticError:
        return {"code": "0002", "message": "数据库异常"}


class DeleteTask(BaseModel):
    sid: str
    id: str


# 完成任务/作业
@app.post("/bwThings/toFinishTask")
async def delete_task(
    task: DeleteTask
):
    try:
        finish_task = FinishTasks(
            task_id=gen_uuid(),
            tid=task.id,
            sid=task.sid
        )
        session.add(finish_task)
        session.commit()
        session.close()
        return {"code": 200, "message": "提交成功"}
    except ArithmeticError:
        return {"code": "0002", "message": "数据库异常"}


@app.get("/bwThings/endTask/{id}")
async def end_task(
        id:Optional[str] = None,
):
    try:
        task_end = session.query(Tasks).filter(Tasks.id == id).first()
        session.delete(task_end)
        session.commit()
        session.close()
        return {"code": 200, "message": "结束成功"}
    except ArithmeticError:
        return {"code": "0002", "message": "数据库异常"}


@app.get("/bwThings/endWork/{id}")
async def end_work(
        id: Optional[str] = None,
):
    try:
        work_end = session.query(Works).filter(Works.id == id).first()
        session.delete(work_end)
        session.commit()
        session.close()
        return {"code": 200, "message": "结束成功"}
    except ArithmeticError:
        return {"code": "0002", "message": "数据库异常"}


@app.get("/bwThings/getFinishTask")
async def get_finish_task(
        id: Optional[str] = None,
):
    try:
        finish_task_list = session.query(FinishTasks).filter(FinishTasks.sid == id).all()
        session.close()
        return {"code": 200, "data": list(finish_task_list)}
    except ArithmeticError:
        return {"code": "0002", "message": "数据库异常"}


@app.get("/bwThings/getTaskFinishList")
async def get_task_finish_list(
        tid: Optional[str] = None,
):
    try:
        finish_task_list = session.query(FinishTasks).filter(FinishTasks.id == tid).all()
        session.close()
        return {"code": 200, "data": list(finish_task_list)}
    except ArithmeticError:
        return {"code": "0002", "message": "数据库异常"}
"""
if __name__ == "__main__":
    # 启动服务，因为我们这个文件叫做 main.py
    # 所以需要启动 main.py 里面的 app
    # 第一个参数 "main:app" 就表示这个含义
    # 然后是 host 和 port 表示监听的 ip 和端口
    uvicorn.run("main:app", host="0.0.0.0", port=8000)


