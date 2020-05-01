#!/usr/bin/env python3
# -*-coding:utf-8-*-

from selenium import webdriver
import time,re,sys
import pandas as pd
import numpy as np
from io import StringIO
import lxml.html,requests
from bs4 import BeautifulSoup
import urllib.parse


def Firefox_hdless():
    options = webdriver.FirefoxOptions()
    options.add_argument('-headless')
    browser = webdriver.Firefox(options=options)
    return browser

def Chrome_hdless():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    if sys.platform=='win32':
        driver = webdriver.Chrome(options=chrome_options)
    else:
        driver = webdriver.Chrome(options=chrome_options)#,executable_path='/usr/local/bin/chromedriver')
    return driver

def LawCaseSearch_abstract(url, search):
    driver.get(url)
    driver.implicitly_wait(5)
    driver.find_element_by_partial_link_text('案例库').click()
    driver.implicitly_wait(5)

    driver.find_element_by_id("mainSerachBox").send_keys(search)
    driver.find_element_by_tag_name('button').click()
    driver.implicitly_wait(5)
    text = getlistext(driver)

    path = 'law/casesearch/'+search+'.txt'
    Gtext='\n\n-------------------------------------\n\n'.join(text)
    with open(path,'w',encoding='utf8') as f:
        f.write(Gtext)
    
    return 

def getlistext(driver):
    lis = []
    ds = driver.find_elements_by_xpath('//ul[@class="ul_list"]/li')
    for d in ds:
        lis.append(d.text)

    for pn in range(1,11):
        try:
            driver.find_element_by_xpath('//div[@class="list_right"]/div[@class="pagination black-page"]//ul/li[%s]'%pn).click()
            print('Click to Page %s'%pn)
            driver.implicitly_wait(5)
            time.sleep(1)
            ds = driver.find_elements_by_xpath('//ul[@class="ul_list"]/li')
            for d in ds:
                lis.append(d.text)        
        except Exception as e:
            print('Falsed Click to Page %s'%pn)
            pass
    return lis
   
def GeText_page(driver,search):
    ds = driver.find_elements_by_xpath('//ul[@class="ul_list"]/li/div[2]/div[1]')
    for i in range(len(ds)):
        try:
            ds[i].click()
            driver.implicitly_wait(5)
            time.sleep(1)
            title = driver.find_element_by_tag_name('h2').text
            text = driver.find_element_by_id('content').text.split('生效文书')[0]
            path = 'law/casesearch/case/'+search+'.txt'
            #print(title)
            with open(path,'a',encoding='utf8') as f:
                f.write(re.sub('\n','\n\n',text))
                f.write('---------------\n'*2)
            driver.back()
            driver.implicitly_wait(5)
            time.sleep(1)
            ds = driver.find_elements_by_xpath('//ul[@class="ul_list"]/li/div[2]/div[1]')
        except Exception as e:
            print(e)
            pass
    return

def LawCaseSearch_Content(url,search):
    driver.get(url)
    driver.implicitly_wait(5)
    driver.find_element_by_partial_link_text('案例库').click()
    driver.implicitly_wait(5)

    driver.find_element_by_id("mainSerachBox").clear()
    driver.find_element_by_id("mainSerachBox").send_keys(search)
    driver.find_element_by_tag_name('button').click()
    driver.implicitly_wait(5)
    time.sleep(2)
    for pn in range(1,11):
        try:
            GeText_page(driver,search)
            driver.find_element_by_xpath('//div[@class="list_right"]/div[@class="pagination black-page"]//ul/li[%s]'%pn).click()
            print('Click to Page %s'%pn)
            driver.implicitly_wait(5)
            time.sleep(1)
        except Exception as e:
            print('Falsed Click to Page %s'%pn)
            pass
    return

if __name__=="__main__":
    driver = Firefox_hdless()
    #driver = webdriver.Firefox()#Chrome_hdless()
    #driver = webdriver.Chrome()
    url='https://anli.court.gov.cn/static/web/index.html#/alk'
    
