#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Lyon Walker
# @Time    : 18/08/11 9:54


import pymysql
import contextlib
import time
from functools import wraps

sql = 'SELECT COUNT(1) tbl_chargingorder from tbl_chargingorder;'
sql2 = 'SELECT COUNT(1) tbl_chargingrecord from tbl_chargingrecord;'
sql3 = 'SELECT COUNT(1) tbl_purchasehistory from tbl_purchasehistory;'
#sql4 = "select concat(round((sum(DATA_LENGTH)+SUM(INDEX_LENGTH))/1024/1024/1024,2),'G') size from information_schema.tables where table_schema='eichong';"
sql4 = "select concat(round(sum(DATA_LENGTH)/1024/1024/1024,2),'G') data_size from information_schema.tables where table_schema='eichong';"
sql5 = "select concat(round(sum(INDEX_LENGTH)/1024/1024/1024,2),'G') index_size from information_schema.tables where table_schema='eichong';"
sql6 = 'select begin_charge_time b_time from tbl_chargingorder order by pk_ChargingOrder desc limit 1;'

#计时器
def fn_timer(function):
    @wraps(function)
    def function_timer(*args, **kwargs):
        t0 = time.time()
        result = function(*args, **kwargs)
        t1 = time.time()
        #t = int(t1-t0)
        t = float('%.2f' % (t1-t0))
        return t, result
    return function_timer


class MysqlClient:
    def __init__(self, host, port, user, passwd, db):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.db = db

    @contextlib.contextmanager
    def mysql(self):
        conn = pymysql.connect(host=self.host,
                               port=self.port,
                               user=self.user,
                               passwd=self.passwd,
                               db=self.db)
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        try:
            yield cursor
        finally:
            conn.commit()
            cursor.close()
            conn.close()

    #@fn_timer
    def exec_sql(self, sql):
        with self.mysql() as cursor:
            cursor.execute(sql)
            res = cursor.fetchall()
            return res
zk3_info = []
rdsm_info = []
rdss_info = []

my_zk3 = MysqlClient('localhost', 3306, 'root', 'aSEe201803efSE', 'eichong')
zk3_char_order = my_zk3.exec_sql(sql)
zk3_char_record = my_zk3.exec_sql(sql2)
zk3_pur_history = my_zk3.exec_sql(sql3)
zk3_data_size = my_zk3.exec_sql(sql4)
zk3_index_size = my_zk3.exec_sql(sql5)
zk3_last_order = my_zk3.exec_sql(sql6)

zk3_info.append(zk3_char_order[0]['tbl_chargingorder'])
zk3_info.append(zk3_char_record[0]['tbl_chargingrecord'])
zk3_info.append(zk3_pur_history[0]['tbl_purchasehistory'])
zk3_info.append(zk3_data_size[0]['data_size'])
zk3_info.append(zk3_index_size[0]['index_size'])
zk3_info.append(zk3_last_order[0]['b_time'])


my_rds_m = MysqlClient('rm-uf6426u9v92z31yjpo.mysql.rds.aliyuncs.com', 3306, 'aichong', 'aichong123', 'eichong')
rdsm_char_order = my_rds_m.exec_sql(sql)
rdsm_char_record = my_rds_m.exec_sql(sql2)
rdsm_pur_history = my_rds_m.exec_sql(sql3)
rdsm_data_size = my_rds_m.exec_sql(sql4)
rdsm_index_size = my_rds_m.exec_sql(sql5)
rdsm_last_order = my_rds_m.exec_sql(sql6)

rdsm_info.append(rdsm_char_order[0]['tbl_chargingorder'])
rdsm_info.append(rdsm_char_record[0]['tbl_chargingrecord'])
rdsm_info.append(rdsm_pur_history[0]['tbl_purchasehistory'])
rdsm_info.append(rdsm_data_size[0]['data_size'])
rdsm_info.append(rdsm_index_size[0]['index_size'])
rdsm_info.append(rdsm_last_order[0]['b_time'])

my_rds_s = MysqlClient('rr-uf6456i7652v46v19o.mysql.rds.aliyuncs.com', 3306, 'aichong', 'aichong123', 'eichong')
rdss_char_order = my_rds_s.exec_sql(sql)
rdss_char_record = my_rds_s.exec_sql(sql2)
rdss_pur_history = my_rds_s.exec_sql(sql3)
rdss_data_size = my_rds_s.exec_sql(sql4)
rdss_index_size = my_rds_s.exec_sql(sql5)
rdss_last_order = my_rds_s.exec_sql(sql6)

rdss_info.append(rdss_char_order[0]['tbl_chargingorder'])
rdss_info.append(rdss_char_record[0]['tbl_chargingrecord'])
rdss_info.append(rdss_pur_history[0]['tbl_purchasehistory'])
rdss_info.append(rdss_data_size[0]['data_size'])
rdss_info.append(rdss_index_size[0]['index_size'])
rdss_info.append(rdss_last_order[0]['b_time'])

#if (rdsm_info[1] - zk3_info[1] <= 10) and (rdsm_info[2] - zk3_info[2] <= 10) and (rdsm_info[3] - zk3_info[3]) <= 10:
#	stat1 = '健康'
#else:
#	stat1 = '异常'
#	
#if (rdss_info[1] - rdsm_info[1] <= 10) and (rdss_info[2] - rdsm_info[2] <= 10) and (rdss_info[3] - rdsm_info[3]) <= 10:
#	stat2 = '健康'
#else:
#	stat2 = '异常'
if rdsm_info[1] - zk3_info[1]:
	stat1 = '健康'
else:
	stat1 = '异常'
	
if rdss_info[1] - rdsm_info[1] <= 10:
	stat2 = '健康'
else:
	stat2 = '异常'

print(type(rdsm_info[2]))
print(zk3_info)
print(rdsm_info)
print(rdss_info)

print(stat1, stat2)
