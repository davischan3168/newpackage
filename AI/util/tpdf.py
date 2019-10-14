#!/usr/bin/env python3
# -*-coding:utf-8-*-
import os
import sys
import time
import string
from PIL import Image
from reportlab.lib.pagesizes import A4, landscape,portrait
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch,cm
#from AI.BDAI.ocr import BD_jsonTtext
from PyPDF2 import PdfFileReader,PdfFileWriter

def imgLongsplitimage2A4(src, dstpath=''):
    """
    将一个长图切割成A4大小的数张图
    """
    img = Image.open(src)
    w,h = img.size
    height=w*297/210 #A4纸比例出的高度
    height_dim=w*297/210# 记录一个固定值，方便后期调用
    num=h/height+1#将分割出的图片数量
    index=0
    print(height)
    s = os.path.split(src)#分割出路径和文件名
    if dstpath == '':
        dstpath = s[0]
    fn = s[1].split('.')
    basename = fn[0]#文件名
    postfix = fn[-1]#后缀名
    img_urls=[]
    #print('Original image info: %sx%s, %s, %s' % (w, h, img.format, img.mode))
    
    
    while (index < num):
        print ('The index is:', index,"height is ",height)
        #box = (0, height-1527, w, height)
        box = (0, height-height_dim, w, height)
        img.crop(box).save(os.path.join(dstpath, basename + '_' + str(index) + '.' + postfix), img.format)
        img_urls.append(os.path.join(dstpath, basename + '_' + str(index) + '.' + postfix))
        #height = height + 1527
        height=height+height_dim
        index = index + 1

    return img_urls

# 零散，大小一致图片，存储为pdf
def imgsto1pdf(input_paths, outputpath=''):
    """将数张大小一致的图存储为pdf文件"""
    index=0
    # 取一个大小
    if outputpath=='':
        import datetime
        outputpath='combinefiles_%s.pdf'%datetime.datetime.strftime(datetime.datetime.today(),'%Y-%m-%d-%H_%M_%S')
    (maxw, maxh) = Image.open(input_paths[0]).size
    c = canvas.Canvas(outputpath, pagesize=portrait((maxw, maxh)))
    for ont_path in input_paths :
        c.drawImage(ont_path, 0, 0, maxw, maxh)
        c.showPage()
        index=index+1
    c.save()
    return

def imgLongplitT1pdf(longPicpath):
    """将一张长图切割为A4大小的数张图，并存储为一pdf文件"""
    out=os.path.splitext(os.path.abspath(longPicpath))[0]+'.pdf'
    d=imgLongsplitimage2A4(longPicpath)
    s=d.pop(-1)
    
    imgsto1pdf(d,outputpath=out)
    for i in d:
        os.remove(i)
    os.remove(s)
    return

def imgLongto1pdf(input_path, outputpath=''):
    """将一张长图直接转为一个pd文件f"""
    #index=0
    # 取一个大小
    out=os.path.splitext(os.path.abspath(input_path))[0]+'.pdf'    
    if outputpath=='':
        #import datetime
        outputpath=out
        #outputpath='combinefiles_%s.pdf'%datetime.datetime.strftime(datetime.datetime.today(),'%Y-%m-%d-%H:%M:%S')
    (maxw, maxh) = Image.open(input_path).size
    c = canvas.Canvas(outputpath, pagesize=portrait((maxw, maxh)))
    #for ont_path in input_paths :
    c.drawImage(input_path, 0, 0, maxw, maxh)
    c.showPage()
    #index=index+1
    c.save()
    return
def imgLongto1pdf_dir(dirpath):
    ff=file_name(dirpath)
    for f in ff:
        path=os.path.splitext(f)[0]+'.pdf'
        if not os.path.exists(path):
            imgLongto1pdf(f)

    return
    

def BdOcrcrop(src, dstpath=''):
    """
    将一个长图切割成A4大小的数张图
    """
    img = Image.open(src)
    w,h = img.size
    if w>1500:
        tw=1500/2
    else:
        tw=w
    if h>4096:
        th=4096/2
    else:
        th=h
    #height=w*297/210 #A4纸比例出的高度
    height=w*th/tw
    #height_dim=w*297/210# 记录一个固定值，方便后期调用
    height_dim=w*th/tw
    num=h/height+1#将分割出的图片数量
    index=0
    print(height)
    s = os.path.split(src)#分割出路径和文件名
    if dstpath == '':
        dstpath = s[0]
    fn = s[1].split('.')
    basename = fn[0]#文件名
    postfix = fn[-1]#后缀名
    img_urls=[]
    #print('Original image info: %sx%s, %s, %s' % (w, h, img.format, img.mode))
    
    
    while (index < num):
        print ('The index is:', index,"height is ",height)
        #box = (0, height-1527, w, height)
        box = (0, height-height_dim, w, height)
        img.crop(box).save(os.path.join(dstpath, basename + '_' + str(index) + '.' + postfix), img.format)
        img_urls.append(os.path.join(dstpath, basename + '_' + str(index) + '.' + postfix))
        #height = height + 1527
        height=height+height_dim
        index = index + 1

    return img_urls
    
    
            
def file_name(file_dir, suffix =[ ".jpg",'.jpeg','.png']):
    L=[]
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1].lower() in suffix:
                L.append(os.path.join(root, file))
    return L

 


def picsTpdf(f_pdf, filedir, suffix):
    #f_pdf pdf file path ,include filename输出的文件名册
    #filedir pic file path
    #suffix pic file suffix examples: .jpg
    (w, h) = landscape(A4)
    #print('w:%s,h:%s'%(w,h))
    #c = canvas.Canvas(f_pdf, pagesize = landscape(A4))
    c = canvas.Canvas(f_pdf, pagesize = (21*cm,29*cm))
    fileList = file_name(filedir, suffix)

    for f in fileList:
        (xsize, ysize) = Image.open(f).size

        ratx = xsize / w
        raty = ysize / h
        ratxy = xsize / (1.0 * ysize)
        if ratx > 1:
            ratx = 0.99
        if raty > 1:
            raty = 0.99

        rat = ratx

        if ratx < raty:
            rat = raty
        widthx = w * rat
        widthy = h * rat
        widthx = widthy * ratxy
        posx = (w - widthx) / 2
        if posx < 0:
            posx = 0
        posy = (h - widthy) / 2
        if posy < 0:
            posy = 0

        mw=widthx-2*posx
        mh=widthy
        #print('posx:%s,posy:%s,widthx:%s,widthy:%s'%(posx, posy, widthx, widthy))
        #c.drawImage(f, posx, posy, widthx, widthy)
        c.drawImage(f, 0, 0, 21*cm, 29*cm)
        #c.drawImage(f,posx,posy, widthx, mh)
        #c.drawImage(f, posx, posy, posx, posy)
        c.showPage()
        #c.drawImage(f, posx, posy, widthx-2*cm, widthy)
        #c.showPage()
    c.save()
    #print("Image to pdf success!")
    return

def MergePDFs(filepath,outfile='outpdf.pdf'):
    output=PdfFileWriter()
    outputPages=0
    pdf_fileName=file_name(filepath, suffix =[".pdf"])
    for each in pdf_fileName:
        print(each)
        # 读取源pdf文件
        input = PdfFileReader(open(each, "rb"))

        # 如果pdf文件已经加密，必须首先解密才能使用pyPdf
        if input.isEncrypted == True:
            input.decrypt("map")

        # 获得源pdf文件中页面总数
        pageCount = input.getNumPages()
        outputPages += pageCount
        print(pageCount)

        # 分别将page添加到输出output中
        for iPage in range(0, pageCount):
            output.addPage(input.getPage(iPage))


    print("All Pages Number:"+str(outputPages))
    # 最后写pdf文件
    outputStream=open(filepath+outfile,"wb")
    output.write(outputStream)
    outputStream.close()
    print("finished")
    return

if __name__=="__main__":
    #imgLongsplitimage2A4(sys.argv[1])
    pass
