# -*- coding: utf-8 -*-
'''
-时间    : 2023/4/15 17:13
-作者 : 王子康
-文件    : inspection.py
-说明    : 巡查任务
'''

from common.Base import *
from fastapi import *
from typing import List, Dict, Any
router = APIRouter(prefix='/inspection')
"""
添加巡查任务
"""
@router.post("/addTask",summary="添加巡查任务")
async def add_inspection_task(task: CreateInspectionTask):
    try:
        print(task)
        task_id = gen_uuid()
        data_task = InspectionTask(
            id=task_id,
            administrative_division=task.administrative_division,
            term=task.term,
            round=task.round,
            inspection_start_date=task.inspection_start_date,
            inspection_end_date=task.inspection_end_date,
            standard_name=task.standard_name,
            # inspection_group=task.inspection_group_id,
            inspected_unit=task.inspected_unit,
            security_classification=task.security_classification,
        )
        session.add(data_task)
        session.commit()
        session.close()
    except ArithmeticError:
        return {"code": "0002", "message": "数据库异常"}
    return {"code": 200, "id": task_id}



"""
添加规避规则
"""
@router.post("/generate_team",summary="添加规避规则")
async def generate_inspection_team(
        # inspected_unit: Optional[str] = "任职单位",native_place:Optional[str] = "籍贯",birth_place:Optional[str] = "出生地",graduation_school:Optional[str] = "毕业院校",
        rule: genTeam
                                   ):
    # 获取所有候选人
    candidates = session.query(Person).all()

    print(candidates)
    # 定义一个空列表，用于存储符合条件的巡视组成员
    inspection_team = []
    try:
        for candidate in candidates:
            # 检查回避条件
            # 1.a)	回避本人任职单位以及亲属关系任职单位承担巡视巡察工作
            avoid_unit = (rule.inspected_unit is not None) and \
                         ((candidate.work_unit == rule.inspected_unit) or
                          any(relative_person.work_unit == rule.inspected_unit
                              for relative in candidate.relatives
                              for relative_person in session.query(Person).filter(Person.id == relative.relative_id)))
            for relative in candidate.relatives:
                for relative_person in session.query(Person).filter(Person.id == relative.relative_id):
                    print("--------------------------")
                    print(relative_person.work_unit)
                    print("--------------------------")
            # print(inspected_unit)
            # print(candidate.work_unit)
            # b)	回避本人所在籍贯承担巡视巡察工作
            avoid_native_place = (rule.native_place is not None) and (candidate.native_place == rule.native_place)
            # print(native_place is not None)
            # print(candidate.native_place == native_place)
            # print(candidate.native_place)
            # print(avoid_native_place)
            # c)	回避本人出生地承担巡视巡察工作
            avoid_birth_place = (rule.birth_place is not None) and (candidate.birth_place == rule.birth_place)
            # e)	回避本人毕业院校承担巡视巡察工作
            avoid_graduation_school = (rule.graduation_school is not None) and (candidate.graduation_school == rule.graduation_school)
            # 如果满足所有回避条件，将候选人添加到巡视组
            if not (avoid_unit or avoid_native_place or avoid_birth_place or avoid_graduation_school):
                inspection_team.append(candidate)
        # print(inspection_team)

        return {"code": 200, "data": inspection_team}
    except ArithmeticError:
        return {"code": "0002", "message": "发生错误"}


# 根据巡查任务ID获取巡视组
@router.get("/{task_id}/groups", summary="根据巡查任务ID获取巡视组")
async def get_groups_by_task(task_id: str):
    try:
        groups = session.query(InspectionGroup).filter(InspectionGroup.task_id == task_id).all()
        return groups
    except Exception as e:
        return {"code": "0001", "message": f"数据库异常: {e}"}


@router.get("/allGroups", summary="根据巡查任务ID获取巡视组")
async def get_groups_by_task(
        pageNum: Optional[int] = 1,
        pageSize: Optional[int] = 10,
):
    try:
        count = len(list(session.query(InspectionGroup).all()))
        offset_data = pageSize * (pageNum - 1)
        groups = session.query(InspectionGroup).offset(offset_data).limit(pageSize).all()
        session.close()
        return {"code": 200, "data": groups, "total": count}
    except Exception as e:
        return {"code": "0001", "message": f"数据库异常: {e}"}


# 获取巡查任务列表
@router.get("/tasks", summary="获取巡查任务列表")
async def list_inspection_tasks(
        pageNum: Optional[int] = 1,
        pageSize: Optional[int] = 10,
):
    try:
        count = len(list(session.query(InspectionTask).all()))
        offset_data = pageSize * (pageNum - 1)
        tasks = session.query(InspectionTask).offset(offset_data).limit(pageSize).all()
        return {"code": 200, "data": tasks, "total": count}
    except Exception as e:
        return {"code": "0001", "message": f"数据库异常: {e}"}


# """
# # 获取巡视任务列表
#
# 包括组和成员
# # """
#
#
# @router.get("/taskList", response_model=Any, summary="获取巡视任务列表")
# async def list_inspection_tasks():
#     tasks = session.query(InspectionTask).all()
#
#     result = []
#     for task in tasks:
#         groups = session.query(InspectionGroup).filter(InspectionGroup.task_id == task.id).all()
#
#         task_groups = []
#         for group in groups:
#             members = session.query(Person).join(inspection_group_membership).filter(
#                 inspection_group_membership.c.inspection_group_id == group.id).all()
#             member_list = []
#             for member in members:
#                 member_dict = member.__dict__
#                 member_dict.pop('_sa_instance_state', None)
#
#                 # 获取亲属信息并添加到成员字典中
#                 relatives = session.query(Relatives).filter(Relatives.person_id == member.id).all()
#                 relative_list = []
#                 for relative in relatives:
#                     relative_dict = relative.__dict__
#                     relative_dict.pop('_sa_instance_state', None)
#                     relative_list.append(relative_dict)
#
#                 member_dict['relatives'] = relative_list
#                 member_list.append(member_dict)
#
#             group_info = {
#                 'group': group.__dict__,
#                 'members': member_list
#             }
#             group_info['group'].pop('_sa_instance_state', None)
#
#             task_groups.append(group_info)
#
#         task_info = {
#             'task': task.__dict__,
#             'groups': task_groups
#         }
#         task_info['task'].pop('_sa_instance_state', None)
#
#         result.append(task_info)
#
#     return {"code": 200, "data": result}



# @router.get("/taskList", response_model=Any,summary="获取巡视任务列表")
# async def list_inspection_tasks():
#     tasks = session.query(InspectionTask).all()
#
#     result = []
#     for task in tasks:
#         groups = session.query(InspectionGroup).filter(InspectionGroup.task_id == task.id).all()
#
#         task_groups = []
#         for group in groups:
#             members = session.query(Person).join(inspection_group_membership).filter(inspection_group_membership.c.inspection_group_id == group.id).all()
#             member_list = [member.__dict__ for member in members]
#             for member in member_list:
#                 member.pop('_sa_instance_state', None)
#
#             group_info = {
#                 'group': group.__dict__,
#                 'members': member_list
#             }
#             group_info['group'].pop('_sa_instance_state', None)
#
#             task_groups.append(group_info)
#
#         task_info = {
#             'task': task.__dict__,
#             'groups': task_groups
#         }
#         task_info['task'].pop('_sa_instance_state', None)
#
#         result.append(task_info)
#
#     return {"code": 200, "data": result}

"""
# 根据任务ID查询
# """
@router.get("/inspection/{task_id}/groupMembers", response_model=Any,summary="根据任务ID查询")
async def get_group_members(task_id: str):
    try:
        task = session.query(InspectionTask).filter(InspectionTask.id == task_id).one()
    except Exception as e:
        return {"code": "0002", "message": "任务未找到"}
    groups = session.query(InspectionGroup).filter(InspectionGroup.task_id == task_id).all()
    result = []
    for group in groups:
        members = session.query(Person).join(inspection_group_membership).filter(
            inspection_group_membership.c.inspection_group_id == group.id).all()
        member_list = [member.__dict__ for member in members]
        for member in member_list:
            member.pop('_sa_instance_state', None)

        group_info = {
            'task': task.__dict__,
            'group': group.__dict__,
            'members': member_list
        }
        group_info['task'].pop('_sa_instance_state', None)
        group_info['group'].pop('_sa_instance_state', None)

        result.append(group_info)
        print(result)

    return {"code": 200, "data": result}