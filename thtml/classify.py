#!/usr/bin/env python3
# -*-coding:utf-8-*-
from thtml.utilth import GFlist,GFlistv2
from thtml.Tohtml import C2html,C2htmlBase
from thtml.txt2html import txt2htmlv1,txt2html_inonefile
from os.path import isfile,isdir
from latex.tolatex import PdfFile,MainSpp,MainsAbs,Mains
import os
import util.ch2num as ut
from mswdoc.docx2txt import msdoc2text
import re
import sys
from os.path import basename,splitext
from thtml.abstract import absSPP,absAPPhtml,absTFilehtml
import shutil
def classified(lawpath='', casepath='',\
               regrex1=None,\
               search=None,startw=None,\
               exclude=None,\
               func=C2html,\
                   item1_bool=False,\
                   item2_bool=False,\
                   item0_bool=False,\
               htmlfile='htmlfile/htmlbook_output',\
               pdffile='htmlbook_Main',mtype='article',\
               num=None,pyin=False,File_num='max',\
               m1=re.compile(r'^第\w{1,3}[编|篇]'),\
               m2=re.compile(r'^第\w{1,3}章'),\
               m3=re.compile(r'^第\w{1,3}节'),\
               m4=re.compile(r'^\w{1,3}、'),\
                   index=True,res=True,\
                   p1=re.compile('【要\s*旨】'),p2=re.compile('【\w*】'),yz=True):

    """
    regrex1:re.compile('\d*'),从文件名中提取中关键字作排序用
    search:str/list,民事诉讼，将文件名中符合含有关键字的文件提取出来
    startw:re.compile('^ok')，将文件名中以特定字开头的文件提取出来
    exclude:str/list,刑事诉讼，将含有exclude的文件予以排除
    num:regrex的作用相同，主要是用于latex的文件中
    m1:html文件中的一级目录
    m2:同上，是2级目录g
    m3:同上,是3级目a
    m4:同上，是4级目录
    
    """
    clf={}
    if lawpath == '':
        lawpath=['law/sikao/law', 'law/sikao/LawDoc','law/sikao/sifa','law/sikao/spp']
    if casepath == '':
        casepath = ['law/case', 'law/caseBJ','law/casechina','law/casecicc','law/casespp','law/caseGD','law/caseshanghai','law/DXLawcase','law/gongbao','law/wx']
    
    File_tmp = GFlistv2(lawpath, research = search, startw = startw, exclude = exclude,res = res)
    try:
        clf['law'] = [ff[1] for ff in File_tmp]
    except Exception as e:
        clf['law'] = []
        pass
    
    File_tmp = GFlistv2(casepath, regrex1 = regrex1, research = search, startw = startw, exclude = exclude,res = res)
    clf['case'] = [ff[1] for ff in File_tmp]

    Final_list = []
    if len(clf['law']) > 0:
        Final_list.extend(clf['law'])
    if len(clf['case']) >0:
        Final_list.extend(clf['case'])
    if len(Final_list)>0:
        if func.__name__ in ['C2html','txt2htmlv1']:
            func(Final_list,output=htmlfile,m1=m1,m2=m2,m3=m3,index=index,py=pyin)
            pass
        elif func.__name__ in ['PdfFile']:
            func(Final_list,OutFile=pdffile,mtype=mtype,\
                 num=num,pyin=pyin,Total=File_num,\
                 item0_bool=item0_bool,\
                 item1_bool=item1_bool,item2_bool=item2_bool)
            #os.remove(pdffile+'.pdf','htmlfile/'+pdffile+'.pdf')
            pass
        else:
            print('Please input right function:','C2html','C2htmlBase','txt2htmlv1','txt2html_inonefile','PdfFile')    
 
    return
