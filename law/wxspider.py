#!/usr/bin/env python3
# -*-coding:utf-8-*-
import requests
import lxml.html
from io import StringIO
import re
import os
from bs4 import BeautifulSoup
def geturls(url):
    r = requests.get(url)
    cs = re.compile(r'^邮箱|联系')
    #html = lxml.html.parse(StringIO(r.text))
    #urls =  html.xpath('//p[contains(@style,"margin-bottom:")]/span/a/@href')
    soup = BeautifulSoup(r.content,'lxml')
    hrefs=soup.find(id='js_content').findAll('a')
    ii = {}
    sc = re.compile(r'\W')
    for i in hrefs:
        href = i.get('href')
        """
        name = i.text.replace(':',"：").\
            replace(',','_').replace('(','（').replace(')','）').\
            replace('!','！').replace('|','').replace('?','？')
        """
        name = sc.sub('_',i.text)
        
        if len(name)>0:
            for p in ['邮箱','联系']:
                if not cs.match(name):
                    ii[name] = href
    return ii
def getext(url):
    r = requests.get(url)
    
    html = lxml.html.parse(StringIO(r.text))
    text = html.xpath('//p[contains(@style, "margin-top:")]//text()')
    if len(text)<1:
        text = html.xpath('//div[contains(@class,"rich_media_content")]/p[contains(@style, "text")]//text()')
    if len(text)<1:
        text = html.xpath('//div[contains(@class,"rich_media_content")]/p//text()')
    tt = '\n'.join(text)
    title = ''.join(html.xpath('//h2//text()')).strip().replace('|','')
    with open('law/wx/'+title+'.txt','w',encoding = 'utf8') as f:
        f.write(tt)
    return (title, tt)

def getextB_Dict(url_dict):

    for k,v in url_dict.items():
        fpath = 'law/wx/zhixing/'+k+'.txt'

        if not os.path.exists(fpath):
            r = requests.get(v)
            soup = BeautifulSoup(r.content,'lxml')
            #title = re.split('[!,\,,！,，]',soup.find('h2').text.strip())
            #if len(title) > 0:
            #title = ''.join(title)
        
            soup = soup.find(id='js_content').findAll(["p","section"])
            cc = re.compile(r'^法律微信公|网络配图|来源：整理|点击图片获取|编者按|关于我们|专注“保全|联系')
            
            text = []
            for txt in soup:
                if not cc.match(txt.text):
                    text.append(txt.text)

            Text = '\n\n'.join(text)
            if '延伸阅读：' in Text:
                Text=Text.split('延伸阅读：')[0]
            elif '编者按：' in Text:
                Text=Text.split('延伸阅读：')[0]
            elif '附：系列文章' in Text:
                Text=Text.split('附：系列文章')[0]
            try:
                with open(fpath,'w',encoding = 'utf8') as f:
                    f.write(Text)
            except Exception as e:
                print(e)
                pass
        
    return

def remove_txt(fpath):
    with open(fpath,'r',encoding='utf8') as f:
        Text = f.readlines()

    ss = []
    s1 = set()
    scc = re.compile(' ')
    ssc = re.compile('^本文由公众号|【关注“保全|本文由作者')
    for line in Text:
        line = line.strip()
        if len(line)>0:
            line1 = scc.sub('',line)
            if (line1 not in s1) and (not ssc.match(line)):
                s1.add(line1)
                ss.append(line)

    Text = '\n\n'.join(ss)
    cc=re.compile('\n附：系列文章')
    c1 = re.compile('\n关注我们|\n专注【财产保全')
    if '延伸阅读：' in Text:
        Text=Text.split('延伸阅读：')[0]
    elif '编者按：' in Text:
        Text=Text.split('延伸阅读：')[0]
    Text=cc.split(Text)[0]
    Text = c1.split(Text)[0]
    with open(fpath,'w',encoding='utf8') as f:
        f.write(Text)

    return


def getextB(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content,'lxml')
    title = re.split('[!,\,,！,，]',soup.find('h2').text.strip())
    if len(title) > 0:
        title = ''.join(title)
        
    soup = soup.find(id='js_content').findAll(["p","section"])
    cc = re.compile(r'^[法律微信公,网络配图,来源：整理,点击图片获取]')

    text = []
    for txt in soup:
        if not cc.match(txt.text):
            text.append(txt.text)

    Text = '\n\n'.join(text)
    if '延伸阅读：' in Text:
        Text=Text.split('延伸阅读：')[0]
    elif '编者按：' in Text:
        Text=Text.split('延伸阅读：')[0]
    try:
        with open('law/wx/'+title+'.txt','w',encoding = 'utf8') as f:
            f.write(Text)
    except Exception as e:
        print(e)
        pass
        
    return Text,title
    
