# -*- coding: utf-8 -*-
'''
-时间    : 2023/4/15 21:51
-作者 : 王子康
-文件    : relative.py
-说明    : 亲属关系的增删改查
'''
from typing import List
from sqlalchemy.exc import SQLAlchemyError
from common.Base import *
from fastapi import *

from lib.inverse_relation import get_inverse_relation

router = APIRouter(prefix='/relative')
@router.get("/{person_id}/relatives")
async def get_person_relatives(person_id: str):
    relatives = session.query(Relatives).filter(Relatives.person_id == person_id).all()
    for relative in relatives:
        print(relative.relative_id)
    # return relatives
    session.commit()
    session.close()
    print("关闭了连接...")
    return {"code":"200" ,"data":relatives}
#
@router.delete("/{person_id}/delRelative/{relative_id}")
async def remove_relative(person_id: str, relative_id: str):
    try:
        relations = session.query(Relatives).filter(
            (Relatives.person_id == person_id) & (Relatives.relative_id == relative_id) |
            (Relatives.person_id == relative_id) & (Relatives.relative_id == person_id)
        ).all()

        for relation in relations:
            session.delete(relation)

        # session.commit()
        # session.close()
        return {"code":"200 ","message": "亲属关系删除成功"}
    except SQLAlchemyError as e:
        session.rollback()
        return {"code": "0001", "message": "失败！"+{e}}
    finally:
        session.commit()
        session.close()
        print("关闭了连接...")

@router.put("{person_id}/uprelative/{relative_id}")
async def update_person_relative(person_id: str, relative_id: str, new_relation: str):
    try:
        inverse_new_relation = get_inverse_relation(new_relation)
        relations = session.query(Relatives).filter(
            (Relatives.person_id == person_id) & (Relatives.relative_id == relative_id) |
            (Relatives.person_id == relative_id) & (Relatives.relative_id == person_id)
        ).all()
        if(relations):
            for relation in relations:
                if relation.person_id == person_id:
                    relation.relation = new_relation
                else:
                    relation.relation = inverse_new_relation
            # session.commit()
            # session.close()
            return {"code":200,"message":"修改成功"}
        else:
            return {"code": "0002", "message": "未找到该关系！"}
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=f"Error updating relative relationship: {e}")
    finally:
        session.commit()
        session.close()
        print("关闭了连接...")

@router.post("/addRelatives",summary="添加亲属关系", description="添加关系为双向的")
def create_relative(relative: RelativeCreate):
    try:
        # 检查两个person_id是否存在
        # 检查两个person_id是否存在
        person1 = session.query(Person).filter(Person.id == relative.person_id).first()
        person2 = session.query(Person).filter(Person.id == relative.relative_id).first()
        inverse_relation = get_inverse_relation(relative.relation)
        if person1 is None or person2 is None:
            raise HTTPException(status_code=404, detail="Person not found")
        # 创建两个Relatives对象，表示双向关系
        relative1 = Relatives(person_id=relative.person_id, relative_id=relative.relative_id,
                                     relation=relative.relation)
        relative2 = Relatives(person_id=relative.relative_id, relative_id=relative.person_id,
                                     relation=inverse_relation)

        # 将两个Relatives对象添加到数据库中
        session.add(relative1)
        session.add(relative2)
        # session.commit()
        # session.close()
        # session.refresh(relative1)
        # session.refresh(relative2)
        # 返回创建的Relatives对象
        return {"relative1": relative.relation, "relative2": inverse_relation}
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error adding relative: {e}")
        return {"code": "0001", "meaasge": "发生错误，添加失败"}
    finally:
        session.commit()
        session.close()
        print("关闭了连接...")