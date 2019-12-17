#!/usr/bin/env python3
# -*-coding:utf-8-*-
from PIL import Image
import os
import sys

def pngCrop(pngfile,x,y,w=0,h=0):
    '''
    裁剪：传入一个元组作为参数
    元组里的元素分别是：（距离图片左边界距离x， 距离图片上边界距离y，距离图片左边界距离+裁剪框宽度x+w，距离图片上边界距离+裁剪框高度y+h）
'''
    im=Image.open(pngfile)
    img_size = im.size
    print("图片宽度和高度分别是{}".format(img_size))
    region = im.crop((x, y, x+w, y+h))
    newf=os.path.splitext(pngfile)
    nf=newf[0]+'_crop'+newf[1]
    region.save(nf)
    return

def pngCropT2(pngfile):
    im=Image.open(pngfile)
    w,h = im.size
    r1=im.crop((0,0,w/2,h))
    r2=im.crop((w/2,0,w,h))
    newf=os.path.splitext(pngfile)
    nf1=newf[0]+'_crop_01'+newf[1]
    nf2=newf[0]+'_crop_02'+newf[1]
    r1.save(nf1)
    r2.save(nf2)
    return
    

if __name__=="__main__":
    pngCropT2(sys)
    
