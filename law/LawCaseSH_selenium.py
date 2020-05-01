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

http = re.compile(r'^[https://www ,http://www]')
base = 'http://www.hshfy.sh.cn/shfy/gweb2017/'

def Firefox_hdless():
    options = webdriver.FirefoxOptions()
    options.add_argument('-headless')
    browser = webdriver.Firefox(options = options)
    return browser


driver = Firefox_hdless()
def SpideUrls_page(driver):
    lis = driver.find_elements_by_xpath('//div[@id="content"]/div[@class="list_a"]/ul/li')
    us = {}
    cc = re.compile('\W')
    for li in lis:
        tt = li.text.split('\n')
        name = cc.sub('', tt[0])
        title = re.sub(r'[\[,\]]','', tt[1]) + '【' + name[:2] +'】' +name[2:]
        #print(title)
        href = li.find_element_by_tag_name('a').get_attribute('href')
        us[title] = href
    
    return us

def _clickToNPage(driver):
    lis =   driver.find_element_by_xpath('//div[@id="content"]/div[@class="meneame"]/div')
    npage = lis.find_element_by_partial_link_text('>')
    while True:
        if npage:
            print('Click to Next Page.....')
            npage.click()
            driver.implicitly_wait(5)
            return True
        else:
            break
            return False

def SpideUrls(url,page):
    us = {}
    driver.get(url)
    driver.implicitly_wait(10)    
    us.update(SpideUrls_page(driver))
    tpage = 2
    while True:
        try:
            lis =   driver.find_element_by_xpath('//div[@id="content"]/div[@class="meneame"]/div')
            npage = lis.find_element_by_partial_link_text('>')        
            if npage:
                print('Click to Page %s.....'%page)
                npage.click()
                driver.implicitly_wait(5)
                us.update(SpideUrls_page(driver))
                tpage = tpage+1
                if tpage >page:
                    break
                
            else:
                break
        except:
            break
        
    return us
    
   
def SpiderText(url):
    #driver = Firefox_hdless()
    driver.get(url)
    driver.implicitly_wait(10)
    Text = driver.find_element_by_xpath('//div[@class="list_a"]').text
    return Text

def LawShSCase(url,page=2,title=False):
    hrefs = SpideUrls(url,page)
    for k, v in hrefs.items():
        if title:
            k=re.sub(r'[【,】,\s]','',k)
        k = re.sub(r'[/,:]','_',k)
        path = 'law/caseshanghai/'+k+'.txt'
        if not os.path.exists(path):
            try:
                txt = SpiderText(v)
                #print(txt)
                print('Downloading the file %s'%path)
                with open(path, 'w', encoding = 'utf8') as f:
                    f.write(txt)
            except:
                pass
    return

if __name__=="__main__":
    #ddd=getlist(sys.argv[1])
    urll='http://www.hshfy.sh.cn/shfy/gweb2017/channel_xw_list.jsp?pa=abG1kbT1MTTA2MDImbG1tYz2wuMD90dDO9gPdcssPdcssz&zd=spyj'
    url ='http://www.hshfy.sh.cn/shfy/gweb2017/channel_xw_list.jsp?pa=abG1kbT1MTTAxMDYmbG1tYz3C27C4y7W3qAPdcssPdcssz&zd=xwzx#'
    #driver = Firefox_hdless()
    #driver.get(url)
    LawShSCase(url)
     LawShSCase(urll)
    pass
    
    
    
