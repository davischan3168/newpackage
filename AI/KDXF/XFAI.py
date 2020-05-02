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


class XF():
    def __init__():
        self.__tts = "http://api.xfyun.cn/v1/service/v1/tts"
        self.__AUE = "raw"
        self.__APPID = "5ae94345"
        self.__API_KEY = "718ea4c61466265e4e88b1e6ecae2cd0"

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

    def getBody(self, text):
        data = {'text':text}
        return data

    def writeFile(self, fs, content):
        with open(fs, 'wb') as f:
            f.write(content)
        return
        
    def tts(self, text,voice="xiaoyan",\
            engine="intp65",speed="45",volume="70",\
            rate="16000",pitch="50",path=''):
        
       if path=='':
           if AUE == "raw":
               path="audio/audio_%s.wav"%re.sub('\W*', '_', text)
           else :
               path="audio/audio_%s.mp3"%re.sub('\W*', '_', text)
        if not os.path.exists(path):
            r = requests.post(self.__URL,headers=self.getHeader(voice,engine,speed,volume,rate,pitch),data=self.getBody(text))
            contentType = r.headers['Content-Type']
            if contentType == "audio/mpeg":
                #sid = r.headers['sid']
                self.writeFile(path,r.content)
                #print ("success, sid = " + sid)
            else:
                #print(text)
                #print(r.text)
                pass
        else :
            #print ("The file %s is exist."%path)
            pass
        return         
