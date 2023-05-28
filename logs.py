#!/usr/bin/python3.10
# -*- coding: utf-8 -*-
# Copyright (C) 2023 , Inc. All Rights Reserved 
# @Time    : 2023/5/7 8:28
# @Author  : raindrop
# @Email   : 1580925557@qq.com
# @File    : logs.py

import requests, json,os

def config():
    path = os.getcwd()
    if path == '/opt/function':
        path = 'code/'
    else:
        path = ''
    with open(path + 'config.json', encoding='utf-8') as f:
        account = f.read()
    a=account.count('/*')
    for i in range(a):
        x=account.find('/*')
        y=account.find('*/')+2
        account=account[:x]+account[y:]
    b=account.find('"cookie":"')+10
    c=account.find('"url"')-8
    cookie=account[b:c]
    account=account[:b]+account[c:]
    account=eval(account)
    account["cookie"]=cookie
    return account



def loggs(loggs):
    if config()["logs"]=="True":
        print(loggs)

