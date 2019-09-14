#!/usr/bin/env python3
# -*-coding:utf-8-*-

from AI.BDAI.tts import BD_TTSBase as Ch_wordTaudio
from AI.trans.youdaodictvoice import download_audio_YX as Eng_wordTaudio
import os
import re

def Ttaudio(textlist,mtype='eng',pl=True):
    wlists=[]
    if isinstance(textlist,list):
        wlists.extend(textlist)
    elif isinstance(textlist,str):
        if os.path.isfile(textlist):
            cc=re.compile('[,，]')
            try:
                text=open(textlist,encoding=utf8).read()
            except Exception as e:
                text=open(textlist,encoding='gbk').read()

            tcontent=re.sub('\n{1,}',',')
            tlist=cc.split(tcontent)
            wlists.extend(tlist)
    else:
        print('Please input txt files or list')

    if mtype == 'eng':
        Eng_wordTaudio(wlists)
    elif mtype == 'ch':
        for w in wlists:
            Ch_wordTaudio(w,pl=pl)

    return
