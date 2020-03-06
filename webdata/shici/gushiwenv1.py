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
        waitForLoad(driver)

    t = {}
    t['title'] = driver.find_element_by_xpath('//div[starts-with(@class,"cont")]//h1').text
    try:
        t['poem'] = driver.find_element_by_xpath('//div[starts-with(@id,"contson")]').text
    except:
        t['poem']=''
    try:
        t['fy']=driver.find_element_by_xpath('//div[starts-with(@id,"fanyiquan")]').text
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


    
def _getsongsan_urls(url):
    #url='http://so.gushiwen.org/gushi/songsan.aspx'
    urls=[]
    global base
    
    r=requests.get(url)
    html=lxml.html.parse(StringIO(r.text))
    t=html.xpath('//div[@class="typecont"]/span/a')

    for tt in t:
        ul=base+tt.xpath('@href')[0]
        urls.append(ul)

    urls=urls[61:]
    #print(urls)
    return urls

def _get_text(url):
    driver.get(url)
    waitForLoad(driver)
    title=driver.find_element_by_xpath('//div[starts-with(@id,"cont")]//h1').text
    print(title)
    us=driver.find_elements_by_link_text("显示全部")
    for uu in us:
        uu.click()

    try:
        poem=driver.find_element_by_xpath('//div[starts-with(@id,"cont")]').text
    except:
        poem=''
    try:
        fy=driver.find_element_by_xpath('//div[starts-with(@id,"fanyiquan")]').text
    except:
        fy=''
    try:
        jx=driver.find_element_by_xpath('//div[starts-with(@id,"shangxiquan")]').text
    except:
        jx=''
        
    cont='\n\n'.join([poem,fy,jx])
    
    return cont

def getSongCiSB(url,path):
    """
    获取宋词三百的全文,翻译,以及赏析
    """
    n=1
    urls=_getsongsan_urls(url)
    for url in urls:
        try:
            print(n)
            content=_get_text(url)
            content=content.replace('1、\n','1、').replace('2、\n','2、').replace('3、\n','3、').replace('4、\n','4、')
            content=content.replace('本节内容整理自网络（或由匿名网友上传），原作者已无法考证，版权归原作者所有。本站免费发布仅供学习参考，其观点不代表本站立场。站务邮箱：service@gushiwen.org','')
            _write(path,'\n\n'+content)
            n = n+1
        except:
            pass
    return

    

if __name__=="__main__":
    #cons=getSongCiSB(sys.argv[1],sys.argv[2])    
    #text=gushiAuthor(sys.argv[1])
    pass
