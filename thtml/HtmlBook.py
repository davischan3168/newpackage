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
def GenerateBookGF(path,regrex1=None,\
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
                   Spp=False,\
                   Spplit=False,\
                   rc=re.compile('(.*?案\s*（检例第\d*号）)'),\
                   p1=re.compile('【要\s*旨】'),p2=re.compile('【\w*】'),yz=True):

    """
    regrex:re.compile('\d*'),从文件名中提取中关键字作排序用
    search:str/list,民事诉讼，将文件名中符合含有关键字的文件提取出来
    startw:re.compile('^ok')，将文件名中以特定字开头的文件提取出来
    exclude:str/list,刑事诉讼，将含有exclude的文件予以排除
    num:regrex的作用相同，主要是用于latex的文件中
    m1:html文件中的一级目录
    m2:同上，是2级目录g
    m3:同上,是3级目录
    m4:同上，是4级目录
    
    """
    if func.__name__ in ['MainSpp']:
        func(path,yz=yz,mtype=mtype)
        return
    if func.__name__ in ['MainsAbs']:
        func(path,pyin=pyin,Startw=startw,mtype=mtype,regrex1=regrex1)
        return

    cc=re.compile('([，、:-》.《—_;；〈〉<>【】（）()])*\s*-')
    
    rs=[]
    if isinstance(search ,list):
        rs.extend(search)
    elif isinstance(search ,str):
        rs.append(search)

    excl=[]
    if isinstance(exclude ,list):
        excl.extend(exclude)
    elif isinstance(exclude,str):
        excl.append(exclude)    

    file_list = []
    path_list = []        
    if isinstance(path,list):
        for f in path:
            if isfile(f):
                file_list.append(f)
            elif isdir(f):
                path_list.append(f)
            
    elif isfile(path):
        file_list.append(path)
    elif isdir(path):
        path_list.append(path)
    elif path is None:
        txtpath = os.getcwd()

    else:
        print('Please in list of dir/file,or dir,file')
        sys.exit()
                   
    File_tmp = GFlist(path_list)

    for ff in File_tmp:
        file_list.append(ff[1])

    only_one = set()
    fls = []
    word = re.compile(r'[\u4e00-\u9fa5]+\d*')
    for ff in file_list:
        aa = os.path.basename(ff)
        nwd = ''.join(word.findall(aa))
        if nwd not in only_one:
            only_one.add(nwd)
            fls.append(ff)

    if len(fls) > 0:
        file_list = fls    

    temff = set()    
    if exclude is not None:
        for ff in file_list:
            for ex in excl:
                if ex in os.path.basename(ff):
                    temff.add(ff)

    File_tmp = [f for f in file_list if f not in temff]

    Final_list = {}
    for f in File_tmp:
        ff=basename(f)
        if regrex1 is not None:
            if splitext(ff)[1].lower() in ['.txt','.doc','.docx']:
                i1 = [i for i in regrex1.findall(ff) if len(i) > 0]
                i2 = [i for i in regrex1.findall(ut.ChNumToArab(ff)) if len(i) > 0]
                if len(i1) > 0:
                    num1 = int(i1[0])
                    Final_list[num1] = f
                elif len(i2) > 0:
                    num1= int(i2[0])
                    Final_list[num1] = f
        else:
            num1 = cc.sub('', ff).replace('&nbsp', '')
            Final_list[num1] = f
        
    if search is not None:
        Tem={}
        for k,v in Final_list.items():
            for rsch in rs:
                if rsch in basename(v):
                    Tem[k]=v
        if len(Tem)>0:
            Final_list=Tem
        else:
            print('没有关于 "%s" 的文件'%search)
            sys.exit()

    if startw is not None:
        dff={}
        for k,v in Final_list.items():
            if startw.match(basename(v)) is not None:
                #print('start word ...',v)
                dff[k]=v
        if len(dff)>0:
            Final_list=dff
        else:
            print('没有符合的文件')
            sys.exit()            
            
    if len(Final_list)>0:
        Final=sorted(Final_list.items(),key=lambda item:item[0],reverse=res)
        Final_files=[i[1] for i in Final]
        
        #if res:
        #    Final_files
        if func.__name__ in ['C2html','txt2htmlv1']:
            func(Final_files,output=htmlfile,m1=m1,m2=m2,m3=m3,index=index)
            pass
        elif func.__name__ in ['PdfFile']:
            func(Final_files,OutFile=pdffile,mtype=mtype,\
                 num=num,pyin=pyin,Total=File_num,\
                 item0_bool=item0_bool,\
                 item1_bool=item1_bool,item2_bool=item2_bool)
            #os.remove(pdffile+'.pdf','htmlfile/'+pdffile+'.pdf')
            pass
        else:
            print('Please input right function:','C2html','C2htmlBase','txt2htmlv1','txt2html_inonefile','PdfFile')
    if Spplit:
        shutil.rmtree(path)
    return#Final_files
###################################
def GenerateBookGFv(path,regrex1=None,\
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
                   Spp=False,\
                   Spplit=False,\
                   rc=re.compile('(.*?案\s*（检例第\d*号）)'),\
                   p1=re.compile('【要\s*旨】'),p2=re.compile('【\w*】'),yz=True):

    """
    regrex:re.compile('\d*'),从文件名中提取中关键字作排序用
    search:str/list,民事诉讼，将文件名中符合含有关键字的文件提取出来
    startw:re.compile('^ok')，将文件名中以特定字开头的文件提取出来
    exclude:str/list,刑事诉讼，将含有exclude的文件予以排除
    num:regrex的作用相同，主要是用于latex的文件中
    m1:html文件中的一级目录
    m2:同上，是2级目录g
    m3:同上,是3级目录
    m4:同上，是4级目录
    
    """
    if func.__name__ in ['MainSpp']:
        func(path,yz=yz,mtype=mtype)
        return
    if func.__name__ in ['MainsAbs']:
        func(path,pyin=pyin,Startw=startw,mtype=mtype,regrex1=regrex1)
        return

    cc=re.compile('([，、:-》.《—_;；〈〉<>【】（）()])*\s*-')
    
    Final_list = GFlistv2(path=path,regrex1=regrex1,research=search,startw=startw,exclude=exclude,res=res)

    if len(Final_list)>0:
        #print(Final_list)
        Final_files=[i[1] for i in Final_list]
        if res:
            Final_files.reverse()
        #if res:
        #    Final_files
        if func.__name__ in ['C2html','txt2htmlv1']:
            func(Final_files,output=htmlfile,m1=m1,m2=m2,m3=m3,index=index,py=pyin)
            pass
        elif func.__name__ in ['PdfFile']:
            func(Final_files,OutFile=pdffile,mtype=mtype,\
                 num=num,pyin=pyin,Total=File_num,\
                 item0_bool=item0_bool,\
                 item1_bool=item1_bool,item2_bool=item2_bool)
            #os.remove(pdffile+'.pdf','htmlfile/'+pdffile+'.pdf')
            pass
        else:
            print('Please input right function:','C2html','C2htmlBase','txt2htmlv1','txt2html_inonefile','PdfFile')
    if Spplit:
        shutil.rmtree(path)
    return
####################################################
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
if __name__=="__main__":
    #df= GenerateBookGFv(['law/gongbao/case'],startw=re.compile(r'^201[4-9]'))
    pass




