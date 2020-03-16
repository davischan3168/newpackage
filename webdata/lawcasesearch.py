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

def get_cookies(url):
    parsed_url = urllib.parse.urlparse(url)
    if parsed_url.scheme:
        domain = parsed_url.netloc
    else:
        raise urllib.error.URLError("You must include a scheme with your URL.")
       
    driver.get(url)
    driver.implicitly_wait(5)
    sl=driver.get_cookies()
    cookies={}
    for dn in sl:
        cookies[dn['name']]=dn['value']
    #print(cookies)
    #driver.quit()
    return cookies

def GetLawCaseSearch(url, search):
    driver.get(url)
    driver.implicitly_wait(5)
    driver.find_element_by_partial_link_text('案例库').click()
    driver.implicitly_wait(5)

    driver.find_element_by_id("mainSerachBox").send_keys(search)
    driver.find_element_by_tag_name('button').click()
    driver.implicitly_wait(5)

    lis = []
    ds = driver.find_elements_by_xpath('//ul[@class="ul_list"]/li')
    lis.extend(ds)
    text = []

    for d in lis:
        print(d.text)
        
        try:
            d.click()
            driver.implicitly_wait(5)
            text.append(GetText(driver))
        except:
            pass

        driver.back()

    return text

def GetLawCaseSearchv1(url, search):
    driver.get(url)
    driver.implicitly_wait(5)
    driver.find_element_by_partial_link_text('案例库').click()
    driver.implicitly_wait(5)

    driver.find_element_by_id("mainSerachBox").send_keys(search)
    driver.find_element_by_tag_name('button').click()
    driver.implicitly_wait(5)

    lis = []
    ds = driver.find_elements_by_xpath('//ul[@class="ul_list"]/li')
    lis.append(ds)
    text = []

    for d in ds:
        d.click()
        driver.implicitly_wait(5)
        try:
            text.append(GetText(driver))
        except:
            pass

        driver.back()

    
    for i in range(10):
        try:
            
            #driver.find_element_by_xpath('//ul[@class="el-pager"]/button[@class="btn-next"]').click()
            driver.find_element_by_xpath('//button[@class="btn-next"]').click()
            driver.implicitly_wait(5)
            
        except Exception as e:
            print(e)

    if len(lis) > 0:
        print(len(lis))
        """
        for li in lis:
            li.click()
            driver.implicitly_wait(5)
            title = driver.find_element_by_tag_name('h2').text
            text = driver.find_element_by_id('content').text
            print(text)
            print('\n'+'**'*10+'\n')
        """

    return
    
def GetText(driver):
    title = driver.find_element_by_tag_name('h2').text
    text = driver.find_element_by_id('content').text    
    return title, text
if __name__=="__main__":
    #driver = Firefox_hdless()
    driver = Chrome_hdless()
    url='https://anli.court.gov.cn/static/web/index.html#/alk'
    
