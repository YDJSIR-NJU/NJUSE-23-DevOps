# --*-- conding:utf-8 --*--
# @Time : 2023/11/18 16:56
# @Author : HongZe
# @File : utils.py
# @Function: 文本和时间处理相关工具类

import os
import re
import urllib
import datetime

"""
判断是否超出文件和大小限制
"""

"""
获得文件后缀
输入参数：文件相对路径
返回：后缀，如 '.java'
"""
def get_suffix(file_path):
    return os.path.splitext(os.path.basename(file_path))[1]

"""
获得文件前缀
输入参数：文件相对路径 如 ‘/usr/home/name.java’
返回：后缀，如 'name'
"""
def get_prefix(file_path):
    return os.path.splitext(os.path.basename(file_path))[0]

"""
对文件路径进行URL编码
"""
def encode_filpath(file_path):
    encoded_file_path = urllib.parse.quote(file_path, safe='')
    return encoded_file_path

"""
因为 List merge request diffs 返回一个文件的所有diff,有碍于根据单个diff查找上下文，故这里要对diff进行切分 (可能写烦了，是不是可以直接一个正则出结果)
输入参数：一个文件的diff
返回：一个文件的单个diff列表
"""
def get_single_diff(file_diff):
    result = []
    # 对字符串以@@ -num,num +num,num @@分割
    tmpList = re.split(r"(@@ -\d+,\d+ \+\d+,\d+ @@)", file_diff)
    array_iter = enumerate(tmpList)
    # 将分隔符和字符串连接
    for index,item in array_iter:
        if re.search(r"(@@ -\d+,\d+ \+\d+,\d+ @@)",item):
            print(tmpList[index] + tmpList[index + 1])
            result.append(tmpList[index] + tmpList[index + 1])
    return result

"""
计算diffNote标识的行位置(可以改进的更加准确或换成多行)，这里的逻辑是取一段diff中新增的最后一行，若没有新增就取减去的最后一行，经测试在comment页中可以显示所有改diff涉及的行(大概)
输入参数：diff字符串
返回：行数
"""
def get_diffNote_postion(single_diff):
    match = re.search(r"\+(\d+)\D+(\d+)", single_diff)
    first = int(match.group(1, 2)[0])
    seco = int(match.group(1, 2)[1])
    if seco == 6:
        match = re.search(r'-.*?(\d+)\D*(\d+)', single_diff)
        second_digit = int(match.group(2))
        first_digit = int(match.group(1))
        return [first_digit + second_digit - 4, 0]
    else:
        return [first + seco - 4, 1]

"""
判断webhook的输入是否来自AI，防止死循环
"""
def match_string(string):
    pattern = r"from GenAI"
    if re.search(pattern, string):
        return 1
    else:
        return 0

"""
获得当时时间
"""

def get_current_time():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S"),now.strftime("%m月 %d, %Y %I:%M%p").replace("PM", "下午").replace("AM", "上午")

if __name__ == '__main__':
    test_string = "@@ -46,13 +46,6"
    print(get_current_time())