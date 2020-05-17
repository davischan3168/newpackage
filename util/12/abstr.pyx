#cython:language_level=3
#!/usr/bin/env python3
# -*-coding:utf-8-*-
import re
import shutil
import os
import sys
# cython: language_level=3

def getTt(path,rc=re.compile('.*?案\s*（检例第\d*号）|.*?案\s*\n+')):#,p1=re.compile('\s*【要\s*旨】')):

    with open(path,encoding='utf8') as f:
        text=f.read()

    tt = rc.findall(text)
    txt = rc.split(text)

    ftxt = list(zip(tt,txt[1:]))

    dlis = []
    for x in ftxt:
        f = x[1].strip()
        if len(f)>0:
            dlis.append((x[0].strip(),f))

    return dlis


#def getTtv1(path,rc=re.compile('([\w+\W].*?)\n*\w*.*?基本案情\n+')):
def getTtv1(path,rc=re.compile('[\w+\W].*?\n*.*?基本案情】*\n*',re.M)):
    #                          '([\w\W].*?)\n*.*?基本案情】*\n+'
    with open(path,encoding='utf8') as f:
        text=f.read()

    tt = rc.findall(text)
    #ftxt = []
    #将主体的文件分离出来
    txt = rc.split(text)

    ftxt = list(zip(tt,txt[1:]))

    dlis = []
    for x in ftxt:
        f = x[1].strip()
        if len(f)>0:
            dlis.append((x[0].strip(),f))    

    return dlis

def gtTall(path,rc=re.compile('.*?案\s*（检例第\d*号）|.*?案\s*\n+'),\
           rc1=re.compile('[\w+\W].*?\n*.*?基本案情】*\n+',re.M)):

    df = getTt(path,rc)

    if len(df) == 0:
        df = getTtv1(path,rc1)

        if len(df) == 0:
            title = os.path.basename(os.path.splitext(path)[0])
            text = open(path,'r',encoding='utf8').read()
            df = [(title,text)]

    return df


def gtTallDir(dirpath,rc=re.compile('.*?案\s*（检例第\d*号）|.*?案\s*\n+'),\
           rc1=re.compile('[\w+\W].*?\n*.*?基本案情】*\n+',re.M)):

    DP = []
    if isinstance(dirpath,list):
        for p in dirpath:
            if os.path.isdir(p):
                DP.append(p)
                
    elif isinstance(dirpath,tuple):
        dirpath = list(dirpath)
        for p in dirpath:
            if os.path.isdir(p):
                DP.append(p)
    elif os.path.isdir(dirpath):
        DP.append(dirpath)        
        

    tem = []

    for dirpath in DP:
        for r,ds,fs in os.walk(dirpath):
            for f in fs:
                path = os.path.join(r,f)
                try:
                    ds = gtTall(path,rc,rc1)
                except:
                    title = os.path.basename(os.path.splitext(path)[0])
                    text = open(path,'r',encoding='utf8').read()
                    ds = [(title,text)]                
                    pass
                if len(ds)>0:
                    tem.extend(ds)

    return tem
