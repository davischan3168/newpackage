#! /usr/bin/env python3
# -*- coding:utf-8 -*-

import os,sys
import pickle,time
from unrar import rarfile
import zipfile
import tarfile
import shutil


delefile=['.ttf','.exe','.avi','.ini','.wav','.bmp','.jpg','.gif','.htm','.idx','.dat','.con','.frq','.mic','.boo','.cab','.seg','.xnx','.pag','.atc','.dic','.id','.xdf','.mp3','.log','.pai','.ind','.mpg','.conf','.xdt','.dll','.inf','.jgp']

def get_filerarinfo(rarf,mtype='dict',search=[]):
    rf=rarfile.RarFile(rarf,'r')
    listf=rf.namelist()
    name=os.path.basename(rarf)
    if mtype in ['txt']:
        with open(name+'.txt','w',encoding='utf8') as f:
            f.write('\n'.join(listf))
        return
    elif mtype in ['dict']:
        datasets={}
        for f in listf:
            name1=os.path.basename(f)
            datasets[name1]=f
        tem=[]
        for k,v in datasets.items():
            try:
                for i in search:
                    if i in k:
                        tem.append(v)
            except:
                pass
        for i in tem:
            rf.extract(i)
        return datasets

def get_filezipinfo(zipf,mtype='dict',search=[]):
    rf=zipfile.ZipFile(zipf,'r')
    listf=rf.namelist()
    name=os.path.basename(zipf)
    rf.close()
    if mtype in ['txt']:
        with open(name+'.txt','w',encoding='utf8') as f:
            f.write('\n'.join(listf))
        return
    elif mtype in ['dict']:
        datasets={}
        for f in listf:
            name1=os.path.basename(f)
            datasets[name1]=f
        tem=[]
        for k,v in datasets.items():
            try:
                for i in search:
                    if i in k:
                        tem.append(v)
            except:
                pass
        for i in tem:
            rf.extract(i)            
        return datasets    

def get_filetarinfo(rarf,mtype='dict',search=[]):
    rf=tarfile.open(rarf,'r')
    listf=rf.getnames()
    name=os.path.basename(rarf)
    rf.close()
    if mtype in ['txt']:
        with open(name+'.txt','w',encoding='utf8') as f:
            f.write('\n'.join(listf))
        return
    elif mtype in ['dict']:
        datasets={}
        for f in listf:
            name1=os.path.basename(f)
            datasets[name1]=f
        tem=[]
        for k,v in datasets.items():
            try:
                for i in search:
                    if i in k:
                        tem.append(v)
            except:
                pass
        for i in tem:
            rf.extract(i)            
        return datasets    

def get_fileisoinfo(fpath,mtype='dict',search=[]):
    cmd='sudo mount -o loop -t iso9660 %s /mnt/iso'%fpath
    os.system(cmd)
    #time.sleep(0.5)
    listf=[]
    name=os.path.basename(fpath)
    for root1,dirs1,files1 in os.walk('/mnt/iso'):
        for f1 in files1:
            name1=os.path.join(root1,f1)
            if os.path.splitext(name1)[1].lower() not in delefile:
                listf.append(name1)
    if mtype in ['txt']:
        with open(name+'.txt','w',encoding='utf8') as f:
            f.write('\n'.join(listf))
        os.system('sudo umount /mnt/iso')
        return
    elif mtype in ['dict']:
        datasets={}
        for f in listf:
            name1=os.path.basename(f)
            datasets[name1]=f
        tem=[]
        for k,v in datasets.items():
            try:
                for i in search:
                    if i in k:
                        tem.append(v)
            except:
                pass
        if not os.path.exists('extract'):
            os.mkdir('extract')
        for i in tem:
            sn=os.path.basename(i)
            shutil.copy(i,'extract/%s'%sn)
        os.system('sudo umount /mnt/iso')
        return datasets
    else:
        os.system('sudo umount /mnt/iso')
        return

def make_datasets(fpath):
    global datasets
    for root,dirs,files in os.walk(fpath):
        for f in files:
            name=os.path.join(root,f)
            named=os.path.basename(name)
            if os.path.splitext(name)[1].lower() not in delefile:
                print(named)
                datasets[named]=name
            if os.path.basename(name).lower().endswith('.iso'):
                get_fileiso(name)
            elif os.path.basename(name).lower().endswith('.zip'):
                get_filezip(name)
            elif os.path.basename(name).lower().endswith('.rar'):
                get_filerar(name)
            elif os.path.basename(name).lower().endswith('.tar'):
                get_filetar(name)                

    sorted(datasets.items(),key=lambda x:x[0],reverse=True)
    f=open('/mnt/d/booksetsqq.pkl','wb')
    pickle.dump(datasets,f)
    f.close()
    return datasets






if __name__=="__main__":
    #convertebooks(sys.argv[1])
    pass
