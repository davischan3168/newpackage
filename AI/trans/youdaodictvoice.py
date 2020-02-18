#!/usr/bin/env python3
# -*-coding:utf-8-*-
import argparse
import random
import time
import os
import re
from collections.abc import Iterable
import requests
import simpleaudio as sa
from pydub import AudioSegment
from contextlib import contextmanager
from os import chdir, getcwd, listdir, remove, makedirs
from os.path import isfile, exists, join, expanduser


def check_cache(f):
    def _wrapper(words):
        if not isinstance(words, Iterable):
            words = (words)
        for word in words:
            if not isfile(word + '.wav'):
                f([word])
    return _wrapper


def format_transfer(name, ori_format, target_format, remove_ori=False):
    """ori_format, target_format: only 'mp3' and 'wav' and supported"""
    try:
        song = getattr(AudioSegment, "from_" + ori_format)(name + "." + ori_format)
    except AttributeError:
        raise ValueError("Only 'mp3' and 'wav' format are supported")
    song.export(name + "." + target_format, format=target_format)
    if remove_ori:
        remove(name + "." + ori_format)


@check_cache
def download_audio(words, outputdir='audio/',target_format='wav'):
    for i,word in enumerate(words):
        fpath=os.path.join(audio,'%s_'%word.replace(' ','')+str(i).zfill(2) + '.mp3')
        if not os.path.exists(fpath):
            r = requests.get(url='http://dict.youdao.com/dictvoice?audio=' + word +'&type=2',stream=True)
            with open(fpath, 'wb+') as f:
                for chunk in r.iter_content(chunk_size=128):
                    f.write(chunk)
            tem=word.split(' ')
            if len(tem)==1:
                print("Download the voice of word fineshed: %s ......"%word)
            elif len(tem)>1:
                print("Download the voice of sentence fineshed: %s ......"%word)            
    return

def download_audio_YX(words, outputdir='audio/',target_format='mp3'):
    if not os.path.exists(outputdir):
        os.mkdir(outputdir)
    for i,word in enumerate(words):
        fpath=os.path.join(outputdir,'%s_%s_'%(str(i).zfill(3),word.replace(' ',''))+'.'+ target_format)
        if not os.path.exists(fpath):
            r = requests.get(url='http://dict.youdao.com/dictvoice?audio=' + word +'&type=2',stream=True)
            with open(fpath, 'wb+') as f:
                for chunk in r.iter_content(chunk_size=128):
                    f.write(chunk)
            tem=word.split(' ')
            if len(tem)==1:
                print("Download the voice of word fineshed: %s ......"%word)
            elif len(tem)>1:
                print("Download the voice of sentence fineshed: %s ......"%word) 
    return

def download_audio_WX(words, outputdir='audio/',target_format='mp3'):
    if not os.path.exists(outputdir):
        os.mkdir(outputdir)
    for i,word in enumerate(words):
        fpath=os.path.join(outputdir,'%s'%word.replace(' ','')+'.'+ target_format)
        if not os.path.exists(fpath):
            r = requests.get(url='http://dict.youdao.com/dictvoice?audio=' + word +'&type=2',stream=True)
            with open(fpath, 'wb+') as f:
                for chunk in r.iter_content(chunk_size=128):
                    f.write(chunk)
            tem=word.split(' ')
            if len(tem)==1:
                print("Download the voice of word fineshed: %s ......"%word)
            elif len(tem)>1:
                print("Download the voice of sentence fineshed: %s ......"%word) 
    return
csub=re.compile('\s+')
def EnglishWordAudio_single(word, outputdir='audio/'):
    word=word.strip()
    fpath=os.path.join(outputdir,csub.sub('_',word) + '.mp3')
    if not os.path.exists(fpath):
        r = requests.get(url='http://dict.youdao.com/dictvoice?audio=' + word +'&type=2',stream=True)
        with open(fpath, 'wb+') as f:
            for chunk in r.iter_content(chunk_size=128):
                f.write(chunk)
        print('Download %s fineshed...'%word)
        tem=word.split(' ')
        if len(tem)==1:
            print("Download the voice of word fineshed: %s ......"%word)
        elif len(tem)>1:
            print("Download the voice of sentence fineshed: %s ......"%word)            
    return

def EnglishWord_audio_list(wordlist, outputdir='audio/'):
    if isinstance(wordlist,list):
        for word in wordlist:
            try:
                EnglishWordAudio_single(word, outputdir)
            except:
                pass
    return

if __name__ == '__main__':
    pass
