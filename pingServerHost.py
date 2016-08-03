# _*_ coding:utf-8 _*_
import MySQLdb as mdb
import sys
import os
import threading


conn = mdb.connect('113.59.61.225','dgcmdb','xt*bbvfhp200451','DGCMDB');
with conn:
    cur = conn.cursor(mdb.cursors.DictCursor)
    cur.execute("SELECT hostIP,id,status_id FROM website_serverhost")
    rows = cur.fetchall()
    #print rows["hostIP"]
    for row in rows:
        print "%s %s" % (row["id"],row["hostIP"])
        threading._sleep(3)
        data = os.system("ping -c 1 %s>/dev/null 2>&1" % row["hostIP"])
        # print data
        if data == 0:
            #print 'ip:' + ip
            print "%s:正常" % row["hostIP"]
            cur.execute("INSERT INTO testrecord(hostIP, status) VALUES ('%s',1)"% row["hsotIP"])
        #else:
            #print "%s:中断" % ip

        #ip = row[0]
        #print ip
        #id = row[1]


