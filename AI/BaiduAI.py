#!/usr/bin/env python3
# -*-coding:utf-8-*-
import base64
from aip import AipSpeech
from aip import AipOcr
import requests
import json

class BaiDAI():
    def __init__():
        self.__APP_ID = '10947352'
        self.__API_KEY = 'gELihIXKQxswEye4Wb3gCdsb'
        self.__SECRET_KEY = '2krKB6kQxfCdeuIDjGzXOfmqis7c1ByH'
        self.__gT =  'https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s'
        self.__tts = 'http://tsn.baidu.com/text2audio?lan=zh&ctp=1&cuid=abcdxxx&tok=%s&tex=%s&vol=%s&per=%s&spd=%s&pit=%s&aue=%s'
        self.client = AipSpeech(self.__APP_ID, self.__API_KEY, self.__SECRET_KEY)

        self.__APP_IDo = '10947557'
        self.__API_KEYo = 'KxCS71VeSUFLk00pUvk641Xz'
        self.__SECRET_KEYo = 'R8cnb80t6CmYXefE7aYzhro1goMLCjyZ'
        self.cliento = AipOcr(self.__APP_IDo, self.__API_KEYo, self.__SECRET_KEYo)
        
    def __getToken(self):
        r = requests.get(self.__gT%(self.__API_KEY, self.__SECRET_KEY))
        data = json.loads(r.text)
        return data['access_token']

    def textTaudiov1(self, text,vol=15,per=1,spd=4,pit=5,aue=6):
        """
        tex:        合成的文本，使用UTF-8编码。小于512个中文字或者英文数字。
            （文本在百度服务器内转换为GBK后，长度必须小于1024字节）
        lan:        固定值zh。语言选择,目前只有中英文混合模式，填写固定值zh
        spd:	选填	语速，取值0-9，默认为5中语速
        pit:	选填	音调，取值0-9，默认为5中语调
        vol:        选填	音量，取值0-15，默认为5中音量
        per:	选填	发音人选择, 0为普通女声，1为普通男生，3为情感合成-度逍遥，4为情感合成-度丫丫，默认为普通女声
        
        """
    
        uurl=self.__tts%(self.__gT,text,vol,per,spd,pit,aue)
        rr=requests.get(uurl)
        return rr.content

    def textTaudiov2(self,text,vol=15,per=1,spd=3,pit=5,aue=6,path='',pl=False):
        """
        tex:        合成的文本，使用UTF-8编码。小于512个中文字或者英文数字。
                （文本在百度服务器内转换为GBK后，长度必须小于1024字节）
        lan:        固定值zh。语言选择,目前只有中英文混合模式，填写固定值zh
        spd:	选填	语速，取值0-9，默认为5中语速
        pit:	选填	音调，取值0-9，默认为5中语调
        vol:        选填	音量，取值0-15，默认为5中音量
        per:	选填	发音人选择, 0为普通女声，1为普通男生，
                        3为情感合成-度逍遥，4为情感合成-度丫丫，默认为普通女声
        aue	        选填	3为mp3格式(默认)； 4为pcm-16k；5为pcm-8k；6为wav（内容同
                        pcm-16k）; 
                        注意aue=4或者6是语音识别要求的格式，但是音频内容不是语音识别要求的自然人发音，所以识别效果会受影响。
        
        """
        result  = self.client.synthesis(text, 'zh', 1, {
            'vol': vol,
            'spd':spd,
            'pit':pit,
            'per':per,
            'aue':aue
            
        })

        # 识别正确返回语音二进制 错误则返回dict 参照下面错误码

        if not isinstance(result, dict):
            return result
        
    def audioText(self, filePath):
        #要对段保存有一段语音的语音文件进行识别
        # 识别本地文件
        with open(filePath,'rb') as f:
            ct = f.read()
    
        d=self.client.asr(ct, 'pcm', 16000, {
            'dev_pid': '1536',
        })

        # 从URL获取文件识别
        """client.asr('', 'pcm', 16000, {
        'url': 'http://121.40.195.233/res/16k_test.pcm',
        'callback': 'http://xxx.com/receive',
        })"""
    
        return d.get('result','None')[0]

    def OCR_G(self, filePath):    

        with open(filePath, 'rb') as f:
            image = f.read()

 
        options = {}
        options["language_type"] = "CHN_ENG"
        options["detect_direction"] = "true"
        options["detect_language"] = "true"
        options["probability"] = "true"

        """ 带参数调用通用文字识别, 图片参数为本地图片 """
        d=self.cliento.basicGeneral(image, options)#用完500次后可改
        #d = client.basicAccurate(image)
        #url = "https//www.x.com/sample.jpg"
        text = []
        for i in d['words_result']:
            text.append(i['words'])

        return '\n'.join(text)

    def OCR_A(self, filePath):    

        with open(filePath, 'rb') as f:
            image = f.read()

 
        options = {}
        options["language_type"] = "CHN_ENG"
        options["detect_direction"] = "true"
        options["detect_language"] = "true"
        options["probability"] = "true"

        """ 带参数调用通用文字识别, 图片参数为本地图片 """
        #d=client.basicGeneral(image, options)#用完500次后可改
        d = self.cliento.basicAccurate(image, options)
        #url = "https//www.x.com/sample.jpg"
        text = []
        for i in d['words_result']:
            text.append(i['words'])

        return '\n'.join(text)    

    def TableOCR(self,mtype='excel'):
        """
        获得一张页面图片的表格文字
        """
        with open(filePath, 'rb') as f:
            image = f.read()

        if mtype=='excel':
            options={}
            options["result_type"] = "excel"
            temp=self.cliento.tableRecognition(image,options)
            r=requests.get(temp['result']['result_data'])
            return r.content

        else:
            options={}
            options["result_type"] = "json"
            temp=self.cliento.tableRecognition(image,options)
            s=json.loads(temp['result']['result_data'])
            return s['forms'][0]['body']
if __name__ == "__main__":
    pass
