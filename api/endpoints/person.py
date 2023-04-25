# -*- coding: utf-8 -*-
'''
-时间    : 2023/4/15 17:01
-作者 : 王子康
-文件    : person.py
-说明    :
'''
from sqlalchemy.exc import SQLAlchemyError

from common.Base import *
from fastapi import *
router = APIRouter(prefix='/person')
"""
添加人才
"""
@router.post("/addPerson",summary="添加人才")
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
                birth_place=person.birth_place,
                work_unit=person.work_unit,
                unit_level=person.unit_level,
                unit_location=person.unit_location,
                current_position=person.current_position,
                proposed_position=person.proposed_position,
                proposed_dismissal_position=person.proposed_dismissal_position,
                personnel_source = person.personnel_source,
                talent_pool_type = person.talent_pool_type,
                graduation_school=person.graduation_school
            )
        session.add(data_person)
        session.commit()
        session.close()
    except ArithmeticError:
        return {"code": "0002", "message": "数据库异常"}
    return {"code": 200, "id": person_id}


"""
获取人员列表
"""
@router.get("/getPersonlist",summary="获取人员列表")
async def get_person(
        number1: Optional[str] = None,
        pageNum: Optional[int] = 1,
        pageSize: Optional[int] = 10,
        name: Optional[str] = '',
        phone: Optional[str] = '',
        native_place: Optional[str] = '',
        work_unit: Optional[str] = '',
):

    try:
        count = len(list(session.query(Person).all()))
        offset_data = pageSize * (pageNum - 1)
        if number1 is not None:
            person = session.query(Person).filter(Person.number == number1).first()
            for relative in person.relatives:
                relative_person = session.query(Person).filter(and_(Person.id == relative.relative_id,
                                                                    Person.name.contains(name),
                                                                    Person.phone.contains(phone),
                                                                    Person.native_place.contains(native_place),
                                                                    Person.work_unit.contains(work_unit)
                                                                    )).first()
                # if relative_person:
                #     print(f"亲属姓名：{relative_person.name}, 工作单位：{relative_person.work_unit}")

            # person.relatives
            # print(person.relatives)
            return {"code": 200, "data": person}
        else:
            persons = session.query(Person).filter(and_(Person.name.contains(name),
                                                    Person.phone.contains(phone),
                                                    Person.native_place.contains(native_place),
                                                    Person.work_unit.contains(work_unit)
                                                    )).offset(offset_data).limit(pageSize).all()
            return {"code": 200, "data": persons, "total": count}
        session.close()
    except ArithmeticError:
        return {"code": "0002", "message": "数据库异常"}


class DelPerson(BaseModel):
    person_id: str


"""
删除人员
"""
@router.post("/deletePerson",summary="删除人员")
async def delete_person(
        person: DelPerson
):
    try:
        # 先查询要删除的记录
        person = session.query(Person).filter(Person.id == person.person_id).first()
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

@router.post("/updatePersn/{person_id}", summary="更新人员", description="更新已经存在的人员信息")
async def update_person(person_id: str, person: UpdatePerson):
    # 查询要更新的Person对象
    person_to_update = session.query(Person).filter(Person.id == person_id).first()

    # 如果找不到Person对象，返回404错误
    if person_to_update is None:
        return {"code": "404", "message": "人员不存在"}

    print(person.dict())
    # 更新Person对象的属性
    for attr, value in person.dict().items():
        if value is not None:
            setattr(person_to_update, attr, value)

    # 将更改提交到数据库
    session.commit()
    session.close()
    # 返回更新后的Person对象
    return {"code": "200", "message": "更新成功"}




