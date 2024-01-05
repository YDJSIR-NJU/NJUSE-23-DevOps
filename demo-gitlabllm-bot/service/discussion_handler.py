# --*-- conding:utf-8 --*--
# @Time : 2023/11/20 17:25
# @Author : HongZe
# @File : discussion_handler.py.py
# @Function: 关于dicussion的note讨论

"""
接受dicussion thread后续的回复并提交大模型，返回信息
"""
from api.api import api_add_existNote, api_AI_post
from service.cache import get_prompt, set_list_byId


def post_discussion_note(project_id, merge_request_iid, discussion_id, content):
    # 添加每次问答的问题
    new_content = get_prompt(discussion_id) + '\n' + format(content)
    print('这里的提问是' + new_content)
    set_list_byId(discussion_id, new_content)
    api_add_existNote(project_id, merge_request_iid, discussion_id, "from GenAI: \n" + api_AI_post(new_content))

if __name__ == '__main__':
    print(api_add_existNote(10920, 8,'e3a44e1dba4e5ac6a572657d1f4ef940a589ec1a','hello'))