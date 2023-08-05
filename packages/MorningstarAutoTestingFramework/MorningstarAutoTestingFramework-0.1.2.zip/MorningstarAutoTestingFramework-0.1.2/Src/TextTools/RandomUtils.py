# -*- coding: utf-8 -*-
import random
import string


class RandomUtils:
    """
    随机数据生成工具类
    """

    def __init__(self):
        pass

    @staticmethod
    def genrandomstring(length):
        """
        随机出数字的个数
        :param length:
        :return:
        """
        numofnum = random.randint(1, length - 1)
        numofletter = length - numofnum
        # 选中numOfNum个数字
        slcnum = [random.choice(string.digits) for i in range(numofnum)]
        # 选中numOfLetter个字母
        slcletter = [random.choice(string.ascii_letters) for i in range(numofletter)]
        # 打乱这个组合
        slcchar = slcnum + slcletter
        random.shuffle(slcchar)
        # 生成密码
        return ''.join([i for i in slcchar])
