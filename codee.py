#!/usr/bin/python3.10
# -*- coding: utf-8 -*-
# Copyright (C) 2023 , Inc. All Rights Reserved 
# @Time    : 2023/5/8 21:22
# @Author  : raindrop
# @Email   : 1580925557@qq.com
# @File    : codee.py.py
from flask import Flask, request, jsonify
#from flask_cors import CORS

import codes
import os
import requests

app = Flask(__name__)
#CORS(app,resource=r'/*')


@app.route('/url',methods=['POST'])
def func():
    if request.method=="POST":
        url=request.form.get("u")
        print("收到链接"+str(url))
        for i in range(30):
            img = requests.get(url)
            with open('code.jpg', 'wb') as f:
                f.write(img.content)
            a = codes.main('code.jpg')
            print(a)
            if len(a) == 4:
                res = {"result": a}
                break
            else:
                res = {"result": "识别失败"}
        return jsonify(code=0, data=res)




if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8899)