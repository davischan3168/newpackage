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

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
#from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

def Firefox_hdless():
    options = webdriver.FirefoxOptions()
    options.add_argument('-headless')
    #profile = webdriver.FirefoxProfile()
    #profile.set_preference('permissions.default.image', 2)
    #profile.set_preference('dom.ipc.plugins.enabled.npswf32.dll', 'false')
    #profile.set_preference('javascript.enabled', 'false')
    #browser = webdriver.Firefox(options=options,firefox_profile = profile)
    browser = webdriver.Firefox(options = options)
    return browser

def SPPspiderUrls(url, \
                   page = 2, \
                   Url_xpath = '//div[@class="commonList_con"]/ul[@class="li_line"]/li'):
    driver = Firefox_hdless()
    driver.get(url)
    driver.implicitly_wait(10)
    urls = driver.find_elements_by_xpath(Url_xpath)
    us = {}
    cc = re.compile('\W')
    for li in urls:
        tt = li.text.split('\n')
        title = cc.sub('', tt[1]) + '_' + cc.sub('', tt[0])
        #print(title)
        href = li.find_element_by_tag_name('a').get_attribute('href')
        #us.append(ul.get_attribute('href'))
        us[title] = href
    while True:
        try:
            driver.find_element_by_partial_link_text('下一页').click()
            driver.implicitly_wait(10)
            urls = driver.find_elements_by_xpath(Url_xpath)
            for li in urls:
                tt = li.text.split('\n')
                title = cc.sub('', tt[1]) + '_' + cc.sub('', tt[0])
                #print(title)
                href = li.find_element_by_tag_name('a').get_attribute('href')
                #us.append(ul.get_attribute('href'))
                us[title] = href
            page -= 1
        except Exception as e:
            #print(e)
            break
        if page < 1:
            break
    return us
def SPPspiderText(url,\
                  Txpath1 = '//div[@id="fontzoom"]', \
                  Txpath2 = '//div[@id="fontzoom"]'):
    driver = Firefox_hdless()
    driver.get(url)
    driver.implicitly_wait(10)
    Text = driver.find_element_by_xpath(Txpath1)
    text = []
    #title = driver.find_element_by_xpath('//h2').text
    text.append(Text.text)
    #cc = re.compile('\W')
    while True:
        try:
            driver.find_element_by_partial_link_text('>').click()
            driver.implicitly_wait(10)
            Text = driver.find_element_by_xpath(Txpath2)
            text.append(Text.text)
        except Exception as e:
            #print(e)
            break
    return '\n\n'.join(text)

if __name__=="__main__":
    #ddd=getlist(sys.argv[1])
    url='https://www.spp.gov.cn/spp/wsfbt/index.shtml'
    #driver = Firefox_hdless()
    #driver.get(url)
    #"""
    urls=SPPspiderUrls(url,2)
    for k, v in urls.items():
        path = 'law/issuespp/'+k+'.txt'
        if not os.path.exists(path):
            try:
                text = SPPspiderText(v)
                print(path)
                with open(path, 'w', encoding = 'utf8') as f:
                    f.write(text)
            except:
                pass
    #"""
    pass
    
    
    
