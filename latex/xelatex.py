#!/usr/bin/env python3
# -*-coding:utf-8-*-
import sys
import re
import os
import time
from xpinyin import  Pinyin
import subprocess
import shutil
import util.ch2num as ut
from thtml.utilth import GFlist
from mswdoc.docx2txt import msdoc2text
from thtml.abstract import (abssplit,abstract,absfile,absSPP)
p=Pinyin()
from latex.tolatex import (title,kindle,pad,end,_removef)
cnum=re.compile('(^[一二三四五六七八九十百千万零]{1,5}\W{1,2})\w{1,10}')
latexs={'article':title,'kindle':kindle,'pad':pad}
section='\section{%s}'
def Singal(InFile,\
           sec=re.compile(r'^第[一二三四五六七八九十百千万零]*[章编]'),\
           sub1=re.compile(r'^第[一二三四五六七八九十百千万零]*节'),\
           sub2=re.compile(r'[(裁判要点)(基本案情)(裁判结果)(裁判理由)(相关法条)]'),\
           sub22=re.compile(r'【\w*】'),\
           item1=re.compile('^第([一二三四五六七八九十百千万零]{1,5})条\s*\w'), pyin=False):
    path=os.path.abspath(InFile)
    dname=os.path.dirname(path)
    rpls=re.compile('[\W_#]')
    allname=os.path.splitext(os.path.basename(path))
    name=rpls.sub('',allname[0]).strip()
    if len(name)<12:
        outFile=p.get_pinyin(name)+'.tex'
    else:
        outFile=p.get_initials(name)+'.tex'
    outFile=rpls.sub('',outFile).replace('&nbsp','')
    
    if sys.platform.startswith('win'):
        rt1=dname.split('\\')
        dname='/'.join(rt1)
    outFile2=dname+'/'+outFile

    if allname[1].lower() in ['.doc','.docx']:
        text=msdoc2text(path)
        tl=text.split('\n')
        content=[i.strip() for i in tl if len(i.strip())>0]

    elif  allname[1].lower() in ['.txt']:
        try:
            f=open(InFile,'r',encoding='utf8')
            content=f.readlines()
            f.close()
        except:
            f=open(InFile,'r',encoding='gb18030')
            content=f.readlines()
            f.close()        

    cts=[]
    for li in content:
        li=li.lstrip()
        if sec.match(li):
            cts.append(r'\section{%s}'%li.strip())
        elif sub1.match(li):
            cts.append(r'\subsection{%s}'%li.strip())
        elif sub2.match(li):
            cts.append(r'\subsubsection{%s}'%li.strip())
        elif sub22.match(li):
            cts.append(r'\subsubsection{%s}'%li.strip())            
        elif item1.match(li):
            ms1=item1.match(li).group()
            li=re.sub(ms1[:-1],ms1[:-1].strip()+r'\\hspace{1em}',li)
            cts.append(li)
        else:
            li=li.strip()
            if (len(li)>0):
                cts.append(li)
                
            
    cts='\n\n'.join(cts).replace('&nbsp','')
    cts=cts.replace('#','\#').replace('&','\&').replace('$','\$').replace('|','\|').replace('_','\_')
    cts=re.sub(r'%',r'\%',cts)

    if os.path.exists(outFile2):
        tmf=os.path.splitext(outFile2)
        time.sleep(0.02)
        outFile2=tmf[0]+'_%s'%int(time.time()*10000)+tmf[1]
    fl=open(outFile2,'w',encoding='utf8')
    fl.write(section%name)
    if pyin:
        fl.write('\n\n'+r'\begin{pinyinscope}')
    fl.write('\n\n'+cts+'\n\n')
    if pyin:
        fl.write('\n\n'+r'\end{pinyinscope}')  
    fl.close()
    return outFile2
#############################    
def SingalFile(inFile,mtype='article',pyin=False,\
               sec=re.compile(r'^第[一二三四五六七八九十百千万零]*[章编]'),\
               sub1=re.compile(r'^第[一二三四五六七八九十百千万零]*节'),\
               sub2=re.compile(r'[(裁判要点)(基本案情)(裁判结果)(裁判理由)(相关法条)]'),\
               sub22=re.compile(r'【\w*】'),\
               item1=re.compile('^第([一二三四五六七八九十百千万零]{1,5})条\s*\w')):
    txt_files={}
    name=os.path.basename(inFile).split('.')[0].replace('&nbsp','')
    outFile='SignalFile.tex'
    txt_files[name]=Singal(inFile,pyin=pyin,sec=sec,sub1=sub1,sub2=sub2,sub22=sub22,item1=item1)
    fl=open(outFile,'w',encoding='utf8')
    fl.write(latexs[mtype]+'\n\n')
    if pyin:
        fl.write('\n\n'+r'\begin{pinyinscope}')

    fl.write('\input{%s}'%txt_files[name])
    
    if pyin:
        fl.write('\n\n'+r'\end{pinyinscope}')  
    fl.write(end)
    fl.close()
    os.system('xelatex -no-pdf -interaction=nonstopmode %s' %outFile)
    os.system('xelatex -interaction=nonstopmode %s' %outFile)

    for root,dirs,files in os.walk(os.getcwd()):
        for f in files:
            if os.path.splitext(f)[1] in ['.aux','.log','.out','.xdv','.tex']:
                os.remove('%s'%os.path.abspath(root+'/'+f))
                pass    

    return
#####################################
def PdfFiles(path,OutFile='Main',mtype='pad',\
            regrex1=None,pyin=False,Total='max',res=True,\
            sec=re.compile(r'^第[一二三四五六七八九十百千万零]*[章编]'),\
            sub1=re.compile(r'^第[一二三四五六七八九十百千万零]*节'),\
            sub2=re.compile(r'[(裁判要点)(基本案情)(裁判结果)(裁判理由)(相关法条)]'),\
            sub22=re.compile(r'【\w*】'),\
            item1=re.compile('^第([一二三四五六七八九十百千万零]{1,5})条\s*\w')
):            
    file_list=[]
    path_list=[]        
    if isinstance(path,list):
        for f in path:
            if isinstance(f,tuple):
                if os.path.isfile(f[1]):
                    file_list.append(f[1])
            if os.path.isfile(f):
                file_list.append(f)
            elif os.path.isdir(f):
                path_list.append(f)
            
    elif os.path.isfile(path):
        file_list.append(path)
    elif os.path.isdir(path):
        path_list.append(path)
    elif path is None:
        txtpath=os.getcwd()
        
    Tem_files_list=[]
    if len(path_list)>0:
        for path in path_list:
            for root,ds,fs in os.walk(path):
                for f in fs:
                    path=os.path.abspath(os.path.join(root,f))
                    Tem_files_list.append(path)


        
 

    if len(file_list)>0:
        for f in file_list:
            Tem_files_list.append(os.path.abspath(f))
    if len(Tem_files_list)<1:
        print('Please in list of dir/file,or dir,file')
        sys.exit()            

    txt_files={}
    for f in Tem_files_list:
        f_name=os.path.basename(f)
        if os.path.splitext(f)[1].lower() in ['.txt','.doc','.docx']:
            if regrex1 is not None:
                fnum=regrex1.findall(ut.ChNumToArab(f_name))
                if len(fnum)==0:
                    txt_files[f_name]=Singal(f,pyin=pyin,sec=sec,sub1=sub1,sub2=sub2,sub22=sub22,item1=item1)
                else:
                    txt_files[''.join(fnum).zfill(3)]=Singal(f,pyin=pyin,sec=sec,sub1=sub1,sub2=sub2,sub22=sub22,item1=item1)
            else:
                txt_files[f_name]=Singal(f,pyin=pyin,sec=sec,sub1=sub1,sub2=sub2,sub22=sub22,item1=item1)

                
    if len(txt_files)>0:
        txt_files1=sorted(txt_files.items(),key=lambda txt:txt[0],reverse=res)                    
        
    if Total=='max':
        OutFile1=OutFile+'.tex'
        fl=open(OutFile1,'w',encoding='utf8')
        fl.write(latexs[mtype]+'\n\n')        
        for ff in txt_files1:
            fl.write('\input{%s}'%ff[1])
            fl.write(r'\newpage')
            #fl.write('\n\n')
        
        fl.write(end)
        fl.close()
        os.system('xelatex -no-pdf -interaction=nonstopmode %s' %OutFile1)
        os.system('xelatex -interaction=nonstopmode %s' %OutFile1)
        _removef(OutFile1)
        ###########################3
    elif isinstance(Total,int):
        for f in txt_files1:
            txp=[txt_files1[i:i+Total] for i in range(0,len(txt_files),Total)]
            fn=1
            for ff in txp:
                OutFile1=OutFile+'_%s.tex'%str(fn).zfill(2)
                fl=open(OutFile1,'w',encoding='utf8')
                fl.write(latexs[mtype]+'\n\n')
                for f in ff:
                    fl.write('\input{%s}'%f[1])
                    fl.write(r'\newpage')
                    #fl.write('\n\n')
        
                fl.write(end)
                fl.close()
                os.system('xelatex -no-pdf -interaction=nonstopmode %s' %OutFile1)
                os.system('xelatex -interaction=nonstopmode %s' %OutFile1)
                _removef(OutFile1)
                
                fn +=1
        
    else:
        print('Total is max out int, please input the right parameter.')

    for f in txt_files1:
        #print(f[1])
        os.remove(f[1])
        pass

    return
###########################

if __name__=="__main__":
    #d=Singal_File(sys.argv[1])
    #d=Mains(sys.argv[1],num=False)
    #d=Singal_input(sys.argv[1],pyin=True)
    #MainSpp(sys.argv[1],yz=False)
    pass
