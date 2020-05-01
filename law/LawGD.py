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
    url='http://www.gdcourts.gov.cn/index.php?v=listing&cid=170'
    driver = requests.Session()
    us = {}
    urls = [ ]
    urls.append(url)
    for i in range(2,page+1):
        urls.append(url+'&page=%s'%i)
    cc=re.compile(r'^(http://www.|https://www)')
    for ul in urls:
        print(ul)
        r = driver.get(ul, verify = False)
        soup = BeautifulSoup(r.content, 'lxml')
        href = soup.find('div',attrs={'class', 'list_3'})
        #print(href)
        hrefs = href.findAll('li')
    
        for i in hrefs:
            title = re.sub('\s','',i.text.strip().replace('.',''))
            href = i.find('a').get('href')
            if not cc.match(href):
                href = 'http://www.gdcourts.gov.cn'+href
            us[title] = href
    return us

def spiderText(url):
    driver = requests.Session()
    r = driver.get(url, verify = False)
    soup = BeautifulSoup(r.content, 'lxml')
    txt = soup.find('div',attrs={'class','text'})
    tt = txt.find_all('p')

    gtext = []
    for i in tt:
        gtext.append(i.text)
    text = '\n\n'.join(gtext)
    return text

def LawGDCase(page = 11):
    hrefs = getUrls(page)
    for k, v in hrefs.items():
        k=re.sub(r'\s','',k).replace('/','_').replace(':','：')
        path = 'law/caseGD/'+k[-10:]+k[:-10]+'.txt'
        if not os.path.exists(path):
            try:
                txt = spiderText(v)
                #print(txt)
                print('Downloading the file %s.'%path)
                with open(path, 'w', encoding = 'utf8') as f:
                    f.write(txt)
            except:
                pass
    return

if __name__ == "__main__":
    #url='http://cicc.court.gov.cn/html/1//218/62/163/index.html'
    LawGDCase(11)
    #df=getUrls(url,page=1)
    pass
