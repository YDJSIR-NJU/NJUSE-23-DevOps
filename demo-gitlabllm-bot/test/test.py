# --*-- conding:utf-8 --*--
# @Time : 2023/11/19 15:06
# @Author : HongZe
# @File : test.py.py
# @Function:

from api.api import api_commit_post, api_file_content

"""为什么这里json对象要用get取？"""
if __name__ == '__main__':
    api_commit_post('11042', 'main', "来自大模型的评审", 'create',
                    'comment1' + '.md',
                    '')
    path = 'comment1' + '.md'
    cont = api_file_content('11042', path,'main')
    print(cont)
    print(api_commit_post('11042', 'main', "来自大模型的评审", 'update',
                    'comment1' + '.md',
                          cont + ' ``` \n 待评审函数开始 ' + '``` \n 待评审函数结束 \n '))
    #
    # '这里改过啦'