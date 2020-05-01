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
zdx = ['https://www.chinacourt.org/article/subjectdetail/type/more/id/MzAwNEiqNACSIGQAAA/page/1.shtml','https://www.chinacourt.org/article/subjectdetail/type/more/id/MzAwNEiqNACSBkYGBgYA/page/1.shtml','https://www.chinacourt.org/article/subjectdetail/type/more/id/MzAwNEiqNACSBsYGBgYA/page/1.shtml']
dx = ['https://www.chinacourt.org/article/subjectdetail/type/more/id/MzAwNEiqNDAwMjAwNjAwAAA/page/1.shtml','https://www.chinacourt.org/article/subjectdetail/type/more/id/MzAwNEiqNDAwAiMDAA/page/1.shtml','https://www.chinacourt.org/article/subjectdetail/type/more/id/MzAwNEiqNDAwMgAyDAwA/page/1.shtml']
qt = ['https://www.chinacourt.org/article/subjectdetail/type/more/id/MzAwNEiqNDAwBiMDAA/page/1.shtml','https://www.chinacourt.org/article/subjectdetail/type/more/id/MzAwNEiqNDAwNjAwMjAwAAA/page/1.shtml','https://www.chinacourt.org/article/subjectdetail/type/more/id/MzAwNEiqNDAwNgAyDAwA/page/1.shtml']
base = 'https://www.chinacourt.org'

cc=re.compile(r'^(http://www.|https://www)')

def getNextpage(url):
    driver = requests.Session()
    r = driver.get(url, verify = False)
    soup = BeautifulSoup(r.content, 'lxml')
    try:
        href = soup.find('div',attrs={'class', 'paginationControl'}).find('a',text = '下一页').get('href')
        if not cc.match(href):
            href = base +href
        #print(href)
        return href
    except:
        return
sub=re.compile(r'[,".:?]')
def _pageitems(url):
    us = {}
    driver = requests.Session()
    r = driver.get(url, verify = False)
    soup = BeautifulSoup(r.content, 'lxml')
    href = soup.find('div',attrs={'class', 'more_right'})
    href = href.find('div',attrs={'class', 'list'})
    hrefs = href.find('ul').findAll('li')
    for i in hrefs:
        try:
            title = re.sub('\s','',i.text.strip().replace('[','')).replace(']','').replace("'",'').replace('"','').replace('.','')
            href = i.find('a').get('href')
            
            if not cc.match(href):
                href = base +href
                #print(href)
            us[title] = href
        except:
            pass
    return us

def getulist(url):
    us = {}
    items = _pageitems(url)
    us.update(items)
    while url:
        url = getNextpage(url)
        if url:
            print(url)
            items = _pageitems(url)
            us.update(items)
        else:
            break
    return us

def spiderText(url):
    driver = requests.Session()
    r = driver.get(url, verify = False)
    soup = BeautifulSoup(r.content, 'lxml')

    gtext = []
    tt = soup.find('div', attrs = {'class','detail_txt'})
    if tt.p:
        tt = tt.find_all('p')
        for i in tt:
            gtext.append(i.text)
        text = '\n\n'.join(gtext)
    else:
        text = tt.text
    
    return text

def LawChinaCasev1(hrefdict):
    for k, v in hrefdict.items():
        path = 'law/casechina/'+k[-10:]+k[:-10]+'.txt'
        if not os.path.exists(path):
            try:
                txt = spiderText(v)
                #print(txt)
                with open(path, 'w', encoding = 'utf8') as f:
                    f.write(txt)
                print('Downloaded the file: %s'%path)
            except Exception as e:
                print(e)
                pass
    return    


def LawChinaCase(url):
    hrefs = getulist(url)
    for k, v in hrefs.items():
        path = 'law/casechina/'+k[-10:]+k[:-10]+'.txt'
        if not os.path.exists(path):
            try:
                txt = spiderText(v)
                #print(txt)
                with open(path, 'w', encoding = 'utf8') as f:
                    f.write(txt)
                print('Downloaded the file: %s'%path)
            except Exception as e:
                print(e)
                pass
    return

if __name__ == "__main__":
    #url='http://cicc.court.gov.cn/html/1//218/62/163/index.html'
    #LawBJCase(1)
    #df=getUrls(url,page=1)
    pass
