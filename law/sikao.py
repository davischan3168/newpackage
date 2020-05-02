#!/usr/bin/env python3
# -*-coding:utf-8-*-


import requests,lxml.html
from bs4 import  BeautifulSoup
from io import StringIO
import sys,os,re

"""
获取司法部的历年真题
"""

def get_sikao_text(url,fpath):
    burl='http://103.42.78.227/index/content/2016-09/26/'
    r=requests.get(url)
    text=r.content.decode('utf8')

    html=lxml.html.parse(StringIO(text))
    
    f=open(fpath,'a', encoding='utf-8')
    tt=html.xpath('//div[@class="div1000"]/div[1]/div[2]/dl//text()')
    #print(tt)
    tf=[node.rstrip() for node in tt]
    #print(tf)
    ctxt='\n'.join(tf)
    f.write(ctxt)

    """
    for i in range(len(tt)):
        #print(line)
        #line=line.lstrip()
        #line=line.encoding('utf8').decoding('gbk')
        f.write(tt[i]+'\n')
        f.flush()
        """
    np=html.xpath('//div[@class="div1000"]//a[text()="下一页"]/@href')
    if len(np)>0:
        uburl=burl+np[0]
        get_sikao_text(uburl,fpath)
    f.close()
    return

def get_sikao_2017(url,fpath):
    #burl='http://103.42.78.227/index/content/2016-09/26/'
    r=requests.get(url)
    text=r.content.decode('utf8')

    html=lxml.html.parse(StringIO(text))
    
    f=open(fpath,'w', encoding='utf-8')
    tt=html.xpath('//div[@name="pg"]/p//text()')
    #print(tt)
    #tf=[node.rstrip() for node in tt]
    #print(tf)
    ctxt='\n'.join(tt)
    f.write(ctxt)
    f.close()
    return

def get_sikao_2015(url,fpath):
    burl=os.path.split(url)[0]#
    #'http://xy.moj.gov.cn/index/content/2015-09/21/'
    r=requests.get(url)
    text=r.content.decode('utf8')

    html=lxml.html.parse(StringIO(text))
    
    f=open(fpath,'a', encoding='utf-8')
    tt=html.xpath('//dd[@class="f14 black02 yh"]/p//text()')
    #print(tt)
    #tf=[node.rstrip() for node in tt]
    #print(tf)
    #print(tt)
    ctxt='\n'.join(tt)
    #ctxt=ctxt.replace('\xa0\xa0\xa0\xa099','\n')
    print(ctxt)
    f.write(ctxt)

    np=html.xpath('//div[@id="displaypagenum"]//a[text()="下一页"]/@href')
    if len(np)>0:
        uburl=burl+'/'+np[0]
        get_sikao_2015(uburl,fpath)    
    f.close()
    return

def settle(path,out):
    f=open(path,'r',encoding='utf8')
    text=f.read()
    f.close()
    ddd=re.sub(r'\n．\n',r'.',text)
    ddd=re.sub(r'\n．',r'.',ddd)
    ddd=ddd.split('\n')
    dtext=[]
    for d in ddd:
        if  re.match('\s*\d*\.',d):
            d='\n'+d
            dtext.append(d)
        else:
            dtext.append(d)

    dtxt='\n'.join(dtext)
    f=open(out,'w',encoding='utf8')
    f.write(dtxt)
    f.close()
    return

if __name__=="__main__":
    #url='http://103.42.78.227/index/content/2016-09/26/content_7083813.htm?node=86553'
    #get_sikao_2015(sys.argv[1],sys.argv[2])
    #get_sikao_2017(sys.argv[1],sys.argv[2])
    settle(sys.argv[1],sys.argv[2])
        
    
