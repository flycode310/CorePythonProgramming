#! /usr/bin/env python
# -*- coding:utf-8 -*-

import MySQLdb
import re
import shutil
import os

__author__ = 'chen'

try:
    conn = MySQLdb.connect(host='localhost', user='root', passwd='root', db='asec', port=3306, charset='utf8')
    print '连接成功'
    cur = conn.cursor()
    sqlString1 = "select category_name from asec.asec_app_category group by category_name"
    cur.execute(sqlString1)
    count = 0
    for data in cur.fetchall():
	os.mkdir(data[0])
	print u'成功创建目录 %s' % data[0]
    conn.commit()
    cur.close()
    conn.close()

except MySQLdb.Error, e:
    print "MySql Error %d: %s" % (e.args[0], e.args[1])
