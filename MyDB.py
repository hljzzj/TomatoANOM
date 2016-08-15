# _*_ coding:utf-8 _*_
import os,sys
import threading
import Queue
import MySQLdb as mdb
import datetime

conn = mdb.connect('127.0.0.1', 'dzcmdb', 'Dzga@110', 'dzcmdb');
cur = conn.cursor(mdb.cursors.DictCursor)
cur.execute("SELECT hostIP,id,status_id FROM website_ServerHostList")
rows = cur.fetchall()

cur.close()
print rows