#!/usr/bin/env python3
# -*-coding:utf-8-*-
import time
import os
import tarfile
import pickle as p
import hashlib
import sys

def md5check(fname):
    m = hashlib.md5()
    with open(fname,'rb') as fobj:
        while True:
            data = fobj.read(4096)
            if not data:
                break
            m.update(data)
            #m.update(bytes(data,encoding='utf8'))
    return m.hexdigest()


def full_backup(src_dir, dst_dir, md5file):
    par_dir, base_dir = os.path.split(src_dir.rstrip('/'))
    back_name = '%s_full_%s.tar.gz' % (base_dir, time.strftime('%Y%m%d'))
    full_name = os.path.join(dst_dir, back_name)
    md5dict = {}

    tar = tarfile.open(full_name, 'w:gz')
    tar.add(src_dir)
    tar.close()
    for path, folders, files in os.walk(src_dir):
        for fname in files:
            full_path = os.path.join(path, fname)
            md5dict[full_path] = md5check(full_path)

    with open(md5file, 'wb') as fobj:
        p.dump(md5dict, fobj)

    return

def incr_backup(src_dir, dst_dir, md5file):
    par_dir, base_dir = os.path.split(src_dir.rstrip('/'))
    back_name = '%s_incr_%s.tar.gz' % (base_dir, time.strftime('%Y%m%d'))
    full_name = os.path.join(dst_dir, back_name)
    md5new = {}

    for path, folders, files in os.walk(src_dir):
        for fname in files:
            full_path = os.path.join(path, fname)
            md5new[full_path] = md5check(full_path)

    with open(md5file,'rb') as fobj:
        md5old = p.load(fobj)
    
    with open(md5file, 'wb') as fobj:
        p.dump(md5new, fobj)

    tar = tarfile.open(full_name, 'w:gz')
    for key in md5new:
        if md5old.get(key) != md5new[key]:
            tar.add(key)
    tar.close()
    #print('tar sucess in time...')
    return 


if __name__ == '__main__':
    
    if sys.platform in ['win32']:
        src_dir = 'J:/sikao/主观题练习/'
        dst_dir = 'J:/sikao/'
        md5file = 'J:/sikao/md5.data'        

    elif sys.platform in ['linux']:
        src_dir = '/mnt/d/sikao/主观题练习/'
        dst_dir = '/media/chen/Davis/sikao/'
        md5file = '/media/chen/Davis/sikao/md5.data'
    full_backup(src_dir, dst_dir, md5file)
    """
    if time.strftime('%a') == 'Mon':
        full_backup(src_dir, dst_dir, md5file)
    else:
        incr_backup(src_dir, dst_dir, md5file)"""
    

