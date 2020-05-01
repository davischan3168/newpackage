#!/usr/bin/env python3
# -*-coding:utf-8-*-

from selenium import webdriver
import time,re,sys
import os
import pandas as pd
import numpy as np
from io import StringIO
import lxml.html,requests
from bs4 import BeautifulSoup
import urllib.parse
from webdata.util.hds import user_agent as hds
import webdata as wd

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
#from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

def Firefox_hdless():
    options = webdriver.FirefoxOptions()
    options.add_argument('-headless')
    profile = webdriver.FirefoxProfile()
    profile.set_preference('permissions.default.image', 2)
    profile.set_preference('dom.ipc.plugins.enabled.npswf32.dll', 'false')
    profile.set_preference('javascript.enabled', 'false')
    browser = webdriver.Firefox(options=options,firefox_profile = profile)
    return browser

def getGb_case(url,pre_pages=12):
    """
    url:
    pre_pages:前几页
    """
    driver=Firefox_hdless()
    driver.get(url)


    html=lxml.html.parse(StringIO(driver.page_source))
    ls=html.xpath('//ul[@id="datas"]/li/span')
    lss=[]
    """
    for i in ls:
        case_name = i.xpath('a/text()')[0]
        qi_name = i.xpath('lable/text()')[0]
        href = 'http://gongbao.court.gov.cn' + i.xpath('a/@href')[0]
        lss.append([case_name,qi_name,href])
    """
    
    for i in range(pre_pages-1):
        print("Getting page %s ......."%i)
        try:
            
            
            html=lxml.html.parse(StringIO(driver.page_source))
            ls=html.xpath('//ul[@id="datas"]/li/span')
            for i in ls:
                case_name = i.xpath('a/text()')[0]
                qi_name = i.xpath('lable/text()')[0]
                href = 'http://gongbao.court.gov.cn' + i.xpath('a/@href')[0]
                lss.append([case_name,qi_name,href])
            driver.find_element_by_link_text("下一页").click()
            driver.implicitly_wait(30)
            time.sleep(1)
        except Exception as e:
            driver.back()
            print(e)
            pass
        
    return lss

def _gettxt(url):
    r=requests.get(url,headers=hds())
    txt=r.content.decode('utf8')
    html=lxml.html.parse(StringIO(txt))
    #title=html.xpath('//div[@class="detail_tit"]/text()')
    tls=html.xpath('//div[@id="gb_content"]//p/text()')
    #tls=[i.replace('\n','') for i in tls]
    #text='\n'.join(tls)
    text=''.join(tls)
    #tza=title[0]+'\n\n'+text
    return text

def _gettxtv1(url):
    r=requests.get(url,headers=hds())
    txt=r.content.decode('utf8')
    ff=BeautifulSoup(txt,'lxml')
    soup=ff.find('div',id="gb_content")
    text=[]
    sources=soup.findAll('p')
    for i in sources:
        text.append(i.text)
    texts='\n'.join(text)
    
    return texts

def _Write(path,content):
    try:
        with open(path,'w',encoding='utf8') as f:
            f.write(content)
    except:
        with open(path,'w',encoding='gbk') as f:
            f.write(content)
    return

def GBCase(url,pre_pages=2):
    hrefs=getGb_case(url,pre_pages)
    for href in hrefs:
        path='law/gongbao/case/'+href[1]+'_'+href[0]+'.txt'
        if not os.path.exists(path):
            df=_gettxtv1(href[2])
            _Write(path,df)
    return

def GBJudicialDocument(url,pre_pages=2):
    hrefs=getGb_case(url,pre_pages)
    for href in hrefs:
        path='law/gongbao/Judicial/'+href[1]+'_'+href[0]+'.txt'
        if not os.path.exists(path):
            df=_gettxtv1(href[2])
            _Write(path,df)
       
    return

def Tohtml(path='law/',func=wd.txt2htmlv1,index=False):
    """
    path:文件夹的名称
    func:txt2html_odir,形成一个个单独的文件
        :txt2htmlv1,合并成一个文件
    """    
    ss={}
    for root,ds,fs in os.walk(path):
        for f in fs:
            #print(f)
            dfd=os.path.splitext(f)
            if dfd[1] in ['.txt']:
                qNo=dfd[0].split('_')
                #dd=re.findall('\d{1,3}',dfd[0])
                #dd=int([i for i in dd if len(i)>0][0])
                ss[qNo[0]]=os.path.abspath(root+'/'+f)

    dds=sorted(ss.items(),key=lambda item:item[0],reverse=True)
    df=[]
    for i in dds:
        print(i)
        df.append(i[1])

    func(df,index=index)
    return

if __name__=="__main__":
    url='http://gongbao.court.gov.cn/ArticleList.html?serial_no=al'
    GBCase(url,2)
    Jurl='http://gongbao.court.gov.cn/ArticleList.html?serial_no=cpwsxd'
    GBJudicialDocument(Jurl,3)
    pass
