# -*- coding: utf-8 -*-
import hashlib
import os
import time


# 简单的测试一个字符串的MD5值
def get_string_md5_value(src):
    m0 = hashlib.md5()
    m0.update(src)
    return m0.hexdigest()


def get_big_file_md5_value(filename):
    """
    计算大文件的MD5值
    :param filename: 大文件的路径
    :return:
    """
    if not os.path.isfile(filename):
        return
    my_hash = hashlib.md5()
    f = file(filename, 'rb')
    while True:
        b = f.read(8096)
        if not b:
            break
        my_hash.update(b)
    f.close()
    return my_hash.hexdigest()


def get_file_sha1_value(file_path):
    """
    计算小文件的SHA1值
    :param file_path:待检查的文件路径
    :return:
    """
    with open(file_path, 'rb') as f:
        sha1obj = hashlib.sha1()
        sha1obj.update(f.read())
        hash_value = sha1obj.hexdigest()
        # print(hash_value)
        return hash_value


def get_file_md5_value(file_path):
    """
    计算小文件的MD5值
    :param file_path: 待检查的文件路径
    :return:
    """
    with open(file_path, 'rb') as f:
        md5obj = hashlib.md5()
        md5obj.update(f.read())
        hash_value = md5obj.hexdigest()
        # print(hash_value)
        return hash_value


if __name__ == "__main__":
    hash_file = r"E:\Others\en_windows_7_ultimate_with_sp1_x64_dvd_u_677332.iso"
    if not os.path.exists(hash_file):
        hash_file = os.path.join(os.path.dirname(__file__), hash_file)
        if not os.path.exists(hash_file):
            print("cannot found file")
        else:
            get_file_md5_value(hash_file)
    else:
        get_file_md5_value(hash_file)
        # raw_input("pause")

    t = time.time()
    print get_big_file_md5_value(hash_file)
    print time.time() - t
