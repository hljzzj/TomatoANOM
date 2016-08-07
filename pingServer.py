# _*_ coding:utf-8 _*_
import os
import threading
import Queue
import MySQLdb as mdb

queue = Queue.Queue()
id = Queue.Queue()
conn = mdb.connect('113.59.61.225','dgcmdb','xt*bbvfhp200451','DGCMDB');
cur = conn.cursor(mdb.cursors.DictCursor)
cur.execute("SELECT hostIP,id,status_id FROM website_ServerHost")
rows = cur.fetchall()
numline = cur.rowcount

_thread = numline

for row in rows:

    queue.put(row)  #将IP放入队列中。函数中使用q.get(ip)获取

def check(i,q):
    while True:
        ip = q.get()    #获取Queue队列传过来的ip，队列使用队列实例queue.put(ip)传入ip，通过q.get() 获得
        print "Thread %s:Pinging %s,创建线程成功,开始扫描" %(i,ip["hostIP"])
        data = os.system("ping -c 1 %s>/dev/null 2>&1" % ip["hostIP"])
        conn = mdb.connect('113.59.61.225', 'dgcmdb', 'xt*bbvfhp200451', 'DGCMDB');
        cur = conn.cursor(mdb.cursors.DictCursor)
        #使用os.system返回值判断是否正常
        if data==0:
            print "%s:正常,开始写入数据库" %ip["hostIP"]
            #id = ip["id"]
            cur.execute("INSERT INTO website_serverhostrecord(hostIP_id, status_id,updateTime ) VALUES ('%s',1,now())" % ip["id"])
            #print "数据库写入成功"
            cur.execute("UPDATE website_ServerHost SET status_id = 1 WHERE id = %s" % ip["id"])
            # conn.commit()
            #print "数据更新成功"
        else:

            print "%s:中断,开始写入数据库" %ip["hostIP"]
            cur.execute("INSERT INTO website_serverhostrecord(hostIP_id, status_id,updateTime ) VALUES ('%s',2,now())" % ip["id"])
            #print "数据库写入成功"
            cur.execute("UPDATE website_ServerHost SET status_id = 2 WHERE id = %s" % ip["id"])
            # conn.commit()
            #print "数据更新成功"
        q.task_done()   #已完成队列中提取元组数据
for i in range(_thread):  # 线程开始工作
    run = threading.Thread(target=check, args=(i, queue))  # 创建一个threading.Thread()的实例，给它一个函数和函数的参数
    run.setDaemon(True)  # 这个True是为worker.start设置的，如果没有设置的话会挂起的，因为check是使用循环实现的
    run.start()  # 开始线程的工作


queue.join()  # 线程队列执行关闭
cur.close()
print "ping 工作已完成"