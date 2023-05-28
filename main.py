#!/usr/bin/python3.10
# coding=UTF-8
# -*- coding: utf-8 -*-
# Copyright (C) 2023 , Inc. All Rights Reserved 
# @Time    : 2023/5/23 12:07
# @Author  : raindrop
# @Email   : 1580925557@qq.com
# @File    : main.py

import requests
import push
import bdpan
import time
import json
from logs import loggs
import re
import os
import csv


class Task(object):
    def __init__(self, sec_user_id):
        self.nickname = None
        self.sec_user_id = sec_user_id
        self.delete = list()

    def inits(self):
        configs = config()
        path = os.getcwd()
        if path == '/opt/function':
            path = 'tmp/cache'
        else:
            path = 'cache/'
        url = 'https://www.douyin.com/aweme/v1/web/aweme/post/?device_platform=webapp&aid=6383&channel=channel_pc_web&sec_user_id=' + self.sec_user_id + '&max_cursor=' + str(
            int(round(
                time.time() * 1000))) + '&locate_query=false&show_live_replay_strategy=1&count=200&publish_video_strategy_type=2&pc_client_type=1&version_code=170400&version_name=17.4.0&cookie_enabled=true&screen_width=1536&screen_height=864&browser_language=zh-CN&browser_platform=Win32&browser_name=Chrome&browser_version=108.0.5359.95&browser_online=true&engine_name=Blink&engine_version=108.0.5359.95&os_name=Windows&os_version=10&cpu_core_num=8&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=250'
        headers = {
            'referer': 'https://www.douyin.com/user/' + self.sec_user_id,
            'cookie': configs['cookie'],
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.95 Safari/537.36'
        }
        resp = requests.get(url, headers=headers)
        resp = resp.text.encode('gbk',errors='ignore').decode('gbk')
        try:
            resp = json.loads(resp)
        except:
            print('cookies失效')
            exit()
        self.nickname = resp["aweme_list"][0]["author"]["nickname"]
        if not os.path.exists(path + "/" + self.nickname + ".csv"):
            with open(path + "/" + self.nickname + ".csv", 'w', newline='',encoding='utf-8') as csvfile:
                fieldnames = ['aweme_id', '时间', 'title', '格式', '收藏', '评论', '点赞', '分享', 'share_url']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
        return resp

    def infos(self, aweme):
        path = os.getcwd()
        if path == '/opt/function':
            path = 'tmp/cache'
        else:
            path = 'cache/'
        with open(path + "/" + self.nickname + ".csv", 'r',encoding='utf-8') as f:
            reader = csv.reader(f)
            aweme_rows = [row for row in reader]
        with open(path + "/" + self.nickname + ".csv", 'r',encoding='utf-8') as f:
            reader = csv.reader(f)
            aweme_list = [row[0] for row in reader]
        if type(aweme) != list:
            if aweme not in aweme_list:
                return 0
            else:
                return 1
        elif type(aweme) == list:
            # print(aweme)
            a = aweme[0]
            if a not in aweme_list:
                with open(path + "/" + self.nickname + ".csv", 'a', newline='',encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(aweme)
                print('添加成功')
            else:
                seat = aweme_list.index(a)
                aweme_rowscopy = aweme_rows
                aweme_rows[seat] = aweme
                try:
                    with open(path + "/" + self.nickname + ".csv", 'w', newline='',encoding='utf-8') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerows(aweme_rows)
                    print('写入成功')
                except:
                    print("写入错误")

    def main(self):
        # 所有数据初始化
        resp = self.inits()
        for aweme in resp["aweme_list"]:
            a = aweme['desc']
            a.encode('utf-8')
            print(aweme['desc'])
            desc = aweme["statistics"]
            desc['收藏'] = desc.pop('collect_count')
            desc['评论'] = desc.pop('comment_count')
            desc['点赞'] = desc.pop('digg_count')
            desc['分享'] = desc.pop('share_count')
            desc['share_url'] = aweme['share_url']
            if aweme['images'] == None:
                desc['格式'] = "video"
            else:
                desc['格式'] = "picture"
            del desc['play_count']
            del desc['admire_count']
            time_1 = int(aweme["create_time"])
            # 转换成localtime
            time_2 = time.localtime(time_1)
            # 转换成新的时间格式
            desc['时间'] = time.strftime("%Y-%m-%d %H:%M:%S", time_2)
            desc['title'] = aweme['desc']
            desc={'aweme_id':desc['aweme_id'], '时间':desc['时间'],'title': desc['title'],'格式': desc['格式'],'收藏': desc['收藏'],'评论': desc['评论'],'点赞': desc['点赞'],'分享':desc['分享'],'share_url': desc['share_url']}
            # 视频
            print('-------------------------------------')
            if not self.infos(desc['aweme_id']):
                sq=[]
                print('数据不存在')
                if aweme['images'] == None:
                    url = aweme["video"]["play_addr"]["url_list"][0]
                    loggs('解析到链接:' + url)
                    res, delete_name = bdpan.main(url, self.nickname, desc['aweme_id']).split(',')
                    i = '\n<a href=\"' + url + '">视频无水印链接</a>  ' + str(res)
                    self.delete.append(delete_name)
                    sq.append(i)
                else:
                    url_list = aweme["images"]
                    s = 0
                    for i in url_list:
                        s += 1
                        url = i["url_list"][1]
                        loggs('解析到链接:' + url)
                        res, delete_name = bdpan.main(url, self.nickname, desc['aweme_id'] + '_' + str(s)).split(',')
                        y = '\n<a href=\"' + i["url_list"][1] + '">图片无水印链接</a>  ' + str(res)
                        #self.delete.append(delete_name)
                        sq.append(y)
                        print(url)
                self.pushing(sq,desc)
            desc_1 = []
            for i in desc:
                desc_1.append(desc[i])
            #desc = [desc['aweme_id'], desc['时间'], desc['title'], desc['格式'], desc['收藏'], desc['评论'],desc['点赞'], desc['分享'], desc['share_url']]
            self.infos(desc_1)
        self.pan_delete()

    def pushing(self,sq,desc):
        logg = []
        log="[玫瑰][玫瑰]raindrop---抖音更新小助手[玫瑰][玫瑰]\n更新如下:\n[昵称]:"+self.nickname
        del desc['share_url']
        for i in desc:
            log=log+'\n['+str(i)+']:'+str(desc[i])
        logg.append(log)
        forss = len(sq) - 1
        if forss >= 5:
            fors = forss // 5
        log='链接如下：'
        if len(sq) <= 5:
            for s in sq:
                log = log + s
            logg.append(log)
        else:
            for s in sq[0:5]:
                log = log + s
            logg.append(log)
            sq = sq[5:len(sq)]
            for ii in range(fors):
                if len(sq) <= 5:
                    log = '接上：'
                    for s in sq:
                        log = log + s
                    logg.append(log)
                else:
                    log = '接上：'
                    for s in sq[0:5]:
                        log = log + s
                    logg.append(log)
                    sq = sq[5:len(sq)]
        for i in logg:
            push.main(i)
        print(logg)

    def pan_delete(self):
        if len(self.delete)>0:
            configs=config()
            time.sleep(50)
            for i in self.delete:
                res = requests.get(configs['check_url']+'/delete.php?file='+i)
                loggs('释放内存'+res.text)



def now():
    time_1 = int(time.time())
    # 转换成localtime
    time_2 = time.localtime(time_1)
    # 转换成新的时间格式
    nows = time.strftime("%Y-%m-%d %H:%M:%S", time_2)
    return nows


def config():
    path = os.getcwd()
    if path == '/opt/function':
        path = 'code/'
    else:
        path = ''
    with open(path + 'config.json', encoding='utf-8') as f:
        account = f.read()
    a = account.count('/*')
    for i in range(a):
        x = account.find('/*')
        y = account.find('*/') + 2
        account = account[:x] + account[y:]
    account = re.sub(' ', '', account)
    account = re.sub('\n', '', account)
    b = account.find('"cookie":') + 10
    c = account.find('","url"')
    cookie = account[b:c]
    account = account[:b] + account[c:]
    account = eval(account)
    account["cookie"] = cookie
    return account


def main():
    configs = config()
    path = os.getcwd()
    if config()["logs"] == "False":
        print('当前日志：静默模式')
    if path == '/opt/function':
        path = 'tmp/cache/'
    else:
        path = 'cache/'
    if not os.path.exists(path + "cache.json"):
        loggs('创建缓存文件')
        try:
            os.mkdir(path)
        except:
            loggs('缓存文件夹已存在')
        cache = {
            "logid": 94808200712254930442
        }
        with open(path + 'cache.json', 'w+') as f:
            json.dump(cache, f, indent=4, ensure_ascii=False)
    time_start = float(round(time.time()))
    print("欢迎使用抖音更新小助手\n开始执行")
    print(now())
    for i in configs["url"]:
        url = requests.head(i)
        headers = {
            "cookie": configs['cookie']
        }
        url = str(url.headers.get('location'))
        url = requests.head(url, headers=headers).headers['Location']
        if "?previous_page=app_code_link" in url:
            url = re.findall('https://www.douyin.com/user/(.*)\?previous_page=app_code_link', url)[0]
        task = Task(url)
        # task.infos()
        task.main()
    loggs('运行结束')
    print(now())
    time_end = float(round(time.time()))
    time_diff = int(time_end - time_start)
    if time_diff >= 3600:
        hh = time_diff // 3600
        time_diff = time_diff % 3600
    else:
        hh = 0
    if time_diff >= 60:
        mm = time_diff // 60
        time_diff = time_diff % 60
    else:
        mm = 0
    if time_diff > 0:
        ss = time_diff
    print('本次执行共耗时{}时{}分{}秒'.format(str(hh), str(mm), str(ss)))


if __name__ == '__main__':
    main()
