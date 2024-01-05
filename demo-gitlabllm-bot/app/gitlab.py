# --*-- conding:utf-8 --*--
# @Time : 2023/11/18 16:20
# @Author : HongZe
# @File : gitlab.py.py
# @Function: 接收webhook并响应
from fastapi import FastAPI, Request
import json
from api.api import api_merge_diff, api_get_sha, api_commit_post
from service.content_handler import file_diff_handler

from service.discussion_handler import post_discussion_note
from service.utils import match_string, get_current_time

app = FastAPI()


# 发起merge时的webhook
@app.post("/merge_request")
async def receive_webhook(request: Request):
    data = await request.json()

    print("Received webhook data:" + data["object_kind"])

    if data["object_kind"] == 'merge_request':
        time = get_current_time()
        # 拼接文档头
        head = f'---\ntitle: Summary From GenAI - {data["object_attributes"]["title"]}\ndate: {time[0]}\ntags:\n- {data["project"]["name"]}\n---\n \n# PR-{data["object_attributes"]["iid"]} {data["object_attributes"]["title"]}\n\n> PR地址：{data["object_attributes"]["url"]}\n\n生成时间：{time[1]}\n\n'

        # 创建指定仓库中的空文件
        # 反复开关同一次merge要删除生成的文件
        path1 = f'source/_posts/Summary_From_GenAI_{data["object_attributes"]["title"]}.md'
        # 修改发送的文档仓库参数(project_id)和分支(branch)为自己的，第1处
        tmp = api_commit_post('11060', 'main', "来自大模型的评审", 'create',
                              path1,
                              head)
        # 推送文件的位置，修改推送文件仓库地址为自己的，此地址仅作评论区仓库地址展示用，可结合需要自己拼接生成文档的具体地址(拼接上文件名)，第2处
        path2 = f'https://git.nju.edu.cn/devops_2023_fall/demo-llm-docs/-/tree/main/source/_posts'
        result = api_merge_diff(data["project"]["id"], data["object_attributes"]["iid"])

        # 对一次merge中的每个发生改变的文件挨个处理
        for item in result:
            file_diff_handler(data["project"]["id"], data["object_attributes"]["iid"],
                              data["object_attributes"]["source_branch"], data["object_attributes"]["target_branch"],
                              item.get('diff'), item.get('old_path'), item.get('new_path'),
                              data["object_attributes"]["description"], path1, path2)

    if data["object_kind"] == 'note':
        if match_string(data["object_attributes"]["description"]) == 0:
            post_discussion_note(data["project_id"], data["merge_request"]["iid"],
                                 data["object_attributes"]["discussion_id"], data["object_attributes"]["description"])

    return {"status": "ok"}
