#!/usr/bin/env python3
# -*-coding:utf-8-*-

from AI.BDAI.ocr import BD_jsonTtext
from AI.util.tpdf import imgLongsplitimage2A4
from AI.util.pymu import pdf2png
from AI.BDAI.ocr import BD_ocrAllIn1dir,BD_jsonTtext,BD_ocr1By1dir
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal, LAParams
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed


def pdf2txt(PDF_path, TXT_path='',mtype='A'):
    if os.path.exists(TXT_path):
        if TXT_path==''
            try:
                os.remove('output_allinone.txt')
            except:
                pass
        else:
            os.remove(TXT_path) 
    with open(PDF_path, 'rb')as fp:  # 以二进制读模式打开
        praser = PDFParser(fp)  # 用文件对象来创建一个pdf文档分析器
        doc = PDFDocument()  # 创建一个PDF文档
        praser.set_document(doc)  # 连接分析器与文档对象
        doc.set_parser(praser)

        # 提供初始化密码
        # 如果没有密码 就创建一个空的字符串
        doc.initialize()

        # 检测文档是否提供txt转换，不提供就忽略
        if not doc.is_extractable:
            pass
        else:
            print('可以获取信息，为文字')
            rsrcmgr = PDFResourceManager()  # 创建PDf 资源管理器 来管理共享资源
            laparams = LAParams()  # 创建一个PDF设备对象
            device = PDFPageAggregator(rsrcmgr, laparams=laparams)
            interpreter = PDFPageInterpreter(rsrcmgr, device)  # 创建一个PDF解释器对象

            # 循环遍历列表，每次处理一个page的内容
            for page in doc.get_pages():  # doc.get_pages() 获取page列表
                interpreter.process_page(page)
                layout = device.get_result()  # 接受该页面的LTPage对象
                # 这里layout是一个LTPage对象 里面存放着 这个page解析出的各种对象 一般包括LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal 等等 想要获取文本就获得对象的text属性，
                for x in layout:
                    if isinstance(x, LTTextBoxHorizontal):
                        with open(TXT_path, 'a', encoding='UTF-8', errors='ignore') as f:
                            results = x.get_text()
                            # print(results)
                            f.write(results + '\n')
    if not os.path.exists(TXT_path):
        pdf2png(PDF_path,txt_path=TXT_path)
        BD_ocrAllIn1dir('pdf2png',mtype=mtype)
        print('pdf文件为为图片')
    return

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
