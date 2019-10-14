#!/usr/bin/env python3
# -*-coding:utf-8-*-
from AI.BDAI.ocr import BD_jsonTtext
from AI.util.tpdf import imgLongsplitimage2A4

def imgLongtoText(longPicpath):
    """将一张长图切割为A4大小的数张图，并存储为一txt文件"""
    out=os.path.splitext(os.path.abspath(longPicpath))[0]+'.txt'
    d=imgLongsplitimage2A4(longPicpath)
    #d=BdOcrcrop(longPicpath)
    f=open(out,'w',encoding='utf8')
    cnts=''
    for i in d:
        d=BD_jsonTtext(i)
        cnts +=d
        #print(i)
        os.remove(i)
        time.sleep(2)
    f.write(cnts)
    f.close()
    return

def imgLongtoTextdir(dirpath):
    for root,ds,files in os.walk(dirpath):
        for f in files:
            if os.path.splitext(f)[1] in ['.jpg','.png']:
                path=os.path.join(root,f)
                imgLongtoText(path)
    return
if __name__=="__main__":
    #imgLongsplitimage2A4(sys.argv[1])
    pass
