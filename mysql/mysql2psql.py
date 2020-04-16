#!/usr/bin/env python3
# -*-coding:utf-8-*-

import sys,os,time
import re
from pypinyin import pinyin, lazy_pinyin, Style
import MySQLdb
import psycopg2
pyconn = psycopg2.connect(database="pySDD", user="root", password="801019", host="127.0.0.1", port="5432")
pycur = pyconn.cursor()
pyconn = psycopg2.connect(database="pysdd", user="postgres", password="801019", host="127.0.0.1", port="5432")
pycur = pyconn.cursor()
conn = MySQLdb.connect(host="localhost", port=3306, user='root', passwd='801019', db='SDD', charset="utf8")
cur = conn.cursor()

gushiweni = 'title,author,content,yiwen,zhus,shangxi,note'
cmd = 'select title,author,content,yiwen,zhus,shangxi,note from gushiwenI'
insert = 'insert into gushiweni(title,author,content,yiwen,zhus,shangxi,note) values(%s,%s,%s,%s,%s,%s,%s)'


cmd = 'select sset,book,charpter,content,zhushi from Guwen'
insert = 'insert into guwen(sset,book,charpter,content,zhushi) values(%s,%s,%s,%s,%s)'


cmd = 'select title,content from poem'
insert = 'insert into poem(title,content) values(%s,%s)'
cur.execute(cmd)
df=cur.fetchall()

pycur.executemany(insert,df)
pyconn.commit()

#########X1 Carbon

import pickle
import psycopg2
pyconn = psycopg2.connect(database="pysdd", user="postgres", password="801019", host="127.0.0.1", port="5432")
pycur = pyconn.cursor()

ff=open('faxin_df','rb')
df=pickle.load(ff)
ff.close()
insert = 'insert into faxin_case(abstract,anyou,laiyuan,href) values(%s,%s,%s,%s)'
pycur.executemany(insert,df)
pyconn.commit()

if __name__=="__main__":
    #Sql2Pdf(sys.argv[1])
    #Sql2html_guwen(sys.argv[1])
    Sql2html_GushiByNote(sys.argv[1])
    #Sql2html_GushiByAuthor(sys.argv[1])

