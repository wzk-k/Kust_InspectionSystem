# -*- coding: utf-8 -*-
'''
-时间    : 2023/4/16 8:52
-作者 : 王子康
-文件    : ins_group.py
-说明    :
'''
from common.Base import *
from fastapi import *
from typing import List, Dict, Any
router = APIRouter(prefix='/insgroup')

"""
为巡查任务添加组
"""
@router.post("/addGroup",summary="为巡查任务添加组")
async def add_inspection_group(group: CreateInspectionGroup):
    try:
        group_id = gen_uuid()
        data_group = InspectionGroup(
            id=group_id,
            name=group.name,
            task_id=group.task_id
        )
        session.add(data_group)
        session.commit()
        session.close()
    except ArithmeticError:
        return {"code": "0002", "message": "数据库异常"}
    return {"code": 200, "id": group_id}

"""
添加人员（符合规则的人员）到组中
"""
@router.post("/add_person_to_group",summary="添加人员（符合规则的人员）到组中")
async def add_person_to_group(request: AddPersonToGroupRequest):
    try:
        # 根据 group_id 查询出对应的 InspectionGroup 对象
        group = session.query(InspectionGroup).filter(InspectionGroup.id == request.group_id).first()

        if not group:
            return {"code": "0003", "message": "组不存在"}

        # 遍历 person_ids 并将每个人员添加到组中
        for person_id in request.person_ids:
            person = session.query(Person).filter(Person.id == person_id).first()

            if not person:
                return {"code": "0004", "message": f"人员ID {person_id} 不存在"}

            # 将满足规避规则的人员添加到组中
            group.members.append(person)

        # 提交更改并关闭会话
        session.commit()
        session.close()

    except ArithmeticError:
        return {"code": "0002", "message": "数据库异常"}

    return {"code": 200, "message": "人员添加成功"}


@router.get("/{group_id}/members", summary="查询巡视组成员")
async def get_group_members(group_id: str):
    try:
        group = session.query(InspectionGroup).filter(InspectionGroup.id == group_id).first()
        if not group:
            return {"code": "0001", "message": "巡视组未找到"}

        members = session.query(Person).join(inspection_group_membership).filter(
            inspection_group_membership.c.inspection_group_id == group.id).all()

        member_list = []
        for member in members:
            member_dict = member.__dict__
            member_dict.pop('_sa_instance_state', None)
            member_list.append(member_dict)

        return {"code": 200, "members": member_list}

    except Exception as e:
        return {"code": "0002", "message": f"数据库异常: {e}"}

# 删除组成员
@router.delete("/{group_id}/member/{member_id}", summary="从巡视组中删除成员")
async def delete_group_member(group_id: str, member_id: str):
    try:
        group = session.query(InspectionGroup).filter(InspectionGroup.id == group_id).first()
        if not group:
            return {"code": "0001", "message": "巡视组未找到"}

        member = session.query(Person).filter(Person.id == member_id).first()
        if not member:
            return {"code": "0002", "message": "成员未找到"}

        group.members.remove(member)
        session.commit()

        return {"code": 200, "message": "成员已从巡视组中移除"}

    except Exception as e:
        return {"code": "0003", "message": f"数据库异常: {e}"}





# # 修改组成员
# @router.put("/group/{group_id}/members", summary="修改巡视组成员")
# async def update_group_members(group_id: str, new_member_ids: List[str]):
#     try:
#         group = session.query(InspectionGroup).filter(InspectionGroup.id == group_id).first()
#         if not group:
#             return {"code": "0001", "message": "巡视组未找到"}
#
#         new_members = session.query(Person).filter(Person.id.in_(new_member_ids)).all()
#
#         # 清空原成员列表
#         group.members = []
#
#         # 添加新成员
#         group.members.extend(new_members)
#         db.commit()
#
#         return {"code": 200, "message": "巡视组成员已更新"}
#
#     except Exception as e:
#         return {"code": "0003", "message": f"数据库异常: {e}"}

# # 修改组成员信息
# @router.put("/group/{group_id}/member/{member_id}", summary="修改巡视组成员信息")
# async def update_group_member(group_id: str, member_id: str, member_update: schemas.PersonUpdate, db: Session = Depends(get_db)):
#     try:
#         group = db.query(models.InspectionGroup).filter(models.InspectionGroup.id == group_id).first()
#         if not group:
#             return {"code": "0001", "message": "巡视组未找到"}
#
#         member = db.query(models.Person).filter(models.Person.id == member_id).first()
#         if not member:
#             return {"code": "0002", "message": "成员未找到"}
#
#         # 更新成员信息
#         for key, value in member_update.dict().items():
#             if value is not None:
#                 setattr(member, key, value)
#
#         db.commit()
#
#         return {"code": 200, "message": "成员信息已更新"}
#
#     except Exception as e:
#         return {"code": "0003", "message": f"数据库异常: {e}"}