#!/usr/bin/env python3
# -*-coding:utf-8-*-

from selenium import webdriver
import re
from bs4 import BeautifulSoup
import requests
import time
from selenium.webdriver.common.action_chains import ActionChains
import pickle
import sys
import os
import shutil
#from webdata.util.hds import user_agent as hds
#from webdata.util.chrome_cookies import firefox_cookies

"""
fp = webdriver.FirefoxProfile()
 
fp.set_preference("browser.download.folderList",2)
fp.set_preference("browser.download.manager.showWhenStarting",False)
fp.set_preference("browser.download.dir", os.getcwd())
fp.set_preference("browser.helperApps.neverAsk.saveToDisk","application/octet-stream")
 
browser = webdriver.Firefox(firefox_profile=fp)
browser.download.dir：c 指vwa定下载路径
browser.download.folderList：设置成 2 表示使用自定义下载路径；设置成 0 表示下载到桌面；设置成 1 表示下载到默认路径
browser.download.manager.showWhenStarting：在开始下载时是否显示下载管理器
browser.helperApps.neverAsk.saveToDisk：对所给出文件类型不再弹出框进行询问
"""
###########################################
"""
options = webdriver.ChromeOptions()
prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': 'd:\\'}
options.add_experimental_option('prefs', prefs)

download.default_directory：设置下载路径
profile.default_content_settings.popups：设置为 0 禁止弹出窗口
"""

def Firefox_hdless():
    options = webdriver.FirefoxOptions()
    options.add_argument('-headless')
    browser = webdriver.Firefox(options=options)
    return browser

def Chrome_hdless():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    if sys.platform=='win32':
        driver = webdriver.Chrome(options=chrome_options)
    else:
        driver = webdriver.Chrome(options=chrome_options)
    return driver

def downLoad(driver):
    dd=driver.find_elements_by_xpath('//a[starts-with(@ng-click,"downloadSingleDocument")]')
    for d in dd:
        d.click()
        time.sleep(2)
    return


def select_down_drop(driver):
    dd=driver.find_element_by_xpath('//i[@class="icon ibass-trig-down"]')
    ActionChains(driver).move_to_element(dd).click().perform()
    driver.find_element_by_xpath('//li/a[text()="100"]').click()    
    #dd=driver.find_element_by_xpath('//span[@class="downIcons"]')
    #ActionChains(driver).move_to_element(dd).click().perform()
    #driver.find_element_by_xpath('//li[@flag="50"]').click()

    return

def insert2pg(df,pyconn,pycur):
    insert = 'insert into faxin_case(abstract,anyou,laiyuan,href) values(%s,%s,%s,%s)'
    pycur.executemany(insert,df)
    pyconn.commit()    
    return

def _getText(driver):
    #handles = driver.window_handles
    
    soup=BeautifulSoup(driver.page_source,'lxml')
    title =  soup.find('div',attrs={'class',"tit ng-binding"}).text
    ss=soup.find(id="content").findAll('p')
    text = []
    csp = re.compile('\W')
    title = csp.sub('_',title)
    for s in ss:
        text.append(s.text)
    with open('./law/alpha/'+title.strip()+'.txt','w',encoding='utf8') as f:
        f.write(title + '\n\n')
        f.write('\n'.join(text))

    #driver.close
    return

def _GetText(driver):
    handles = driver.window_handles
    driver.switch_to.window(handles[1])
    _getText(driver)
    driver.close()
    driver.switch_to.window(handles[0])
    return

def GetTextList(driver,page=2):
    dd=driver.find_elements_by_xpath('//span[starts-with(@ng-bind-html,"item.viewTitle")]')

    for d in dd:
        d.click()
        time.sleep(2)
        _GetText(driver)

    while page>0:
        try:
            driver.find_element_by_link_text('下一页').click()
            time.sleep(2)
            page = page-1
            dd=driver.find_elements_by_xpath('//span[starts-with(@ng-bind-html,"item.viewTitle")]')

            for d in dd:
                d.click()
                time.sleep(2)
                _GetText(driver)
        except Exception as e:
            print(e)
            break
    return     

def GBCaseYZ(fpath,RT='tuple'):
    cpyz = re.compile(r'裁判要旨|案例要旨|【裁判摘要】|裁判要点|【裁判要旨】|要点提示：|参阅要点')
    ss=re.compile(r'.*?案\s*$')
    anhao = re.compile(r'[(（]{1}\d{4}[\u4e00-\u9fa5(（）)\d]*\d+号')
    yz = re.compile(r'相关法条|【案情】|原告：|案例索引：')
    #anhao = re.compile(r'\d{4}([\u4e00-\u9fa5])+\d+号')
    text = open(fpath, 'r', encoding='utf8').read()
    text = re.sub(' 法信大纲 \n.*?\n','',text).replace('<!--fx-->','')
    try:
        text1 = cpyz.split(text)[1]
    except:
        text1 = text
        
    ast = {'lx':'','ah':'','yz':''}
    ast['qw'] = text#re.sub(' 法信大纲 \n.*?\n','',text).replace('<!--fx-->','')
    #

    ltext = [i for i in text.split('\n') if len(i.strip())>0]
    for i in ltext:
        if ss.search(i):
            if len(ast['lx'])<1:
                ast['lx'] = i.strip()
                #说明属于什么纠纷案件
        if anhao.search(i):
            if len(ast['ah'])<1:
                ast['ah'] = anhao.search(i).group().strip()
                #说明案号
    try:
        ast['yz'] = yz.split(cpyz.split(text)[1])[0].strip()
        #说明案件的裁判要旨
    except:
        pass

    if ast['ah'].strip() == '':
        ast['ah'] = 'unavailable'
    if ast['yz'] == '':
        ast['yz'] = 'unavailable'
    if ast['lx'] == '':
        ast['lx'] = os.path.basename(os.path.splitext(fpath)[0])

        
    if RT == 'dict':
        return ast
    elif RT == 'tuple':
        return ast['lx'].strip(),ast['ah'].strip(),ast['yz'].strip(),ast['qw'].strip()

def readpickle(path):
    return pickle.load(open(path, 'rb'))

def savepickle(df,path):
    pickle.dump(df,open(path,'wb'))
    return

def SearchClassify(df,search,mtype=2):
    sch = []
    if isinstance(search, str):
        sch.append(str)
    elif isinstance(search,list):
        sch.extend(search)

    lenght = len(sch)
    tem = []
    for dff in df:
        for i in range(lenght):
            if sch[i] in dff[mtype]:
                if i == lenght-1:
                    tem.append(dff)
            else:
                break
    return tem
"""
df = []
for ii in items:
    try:
        df.append((ii[0][0],ii[0][1],ii[0][2],ii[1]))
    except:
        df.append(('','','',ii[1]))
        print(ii)
import psycopg2
pyconn = psycopg2.connect(database="pysdd", user="postgres", password="801019", host="127.0.0.1", port="5432")
pycur = pyconn.cursor()
insert = 'insert into faxin_case(abstract,anyou,laiyuan,href) values(%s,%s,%s,%s)'
pycur.executemany(insert,df)
pyconn.commit()

f=open('faxin_case','wb')
pickle.dump(df,f)
f.close()
"""



if __name__=="__main__":
    #driver = Firefox_hdless()
    #driver = webdriver.Firefox()#Chrome_hdless()
    options = webdriver.ChromeOptions()
    
    
    if sys.platform=='win32':
        prefs = {
            "download.prompt_for_download": False,
            'download.default_directory': 'e:\\faxin',#下载目录
            "plugins.always_open_pdf_externally": True,
            'profile.default_content_settings.popups': 0,#设置为0，禁止弹出窗口
            #'profile.default_content_setting_values.images': 2,#禁止
            #图片加载
        }
    else:        
        prefs = {
            "download.prompt_for_download": False,
            'download.default_directory': '/media/chen/Davis/python/law/alpha/',#下载目录
            #'download.default_directory': '/home/chen/python/law/faxin/',#下载目录
            "plugins.always_open_pdf_externally": True,
            'profile.default_content_settings.popups': 0,#设置为0，禁止弹出窗口
            #'profile.default_content_setting_values.images': 2,#禁止图片加载
        }

    options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(options=options)
    url = 'https://alphalawyer.cn/#/app/tool/judicialView/%5B%5D'
    driver.get('https://alphalawyer.cn/')
    
