# --*-- conding:utf-8 --*--
# @Time : 2023/11/21 12:31
# @Author : HongZe
# @File : cache.py.py
# @Function:

# 用作[discussion_id -> prompt]的缓存，保存讨论状态
ca_list = []


# 添加缓存
def set_list(discussion_id, prompt):
    ca_list.append([discussion_id, prompt])


def get_prompt(discussion_id):
    for i in ca_list:
        if (i[0] == discussion_id):
            return i[1]
    return ""

# 根据discussion_id修改prompt
def set_list_byId(discussion_id , prompt):
    for i in ca_list:
        if i[0] == discussion_id:
            i[1] = prompt
            return 1
    return 0


def remove_prompt():
    ca_list.clear()
    return None
