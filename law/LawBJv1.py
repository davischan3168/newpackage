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
def getUrls(page = 2):
    #http://www.bjcourt.gov.cn/zdal/index.htm?c=100015001
    url='http://www.bjcourt.gov.cn/zdal/index.htm?c=10001500%s'
    driver = requests.Session()
    us = {}
    urls = []
    cc=re.compile(r'^(http://www.|https://www)')
    for i in range(1,8):
        ul=url%i
        urls.append(ul)
        if page > 1:
            for j in range(2,page+1):
                urls.append(ul+'&p%s'%j)
    for uu in urls:
        r = driver.get(uu, verify = False)
        soup = BeautifulSoup(r.content, 'lxml')
        href = soup.find('ul',attrs={'class', 'ul_news_01'})
        hrefs = href.findAll('li')
    
        for i in hrefs:
            try:
                title = re.sub('\s','',i.text.strip().replace('.','')).replace('/','_').replace(':','：')
                href = i.find('a').get('href')
                #print(title)
                if not cc.match(href):
                    href = 'http://www.bjcourt.gov.cn'+href
                    #print(href)
                us[title] = href
            except:
                pass        
    return us

def spiderText(url):
    driver = requests.Session()
    r = driver.get(url, verify = False)
    soup = BeautifulSoup(r.content, 'lxml')
    turl = 'http://www.bjcourt.gov.cn'+soup.find(id='ifm').get('src')
    rr = driver.get(turl, verify = False)
    soup = BeautifulSoup(rr.content, 'lxml')
    tt = soup.find_all('p')

    gtext = []
    for i in tt:
        gtext.append(i.text)
    text = '\n\n'.join(gtext)
    return text

def LawBJCase(page=2):
    hrefs = getUrls(page)
    for k, v in hrefs.items():
        path = 'law/caseBJ/'+k[-10:]+k[:-10]+'.txt'
        if not os.path.exists(path):
            try:
                txt = spiderText(v)
                #print(txt)
                with open(path, 'w', encoding = 'utf8') as f:
                    f.write(txt)
                print('Downloaded the file: %s'%path)
            except:
                pass
    return

if __name__ == "__main__":
    #url='http://cicc.court.gov.cn/html/1//218/62/163/index.html'
    LawBJCase(1)
    #df=getUrls(url,page=1)
    pass
