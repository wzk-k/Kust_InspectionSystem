
from common.Base import *
from typing import List, Dict, Any
from core import Router

app = FastAPI(title="昆工巡查系统测试文档",
              description="后台接口详情")

app.include_router(Router.router)





# """
# 添加人才
# """
# @app.post("/person/addPerson",summary="添加人才")
# async def add_person(person : CreatPerson ):
#
#     try:
#         # user1 = session.query(Person).filter(Person.number== person.number).first()
#         # if user1:
#         #     return {"code": "0002", "message": "该人员已经添加！"}
#         # else:
#         person_id = gen_uuid()
#         data_person = Person(
#                 id = person_id,
#                 name=person.name,
#                 sex=person.sex,
#                 phone=person.phone,
#                 native_place=person.native_place,
#                 birth_place=person.birth_place,
#                 work_unit=person.work_unit,
#                 unit_level=person.unit_level,
#                 unit_location=person.unit_location,
#                 current_position=person.current_position,
#                 proposed_position=person.proposed_position,
#                 proposed_dismissal_position=person.proposed_dismissal_position,
#                 personnel_source = person.personnel_source,
#                 talent_pool_type = person.talent_pool_type,
#                 graduation_school=person.graduation_school
#             )
#         session.add(data_person)
#         session.commit()
#         session.close()
#     except ArithmeticError:
#         return {"code": "0002", "message": "数据库异常"}
#     return {"code": 200, "id": person_id}
#
#
# """
# 获取人员列表
# """
# @app.get("/person/getPersonlist",summary="获取人员列表")
# async def get_person(number1: Optional[str] = None ):
#
#     try:
#         if number1 is not None:
#             person = session.query(Person).filter(Person.number == number1).first()
#             for relative in person.relatives:
#                 relative_person = session.query(Person).filter(Person.id == relative.relative_id).first()
#                 print(session.query(Person).filter(Person.id == relative.relative_id).first().work_unit)
#                 # if relative_person:
#                 #     print(f"亲属姓名：{relative_person.name}, 工作单位：{relative_person.work_unit}")
#
#             # person.relatives
#             # print(person.relatives)
#             return {"code": 200, "data": person}
#         else:
#             persons = session.query(Person).all()
#             return {"code": 200, "data": persons}
#         session.commit()
#         session.close()
#     except ArithmeticError:
#         return {"code": "0002", "message": "数据库异常"}
#
# """
# 删除人员
# """
# @app.delete("/person/deletePerson",summary="删除人员")
# async def delete_person(person_id:str):
#     try:
#         # 先查询要删除的记录
#         person = session.query(Person).filter(Person.id == person_id).first()
#         if not person:
#             # 如果记录不存在，抛出 HTTPException 异常
#             return {"code": "0002", "message": "该人员未找到！"}
#         # 删除记录
#         session.delete(person)
#         session.commit()
#         return {"code": 200, "message": "Person deleted successfully"}
#     except Exception as e:
#         # 捕获异常，并返回错误信息
#         return {"code": "0002", "message": "未知错误"}
#
#
#
# """
# 添加巡查任务
# """
# @app.post("/inspection/addTask",summary="添加巡查任务")
# async def add_inspection_task(task: CreateInspectionTask):
#     try:
#         task_id = gen_uuid()
#         data_task = InspectionTask(
#             id=task_id,
#             administrative_division=task.administrative_division,
#             term=task.term,
#             round=task.round,
#             inspection_start_date=task.inspection_start_date,
#             inspection_end_date=task.inspection_end_date,
#             standard_name=task.standard_name,
#             inspection_group=task.inspection_group_id,
#             inspected_unit=task.inspected_unit,
#             security_classification=task.security_classification,
#         )
#         session.add(data_task)
#         session.commit()
#         session.close()
#     except ArithmeticError:
#         return {"code": "0002", "message": "数据库异常"}
#     return {"code": 200, "id": task_id}
#
#
#
# """
# 为巡查任务添加组
# """
# @app.post("/inspection/addGroup",summary="为巡查任务添加组")
# async def add_inspection_group(group: CreateInspectionGroup):
#     try:
#         group_id = gen_uuid()
#         data_group = InspectionGroup(
#             id=group_id,
#             name=group.name,
#             task_id=group.task_id
#         )
#         session.add(data_group)
#         session.commit()
#         session.close()
#     except ArithmeticError:
#         return {"code": "0002", "message": "数据库异常"}
#     return {"code": 200, "id": group_id}
#
# """
# 添加规避规则
# """
# @app.post("/inspection/generate_team",summary="添加规避规则")
# async def generate_inspection_team(inspected_unit: Optional[str] = "任职单位",native_place:Optional[str] = "籍贯",birth_place:Optional[str] = "出生地",graduation_school:Optional[str] = "毕业院校",
#                                    ):
#     # 获取所有候选人
#     print(inspected_unit,native_place,birth_place,graduation_school)
#     candidates = session.query(Person).all()
#
#     print(candidates)
#     # 定义一个空列表，用于存储符合条件的巡视组成员
#     inspection_team = []
#     try:
#         for candidate in candidates:
#             # 检查回避条件
#             # 1.a)	回避本人任职单位以及亲属关系任职单位承担巡视巡察工作
#             avoid_unit = (inspected_unit is not None) and \
#                          ((candidate.work_unit == inspected_unit) or
#                           any(relative_person.work_unit == inspected_unit
#                               for relative in candidate.relatives
#                               for relative_person in session.query(Person).filter(Person.id == relative.relative_id)))
#             for relative in candidate.relatives:
#                 for relative_person in session.query(Person).filter(Person.id == relative.relative_id):
#                     print("--------------------------")
#                     print(relative_person.work_unit)
#                     print("--------------------------")
#             # print(inspected_unit)
#             # print(candidate.work_unit)
#             # b)	回避本人所在籍贯承担巡视巡察工作
#             avoid_native_place = (native_place is not None) and (candidate.native_place == native_place)
#             # print(native_place is not None)
#             # print(candidate.native_place == native_place)
#             # print(candidate.native_place)
#             # print(avoid_native_place)
#             # c)	回避本人出生地承担巡视巡察工作
#             avoid_birth_place = (birth_place is not None) and (candidate.birth_place == birth_place)
#             # e)	回避本人毕业院校承担巡视巡察工作
#             avoid_graduation_school = (graduation_school is not None) and (candidate.graduation_school == graduation_school)
#             # 如果满足所有回避条件，将候选人添加到巡视组
#             if not (avoid_unit or avoid_native_place or avoid_birth_place or avoid_graduation_school):
#                 inspection_team.append(candidate)
#         # print(inspection_team)
#
#         return {"code": 200, "data": [team_member.id for team_member in inspection_team]}
#     except ArithmeticError:
#         return {"code": "0002", "message": "发生错误"}
#
# """
# 添加人员（符合规则的人员）到组中
# """
# @app.post("/inspection/add_person_to_group",summary="添加人员（符合规则的人员）到组中")
# async def add_person_to_group(request: AddPersonToGroupRequest):
#     try:
#         # 根据 group_id 查询出对应的 InspectionGroup 对象
#         group = session.query(InspectionGroup).filter(InspectionGroup.id == request.group_id).first()
#
#         if not group:
#             return {"code": "0003", "message": "组不存在"}
#
#         # 遍历 person_ids 并将每个人员添加到组中
#         for person_id in request.person_ids:
#             person = session.query(Person).filter(Person.id == person_id).first()
#
#             if not person:
#                 return {"code": "0004", "message": f"人员ID {person_id} 不存在"}
#
#             # 将满足规避规则的人员添加到组中
#             group.members.append(person)
#
#         # 提交更改并关闭会话
#         session.commit()
#         session.close()
#
#     except ArithmeticError:
#         return {"code": "0002", "message": "数据库异常"}
#
#     return {"code": 200, "message": "人员添加成功"}
#
#
# # 添加管理员
# @app.post("/User/addUser",summary="添加管理员")
# async def add_user(user : CreatUser ):
#
#     try:
#         user1 = session.query(User).filter(User.unifiedNumber == user.unifiedNumber).first()
#         if user1:
#             return {"code": "0002", "message": "该人员已经注册！"}
#         else:
#             userid = gen_uuid()
#             user_id = userid
#             data_user = User(
#                 userId=userid,
#                 userName=user.userName,
#                 password=user.password,
#                 userSex=user.userSex,
#                 userPhone=user.userPhone,
#                 unifiedNumber=user.unifiedNumber
#
#             )
#             session.add(data_user)
#         session.commit()
#         session.close()
#     except ArithmeticError:
#         return {"code": "0002", "message": "数据库异常"}
#     return {"code": 200, "id": user_id}
#
#
# """
# 根据任务ID查询
# """
# @app.get("/inspection/{task_id}/groupMembers", response_model=Any,summary="根据任务ID查询")
# async def get_group_members(task_id: str):
#     try:
#         task = session.query(InspectionTask).filter(InspectionTask.id == task_id).one()
#     except Exception as e:
#         return {"code": "0002", "message": "任务未找到"}
#     groups = session.query(InspectionGroup).filter(InspectionGroup.task_id == task_id).all()
#     result = []
#     for group in groups:
#         members = session.query(Person).join(inspection_group_membership).filter(
#             inspection_group_membership.c.inspection_group_id == group.id).all()
#         member_list = [member.__dict__ for member in members]
#         for member in member_list:
#             member.pop('_sa_instance_state', None)
#
#         group_info = {
#             'task': task.__dict__,
#             'group': group.__dict__,
#             'members': member_list
#         }
#         group_info['task'].pop('_sa_instance_state', None)
#         group_info['group'].pop('_sa_instance_state', None)
#
#         result.append(group_info)
#         print(result)
#
#     return {"code": 200, "data": result}
#
#
# """
# 获取巡视任务列表
# """
# @app.get("/inspection/taskList", response_model=Any,summary="获取巡视任务列表")
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


# if __name__ == "__main__":
#     # 启动服务，因为我们这个文件叫做 main.py
#     # 所以需要启动 main.py 里面的 app
#     # 第一个参数 "main:app" 就表示这个含义
#     # 然后是 host 和 port 表示监听的 ip 和端口
#     uvicorn.run("main:app", host="0.0.0.0", port=8000)