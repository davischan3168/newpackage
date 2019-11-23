#!/usr/bin/python3
# _*_ coding:utf-8 _*_
import os
from chardet import detect

def runcoding(path):
    fls=[]

    if os.path.isfile(path):
        fls.append(path)
        print('%s is a file'%path)
    elif os.path.isdir(path):
        print('%s is a dir'%path)
        for root,ds,files in os.walk(path):
            for f in files:
                if f.lower().endswith ('.txt'):
                    fls.append(os.path.join(root,f))
    if len(fls)>0:
        for f in fls:
            with open(f,'rb+') as fileObj:
                fileContent = fileObj.read()
                #判断编码格式
                encodingtype = detect(fileContent)['encoding']
                #ansi编码检测结果为none
                if encodingtype.lower() in ['gbk','gb2312']:
                    encodingtype='gb18030'
                if encodingtype==None:
                    print(filename)
                    continue
                #print(encodingtype)
                #格式转换
                #print(encodingtype)
                fileContent = fileContent.decode(encodingtype).encode('utf8')
                #写回文件
                fileObj.seek(0)
                fileObj.write(fileContent)

                
    return

def convert(filename, in_enc = ["ASCII","GB2312","GBK","gb18030"], out_enc = "UTF-8"):
    try:
        print "convert " + filename
        content = open(filename).read()
        result = chardet.detect(content)
        coding = result.get("encoding")
        for k in in_enc:
            if k == coding:
                print( coding + " To UTF-8")
                new_content = content.decode(coding).encode(out_enc)
                open(filename,'w').write(new_content)
                print( "done.")
                break;
    except IOError as e:
        print("error")


if __name__=="__main__":
    #runcoding(g_filedir)
    import sys
    runcoding('林彪传.txt')
    #pass
