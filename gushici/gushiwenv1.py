#!/usr/bin/env python3
# -*-coding:utf-8-*-
from selenium import webdriver
import time,sys
from bs4 import BeautifulSoup
from io import StringIO
import requests
import lxml.html
import re
import pickle
from playsound import playsound
if sys.platform == "linux":
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(chrome_options=chrome_options)
else :
    driver = webdriver.PhantomJS()

titleset=set()

base='http://so.gushiwen.org'

def _write(path,content):
    f=open(path,'a')
    f.write(content)
    f.flush()
    return

def waitForLoad(driver):
    elem = driver.find_element_by_tag_name("html")
    count = 0
    while True:
        count += 1
        if count > 20:
            print("Timing out after 10 seconds and returning")
            return
        time.sleep(.5)
        try:
            elem == driver.find_element_by_tag_name("html")
        except StaleElementReferenceException:
            return


def GetAllType(url):
    driver.get(url)
    t = {}
    df = driver.find_elements_by_xpath('//div[@class="main3"]/div[@class="right"]/div[@class="sons"]/div[@class="cont"]/a')
    for i in df:
        t[i.text] = i.get_attribute('href')

    return t

def GetItemsFromType(url):
    driver.get(url)
    t={}
    df=driver.find_elements_by_xpath('//div[@class="main3"]/div[@class="left"]/div[@class="sons"]//a')
    for i in df:
        t[i.text] = i.get_attribute('href')
    return t

def Poem_text(url):
    driver.get(url)
    waitForLoad(driver)
    ss=driver.find_elements_by_partial_link_text('展开阅读全文')
    for i in ss:
        i.click()
        #waitForLoad(driver)

    t = {}
    t['title'] = driver.find_element_by_xpath('//div[starts-with(@class,"cont")]//h1').text
    try:
        t['poem'] = driver.find_element_by_xpath('//div[starts-with(@id,"contson")]').text
    except:
        t['poem']=''
    try:
        t['fy']=driver.find_element_by_xpath('//div[starts-with(@id,"fanyiquan") or contains(@class,"yishang")]').text
    except:
        t['fy']=''
    try:
        t['jx']=driver.find_element_by_xpath('//div[starts-with(@id,"shangxiquan")]').text
    except:
        t['jx']=''
    try:
        t['pid']=driver.find_element_by_xpath('//div[@class="sons"]/div[@class="tool"]//a[starts-with(@href,"javascript:Play")]').get_attribute('href').split('(')[1].replace(')','')

    except:
        t['pid']=''

    return t

def getPlayurl(pid,pl=True):
    """
    播放诗词的主体内容
    """
    
    url='https://so.gushiwen.org/viewplay.aspx?id=%s'%pid
    r=requests.get(url)
    soup=BeautifulSoup(r.content,'lxml')
    d=soup.find(src=re.compile('^https:'))
    href=d.get('src')
    if href:
        if pl:
            playsound(href)
        return href
    else:
        return ''

def getPlayurl_FY(pid,pl=True):
    """
    播放诗词的翻译内容
    """
    url='https://so.gushiwen.org/fanyiplay.aspx?id=%s'%pid
    r=requests.get(url)
    soup=BeautifulSoup(r.content,'lxml')
    d=soup.find(src=re.compile('^https:'))
    href=d.get('src')
    if href:
        if pl:
            playsound(href)
        return href
    else:
        return ''
def getPlayurl_Sx(pid,pl=True):
    """
    播放诗词的赏析内容
    """
    url='https://so.gushiwen.org/shangxiplay.aspx?id=%s'%pid
    r=requests.get(url)
    soup=BeautifulSoup(r.content,'lxml')
    d=soup.find(src=re.compile('^https:'))
    href=d.get('src')
    if href:
        if pl:
            playsound(href)
        return href
    else:
        return ''

def getPlayurl_author(pid,pl=True):
    """
    播放诗词的作者的基本情况、生评
    """
    url='https://so.gushiwen.org/authorplay.aspx?id=%s'%pid
    r=requests.get(url)
    soup=BeautifulSoup(r.content,'lxml')
    d=soup.find(src=re.compile('^https:'))
    href=d.get('src')
    if href:
        if pl:
            playsound(href)
        return href
    else:
        return ''

    
def getAll_ID(url):
    """
    获取该页面所有可以用于播放的PId号，
    涉及诗歌的内容、翻译、赏析以及诗人的介绍
    等情况
    """
    driver.get(url)
    soup=BeautifulSoup(driver.page_source,'lxml')
    ds=soup.findAll(href=re.compile('^javascript:Play',re.I))
    t = {}
    if len(ds) > 0:
        for d in ds:
            n=d.get('href')
            dd=n.split(':')[1]
            name = dd.split('(')[0]
            pid=dd.split('(')[1].replace(')','')
            if name not in t.keys():
                t[name]=pid
            print('%s:%s'%(name,pid))
        return t

def PlayPoem(url):
    t=getAll_ID(url)
    for k,v in t.items():
        if 'author' in k.lower():
            getPlayurl_author(v)
        elif 'shangxi' in k.lower():
            getPlayurl_Sx(v)
        elif 'fangyi' in k.lower():
            getPlayurl_FY(v)
        else:
            try:
                getPlayurl(v)
            except:
                pass
    return


if __name__=="__main__":
    #cons=getSongCiSB(sys.argv[1],sys.argv[2])    
    #text=gushiAuthor(sys.argv[1])
    pass
