# --*-- conding:utf-8 --*--
# @Time : 2023/11/18 16:23
# @Author : HongZe
# @File : content_handler.py
# @Function: 所有访问gitlab的接口

import requests
import json

from service.utils import encode_filpath

server = "https://git.nju.edu.cn/api/v4"
token = ""  # merge_request_token 项目仓库token 请替换为自己的
target_token = ""  # target_token 文档仓库token 请替换为自己的

#

headers = {
    "PRIVATE-TOKEN": token
}


# response统一处理方法
# def response()

# 获取merge时的commit sha以用作之后的diffNote discussion
def api_get_sha(project_id, merge_request_iid):
    response = requests.get(
        f'{server}/projects/{project_id}/merge_requests/{merge_request_iid}/versions',
        headers={
            "PRIVATE-TOKEN": token
        })

    if response.status_code == 200:
        return json.loads(response.content)[0]
    else:
        # 报错还没有处理
        print(f'sha API请求失败：{response.status_code} {response.reason}')
        return None


# 推送到gitlab的diffNote discussion
# 此接口只支持单行diffNote discussion标识评论，但经测试显示内容已覆盖单次diff大部分内容
# 若想实现多行diffNote discussion标识评论请参考 https://docs.gitlab.com/ee/api/discussions.html#create-a-new-thread-in-the-merge-request-diff
def api_post_diffNote(project_id, merge_request_iid, base_sha, head_sha, start_sha, new_path, old_path, new_line,
                      old_line, content):
    # 为什么这里要先转化为json而不能直接使用dataForm的形式？和js比较呢？
    prama = {
        'body': content,
        'position': {
            'base_sha': base_sha,
            'head_sha': head_sha,
            'start_sha': start_sha,
            'position_type': 'text',
            'new_path': new_path,
            'old_path': old_path,
            'new_line': new_line,
            'old_line': old_line
        }
    }
    response = requests.post(
        f'{server}/projects/{project_id}/merge_requests/{merge_request_iid}/discussions',
        json.dumps(prama), headers={
            "PRIVATE-TOKEN": token,
            "Content-Type": "application/json"
        })

    if response.status_code == 201:
        # 救命啊为什么这里是个数组，为什么正确是201
        return response.content
    else:
        # 报错还没有处理
        print(f'post——diff API请求失败：{response.status_code} {response.content}')
        return None


def api_add_existNote(project_id, merge_request_iid, discussion_id, content):
    prama = {
        'body': content
    }
    response = requests.post(
        f'{server}/projects/{project_id}/merge_requests/{merge_request_iid}/discussions/{discussion_id}/notes',
        json.dumps(prama), headers={
            "PRIVATE-TOKEN": token,
            "Content-Type": "application/json"
        })

    if response.status_code == 201:
        # 救命啊为什么这里是个数组，为什么正确是201
        return response.content
    else:
        # 报错还没有处理
        print(f'add_note API请求失败：{response.status_code} {response.content}')
        return None


# 获取指定分支上文件内容
def api_file_content(project_id, file_path, version):
    response = requests.get(
        f'{server}/projects/{project_id}/repository/files/{encode_filpath(file_path)}/raw?ref={version}',
        headers={
            "PRIVATE-TOKEN": token
        })

    if response.status_code == 200:
        return response.text
    else:
        # 报错还没有处理
        print(f'get_file API请求失败：{response.status_code} {response.reason}')
        return None


# 获取某次merge的所有diff
def api_merge_diff(project_id, merge_request_iid):
    response = requests.get(
        f"https://git.nju.edu.cn/api/v4/projects/{project_id}/merge_requests/{merge_request_iid}/diffs",
        headers={
            "PRIVATE-TOKEN": token
        })

    if response.status_code == 200:
        return json.loads(response.content)
    else:
        # 报错还没有处理
        print(f'get——merge——diff API请求失败：{response.status_code} {response.reason}')
        return None


def api_AI_post(content):
    params = {
        "model": "Qwen-14B",
        "temperature": 0.7,
        "messages": [{"role": "user", "content": content}],
        "max_tokens": 512,
        "stop": None,
        "n": 1,
        "top_p": 1.0,
    }
    response = requests.post("http://${LLM_SERVER}:8000/v1/chat/completions", headers=headers, json=params)

    if response.status_code == 200:
        return json.loads(response.text).get("choices")[0].get("message").get("content")
    else:
        # 报错还没有处理
        print(f'AIpost_API请求失败：{response.status_code} {response.reason}')
        return None


"""
关闭merge的接口
官方文档：https://docs.gitlab.com/ee/api/merge_requests.html#merge-a-merge-request

输入参数：
    'id':The ID or URL-encoded path of the project owned by the authenticated user. 可以从merge_request的webhook中获取
    'request_iid':	The internal ID of the merge request. 同上
     
返回参数：见官方文档
"""


def api_close_merge(id, request_iid):
    return requests.put(server + f"/projects/{id}/merge_requests/{request_iid}", headers={
        "PRIVATE-TOKEN": token,
        "Content-Type": "multipart/form-data"
    }, data={"state_event": "close"})


"""
提交内容至仓库
https://docs.gitlab.com/ee/api/commits.html#create-a-commit-with-multiple-files-and-actions

request_body如下
{
    "id":  # The ID or URL-encoded path of the project
    "branch": "master", # 要提交的分支
    "commit_message":"123456", # 提交信息
    "actions":[ # 提交内容，可提交多个文件
        {
            "action":"create", # 提交类型，这里是创建文件，其他内容见官方文档
            "file_path": "new_test.md", # 新建的文件路径
            "content":"123456" # 写入文件中的内容
        }
    ]   
}

返回参数：见官方文档
"""


def api_commit_post(id, branch, commit_message, action, file_path, content):
    params = {
        "branch": branch,
        "commit_message": commit_message,
        "actions": [
            {
                "action": action,
                "file_path": file_path,
                "content": content,
                "execute_filemode": 'true'
            }
        ]
    }
    response = requests.post(f'https://git.nju.edu.cn/api/v4/projects/{id}/repository/commits', headers={
        "PRIVATE-TOKEN": target_token
    }, json=params)

    if response.status_code == 201:
        return json.loads(response.content)
    else:
        # 报错还没有处理
        print(f'get——commit——post API请求失败：{response.status_code} {response.content}')
        return None

# 关闭merge
def close_merge_request(proj_id, request_id):
    return requests.put(server + f"/projects/{proj_id}/merge_requests/{request_id}", headers={
            "PRIVATE-TOKEN": token,
            "Content-Type": "multipart/form-data"
            }, data={"state_event": "close"})



if __name__ == '__main__':
    close_merge_request(10920,103)
