#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# uzip.py
"""
解决在linux下解压的乱码问题
""" 
import os
import sys
import zipfile
from unrar import rarfile
import tarfile  
#import codecs

def uzipall(fpath):
    """
    解压缩zip类型的文件,可以自动识别是在py2或py3的环境
    """
 
    print("Processing File %s" %fpath)
    file=zipfile.ZipFile(fpath,"r")

    for name in file.namelist():
        if sys.version[0] == '2':
            uname=name.decode('gbk')
        elif sys.version[0] == '3':
            uname=name.encode('cp437')
            uname=uname.decode('gbk')
            
        print("Extracting %s"  %uname)
        pathname = os.path.dirname(uname)
        if not os.path.exists(pathname) and pathname!= "":
            os.makedirs(pathname)
            
        data = file.read(name)
        if not os.path.exists(uname):
            try:
                fo = open(uname, "w")
                fo.write(data)
            except:
                fo = open(uname, "wb")
                fo.write(data)
            fo.close
            
    file.close()
    return

def decompress(mfile,decpres=True,*GSfs):
    """
    mfile:压缩文件，待解压的文件。
    GSfs：是需要解压出来的文件。
    Return：
          压缩文件中所包含的文件列表。
    """
    if isinstance(GSfs,str):
        lis=[]
        lis.append(GSfs)
        GSfs=lis
        print(GSfs)
        del lis

    #mfile=os.path.abspath(mfile)
    if os.path.splitext(mfile)[1].lower()=='.rar':
        rf=rarfile.RarFile(mfile,'r')
        listf=rf.namelist()
        namelist=[rf.filename+'//'+i for i in listf]
        if len(GSfs)>0:
            if not os.path.exists('extract'):
                os.mkdir('extract')
            for i in GSfs:
                if i in listf:
                    rf.extract(i,'extract/')
                else:
                    print('File %s is not in the Compress File'%i)
        #rf.close()
        elif decpress:
            if not os.path.exists('extract'):
                os.mkdir('extract')
            for i in listf:
               rf.extract(i,'extract') 
        return namelist
    elif os.path.splitext(mfile)[1].lower()=='.zip':
        rf=zipfile.ZipFile(mfile,'r')
        listf=rf.namelist()
        namelist=[rf.filename+'//'+i for i in listf]
        if len(GSfs)>0:
            if not os.path.exists('extract'):
                os.mkdir('extract')
            for i in GSfs:
                if i in listf:
                    rf.extract(i,'extract')
        elif decpress:
            if not os.path.exists('extract'):
                os.mkdir('extract')
            for i in listf:
               rf.extract(i,'extract')                     
        rf.close()        
        return namelist        
    elif os.path.splitext(mfile)[1].lower() in ['.tar','.gz']:
        rf=tarfile.open(mfile,'r')
        listf=rf.getnames()
        namelist=[rf.name+'//'+i for i in listf]
        if len(GSfs)>0:
            if not os.path.exists('extract'):
                os.mkdir('extract')
            for i in GSfs:
                if i in listf:
                    rf.extract(i,'extract')
        elif decpress:
            if not os.path.exists('extract'):
                os.mkdir('extract')
            for i in listf:
               rf.extract(i,'extract')                     
        rf.close()        
        return namelist        
    else:
        return False

if __name__=="__main__":
    #f=sys.argv[1]
    #uzipall(f)
    pass
