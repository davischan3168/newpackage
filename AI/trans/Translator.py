#!/usr/bin/env python3
# -*-coding:utf-8-*-
import urllib.request
import urllib.parse
import json
import requests
import hashlib
import time
import random
import execjs
import re
import os
from playsound import playsound
import sys
if sys.platform == 'linux':
    os.environ["EXECJS_RUNTIME"] = "Node"

crs=re.compile(r'\s+')
def trans360(text):
    url = 'http://fanyi.so.com/index/search'
    data = {
        'query':text,
        'eng':'0'
    }
    data = urllib.parse.urlencode(data).encode('utf - 8')
    wy = urllib.request.urlopen(url,data)
    html = wy.read().decode('utf - 8')
    ta = json.loads(html)
    return ta['data']['fanyi']

def trans_iciba(text):
    url = 'http://fy.iciba.com/ajax.php?a=fy'
    data = {
        'w':text,
        'f':'auto',
        't':'auto'
    }
    data = urllib.parse.urlencode(data).encode('utf - 8')
    wy = urllib.request.urlopen(url,data)
    html = wy.read().decode('utf - 8')
    ta = json.loads(html)
    return ta['content']['out']

def trans_youd(txt):
    url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&sessionFrom=https://www.baidu.com/link'
    data = {'from': 'AUTO', 'to': 'AUTO', 'smartresult': 'dict', 'client': 'fanyideskweb', 'salt': '1500092479607',
            'sign': 'c98235a85b213d482b8e65f6b1065e26', 'doctype': 'json', 'version': '2.1', 'keyfrom': 'fanyi.web',
            'action': 'FY_BY_CL1CKBUTTON', 'typoResult': 'true', 'i': txt}

    data = urllib.parse.urlencode(data).encode('utf-8')
    wy = urllib.request.urlopen(url, data)
    html = wy.read().decode('utf-8')
    ta = json.loads(html)
    return ta['translateResult'][0][0]['tgt']

class Youdao(object):
    def __init__(self, msg):
        self.msg = msg
        self.url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
        self.D = "ebSeFb%=XZ%T[KZ)c(sy!"
        self.salt = self.get_salt()
        self.sign = self.get_sign()

    def get_md(self, value):
        '''md5加密'''
        m = hashlib.md5()
        # m.update(value)
        m.update(value.encode('utf-8'))
        return m.hexdigest()

    def get_salt(self):
        '''根据当前时间戳获取salt参数'''
        s = int(time.time() * 1000) + random.randint(0, 10)
        return str(s)

    def get_sign(self):
        '''使用md5函数和其他参数，得到sign参数'''
        s = "fanyideskweb" + self.msg + self.salt + self.D
        return self.get_md(s)

    def get_result(self):
        '''headers里面有一些参数是必须的，注释掉的可以不用带上'''
        headers = {
            # 'Accept': 'application/json, text/javascript, */*; q=0.01',
            # 'Accept-Encoding': 'gzip, deflate',
            # 'Accept-Language': 'zh-CN,zh;q=0.9,mt;q=0.8',
            # 'Connection': 'keep-alive',
            # 'Content-Length': '240',
            # 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'OUTFOX_SEARCH_USER_ID=-2022895048@10.168.8.76;',
            # 'Host': 'fanyi.youdao.com',
            # 'Origin': 'http://fanyi.youdao.com',
            'Referer': 'http://fanyi.youdao.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; rv:51.0) Gecko/20100101 Firefox/51.0',
            # 'X-Requested-With': 'XMLHttpRequest'
        }
        data = {
            'i': self.msg,
            'from': 'AUTO',
            'to': 'AUTO',
            'smartresult': 'dict',
            'client': 'fanyideskweb',
            'salt': self.salt,
            'sign': self.sign,
            'doctype': 'json',
            'version': '2.1',
            'keyfrom': 'fanyi.web',
            'action': 'FY_BY_CL1CKBUTTON',
            'typoResult': 'true'
        }
        html = requests.post(self.url, data=data, headers=headers).text
        print(html)
        infos = json.loads(html)
        if 'translateResult' in infos:
            try:
                result = infos['translateResult'][0][0]['tgt']
                return result
            except:
                pass

def trans_youdf(text):
    y = Youdao(text)
    return y.get_result()

class GoogleTrans():

    def __init__(self):
        self.ctx = execjs.compile(""" 
        function TL(a) { 
        var k = ""; 
        var b = 406644; 
        var b1 = 3293161072; 
        var jd = "."; 
        var $b = "+-a^+6"; 
        var Zb = "+-3^+b+-f"; 
        for (var e = [], f = 0, g = 0; g < a.length; g++) { 
            var m = a.charCodeAt(g); 
            128 > m ? e[f++] = m : (2048 > m ? e[f++] = m >> 6 | 192 : (55296 == (m & 64512) && g + 1 < a.length && 56320 == (a.charCodeAt(g + 1) & 64512) ? (m = 65536 + ((m & 1023) << 10) + (a.charCodeAt(++g) & 1023), 
            e[f++] = m >> 18 | 240, 
            e[f++] = m >> 12 & 63 | 128) : e[f++] = m >> 12 | 224, 
            e[f++] = m >> 6 & 63 | 128), 
            e[f++] = m & 63 | 128) 
        } 
        a = b; 
        for (f = 0; f < e.length; f++) a += e[f], 
        a = RL(a, $b); 
        a = RL(a, Zb); 
        a ^= b1 || 0; 
        0 > a && (a = (a & 2147483647) + 2147483648); 
        a %= 1E6; 
        return a.toString() + jd + (a ^ b) 
    }; 
    function RL(a, b) { 
        var t = "a"; 
        var Yb = "+"; 
        for (var c = 0; c < b.length - 2; c += 3) { 
            var d = b.charAt(c + 2), 
            d = d >= t ? d.charCodeAt(0) - 87 : Number(d), 
            d = b.charAt(c + 1) == Yb ? a >>> d: a << d; 
            a = b.charAt(c) == Yb ? a + d & 4294967295 : a ^ d 
        } 
        return a 
    } 
    """)

    def getTk(self, text):
        return self.ctx.call("TL", text)

def open_url(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64;rv:23.0) Gecko/20100101 Firefox/23.0',
               'Content-Type':'application/x-www-form-urlencoded;charset=UTF-8',
               'Host': 'translate.google.cn'
               #'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
    }
    req = urllib.request.Request(url=url, headers=headers)
    response = urllib.request.urlopen(req)
    data = response.read().decode('utf-8')
    return data

def translate(content, tk, sl, tl):
    """
    sl代表源语言，tl代表目标语言。
    """    
    if len(content) > 4891:
        print("翻译文本超过限制！")
        return

    content = urllib.parse.quote(content)

    url = "http://translate.google.cn/translate_a/single?client=t" \
          "&sl=%s&tl=%s&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca" \
          "&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&clearbtn=1&otf=1&pc=1" \
          "&srcrom=0&ssel=0&tsel=0&kc=2&tk=%s&q=%s" % (sl, tl, tk, content)


    result = open_url(url)

    end = result.find("\",")
    if end > 4:
        #print(result[4:end])
        return result[4:end]

def trans_google(text, sl, tl):
    """
    sl代表源语言，tl代表目标语言。
    """
    js=GoogleTrans()

    tk = js.getTk(text)
    tt=translate(text,tk, sl, tl)
    return tt

def open_urlv(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64;rv:23.0) Gecko/20100101 Firefox/23.0',
               'Content-Type':'application/x-www-form-urlencoded;charset=UTF-8',
               'Host': 'translate.google.cn'
               #'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
    }
    req = urllib.request.Request(url=url, headers=headers)
    response = urllib.request.urlopen(req)
    #data = response.read().decode('utf-8')
    return response

def GetEnglishMp3_google(content, tl='en',Ts=2):
    """
    sl代表源语言
    """    
    if len(content) > 4891:
        print("翻译文本超过限制！")
        return
    js=GoogleTrans()
    tk = js.getTk(content)
    word=crs.sub('_',content.strip())
    content = urllib.parse.quote(content)
    url = "https://translate.google.cn/translate_tts?ie=UTF-8&client=t&prev=input&q=%s&tl=%s&total=1&idx=0&textlen=4&tk=%s&client=webapp"% (content, tl, tk)
    
    fp='ggaudio/'+word+'.mp3'
    if not os.path.exists(fp):
        r = requests.get(url,stream=True)
        with open(fp, 'wb+') as f:
            for chunk in r.iter_content(chunk_size=128):
                f.write(chunk)
    for _ in range(Ts):
        playsound(fp)
        time.sleep(1)
    return

def GetEnglishMp3_youdao(word, outputdir='audio/',Ts=2):
    word=word.strip()
    fpath=os.path.join(outputdir,crs.sub('_',word) + '.mp3')
    if not os.path.exists(fpath):
        r = requests.get(url='http://dict.youdao.com/dictvoice?audio=' + word +'&type=2',stream=True)
        with open(fpath, 'wb+') as f:
            for chunk in r.iter_content(chunk_size=128):
                f.write(chunk)
        #print('Download %s fineshed...'%word)
        tem=word.split(' ')
 
        if len(tem)==1:
            pass
            #print("Download the voice of word fineshed: %s ......"%word)
        elif len(tem)>1:
            pass
            #print("Download the voice of sentence fineshed: %s ......"%word)
    for _ in range(Ts):
        playsound(fpath)
        time.sleep(1)
    return

def ListenF_words(path='unit_all.txt',fun=GetEnglishMp3_google, nums=20):
    fwords = open(path,encoding = 'utf8').readlines()
    i = int(input('输入开始的单词数:\n'))
    if i+nums > len(fwords):
        Li = fwords[i:len(words)]
    else:
        Li = fwords[i:i+nums]
    
    ll=fwords[i:i+nums]
    rs = re.compile('\s+')
    for n,i in enumerate(ll):
        i=i.strip()
        ii=rs.sub('_',i)
        fun(i)
        print('%s : %s'%(n+1,i))
    return
if __name__=="__main__":
    lf='/home/chen/listen.txt'
 
    Typ = sys.argv[1]
    #选听写的类型1为每个输入，2为听写以前的听写过的单词
    if Typ == '1':
        with open(lf,'r') as t:
            wds=set(t.readlines())
        f=open(lf,'a')
        while True:
            word = input('Enter word:').strip()
            if len(word)>0:
                GetEnglishMp3_youdao(word,Ts=3)
                if word not in wds:
                    wds.add(word)
                    f.write(word+'\n')
                    f.flush()
            else:
                break
    elif Typ == '2':
        f=open(lf,'r').readlines()
        words = set(f)
        #f.close()
        for i,word in enumerate(words):
            print('%s  : %s'%(i+1, word))
            GetEnglishMp3_youdao(word,Ts=3)
            
        
    
