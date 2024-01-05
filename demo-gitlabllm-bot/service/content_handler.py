# --*-- conding:utf-8 --*--
# @Time : 2023/11/18 16:23
# @Author : HongZe
# @File : content_handler.py
# @Function: 获得
import tempfile
import json

from api.api import api_file_content, api_merge_diff, api_AI_post, api_post_diffNote, api_get_sha, api_commit_post
from java_analysis.functionManager import FunctionManager
from service.cache import set_list, get_prompt
from service.utils import get_suffix, get_single_diff, get_diffNote_postion

"""
对每个文件的diff进行大模型review并添加diffNote comment

传入参数：project_id , version(源分支名or被合并的分支名)...
返回参数：

"""


def file_diff_handler(project_id, merge_iid, origin_version, target_version, diff, old_path, new_path, post, path1,
                      path2):
    # list = get_all_func(project_id, origin_version ,target_version ,diff , old_path ,new_path)
    # get_limit
    list = get_new_func(project_id, origin_version, diff, new_path)
    sha = api_get_sha(project_id, merge_iid)

    # 可能需要添加线程池异步处理
    for item in list:
        rs = api_AI_post(format(post) + '```待评审函数开始' + item[0] + '```待评审函数结束')
        flag = get_diffNote_postion(item[1])
        tmp2 = api_post_diffNote(project_id, merge_iid, sha.get("base_commit_sha"), sha.get("head_commit_sha"),
                                 sha.get("start_commit_sha"), new_path, old_path, flag[0] if flag[1] == 1 else None,
                                 flag[0] if flag[1] == 0 else None, 'from GenAI: \n' + rs + '\n评审文本地址是' + path2)

        # 读之前生成的文件并添加新内容，修改发送的文档仓库参数(project_id)和分支(version)为自己的，第3处和第4处
        cont = api_file_content('11060', path1, 'main')
        api_commit_post('11060', 'main', "来自大模型的评审", 'update',
                        path1,
                        cont + f'## {new_path}\n' + f'### Code \n```\n // 待评审函数开始 \n {item[0]} \n // 待评审函数结束 \n```\n\n### Summary\n {rs}\n\n')
        # 将第一次提问的内容添加缓存
        print('推送成功，prompt全文是' + format(post) + '```待评审函数开始' + item[0] + '```待评审函数结束')
        set_list(json.loads(tmp2).get("id"), format(post) + '```待评审函数开始' + item[0] + '```待评审函数结束')


"""
获取新的函数和原来的函数，备用
返回参数：[[新函数，原来函数，diff]]
"""


def get_all_func(project_id, origin_version, target_version, diff, old_path, new_path):
    list = []
    flag = 0
    result = get_single_diff(diff)
    origin_file_path = get_gitlab_file_content(project_id, new_path, origin_version)
    # 如果只是新增没有修改呢，需要测试；如果修改的地方在不在函数中呢，需要测试；如果是新增新文件呢，需要测试
    target_file_path = get_gitlab_file_content(project_id, old_path, target_version)
    print('origin_file_path：' + origin_file_path)
    print("target_file_path: " + target_file_path)

    # manager可复用，可不可以用单例模式重构？
    manager1 = FunctionManager(origin_file_path)
    manager2 = FunctionManager(target_file_path)

    # 去重，防止一个函数有多个diff，并且当同一个文件的single diff第一次进入时直接添加入list,减少新文件的遍历次数
    # 疑惑为什么python里面的对象和hashmap这么麻烦，对象储存实现版setattr无法使用
    for item in result:
        if not list:
            list.append([manager1.get_function(item).decode(), manager2.get_function(item).decode(), item])
        else:
            origin_tmp_function = manager1.get_function(item).decode()
            flag = 0
            for i in list:
                if i[0] == origin_tmp_function:
                    i[2] = item
                    flag = 1
                    break
            if flag == 0:
                list.append([origin_tmp_function, manager2.get_function(item).decode(), item])

    return list


"""
获取新的函数
返回参数：[[新函数，diff]]
"""


def get_new_func(project_id, origin_version, diff, new_path):
    list = []
    result = get_single_diff(diff)
    # 如果只是新增没有修改呢，需要测试；如果修改的地方在不在函数中呢，需要测试；如果是新增新文件呢，需要测试
    origin_file_path = get_gitlab_file_content(project_id, new_path, origin_version)
    print('origin_file_path：' + origin_file_path)

    # manager可复用，可不可以用单例模式重构？
    manager1 = FunctionManager(origin_file_path)

    # 去重，防止一个函数有多个diff，并且当同一个文件的single diff第一次进入时直接添加入list,减少新文件的遍历次数
    # 疑惑为什么python里面的对象和hashmap这么麻烦，对象储存实现版setattr无法使用,同时二维数组也有很多限制
    for item in result:
        if not list:
            list.append([manager1.get_function(item).decode(), item])
        else:
            origin_tmp_function = manager1.get_function(item).decode()
            print("提取的函数在这里" + origin_tmp_function)
            flag = 0
            for i in list:
                if i[0] == origin_tmp_function:
                    i[1] = item
                    flag = 1
                    break
            if flag == 0:
                list.append([origin_tmp_function, item])
    print("除报错外所有函数提取成功！")
    return list


"""
获取gitlab中指定文件的内容

传入参数：略
返回参数：文件相对路径

"""


def get_gitlab_file_content(project_id, file_path, version):
    file_content = api_file_content(project_id, file_path, version)

    # 创建临时文件 什么时候删除呢？
    with tempfile.NamedTemporaryFile(suffix=get_suffix(file_path), delete=False) as temp_file:
        # 获取临时文件路径
        temp_file_path = temp_file.name

    # 写入文件内容
    with open(temp_file_path, 'w', encoding="utf-8") as file:
        file.write(file_content)

    return temp_file_path


if __name__ == '__main__':
    print(get_new_func(10920, '啊',
                       "@@ -29,10 +29,6 @@ static class textHandler {\n         final List<String> keyphrase = extractor.getKeyphraseFromString(text);\n         double c_time = (System.nanoTime() - s_time)/1E9;\n \n-        final Map<String, Object> map = new HashMap<>();\n-        DecimalFormat df = new DecimalFormat(\"0.00000\");\n-        map.put(\"took\", Float.valueOf(df.format(c_time)));\n-\n         //response the request\n         response(0, map);\n     }\n@@ -44,6 +40,8 @@ static class textHandler {\n         if ( text == null || \"\".equals(text) ) {\n             response(STATUS_INVALID_ARGS, \"Invalid Arguments\");\n             return;\n+            response(STATUS_INVALID_ARGS, \"Invalid Arguments\");\n+            response(STATUS_INVALID_ARGS, \"Invalid Arguments\");\n         }\n \n         final JcsegGlobalResource resourcePool = (JcsegGlobalResource)globalResource;\n@@ -62,7 +60,7 @@ static class textHandler {\n         double c_time = (System.nanoTime() - s_time)/1E9;\n \n         final Map<String, Object> map = new HashMap<>();\n-        final DecimalFormat df = new DecimalFormat(\"0.00000\");\n+        final DecimalFormat\n         map.put(\"took\", Float.valueOf(df.format(c_time)));\n         map.put(\"sentence\", sentence);\n \n",
                       "src/main/java/com/example/demo/handler/textHandler.java"))
