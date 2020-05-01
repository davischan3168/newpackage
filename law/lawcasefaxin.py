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

def login(driver):
    driver.get('http://www.faxin.cn')
    driver.implicitly_wait(5)
    driver.find_element_by_link_text('登录').click()
    driver.implicitly_wait(5)
    driver.find_element_by_id('user_name').clear()
    driver.find_element_by_id('user_name').send_keys('18929527191')
    driver.implicitly_wait(5)
    driver.find_element_by_id('user_password').clear()
    driver.find_element_by_id('user_password').send_keys('chen&801019')
    driver.implicitly_wait(5)
    driver.find_element_by_id('submitButton').click()
    return

items = []
def getlist_zhichan(driver,start,end):
    cc = re.compile(r'^http')
    df = driver.find_elements_by_xpath('//ul[@id="alFourthDiv"]/li')
    global items
    for ds in df:
        dd = ds.text.split('\n')[:3]
        #print(dd)
        href = ds.find_element_by_tag_name('a').get_attribute('href')
        #print(href)
        if cc.match(href):
            #print(dd,href)
            items.append((dd,href))

    for page in range(start+1,end+1):
        try:
            print('Click to Page %s'%page)
            driver.find_element_by_link_text('%s'%page).click()
            driver.implicitly_wait(10)
            time.sleep(3)
            df = driver.find_elements_by_xpath('//ul[@id="alFourthDiv"]/li')
            with open('sucessed.txt','a',encoding='utf8') as f:
                f.write('%s'%page+'\n')
            for ds in df:
                dd = ds.text.split('\n')[:3]
                #print(dd)
                href = ds.find_element_by_tag_name('a').get_attribute('href')
                #print(href)
                if cc.match(href):
                    print(href)
                    items.append((dd,href))
        except:
            with open('failed.txt','a',encoding='utf8') as f:
                f.write('%s'%page+'\n')            
    return

def getlist_xingzheng(driver,start,end):
    cc = re.compile(r'^http')
    df = driver.find_elements_by_xpath('//ul[@id="alThirdDiv"]/li')
    global items
    for ds in df:
        dd = ds.text.split('\n')[:3]
        #print(dd)
        href = ds.find_element_by_tag_name('a').get_attribute('href')
        #print(href)
        if cc.match(href):
            #print(dd,href)
            items.append((dd,href))

    for page in range(start+1,end+1):
        try:
            print('Click to Page %s'%page)
            driver.find_element_by_link_text('%s'%page).click()
            driver.implicitly_wait(10)
            time.sleep(3)
            df = driver.find_elements_by_xpath('//ul[@id="alThirdDiv"]/li')
            with open('sucessed.txt','a',encoding='utf8') as f:
                f.write('%s'%page+'\n')
            for ds in df:
                dd = ds.text.split('\n')[:3]
                #print(dd)
                href = ds.find_element_by_tag_name('a').get_attribute('href')
                #print(href)
                if cc.match(href):
                    print(href)
                    items.append((dd,href))
        except:
            with open('failed.txt','a',encoding='utf8') as f:
                f.write('%s'%page+'\n')            
    return

def getlist_xingshi(driver,start,end):
    cc = re.compile(r'^http')
    df = driver.find_elements_by_xpath('//ul[@id="alSecondDiv"]/li')
    global items
    for ds in df:
        dd = ds.text.split('\n')[:3]
        #print(dd)
        href = ds.find_element_by_tag_name('a').get_attribute('href')
        #print(href)
        if cc.match(href):
            #print(dd,href)
            items.append((dd,href))

    for page in range(start+1,end+1):
        try:
            print('Click to Page %s'%page)
            driver.find_element_by_link_text('%s'%page).click()
            driver.implicitly_wait(10)
            time.sleep(3)
            df = driver.find_elements_by_xpath('//ul[@id="alSecondDiv"]/li')
            with open('sucessed.txt','a',encoding='utf8') as f:
                f.write('%s'%page+'\n')
            for ds in df:
                dd = ds.text.split('\n')[:3]
                #print(dd)
                href = ds.find_element_by_tag_name('a').get_attribute('href')
                #print(href)
                if cc.match(href):
                    print(href)
                    items.append((dd,href))
        except:
            with open('failed.txt','a',encoding='utf8') as f:
                f.write('%s'%page+'\n')            
    return

def getlist_minshi(driver,start,end):
    cc = re.compile(r'^http')
    df = driver.find_elements_by_xpath('//ul[@id="alFirstDiv"]/li')
    global items
    for ds in df:
        dd = ds.text.split('\n')[:3]
        #print(dd)
        href = ds.find_element_by_tag_name('a').get_attribute('href')
        #print(href)
        if cc.match(href):
            print(dd,href)
            items.append((dd,href))

    for page in range(start+1,end+1):
        try:
            print('Click to Page %s'%page)
            driver.find_element_by_link_text('%s'%page).click()
            driver.implicitly_wait(10)
            time.sleep(3)
            df = driver.find_elements_by_xpath('//ul[@id="alFirstDiv"]/li')
            with open('sucessed.txt','a',encoding='utf8') as f:
                f.write('%s'%page+'\n')
            for ds in df:
                dd = ds.text.split('\n')[:3]
                #print(dd)
                href = ds.find_element_by_tag_name('a').get_attribute('href')
                #print(href)
                if cc.match(href):
                    print(dd,href)
                    items.append((dd,href))
        except:
            with open('failed.txt','a',encoding='utf8') as f:
                f.write('%s'%page+'\n')            
    return

def select_down_drop(driver):
    dd=driver.find_element_by_xpath('//span[@class="downIcons"]')
    ActionChains(driver).move_to_element(dd).click().perform()
    driver.find_element_by_xpath('//li[@flag="50"]').click()

    return

def insert2pg(df,pyconn,pycur):
    insert = 'insert into faxin_case(abstract,anyou,laiyuan,href) values(%s,%s,%s,%s)'
    pycur.executemany(insert,df)
    pyconn.commit()    
    return

def gethref(url):
    c = re.findall(r'^http.*&(.*)&.*',url)
    href = 'http://www.faxin.cn/lib/cpal/DownloadAlyz.aspx?%s&downloadType=txt&isProperty=true&isKeyword=true&tiao='
    if len(c)>0:
        href = href%c[0]
        return href
    
fdown = []
#ckies = firefox_cookies('www.faxin.cn')

def getText(driver, df):
    cc = re.compile(r'^http.*&(.*)&.*')
    global fdown
    count = 0
    href = 'http://www.faxin.cn/lib/cpal/DownloadAlyz.aspx?%s&downloadType=txt&isProperty=true&isKeyword=true&tiao='
    for i in df:
        gid = cc.findall(i[3])[0]
        try:
            driver.get(href%gid)
            river.implicitly_wait(5)
            time.sleep(0.5)
        except:
            count = count +1
            print('failed %s ....'%count)
            #fdown.append(i)
            time.sleep(0.8)
            pass
    return

def SpiderText(driver, df):
    cc = re.compile(r'^http.*&(.*)&.*')
    ss = re.compile(r'\s')
    global fdown
    href = 'http://www.faxin.cn/lib/cpal/DownloadAlyz.aspx?%s&downloadType=txt&isProperty=true&isKeyword=true&tiao='
    for i in df:
        gid = cc.findall(i[3])[0]
        text = []
        newpath = 'law/faxin/'+i[1].strip()+'_'+gid[5:]+'.txt'
        newpath1 = 'law/faxin/'+ss.sub('@',i[0].strip())+'_'+gid[5:]+'.txt'
        oldpath = 'law/faxin/'+i[0]+'.txt'
        if (not os.path.exists(oldpath)) or (not os.path.exists(newpath))or (not os.path.exists(newpath1)):
            try:
                driver.get(i[3])
                driver.implicitly_wait(5)
                time.sleep(0.5)
                soup = BeautifulSoup(driver.page_source,'lxml')
                h1 = soup.h1.text.strip()
                h2 = soup.h1.text.strip()
                yz = soup.find('div',attrs={'class','content_title'}).text
                content = soup.find('div',attrs={'class','content_body'}).text
                with open(newpath, 'w') as f:
                    f.write(h1+'\n\n'+h2+'\n\n'+yz+'\n\n'+content)
            except:
                fdown.append(i)
                pass
        elif os.path.exists(oldpath):
            #shutil.move(oldpath,newpath1)
            pass
    return

def getTextpop(driver, df):
    cc = re.compile(r'^http.*&(.*)&.*')
    ss = re.compile(r'\s')
    count = 1
    href = 'http://www.faxin.cn/lib/cpal/DownloadAlyz.aspx?%s&downloadType=txt&isProperty=true&isKeyword=true&tiao='
    while True:
        if len(df)<1:
            break
        i = df.pop(0)
        gid = cc.findall(i[3])[0]
        if sys.platform=='win32':
            newpath = 'e:/faxin/'+i[1].strip()+'_'+gid[5:]+'.txt'
            newpath1 = 'e:/faxin/'+ss.sub('@',i[0].strip())+'_'+gid[5:]+'.txt'
            oldpath = 'e:/faxin/'+i[0]+'.txt'
        else:
            newpath = 'law/faxincase/'+i[1].strip()+'_'+gid[5:]+'.txt'
            newpath1 = 'law/faxincase/'+ss.sub('@',i[0].strip())+'_'+gid[5:]+'.txt'
            oldpath = 'law/faxincase/'+i[0]+'.txt'
        if (not os.path.exists(oldpath)) or (not os.path.exists(newpath))or (not os.path.exists(newpath1)):
            try:
                #print('%s not exists'%oldpath)
                driver.get(href%gid)
                driver.implicitly_wait(5)
                time.sleep(0.5)
                #shutil.move(oldpath,newpath1)
            except:
                #fdown.append(i)
                pass
        elif os.path.exists(oldpath):
            print('%s: %s is exists'%(count,oldpath))
            count = count + 1
            pass
            #shutil.move(oldpath,newpath1)
        elif os.path.exists(newpath):
            print('%s: %s is exists'%(count,newpath))
            count = count +1
        elif os.path.exists(newpath1):
            print('%s: %s is exists'%(count,newpath1))
            count = count +1
            
    return

def Cleardf(df):
    cc = re.compile(r'^http.*&(.*)&.*')
    ss = re.compile(r'\s')
    count = 1
    dd = []
    for i in df:
        gid = cc.findall(i[3])[0]
        print(i[0])
        if sys.platform == 'win32':
            newpath = 'e:/faxin/'+i[1].strip()+'_'+gid[5:]+'.txt'
            newpath1 = 'e:/faxin/'+ss.sub('@',i[0].strip())+'_'+gid[5:]+'.txt'
            oldpath = 'e:/faxin/'+i[0]+'.txt'
        else:
            newpath = 'law/faxincase/'+i[1].strip()+'_'+gid[5:]+'.txt'
            newpath1 = 'law/faxincase/'+ss.sub('@',i[0].strip())+'_'+gid[5:]+'.txt'
            oldpath = 'law/faxincase/'+i[0]+'.txt'
        if (not os.path.exists(oldpath)) or (not os.path.exists(newpath))or (not os.path.exists(newpath1)):
            try:
                #print('%s not exists'%oldpath)
                #driver.get(href%gid)
                #driver.implicitly_wait(5)
                #time.sleep(0.5)
                #shutil.move(oldpath,newpath1)
                dd.append(i)
            except:
                #fdown.append(i)
                pass
        elif os.path.exists(oldpath):
            print('%s: %s is exists'%(count,oldpath))
            count = count + 1
            pass
            #shutil.move(oldpath,newpath1)
        elif os.path.exists(newpath):
            print('%s: %s is exists'%(count,newpath))
            count = count +1
        elif os.path.exists(newpath1):
            print('%s: %s is exists'%(count,newpath1))
            count = count +1

    print('the sum files is %s'%count)
    return dd

    
def SearchFaxin(search, mtype):
    sch = [ ]
    if isinstance(search,str):
        sch.append(search)
    elif isinstance(search, list):
        sch.extend(search)

    #sch = set(sch)
    gets = []
    
    if mtype == 'minfa':
        df = pickle.load(open('law/faxincase/faxin_minfa','rb'))

    elif mtype == 'xingshi':
        df = pickle.load(open('law/faxincase/faxin_xingshi','rb'))

    elif mtype == 'zhichan':
        df = pickle.load(open('law/faxincase/faxin_zhichan','rb'))

    elif mtype == 'xingzheng':
        df = pickle.load(open('law/faxincase/faxin_xingzheng','rb'))

    for dd in df:
        for word in sch:
            if word in dd[0]:
                gets.append(dd)

    return gets


def FaxinCaseYZ(fpath,RT='tuple'):
    cpyz = re.compile(r'裁判要旨|案例要旨|【裁判摘要】')

    #ss=re.compile(r'(纠纷案\s*$)|(纠纷上诉案\s*$)|(纠纷再审案\s*$')
    #ss=re.compile(r'(纠纷案\s*$)|(纠纷上诉案\s*$)|(纠纷再审案\s*$)')
    #ss=re.compile(r'纠纷\w{0,2}?案\s*$')
    ss=re.compile(r'.*?案\s*$')
    anhao = re.compile(r'[(（]{1}\d{4}[\u4e00-\u9fa5(（）)\d]*\d+号')
    yz = re.compile(r'相关法条|^\s*原告[:：]?.*?\n')
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
        ast['yz'] = text1.split(ast['lx'])[0].strip()
        #说明案件的裁判要旨
        #for ix in ['相关法条','^\s*原告[:：]?.*?\n',ast['lx']]:
    except:
        pass

    if ast['ah'].strip() == '':
        ast['ah'] = 'unavailable'
    if ast['yz'] == '':
        ast['yz'] = 'unavailable'
    if RT == 'dict':
        return ast
    elif RT == 'tuple':
        return ast['lx'].strip(),ast['ah'].strip(),ast['yz'].strip(),ast['qw'].strip()

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
            #'profile.default_content_setting_values.images': 2,#禁止图片加载
        }
    else:        
        prefs = {
            "download.prompt_for_download": False,
            'download.default_directory': '/home/chen/python/law/faxin/',#下载目录
            "plugins.always_open_pdf_externally": True,
            'profile.default_content_settings.popups': 0,#设置为0，禁止弹出窗口
            #'profile.default_content_setting_values.images': 2,#禁止图片加载
        }

    options.add_experimental_option('prefs', prefs)
    #driver = webdriver.Chrome(options=options)
    #driver.maximize_window()
    #login(driver)
    #"""
    url='http://www.faxin.cn/lib/cpal/AlyzLibrary.aspx?libid=0201'
    pass
    
