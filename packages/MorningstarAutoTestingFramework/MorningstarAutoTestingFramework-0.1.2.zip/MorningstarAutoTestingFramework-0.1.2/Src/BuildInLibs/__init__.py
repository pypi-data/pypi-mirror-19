# -*- coding: utf-8 -*-

import time


def get_time_in_millies():
    time_millies = lambda: int(round(time.time() * 1000))

    return time_millies


def main():
    print "Do something."


if __name__ == '__main__':
    main()
