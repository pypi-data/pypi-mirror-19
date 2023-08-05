# -*- coding: utf-8 -*-
import os


class FileTraversal:
    def __init__(self, rootpath):

        self.rootpath = rootpath

        # 从顶至底的遍历(在剪短的代码里，我比较喜欢这清晰的变量名)
        self.tracersal_from_top_to_down = True

        # 遍历发生错误的时候的回调函数
        # 函数参数为一个OSError类型参数
        # 文件名会作为错误参数的一个属性 , 如 error.filename
        self.on_error_func = None

        # 是否变量链接文件(如:软链接、硬链接、windows上的快捷方式)
        self.follow_links = False

    def setTopToDown(self, from_top_to_dowm=True):
        """
        设置遍历顺序
        :param from_top_to_dowm:
        :return:
        """
        self.tracersal_from_top_to_down = from_top_to_dowm
        return self

    def setErrorFunc(self, err_func=None):
        """
        设置错误回调函数
        :param err_func:
        :return:
        """
        self.on_error_func = err_func
        return self

    def setFollowLinks(self, follow_links=False):
        """
        设置是否遍历连接文件
        :param follow_links:
        :return:
        """
        self.follow_links = follow_links
        return self

    def getGenerator(self):
        """
         获取迭代器
        :return:
        """
        return os.walk(self.rootpath, self.tracersal_from_top_to_down, self.on_error_func, self.follow_links)

    def getFiles(self, absolute_path=True):
        """
        获取所有文件
        :param absolute_path: 是否返回绝对路径，或者仅仅文件名
        :return:
        """
        files = []
        for parent, dirnames, filenames in self.getGenerator():  # 三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
            for file in filenames:
                filepath = os.path.join(parent, file)
                files.append(filepath if absolute_path else file)
        return files

    def getThisLevelFiles(self, absolute_path=True):
        """
        获取当前目录下所有的文件(不递归遍历)
        :param absolute_path:
        :return:
        """
        files = []
        all_in_dir = os.listdir(self.rootpath)
        for m_file in all_in_dir:
            file_path = os.path.join(self.rootpath, m_file)
            if not os.path.isdir(file_path):
                files.append(file_path if absolute_path else m_file)
        return files
