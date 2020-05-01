#!/usr/bin/env python3
# -*-coding:utf-8-*-
import sys,os
import re
import requests
import lxml.html
from bs4 import BeautifulSoup
from io import StringIO
import time,re
from webdata.util.hds import user_agent as hds
import pandas as pd

def CZB(url):
    r=requests.get(url,headers=hds())
    try:
        txt=r.content.decode('utf8')
    except:
        txt=r.content.decode('gbk')
    html=lxml.html.parse(StringIO(txt))
    tds=html.xpath('//table[@id="id_bl"]//td[@class="ZITI"]')
    hts=[]
    for td in tds:
        title=td.xpath('@title')[0].replace(u'\xa0','')
        href=td.xpath('a/@href')[0]
        hts.append([title,href])
    return hts

def CZBlist():
    df=[]
    urll='http://www.mof.gov.cn/zhengwuxinxi/zhengcefabu/index_%s.htm'
    urls=[urll%i for i in range(1,23)]
    urls.append('http://www.mof.gov.cn/zhengwuxinxi/zhengcefabu/index.htm')
    for url in urls:
        hs=CZB(url)
        df.extend(hs)

    dff=pd.DataFrame(df,columns=['title','href'])
    return dff

def FGW(url):
    r=requests.get(url,headers=hds())
    try:
        txt=r.content.decode('utf8')
    except:
        txt=r.content.decode('gbk')
    html=lxml.html.parse(StringIO(txt))
    tds=html.xpath('//ul[starts-with(@class,"list_02")]/li[@class="li"]')
    hts=[]
    for td in tds:
        title=td.xpath('a/text()')[0]
        href='http://www.ndrc.gov.cn/zcfb/gfxwj'+td.xpath('a/@href')[0][1:]
        tm=td.xpath('font/text()')[0]
        hts.append([title,href,tm])
    return hts    

def FGWlist():
    df=[]
    urll='http://www.ndrc.gov.cn/zcfb/gfxwj/index_%s.html'
    urls=[urll%i for i in range(1,5)]
    urls.append('http://www.ndrc.gov.cn/zcfb/gfxwj/index.html')
    for url in urls:
        print(url)
        hs=FGW(url)
        print(hs)
        df.extend(hs)
    dff=pd.DataFrame(df,columns=['title','href','time'])
    return dff

def ZJB(url):
    r=requests.get(url,headers=hds())
    try:
        txt=r.content.decode('utf8')
    except:
        txt=r.content.decode('gbk')
    html=lxml.html.parse(StringIO(txt))
    tds=html.xpath('//tr/td[starts-with(@style,"text-align:center")]//tr')
    #print(len(tds))
    hts=[]
    for td in tds:
        try:
            title=''.join(td.xpath('td[2]/a/text()'))
            #print(title)
            href=''.join(td.xpath('td[2]/a/@href'))
            wNo=''.join(td.xpath('td[3]/text()'))
            tm=''.join(td.xpath('td[4]/text()')).replace('[','').replace(']','')
            hts.append([title,href,wNo,tm])
        except Exception as e:
            #print(e)
            pass
    return hts

def ZJBlist():
    df=[]
    urll='http://www.mohurd.gov.cn/wjfb/index_%s.html'
    urls=[urll%i for i in range(1,51)]
    urls.append('http://www.mohurd.gov.cn/wjfb/index.html')
    for url in urls:
        #print(url)
        hs=ZJB(url)
        #print(hs)
        df.extend(hs)
    dff=pd.DataFrame(df,columns=['title','href','No.','time'])
    return dff

def LawDoc(url):
    r=requests.get(url,headers=hds())
    try:
        txt=r.content.decode('utf8')
    except:
        txt=r.content.decode('gbk')
    html=lxml.html.parse(StringIO(txt))
    tds=html.xpath('//div[@id="container"]/div[@class="sec_list"]/ul/li')
    #print(len(tds))
    hts=[]
    for td in tds:
        try:
            title=re.sub(r'\s','',''.join(td.xpath('a/@title')))
            #print(title)
            href='http://www.court.gov.cn'+''.join(td.xpath('a/@href'))
            tm=''.join(td.xpath('i/text()')).replace('[','').replace(']','')
            hts.append([title,href,tm])
        except Exception as e:
            #print(e)
            pass
    return hts
    
if __name__=="__main__":
    pass
    
    
    
