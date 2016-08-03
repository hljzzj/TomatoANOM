# _*_ coding:utf-8 _*_
import os
import threading
import Queue
import MyDB

queue = Queue.Queue()
db = MyDB.MySQL()
db.query("SELECT hostIP,id FROM website_ServerHost");

hostIP = db.fetchAllRows()

#hostIP = ['113.59.61.225','115.29.16.72','www.sina.com.cn']
_thread = 4
print hostIP
for ip in hostIP:
    queue.put(ip)  #将IP放入队列中。函数中使用q.get(ip)获取
def check(i,q):
    while True:
        ip = q.get()    #获取Queue队列传过来的ip，队列使用队列实例queue.put(ip)传入ip，通过q.get() 获得
        print "Thread %s:Pinging %s" %(i,ip)
        data = os.system("ping -c 1 %s>/dev/null 2>&1" % ip)

        #使用os.system返回值判断是否正常
        if data==0:
            print "%s:正常" %ip

            value = (ip,1)
            sql = """INSERT INFO testrecord(hostIP,status) VALUES(%s,%d)""" % (ip,1)
            print sql
            db.insert(sql)
        else:
            sql = "insert info website_ServerHostRecord(hostIP_id,status_id) values(%ip,'2')"
            db.insert(sql)
            print "%s:中断" %ip
        q.task_done()   #已完成队列中提取元组数据
for i in range(_thread):  # 线程开始工作
    run = threading.Thread(target=check, args=(i, queue))  # 创建一个threading.Thread()的实例，给它一个函数和函数的参数
    run.setDaemon(True)  # 这个True是为worker.start设置的，如果没有设置的话会挂起的，因为check是使用循环实现的
    run.start()  # 开始线程的工作


queue.join()  # 线程队列执行关闭
db.close()
print "ping 工作已完成"