#!/usr/bin/env python3
# -*-coding:utf-8-*-
import tinify
import os
import sys

tinify.key = 'hVXdKgpv8YKwYlMzzypsfN72B9hPZCLj'
#path = "C:\\Users\\yunpoyue\\Pictures\\cat" # 图片存放的路径
#当验证了API key之后，可以通过tinify.compression_count查看当月的API调用次数

def picTinify(path):
    if os.path.splitext(path)[1].lower() in ['.jpg','.jepg','.png']:
        dirpath=os.path.dirname(path)
        npath='optimized_'+os.path.basename(path)
        nimgpath=os.path.join(dirpath, npath)
        print("compressing ..."+ nimgpath)
        tinify.from_file(path).to_file(nimgpath)
    return


def picTinifys(path):
    for dirpath, dirs, files in os.walk(path):
        for f in files:
            if os.path.splitext(f)[1].lower() in ['.jpg','.jepg','.png']:
                imgpath = os.path.join(dirpath, f)
                print("compressing ..."+ imgpath)
                npath='optimized_'+f
                nimgpath=os.path.join(dirpath, npath)
                tinify.from_file(imgpath).to_file(nimgpath)
    return


if __name__=="__main__":
    picTinify(sys.argv[1])
