#!/usr/bin/python3.10
# -*- coding: utf-8 -*-
# Copyright (C) 2023 , Inc. All Rights Reserved 
# @Time    : 2023/4/26 0:58
# @Author  : raindrop
# @Email   : 1580925557@qq.com
# @File    : demo2.py
import time

import requests
import re
from urllib.parse import quote
import json
import os
import codes
from logs import loggs


def main(url,save_path,name):
    loggs('正在上传百度网盘')
    check_url=config()["check_url"]
    for i in range(10):
        try:
            if '/video/' in url:
                url = quote(url)
                pan_url = check_url + '/download.php'
                res = requests.get(pan_url + '?url=' + url + '&name=' + name + '.mp4')
                pan_url = check_url + '/' + name + '.mp4'
                delete_name=name + '.mp4'
            else:
                pan_url = check_url + '/download.php'
                res = requests.get(pan_url + '?url=' + url + '&name=' + name + '.jpeg')
                pan_url = check_url + '/' + name + '.mp4'
                delete_name = name + '.jpeg'
            res = res.text
            if res == "True":
                break
        except:
            loggs('触发高频错误，休眠10秒后继续执行')
            time.sleep(10)

    pan_s = config()['upload']['baidu_pan']['pan_s']
    if not eval(pan_s):
        return '关闭上传网盘'
    code=0
    vcode=0
    aaa=0
    for i in range(10):
        aaa+=1
        a=bdp_vice(pan_url, save_path,code, vcode)
        print("第{}次尝试上传网盘".format(str(aaa)))
        if a=='上传成功':
            return '上传百度网盘成功,'+delete_name
        else:
            try:
                code,vcode=a.split(',')
            except:
                code=0
                vcode=0
    return '上传失败,'+delete_name





def bdp_vice(url,save_path,code=0,vcode=0):
    bdp_url = config()['upload']['baidu_pan']['baidupan_url']
    bdp_cookie = config()['upload']['baidu_pan']['baidupan_cookie']
    logid=int(logidd())+2
    bd_url = re.sub('(\d{15,30})', str(logid), bdp_url)
    if code:
        loggs('传入验证码上传网盘')
        data = {'method': 'add_task', 'source_url': url, 'save_path': '/'+save_path+'/', 'app_id': '250528','input':code,'vcode':vcode}
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.54',
            'content-type': 'application/x-www-form-urlencoded',
            'referer': 'https://pan.baidu.com/disk/main',
            'cookie': bdp_cookie
        }
        response = requests.post(bd_url, data=data, headers=headers)
        response = json.loads(response.text)
        loggs(response)
        if 'error_code' in response:
            error_code = response['error_code']
            if error_code == '36020':
                return "下载地址无效，请核对"
            if error_code == 36031:
                loggs(response['show_msg']+'休眠10秒')
                time.sleep(10)
                return response['show_msg']
            if error_code == -19:
                img = response['img']
                code=code_img(img)
                loggs('出现验证码')
                return str(code) + ',' + response['vcode']
        elif "task_id" in response:
            loggs('网盘保存位置：{}'.format(response['save_path']))
            return '上传成功'
        else:
            return '未知错误'
    else:
        #无验证码
        data = {'method': 'add_task', 'source_url': url, 'save_path':'/'+save_path+'/', 'app_id': '250528'}
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.54',
            'content-type': 'application/x-www-form-urlencoded',
            'referer': 'https://pan.baidu.com/disk/main',
            'cookie': bdp_cookie
        }
        response = requests.post(bd_url, data=data, headers=headers)
        response = json.loads(response.text)
        loggs(response)
        if 'error_code' in response:
            error_code=response['error_code']
            if error_code=='36020':
                return "下载地址无效，请核对"
            if error_code == 36031:
                loggs(response['show_msg']+'休眠10秒')
                time.sleep(10)
                return response['show_msg']
            if error_code==-19:
                loggs('出现验证码')
                img=response['img']
                code=code_img(img)
                return str(code)+','+response['vcode']
        elif "task_id" in response:
            return '上传成功'
        else:
            return '未知错误'
    loggs(logidd(logid))

def logidd(logid=0):
    path = os.getcwd()
    if path == '/opt/function':
        path = 'tmp/cache/'
    else:
        path = 'cache/'
    with open(path + 'cache.json', 'r') as f:
        cache=json.load(f)
        '''cac=f.read()
        #cache=eval(cache)
        cache = json.loads(cac)
        #cache = json.load(f)'''
    if not logid:
            account=cache["logid"]
            return account
    else:
        with open(path + 'cache.json', 'w+') as f:
            cache["logid"]=logid
            json.dump(cache, f,indent=4, ensure_ascii=False)
            #f.write(str(cache))
            #json.dump(cache, f, indent=4, ensure_ascii=False)
            return 'ok'




def code_img(url):
    path = os.getcwd()
    if path == '/opt/function':
        path = 'tmp/cache/'
    else:
        path = 'cache/'
    code_url=config()['upload']['baidu_pan']['code_url']
    if 'http' in code_url:
        data={'u':url}
        for i in range(30):
            s = i + 1
            try:
                codee=requests.post(code_url,data=data)
                print(codee.text)
                img = json.loads(codee.text)
                a = img["data"]["result"]
                loggs('第' + str(s) + '次识别验证码:' + a)
                if len(a) == 4:
                    loggs('长度符合')
                    return a
            except:
                print("什么废物服务器？休眠3秒再识别")
                time.sleep(3)

    else:
        for i in range(30):
            s=i+1
            img=requests.get(url)
            with open(path + 'code.jpg', 'wb') as f:
                f.write(img.content)
            a=codes.main(path + 'code.jpg')
            loggs('第'+str(s)+'次识别验证码:'+a)
            if len(a)==4:
                loggs('长度符合')
                return a

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
    account=re.sub(' ', '', account)
    account = re.sub('\n', '', account)
    b=account.find('"cookie":')+10
    c=account.find('","url"')
    cookie=account[b:c]
    account=account[:b]+account[c:]
    account=eval(account)
    account["cookie"]=cookie
    return account

#bdp_main('https://p9-pc-sign.douyinpic.com/tos-cn-i-0813/fddd327cd93a406c92cf877a3961ed01~tplv-dy-aweme-images:q75.jpeg?biz_tag=aweme_images&from=3213915784&s=PackSourceEnum_AWEME_DETAIL&se=false&x-expires=1684422000&x-signature=1r9LI0K1wPhPz3tIcObkvDMAT4M%3D','ceshi2')

#code_img("https://pan.baidu.com/genimage?3332423865633234636166333465663732323763363637363764323966666433666238383631393638393230303030303030303030303030303136383336333434333373AFB9E96D947965B7E5E7346B6A5F73")
#main(url)
