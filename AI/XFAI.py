#!/usr/bin/env python3
# -*-coding:utf-8-*-
import requests
import time
import hashlib
import base64
import os
import sys
import json
import re


class XFAI():
    def __init__(self):
        self.__tts = "http://api.xfyun.cn/v1/service/v1/tts"
        self.__AUE = "raw"
        self.__APPID = "5ae94345"
        self.__API_KEY = "718ea4c61466265e4e88b1e6ecae2cd0"
        
        self.__ocr = "http://webapi.xfyun.cn/v1/service/v1/ocr/general"
        self.__API_KEYocr = "069d8996e03e644d08458625df894f53"

        self.__iat = "http://api.xfyun.cn/v1/service/v1/iat"
        self.__API_KEYiat = "a8b94ef76fda8f87b990f24c660213d9"

    def getHeaderiat(self, engineType):
        curTime = str(int(time.time()))
        param = "{\"aue\":\"" + self.__AUE + "\"" + ",\"engine_type\":\"" + engineType + "\"}"
        paramBase64 = str(base64.b64encode(param.encode('utf-8')), 'utf-8')
        
        m2 = hashlib.md5()
        m2.update((self.__API_KEYiat + curTime + paramBase64).encode('utf-8'))
        checkSum = m2.hexdigest()
        header = {
            'X-CurTime': curTime,
            'X-Param': paramBase64,
            'X-Appid': self.__APPID,
            'X-CheckSum': checkSum,
            'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
        }
        return header

    def getBodyiat(self, filepath):
        binfile = open(filepath, 'rb')
        data = {'audio': base64.b64encode(binfile.read())}
        return data

    def IatFpcm(self,audioFilePath, engineType= "sms16k"):
        """
        将音频文件转为文字。
        audioFilePath:音频文件,为pcm格式。
        """
        r = requests.post(self.__iat, headers=self.getHeaderiat(engineType), data=self.getBodyiat(audioFilePath))
        content=r.content.decode('utf-8')
        word = json.loads(content)
        return word

    def getHeader(self,voice,engine,speed,volume,rate,pitch):
        curTime = str(int(time.time()))
        param ={
            "aue":self.__AUE,
            "auf":"audio/L16;rate=%s"%rate,
            "voice_name":voice,
            "engine_type":engine,
            "speed":speed,
            "pitch":pitch,
            "volume":volume
        }
        paramBase64 = base64.b64encode(json.dumps(param).replace(' ', '').encode('utf8'))
        m2 = hashlib.md5()
        m2.update((self.__API_KEY.encode('utf8') + curTime.encode('utf8') + paramBase64))
        checkSum = m2.hexdigest()
        header ={
            'X-CurTime':curTime,
            'X-Param':paramBase64,
            'X-Appid':self.__APPID,
            'X-CheckSum':checkSum,
            'X-Real-Ip':'127.0.0.1',
            'Content-Type':'application/x-www-form-urlencoded; charset=utf-8',
        }
        return header

    def getHeader_ocr(self):
        curTime = str(int(time.time()))
        param = {"language": "cn|en", "location": "false"}
        param = json.dumps(param)
        paramBase64 = base64.b64encode(param.encode('utf-8'))
        
        m2 = hashlib.md5()
        str1 = self.__API_KEYocr + curTime + str(paramBase64,'utf-8')
        m2.update(str1.encode('utf-8'))
        checkSum = m2.hexdigest()

        header = {
            'X-CurTime': curTime,
            'X-Param': paramBase64,
            'X-Appid': self.__APPID,
            'X-CheckSum': checkSum,
            'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
        }
        return header

    def OCRG(self, path):
        """
        path: image file path,jpeg,
        """
        with open(path, 'rb') as f:
            f1 = f.read()

        f1_base64 = str(base64.b64encode(f1), 'utf-8')
        
        data = {
            'image': f1_base64
        }

        #headers=getHeader(language, location)
        r = requests.post(self.__ocr, data=data, headers=self.getHeader_ocr())
        result = str(r.content, 'utf-8')
        return result

    def Ocr2Text(self, path):
        d=self.OCRG(path)
        ds=json.loads(d)
        text=[]
        if ds['code']=='0':
            df=ds['data']['block'][0]['line']
            #print(df)
            for i in df:
                text.append(i['word'][0]['content'])
            T='\n'.join(text)
            return T
        else:
            print("The Errors code is %s, decs is %s."%(ds['code'],ds["desc"]))
            return ''.join(text)    

    def getBody(self, text):
        data = {'text':text}
        return data

    def writeFile(self, fs, content):
        with open(fs, 'wb') as f:
            f.write(content)
        return
        
    def Tts(self, text,voice="xiaoyan",\
            engine="intp65",speed="45",volume="70",\
            rate="16000",pitch="50",path=''):
        
        if path=='':
            if self.__AUE == "raw":
                path="audio/audio_%s.wav"%re.sub('\W+', '_', text)
            else :
                path="audio/audio_%s.mp3"%re.sub('\W+', '_', text)
               
        if not os.path.exists(path):
            r = requests.post(self.__tts,headers=self.getHeader(voice,engine,speed,volume,rate,pitch),data=self.getBody(text))
            contentType = r.headers['Content-Type']
            if contentType == "audio/mpeg":
                #sid = r.headers['sid']
                self.writeFile(path,r.content)
                #print ("success, sid = " + sid)
            else:
                #print(text)
                print(r.text)
                pass
        else :
            #print ("The file %s is exist."%path)
            pass
        return         
