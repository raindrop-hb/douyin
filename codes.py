#!/usr/bin/python3.10
# -*- coding: utf-8 -*-
# Copyright (C) 2023 , Inc. All Rights Reserved 
# @Time    : 2023/4/24 12:07
# @Author  : raindrop
# @Email   : 1580925557@qq.com
# @File    : demo.py
try:
    import ddddocr
except:
    pass


def main(code_dir):
    try:
        ocr = ddddocr.DdddOcr()
        with open(code_dir, 'rb') as f:
            image = f.read()
        res = ocr.classification(image)
        return res
    except:
        print('脚本目录下无ddddocr文件')
        exit()
