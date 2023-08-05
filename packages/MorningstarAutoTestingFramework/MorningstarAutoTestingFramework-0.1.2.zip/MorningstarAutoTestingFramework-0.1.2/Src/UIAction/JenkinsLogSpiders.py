# -*- coding:utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


class JenkinsLogSpiders:
    LoginUsername = ""
    LoginPassword = ""
    wd = webdriver.Firefox

    def __init__(self, user_name, user_password):
        global LoginUsername, LoginPassword, wd
        LoginUsername = user_name
        LoginPassword = user_password
        wd = webdriver.Firefox()
        pass

    def login(self):
        wd.get("https://jenkins.morningstar.com/login?from=%2F")
        wd.maximize_window()

        try:
            """这段可以查看selenium的源码,属于smart wait"""
            email = WebDriverWait(wd, timeout=10).until(EC.presence_of_element_located((By.NAME, 'j_username')),
                                                        message=u'元素加载超时!')
            email.send_keys(LoginUsername)
            password = WebDriverWait(wd, timeout=10).until(EC.presence_of_element_located((By.NAME, 'j_password')),
                                                           message=u'元素加载超时!')
            password.send_keys(LoginPassword)
            wd.find_element_by_id("yui-gen1-button").click()  # 点击登录
        except NoSuchElementException as e:
            print e.message

    def get_pagecontent(self, url):
        try:
            wd.get(url)
            div_log = wd.find_element_by_class_name("console-output")
            log_content = div_log.text
            print(log_content)
        except:
            print("未找到Log区块.")
