#!/usr/bin/env python3
# -*-coding:utf-8-*-

import sys,requests,os
import lxml.html
from lxml import etree
import json
import re,time
import datetime as dt
from webdata.util.hds import user_agent as hds
try:
    from io import StringIO
except:
    from pandas.compat import StringIO

from bs4 import BeautifulSoup

"""
主要是获取在司法部上的历年真题
"""

base='http://www.moj.gov.cn'
def _get_links():
    global base
    urls=[]
    url=['http://www.moj.gov.cn/node_87384.htm','http://www.moj.gov.cn/node_87384_2.htm']
    for u in url: 
        r=requests.get(u,headers=hds())
        html=lxml.html.parse(StringIO(r.text))
        ul=html.xpath("//div[@class='div730']/dl/dd[2]/div[1]//a/@href")
        for s in ul:
            urls.append(base+s)

    return urls

def get_content():
    urls=_get_links()
    for url in urls:
        r=requests.get(url,headers=hds())
        html=lxml.html.parse(StringIO(r.content.decode('utf8')))
        title=html.xpath("//div[@class='div1000']/div[1]/div[2]/dl/dd[2]/text()")[0]
        content=html.xpath("//div[@class='div1000']/div[1]/div[2]/dl/dd//text()")
        cnt=''.join(content)
        f=open(title,'w')
        f.write(cnt)
        f.close()
    return

if __name__=="__main__":
    get_content()
    
