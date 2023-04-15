# -*- coding: utf-8 -*-
'''
-时间    : 2023/4/15 21:54
-作者 : 王子康
-文件    : inverse_relation.py
-说明    :
'''
# 亲属关系映射表
def get_inverse_relation(relation: str) -> str:
    relation_mapping = {
        "母亲": "女儿",
        "父亲": "儿子",
        "女儿": "母亲",
        "儿子": "父亲",
        # ... 添加其他关系映射
    }
    return relation_mapping.get(relation, "未知关系")