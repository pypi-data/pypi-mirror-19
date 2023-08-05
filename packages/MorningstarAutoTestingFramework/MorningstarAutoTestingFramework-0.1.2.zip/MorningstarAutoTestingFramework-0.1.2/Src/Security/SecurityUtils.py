# -*- coding: utf-8 -*-
import hashlib
from functools import partial


@staticmethod
def iofilesysgetfilemd5hash(filepath):
    """
    计算文件的MD5 Hash值

    :param filepath: 待传入文件的Path

    :return: 返回文件的MD5 Hash值
    """
    fp = open(filepath, 'rb')
    data = fp.read()
    fp.close()
    md5 = hashlib.md5()
    md5.update(data)
    return md5.hexdigest()


def calcfilemd5sum(filename):
    """
    计算一个文件的MD5值
    :param filename:
    :return:
    """
    with open(filename, "rb") as f:
        d = hashlib.md5()
        for buf in iter(partial(f.read, 128), b''):
            d.update(buf)
    return d.hexdigest()


@staticmethod
def string_encrypt_md5(inputstring):
    """
    计算输入字符串的MD5值

    :param inputstring:输入字符串

    :return: 返回计算后的MD5值

    """
    return hashlib.md5(inputstring).hexdigest()


@staticmethod
def string_encrypt_sha256(inputstring):
    """
    计算输入字符串的SHA256值

    :param inputstring: 输入字符串

    :return: 返回计算后的SHA256值
    """
    return hashlib.sha256(inputstring).hexdigest()
