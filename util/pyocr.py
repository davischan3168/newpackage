#!/usr/bin/env python3
# -*-coding:utf-8-*-
import pytesseract as pyt
from PIL import Image

def PngOcr(imf,lang='chi_sim'):
    """
    imf:  为图片文件
    lang：为语言，主要有chi_sim,chi_tra,eng三种，分别为简体、繁体中文，
          以及英语。
    """
    im = Image.open(imf)
    code = pyt.image_to_string(im,lang=lang)
    return code
