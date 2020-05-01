#!/usr/bin/env python3
# -*-coding:utf-8-*-
import requests
import lxml.html
from io import StringIO
import re
from bs4 import BeautifulSoup
def geturls(url):
    r = requests.get(url)
    #html = lxml.html.parse(StringIO(r.text))
    #urls =  html.xpath('//p[contains(@style,"margin-bottom:")]/span/a/@href')
    soup = BeautifulSoup(r.content,'lxml')
    hrefs=soup.find(id='js_content').findAll('a')
    ii = []
    for i in hrefs:
        ii.append(i.get('href'))
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

def getextB(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content,'lxml')
    title = re.split('[!,\,,！,，]',soup.find('h2').text.strip())
    if len(title) > 0:
        title = ''.join(title)
        
    soup = soup.find(id='js_content').findAll('p')
    cc = re.compile(r'^[法律微信公,网络配图,来源：整理,点击图片获取]')

    text = []
    for txt in soup:
        if not cc.match(txt.text):
            text.append(txt.text)

    Text = '\n\n'.join(text)
    if '延伸阅读：' in Text:
        Text=Text.split('延伸阅读：')[0]
    try:
        with open('law/wx/'+title+'.txt','w',encoding = 'utf8') as f:
            f.write(Text)
    except Exception as e:
        print(e)
        pass
        
    return Text,title
    
