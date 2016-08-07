# _*_ coding:utf-8 _*_
import MySQLdb as mdb
import os
import threading
import time

global IP,ID,NUMLINE
IP = None
ID = None
NUMLINE = None

def Success():
    global ID
    global IP
    conn = mdb.connect('113.59.61.225', 'dgcmdb', 'xt*bbvfhp200451', 'DGCMDB');
    cur = conn.cursor(mdb.cursors.DictCursor)
    print "%s:连接成功，开始写入数据库" % IP
    cur.execute("INSERT INTO website_serverhostrecord(hostIP_id, status_id,updateTime ) VALUES ('%s',1,now())" % ID)
    print "数据写入成功"
    cur.execute("UPDATE website_ServerHost SET status_id = 1 WHERE id = %d" % ID)
    #conn.commit()
    print "数据更新成功"
    #cur.close()
    #conn.close()
def Fail():
    global IP
    global ID
    conn = mdb.connect('113.59.61.225', 'dgcmdb', 'xt*bbvfhp200451', 'DGCMDB');
    cur = conn.cursor(mdb.cursors.DictCursor)
    print "%s:连接中断,开始写入数据库" % IP
    cur.execute("INSERT INTO website_serverhostrecord(hostIP_id, status_id,updateTime ) VALUES ('%s',2,now())" % ID)
    print "数据写入成功"
    cur.execute("UPDATE website_ServerHost SET status_id = 2 WHERE id = %d" % ID)
    #conn.commit()
    print "数据更新成功"
    #cur.close()
    #conn.close()
def conn():
    conn = mdb.connect('113.59.61.225', 'dgcmdb', 'xt*bbvfhp200451', 'DGCMDB');
    cur = conn.cursor(mdb.cursors.DictCursor)
    cur.execute("SELECT hostIP,id,status_id FROM website_serverhost")
    rows = cur.fetchall()
    numline = cur.rowcount#获取到的行数
    def sss():
        for row in rows:
            print row["hostIP"]
            data = os.system("ping -c 1 %s>/dev/null 2>&1" % row["hostIP"])
            global IP
            IP = row["hostIP"]
            global ID
            ID = row["id"]
            # print data
            if data == 0:
                t = threading(target=Success())
                t.start()
            else:
                t = threading(target=Fail())
                t.start()
            #time.sleep(1)
    ping = threading.Thread(target=sss)
    #ping.setDaemon(True)
    ping.start()


if __name__ == '__main__':
    conn()

