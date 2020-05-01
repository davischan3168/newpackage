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


def SPPspiderUrls(url='https://www.spp.gov.cn/spp/wsfbt/index.shtml', page = 2):
    driver = requests.Session()
    r = driver.get(url, verify = False)
    soup = BeautifulSoup(r.content, 'lxml')
    hrefs = soup.find('ul',attrs={'class','li_line'})
    hrefs = hrefs.find_all('li')
    us = []
    us.extend(hrefs)
    if page > 1:
        for i in range(2,page+1):
            urll = url[:-6] + '_%s.shtml'%i
            r = driver.get(urll, verify = False)
            soup = BeautifulSoup(r.content, 'lxml')
            hrefs = soup.find('ul',attrs={'class','li_line'})
            hrefs = hrefs.find_all('li')
            us.extend(hrefs)
    return us
def SPPspiderText(url):
    driver = requests.Session()
    r = driver.get(url, verify = False)
    soup = BeautifulSoup(r.content, 'lxml')
    text = soup.find(id='fontzoom').text
    ss = re.compile(r'<!--内容加载完，执行分页，优化展示效果-->')
    text = ss.split(text)
    #text = text.split('<!--内容加载完，执行分页，优化展示效果-->')
    if isinstance(text, list):
        text=text[0]
    return text

def SPPIssue(url,page=2):
    urls=SPPspiderUrls(url,page)
    
    for u in urls:
        tt = u.text
        title = tt[-11:]+'_'+tt[:-11]
        path = 'law/issuespp/'+title.replace(' ', '')+'.txt'
        href = u.find('a').get('href')
        #print(title,href)
        if not os.path.exists(path):
            try:
                text = SPPspiderText(href)
                with open(path, 'w', encoding = 'utf8') as f:
                    f.write(text)
                print('Getting file %s sucessed!'%path)
            except Exception as e:
                #print(e)
                pass
    return
                

if __name__=="__main__":
    #ddd=getlist(sys.argv[1])
    url='https://www.spp.gov.cn/spp/wsfbt/index.shtml'
    SPPIssue(url,2)
    pass
    
    
    
