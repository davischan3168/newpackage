#!/usr/bin/env python3
# -*-coding:utf-8-*-

import psycopg2
pyconn = psycopg2.connect(database="pysdd", user="postgres", password="801019", host="127.0.0.1", port="5432")
pycur = pyconn.cursor()
from AI.BaiduAI import BaiDAI
from playsound import playsound
import requests
from bs4 import BeautifulSoup
import re
import os

select = "select distinct title, chaodai, author, poemtext, playid from mypoemtable where tag like '%{}%'"

def spsql(select):
    pycur.execute(select)
    df = pycur.fetchall()
    return df

def getPlayurl(pid):
    """
    播放诗词的主体内容
    """
    
    url='https://so.gushiwen.org/viewplay.aspx?id=%s'%pid
    r=requests.get(url)
    soup=BeautifulSoup(r.content,'lxml')
    d=soup.find(src=re.compile('^https:'))
    href=d.get('src')
    playsound(href)
    return

BD = BaiDAI()

def playst(text):
    fp='audio/tems.mp3'
    with open(fp,'wb') as f:
        f.write(BD.Text2Audiov2(text))

    playsound(fp)
    os.remove(fp)
    return

def playTS(ss = select.format('唐诗三百')):
    df = spsql(ss)
    for d in df:
        try:
            playst(d[0].strip())
            # print(d[0]+'--'*10)
        except:
            pass
        
        print(d[0]+'--'*10)
        time.sleep(10)
        getPlayurl(d[-1].strip())
        print(d[3])
        print('----'*10+'\n')

    return

if __name__ == "__main__":
    df = spsql(select.format('唐诗三百'))
    for d in df:
        playst(d[0].strip())
        time.sleep(10)
        getPlayurl(d[-1].strip())
        print(d[3])
        print('----'*10+'\n')
