#!/usr/bin/env python3
# -*-coding:utf-8-*-

import re
import os
from mswdoc.docx2txt import msdoc2text
#cs = re.compile(r'^[(第\w{1,6}条),(第\w{1,6}条之一),(第\w{1,6}条之二)]')
cs = re.compile(r'^(第\w{1,6}条)|(第\w{1,6}条之一)|(第\w{1,6}条之二)')

def File2item(fpath):
    tem=os.path.splitext(fpath)
    if tem[1].lower() in ['.txt']:
        try:
            txt=open(fpath,'r',encoding='utf8').readlines()
        except:
            txt=open(fpath,'r',encoding='gb18030').readlines()
    elif tem[1].lower() in ['.doc','.docx']:
        text=msdoc2text(fpath)
        txt=text.split('\n')
        #txt=[i.strip() for i in tl if len(i.strip())>0]
    
    txtlist = [i.strip() for i in txt if len(i.strip()) > 0]
    emoi = []
    for i in txtlist:
        if cs.match(i):
    	    emoi.append(i)
        else:
            if len(emoi) > 0:
                emoi[-1] = emoi[-1]+'\n'+i
                
    name = os.path.splitext(os.path.basename(fpath))[0]
    tt = []
    for i in emoi:
        tt.append((i,name))
    return tt

def File2read(fpath):
    tem=os.path.splitext(fpath)
    if tem[1].lower() in ['.txt']:
        try:
            txt=open(fpath,'r',encoding='utf8').readlines()
        except:
            txt=open(fpath,'r',encoding='gb18030').readlines()
    elif tem[1].lower() in ['.doc','.docx']:
        text=msdoc2text(fpath)
        txt=text.split('\n')
        
        
    txtlist = [i.strip() for i in txt if len(i.strip()) > 0]
    name = os.path.splitext(os.path.basename(fpath))[0]
    text = '\n'.join(txtlist)

    return text,name
    

        
def File2all(fpath):
    tem=os.path.splitext(fpath)
    if tem[1].lower() in ['.txt']:
        try:
            txt=open(fpath,'r',encoding='utf8').readlines()
        except:
            txt=open(fpath,'r',encoding='gb18030').readlines()
    elif tem[1].lower() in ['.doc','.docx']:
        text=msdoc2text(fpath)
        txt=text.split('\n')
        #txt=[i.strip() for i in tl if len(i.strip())>0]
    
    txtlist = [i.strip() for i in txt if len(i.strip()) > 0]
    emoi = []
    for i in txtlist:
        if cs.match(i):
    	    emoi.append(i)
        else:
            if len(emoi) > 0:
                emoi[-1] = emoi[-1]+'\n'+i
                
    name = os.path.splitext(os.path.basename(fpath))[0]

    if len(emoi)>0:
        tt = []
        for i in emoi:
            tt.append((i,name))
        return tt
    else:
        text = '\n'.join(txtlist)
        return text,name

def File2dir(path):
    afl = []

    dirl = []
    files = []

    if isinstance(path,list) or isinstance(path,set):
        for pp in path:
            if os.path.isdir(pp):
                dirl.append(pp)
            elif os.path.isfile(pp):
                tem=os.path.splitext(f)[1]
                if tem.lower() in ['.txt','.doc','.docx']:
                    files.append(pp)
    elif isinstance(path,str):
        if os.path.isdir(path):
            dirl.append(path)
        elif os.path.isfile(path):
            tem=os.path.splitext(f)[1]
            if tem.lower() in ['.txt','.doc','.docx']:
                files.append(path)
                
    for ppath in dirl:
        for root,dirs,fs in os.walk(ppath):
            for f in fs:
                tem=os.path.splitext(f)[1]
                if tem.lower() in ['.txt','.doc','.docx'] :            
                    fpath = os.path.join(root,f)
                    files.append(fpath)

    for fpath in files:
        df = File2all(fpath)
        afl.extend(df)

    return afl
        

    

try:
    import psycopg2
    pyconn = psycopg2.connect(database="pysdd", user="postgres", password="801019", host="127.0.0.1", port="5432")
    pycur = pyconn.cursor()
    insert = 'insert into law(item_txt,lawname) values(%s,%s)'
    #pycur.executemany(insert,df)
    #pyconn.commit()
    def insert2psql(df,insert):
        pycur.executemany(insert,df)
        pyconn.commit()
        return
    def F2psql(fpath,insert):
        df = file2item(fpath)
        insert2psql(df,insert)
        return
except Exception as e:
    print(e)
    pass
