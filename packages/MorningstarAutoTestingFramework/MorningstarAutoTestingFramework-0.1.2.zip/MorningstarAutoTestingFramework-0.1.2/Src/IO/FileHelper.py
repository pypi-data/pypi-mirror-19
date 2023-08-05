# -*- coding: utf-8 -*-
import fileinput
import os
import hashlib


def replace_in_file(file_path, find_string, replace_string):
    """
    将指定文件file_path中的特定字符串find_string替换为replace_string
    :param file_path: 目标文件的路径
    :param find_string: 待查找的字串
    :param replace_string: 要替换的字串
    :return:
    """
    # 将c:\\a.txt文件中的001替换为MM
    for l in fileinput.input(file_path, inplace=1):
        nl = l.replace(find_string, replace_string)
        print nl  # 该句必须要存在，用于写入文件，否则文件会为空


def read_file_content_to_string(file_path):
    """
    读取文件的全部内容到字串变量中
    :param file_path:
    :return:
    """
    # 不能把open语句放在try块里，因为当打开文件出现异常时，文件对象file_obj无法执行close()方法。
    file_obj = open(file_path, 'r')
    try:
        result = file_obj.read()
    finally:
        file_obj.close()
    return result


def read_file_content_to_lines(file_path):
    file_obj = open(file_path, 'r')
    try:
        list_of_all_the_lines = file_obj.readlines()
    finally:
        file_obj.close()
    return list_of_all_the_lines


def write_file_content_to_text_file(file_path, content):
    file_object = open(file_path, 'w')
    file_object.write(content)
    file_object.close()


def append_file_content_to_text_file(file_path, content):
    file_object = open(file_path, 'a')
    file_object.write(content)
    file_object.close()


def file_info_output():
    print("得到当前工作目录，即当前Python脚本工作的目录路径: " + os.getcwd())
    print("返回指定目录下的所有文件和目录名:")
    dirs = os.listdir(os.getcwd())
    for f in dirs:
        print(f)


def create_dir(path):
    os.mkdir(path)


def main():
    replace_in_file(r"D:\1.txt", "ABC", "123")


if __name__ == '__main__':
    main()
