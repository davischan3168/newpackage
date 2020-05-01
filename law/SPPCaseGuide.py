#!/usr/bin/env python3
# -*-coding:utf-8-*-
import sys,os
import requests
import lxml.html
from bs4 import BeautifulSoup
from io import StringIO
import time,re
from webdata.util.hds import user_agent as hds
import webdata as wd
from webdata.util.myenum import tonum

def gettxt(url):
    r=requests.get(url,headers=hds())
    try:
        txt=r.content.decode('utf8')
    except:
        txt=r.text
    html=lxml.html.parse(StringIO(txt))
    title=html.xpath('//div[@id="fontzoom"]//h2//text()')
    html=html.xpath('//div[@id="fontzoom"]//p//text()')
    text='\n'.join(html)
    tza=''.join(title)+'\n\n'+text
    return tza
def gettxtv1(url):
    r=requests.get(url,headers=hds())
    txt=r.content.decode('utf8')
    html=lxml.html.parse(StringIO(txt))
    title=html.xpath('//div[@class="detail_tit"]/text()')
    html=html.xpath('//div[@id="fontzoom"]//text()')
    text='\n'.join(html)
    tza=title[0]+'\n\n'+text
    return tza

def getlist(url,GCase=True):
    rr=re.compile('(^http://)|(^https://)')
    r=requests.get(url,headers=hds())
    txt=r.content.decode('utf8')
    html=lxml.html.parse(StringIO(txt))
    lis=html.xpath('//div[@class="commonList_con"]/ul[@class="li_line"]/li')
    datasets={}
    for li in lis:
        name=re.sub(r'\s*','',li.xpath('a/text()')[0].strip())
        name=name.replace('“','').replace('”','')
        tm=li.xpath('span/text()')[0].strip()
        href=li.xpath('a/@href')[0].strip()
        name=tm+name
        if not rr.match(href):
            href='http://www.spp.gov.cn'+li.xpath('a/@href')[0]        
        #print(name,href)
        if (name.endswith('指导性案例')) and GCase:
            datasets[name]=href
        else:
            datasets[name]=href
    return datasets

def SPPlawcase(url='http://www.spp.gov.cn/spp/jczdal/index.shtml',GCase=True,mtype='case'):
    urls=getlist(url)
    n=1
    for k,v in urls.items():
        if mtype == 'case':
            path='law/casespp/'+k+'.txt'
        elif mtype=='spp':
            path='law/sikao/spp/'+k+'.txt'
        elif mtype == 'sppdoc':
            path='law/sikao/sppdoc/'+k+'.txt'
        #print(n)
        #n=n+1
        #if n>10:
        #    break
        if not os.path.exists(path):
            print(v)
            text=gettxt(v)
            try:
                f=open(path,'w',encoding='utf8')
                f.write(text)
                f.close()
            except:
                f=open(path,'w',encoding='gbk')
                f.write(text)
                f.close()
            finally:
                f.close()
        time.sleep(0.1)

    return

def SPPtohtml(path='law/casespp',func=wd.txt2html_odir,index=False):
    """
    path:文件夹的名称
    func:txt2html_odir,形成一个个单独的文件
        :txt2htmlv1,合并成一个文件
    """    
    ss={}
    for root,ds,fs in os.walk(path):
        for f in fs:
            #print(f)
            if os.path.splitext(f)[1] in ['.txt']:
                xu=tonum(f)
                ss[xu]=os.path.abspath(root+'/'+f)

    dd=sorted(ss.items(),key=lambda item:item[0])
    df=[]
    for i in dd:
        df.append(i[1])

    func(df,index=index)
    return
    
    

   
    
if __name__=="__main__":
    #ddd=getlist(sys.argv[1])
    #url='http://www.court.gov.cn/fabu-gengduo-77.html'
    #lawcase(url)
    SPPlawcase()
    #SPPtohtml(func=wd.txt2htmlv1)
    #os.rename('outputtxt.html','最高检指导案例.html')
    #lawcase(sys.argv[1])
    pass
    
    
    
