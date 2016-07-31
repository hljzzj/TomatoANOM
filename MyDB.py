# encoding:utf-8
import MySQLdb
import sys


class DBConn:

    conn = None

    #建立和数据库系统的连接
    def connect(self):
        self.conn = MySQLdb.connect(host="113.59.61.225",port=3306,user="dgcmdb", passwd="xt*bbvfhp200451",db="DGCMDB",charset="utf8")

    #获取操作游标
    def cursor(self):
        try:
            return self.conn.cursor()
        except (AttributeError, MySQLdb.OperationalError):
            self.connect()
            return self.conn.cursor()

    def commit(self):
        return self.conn.commit()

    #关闭连接
    def close(self):
        return self.conn.close()