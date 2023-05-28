# 抖音自动解析并推送微信，上传云盘(粉丝神器)

<p align="center">
    <a href="https://github.com/raindrop-hb"><img alt="Author" src="https://img.shields.io/badge/author-raindrop-blueviolet"/></a>
    <img alt="PHP" src="https://img.shields.io/badge/code-Python-success"/></a>
    <a href="https://jq.qq.com/?_wv=1027&k=fzhZMSbP"><img alt="QQ群" src="https://img.shields.io/badge/QQ-交流群-blackviolet"/></a>
</p>


通过解析官方网站，每天自动检测博主的更新动态，并将作品信息和无水印链接push到微信,自动上传至百度网盘。

一个账号平均耗时为3分钟左右。放在服务器运行不需要人工干预，支持无服务器的云函数部署，每天自动push相关信息。
![MGKOZYKFC51%%FK7_`D(QZX_tmb](https://github.com/raindrop-hb/douyin/assets/72308008/dbff64ea-192c-449e-add6-8b12041c89dc)




------
目前已实现功能：


- [x] 自动执行
- [x] 推送到微信
- [x] 无水印视频上传至百度网盘
- [x] 自动识别验证码
- [x] 生成视频数据表格
- [x] 自定义博主主页链接

如有其他好的建议请提交issues

## 环境要求
python 3.6 

## 文件说明
| 文件名 | 说明|其他|
| -------- | ----- | ----- |
| main.py | 入口 |无|
| bdpan.py | 百度网盘 |无|
| push.py | 消息推送 |无|
| logs.py | 输出日志 |无|
| codes.py | 本地验证码识别 |无|
| PHP/download.php | 临时下载 |若不想/不会搭建，可以在check_url填http://dy.hanbao16.top|
| PHP/delete.php | 释放内存|若不想/不会搭建，可以在check_url填http://dy.hanbao16.top|
| ddddocr | 验证码识别 |青龙和云函数需要使用识别接口，不想/不会搭建可以在code_url填http://code.hanbao16.top/url|

## 青龙面板部署方法
![image](https://github.com/raindrop-hb/douyin/assets/72308008/dcb33eeb-03d9-48c2-993e-bcb23548aaae)

### 一、Fork 此仓库

### 二、上传青龙面板

新版青龙直接订阅git@github.com:raindrop-hb/mimotion.git

### 三、安装模块

包括requests、re、urllib.parse、json、os、csv

### 四、填写config.json

配置文件都有说明，自己看就行。

check_url是视频转储，需要上传download.php和delete.php，实在不行可以用我的；http://dy.hanbao16.top;

code_url是验证码识别接口，使用flask框架，需要上传code文件，实在不行可以用我的；http://code.hanbao16.top/url。


### 设置项


| 设置项 |  内容  |说明|
| -------- | ----- |----- |
|cookie|抖音pc登录时的cookie|必填|
|url|填写你要监控的博主填写你要监控的博主|必填|
|check_url|末尾不要加/|必填|
|pan_s|上传网盘开关 True或False|必填|
|baidupan_url|百度网盘链接|非必填|
|baidupan_cookie|百度网盘cookie|非必填|
|check_url|验证码识别|必填|




### 抓取抖音cookie
![image](https://user-images.githubusercontent.com/72308008/227768965-298d07e7-d75f-4861-8e7a-dc313484a90b.png)

1.手机复制博主主页链接，电脑访问

2.手机号登录抖音后按F12，点全部-标头，刷新一下，随便找一个数据包，在请求标头里应该都会有cookie

### 抓取百度网盘链接及cookie
![image](https://user-images.githubusercontent.com/72308008/229359685-fc4b0538-481b-4a11-917c-c6f60af5910c.png)

pc登录百度网盘后，先按F12，再离线下载链接https://user-images.githubusercontent.com/72308008/229359685-fc4b0538-481b-4a11-917c-c6f60af5910c.png
，找到上图数据，请求url即为baidupan_url，下滑找到cookie，即为baidupan_cookie

