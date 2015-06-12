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
    sqlString = "select c.app_url_bin " \
                "from asec.asec_app as a, asec.asec_app_category as b, asec.asec_app_meta as c " \
                "where a.app_id = c.app_id and a.app_category_ids = b.category_id " \
                "and b.category_name = \'社交通信\' and c.app_url_bin is not null " \
                "order by a.app_id;"
    sqlString1 = "select * from asec.asec_app_category"
    cur.execute(sqlString)
    regexString = '/M00'
    count = 0
    for data in cur.fetchall():
        srcpath = u'/var/fastdfs/' + re.sub(regexString,'/data',data[0])
        despath = u'/opt/apks/社交通信'
        os.system(('cp %s %s' % (srcpath, despath)).encode('gbk'))
        # shutil.copy(srcpath, despath)
        count += 1
        print '成功复制' + str(count) + '条数据'
    conn.commit()
    cur.close()
    conn.close()

except MySQLdb.Error, e:
    print "MySql Error %d: %s" % (e.args[0], e.args[1])