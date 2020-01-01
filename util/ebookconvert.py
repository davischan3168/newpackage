#!/usr/bin/env python3
# -*-coding:utf-8-*-

import os
import sys

def ebookconvert(pf):

    for i in ['.epub','.mobi']:
        op=os.path.split(pf)[0]+i
        name = os.path.splitext(os.path.basename(pf))[0]
        os.system('ebook-convert %s %s --title %s'%(pf,op,name))
    return

if __name__=="__main__":
    ebookconvert(sys.argv[1])
    
