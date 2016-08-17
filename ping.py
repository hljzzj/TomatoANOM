# _*_ coding:utf-8 _*_
import os,sys
import threading
import Queue
import MySQLdb as mdb
import datetime


def Success(ip):
    try:
        #print "通：%s" % ip["hostIP"]
        conn = mdb.connect('127.0.0.1', 'dgcmdb', 'Dzga@110', 'dgcmdb');
        cur = conn.cursor(mdb.cursors.DictCursor)
        cur.execute("INSERT INTO website_serverhostrecord(hostIP_id, status_id,updateTime ) VALUES ('%s',1,now())" % ip["id"])
        cur.execute("UPDATE website_serverhost SET status_id = 1,updatetime = now() WHERE id = %s" % ip["id"])
        cur.close()
    except:
        print '%s\t 运行失败,失败原因' % ip["hostIP"]
        info = sys.exc_info()
        print info[0], ":", info[1]

def Fail(ip):
    try:
        #print "不通：%s" % ip["hostIP"]
        conn = mdb.connect('127.0.0.1', 'dgcmdb', 'Dzga@110', 'dgcmdb');
        cur = conn.cursor(mdb.cursors.DictCursor)
        cur.execute("INSERT INTO website_serverhostrecord(hostIP_id, status_id,updateTime ) VALUES ('%s',2,now())" % ip["id"])
        cur.execute("UPDATE website_serverhost SET status_id = 2 WHERE id = %s" % ip["id"])
    except :
        print '%s\t 运行失败,失败原因' % ip["hostIP"]
        info = sys.exc_info()
        print info[0], ":", info[1]
def check(i, q):
    i = q.get()  # 获取Queue队列传过来的ip，队列使用队列实例queue.put(ip)传入ip，通过q.get() 获得
    try:
        data = os.system("ping -c 1 %s>/dev/null 2>&1" % i["hostIP"])
    except:
        print "执行PING命令时出错"
        info = sys.exc_info()
        print info[0], ":", info[1]
    # print "ip:%s" % ip["hostIP"]
    if data == 0:
        Success(i)
    else:
        Fail(i)

if __name__=='__main__':
    while True:
        queue = Queue.Queue()
        try:
            conn = mdb.connect('127.0.0.1', 'dgcmdb', 'Dzga@110', 'dgcmdb');
            cur = conn.cursor(mdb.cursors.DictCursor)
            cur.execute("SELECT hostIP,id,status_id FROM website_serverhost")
            rows = cur.fetchall()
            print rows
            cur.close()
        except:
            print "连接出错"
            info = sys.exc_info()
            print info[0], ":", info[1]
        print "程序开始运行%s" % datetime.datetime.now()
        threads = []
        for row in rows:
            queue.put(row)
            th = threading.Thread(target=check, args=(row, queue))
            th.start()
            threads.append(th)

        for th in threads:
            th.join()
        print "程序结束运行%s" % datetime.datetime.now()


