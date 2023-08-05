# -*- coding: utf-8 -*-
import time


def revert_list():
    a = [1, 2, 3]
    b = a
    c = a[1:]
    d = a[::-1]
    print a
    print b
    print c
    print d

    for i in range(0, a.__len__())[::-1]:
        print a[i]


def output_dict_obj():
    myD = {1: 'a', 2: 'b'}
    for key, value in dict.items(myD):
        print key, value
        time.sleep(1)  # 暂停 1 秒


def check_instance_type(n):
    if isinstance(n, int):
        print "n is int."
    if isinstance(n, str):
        print "n is string."


def output_object_type(obj):
    print type(obj)


def tuple_operation():
    # create tuple
    tup1 = ('physics', 'chemistry', 1997, 2000)
    tup2 = (1, 2, 3, 4, 5, 6, 7)
    tup3 = "a", "b", "c", "d"

    # create empty tuple
    tup4 = ()

    # there is only 1 element in tuple, you must add ","
    tup5 = (50,)

    # Access tuple
    print "tup1[0]: ", tup1[0]
    print "tup2[1:5]: ", tup2[1:5]

    # Can't change element value in tuple
    # Can't delete element value in tuple too, but we can delete entire tuple.

    # built-in function
    cmp(tup1, tup2)
    len(tup3)
    my_seq = ['fox', 'tiger', 'rabbit', 'snake']  # convert list to tuple
    my_tup = tuple(my_seq)
    print my_tup[2]

    # we can change
    t = ('a', 'b', ['A', 'B'])
    t[2][0] = 'X'
    t[2][1] = 'Y'

    print t


def main():
    check_instance_type(100)
    check_instance_type("100")

    obj = "string"
    print type(obj)

    tuple_operation()

    print "Exit the program."


if __name__ == '__main__':
    main()
