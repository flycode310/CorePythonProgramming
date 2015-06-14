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
    sqlString = "select c.app_url_bin, b.category_name " \
                "from asec.asec_app as a, asec.asec_app_category as b, asec.asec_app_meta as c " \
                "where a.app_id = c.app_id and a.app_category_ids = b.category_id " \
                "and c.app_url_bin is not null;"
    cur.execute(sqlString)
    regexString = '/M00'
    count = 0
    for data in cur.fetchall():
        srcpath = '/var/fastdfs/' + re.sub(regexString, '/data', data[0])
        despath = 'chen.yayun:~/local/apks/tmp/' + data[1] + '/' + data[0].split('/')[4] + '.apk'
        os.system(('scp ' + srcpath + ' ' + despath).encode("utf-8"))
        count += 1
        print '成功复制第' + str(count) + '条数据到' + despath.encode("utf-8")

    conn.commit()
    cur.close()
    conn.close()

except MySQLdb.Error, e:
    print "MySql Error %d: %s" % (e.args[0], e.args[1])
