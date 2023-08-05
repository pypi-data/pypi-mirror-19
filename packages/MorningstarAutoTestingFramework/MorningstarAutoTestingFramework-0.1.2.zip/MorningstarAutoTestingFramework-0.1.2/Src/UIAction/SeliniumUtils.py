# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary


# TODO: Benjamin 2016/11/29 这个方法在Firefox V47.0 之上仍然无效。目前的做法只能是将FireFox降级
def open_firefox_with_gecko_driver():
    binary = FirefoxBinary('C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe')
    return webdriver.Firefox(firefox_binary=binary)


def open_chrome():
    return webdriver.Chrome()


def open_ie():
    return webdriver.Ie()


def main():
    wd = open_chrome()
    wd.implicitly_wait(15)
    wd.maximize_window()
    wd.get("http://www.baidu.com")


if __name__ == '__main__':
    main()
