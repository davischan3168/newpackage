#!/usr/bin/env python3
# -*-coding:utf-8-*-
from selenium import webdriver
import time,sys
from bs4 import BeautifulSoup
from io import StringIO
import requests
import os
import lxml.html
import re
#from mysql.gushiwen2sql import InsertSql
#import pickle
from playsound import playsound
try:
    import MySQLdb
except:
    import pymysql as MySQLdb
finally:
    pass
cmd="insert into MyPoemTable(title,chaodai,author,PoemText,fanyizhushi,fanyi,zhushi,shangxi,Tag,playid,href) value(%s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s)"
def InsertSql(datasets,cmd):
    try:
        conn = MySQLdb.connect(host="localhost", port=3306, user='root',passwd='801019', db='SDD', charset="utf8")
    except:
        pass
    cur = conn.cursor()
    try:
        cur.executemany(cmd,datasets)
    except:
        pass
    conn.commit()
    print('Finished insert..')
    cur.close()
    conn.close()
    return

sqll = "select href from MyPoemTable"
def FetchFromSql(cmd):
    try:
        conn = MySQLdb.connect(host="localhost", port=3306, user='root',passwd='801019', db='SDD', charset="utf8")
    except:
        pass
    cur = conn.cursor()
    cur.execute(cmd)
    #c=[]
    #c.append(cur.fetchall())
    return cur.fetchall()

if sys.platform == "linux":
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    #chrome_options.add_argument('--disable-gpu')
    #driver = webdriver.Chrome(chrome_options=chrome_options)
    driver = webdriver.Chrome(options=chrome_options)
else :
    driver = webdriver.PhantomJS()

titleset=set()

base='https://so.gushiwen.org'

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
        if count > 10:
            print("Timing out after {} seconds.".format(count*0.2))
            return
        time.sleep(.25)
        try:
            elem == driver.find_element_by_tag_name("html")
        except:
            #StaleElementReferenceException:
            return


def GetAllType(url):
    driver.get(url)
    t = {}
    df = driver.find_elements_by_xpath('//div[@class="main3"]/div[@class="right"]/div[@class="sons"]/div[@class="cont"]/a')
    for i in df:
        t[i.text] = i.get_attribute('href')

    return t
def getsqlhref(cmd):
    href = FetchFromSql(cmd)
    t = [i[0] for i in href]
    return set(t)
def GetItemsFromType(url):
    driver.get(url)
    t={}
    df=driver.find_elements_by_xpath('//div[@class="main3"]/div[@class="left"]/div[@class="sons"]//a')
    for i in df:
        t[i.text] = i.get_attribute('href')
    return t

def GetPoemIfoType(url):
    """
    从www.gushiwen.org网址，爬去按类型分类的古诗，并返回相应的内容
    """
    type_urls = GetAllType(url)
    urls = type_urls.values()
    hrefs = getsqlhref(sqll)
    Nusep = 'packages/gushici/href.txt'
    if os.path.exists(Nusep):
        Nuse = open(Nusep,'r').readlines()
        hrefs = hrefs.union(Nuse)
    for turl in urls:
        #poem = []
        try:
            Items_urls = GetItemsFromType(turl)
            uu=Items_urls.values()
            for num,iurl in enumerate(uu):
                if iurl not in hrefs:
                    #print(iurl)
                    t = []
                    try:
                        pif = Poem_text(iurl)
                        t.append([pif['title'],pif['chaod'],pif['author'],\
                                     pif['poem'],pif['fyz'],pif['fany'],\
                                     pif['zhusi'],pif['shangxi'],pif['tag'],\
                                     pif['pid'],pif['href']])
                        """
                        poem.append([pif['title'],pif['chaod'],pif['author'],\
                                     pif['poem'],pif['fyz'],pif['fany'],\
                                     pif['zhusi'],pif['shangxi'],pif['tag'],\
                                     pif['pid'],pif['href']])
                        """
                        InsertSql(t, cmd)
                        print('%s: %s'%(num+1,pif['title']))
                    except Exception as e:
                        #print(e)
                        with open(Nusep,'a') as f:
                            f.write(iurl+'\n')
                            f.flush()
            """
            if len(poem) > 0:
                InsertSql(poem,cmd)
            """
        except Exception as e:
            print(e)
    return
            

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
        t['tag'] = driver.find_element_by_xpath('//div[@class="left"]/div[@class="sons"]/div[@class="tag"]').text
    except:
        t['tag']=''        
    try:
        #t['fy']=driver.find_element_by_xpath('//div[starts-with(@id,"fanyiquan") or contains(@class,"yishang")]').text
        t['fyz']=driver.find_element_by_xpath('//div[starts-with(@id,"fanyiquan")]').text
        if t['fyz']=='':
            t['fyz']=driver.find_element_by_xpath('//div[contains(@class,"yishang")]').text
    except:
        t['fyz']=driver.find_element_by_xpath('//div[contains(@class,"yishang")]').text
    finally:
        t['fyz']=''
    try:
        t['fany']=driver.find_element_by_xpath('//div[starts-with(@id,"fanyiquan")]//p[1]').text
        if t['fany']=='':
            t['fany']=driver.find_element_by_xpath('//div[contains(@class,"yishang")]//p[1]').text
    except:
        t['fany']=driver.find_element_by_xpath('//div[contains(@class,"yishang")]//p[1]').text
    finally:
        t['fany']=''
    try:
        t['zhusi']=driver.find_element_by_xpath('//div[starts-with(@id,"fanyiquan")]//p[2]').text
        if t['zhusi']=='':
            t['zhusi']=driver.find_element_by_xpath('//div[contains(@class,"yishang")]//p[2]').text
    except:
        t['zhusi']=driver.find_element_by_xpath('//div[contains(@class,"yishang")]//p[2]').text       
    finally:
        t['zhusi']=''
    try:
        t['shangxi']=driver.find_element_by_xpath('//div[starts-with(@id,"shangxiquan")]').text
    except:
        t['shangxi']=''
    try:
        t['chaod'] = driver.find_element_by_xpath('//p[@class="source"]/a[1]').text
    except:
        t['chaod']=''
    try:
        t['author'] = driver.find_element_by_xpath('//p[@class="source"]/a[2]').text
    except:
        t['author']=''                
    try:
        t['pid']=driver.find_element_by_xpath('//div[@class="sons"]/div[@class="tool"]//a[starts-with(@href,"javascript:Play")]').get_attribute('href').split('(')[1].replace(')','')
    except:
        t['pid']=''

    t['href']=url

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
