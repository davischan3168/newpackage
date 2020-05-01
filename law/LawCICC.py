#!/usr/bin/env python3
# -*-coding:utf-8-*-
import requests
from requests.auth import HTTPBasicAuth
import warnings
import urllib3
import re
warnings.filterwarnings("ignore")
requests.packages.urllib3.disable_warnings()
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += 'HIGH:!DH:!aNULL'
import os
from bs4 import BeautifulSoup

def getUrls(url='http://cicc.court.gov.cn/html/1//218/62/163/index.html', page = 3):
    driver = requests.Session()
    r = driver.get(url, verify = False)
    soup = BeautifulSoup(r.content, 'lxml')
    hrefs = soup.find('ul',attrs={'class','list-unstyled columns-list essayList'})
    hrefs = hrefs.findAll('a')
    us = {}
    for i in hrefs:
        us[i.text] = i.get('href')
    if page > 1:
        for i in range(2,page+1):
            urll = url[:-10] + 'list%s.html'%i
            print(urll)
            rr = driver.get(urll, verify = False)
            soup = BeautifulSoup(rr.content, 'lxml')
            hrefs = soup.find('ul',attrs={'class','list-unstyled columns-list essayList'})
            hrefs = hrefs.findAll('a')
            for i in hrefs:
                us[i.text] = i.get('href')            
    return us

def spiderText(url):
    driver = requests.Session()
    r = driver.get(url, verify = False)
    soup = BeautifulSoup(r.content, 'lxml')
    tt = soup.find('article', attrs={'class','essay-content'})
    tl = tt.findAll('p')
    gtext = []
    for i in tl:
        gtext.append(i.text)
    text = '\n\n'.join(gtext)
    return text

def LawCICCase(url,page=3):
    hrefs = getUrls(url,page)
    for k, v in hrefs.items():
        k=re.sub(r'\s','',k).replace('/','_')
        path = 'law/casecicc/'+k[-10:]+k[:-10]+'.txt'
        if not os.path.exists(path):
             txt = spiderText(v)
             print(txt)
             with open(path, 'w', encoding = 'utf8') as f:
                 f.write(txt)
    return

if __name__ == "__main__":
    url='http://cicc.court.gov.cn/html/1//218/62/163/index.html'
    LawCICCase(url)
    pass
