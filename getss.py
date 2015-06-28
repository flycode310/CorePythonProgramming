#! /usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'chen'

import os
import re
import MySQLdb

# query data from asec.asec_app_stastics and generate
# the configuration file for every classfication
def gen_ss():
    # get the source list
    ss_file = open("SourcesAndSinks.txt")
    sources_list = []
    for line in ss_file:
        if re.search('_SOURCE_', line):
            sources_list.append(line.split(' -> ')[0])

    # query the mysql
    conn = MySQLdb.Connect(host="localhost", user="root", passwd="root", db="asec", port=3306, charset='utf8')
    cur = conn.cursor()
    sql_string = "select * from asec.asec_app_statistics"
    cur.execute(sql_string)
    files_dir = "sourcesandsinks/"
    files_list = []
    # open file
    for index in range(0, 11):
        files_list.append(open(files_dir + str(index + 1) + '.txt', 'w+'))
    # write file
    for item in cur.fetchall():
        call_name = '<' + item[0] + '>'
        for index in range(0, 11):
            if item[index + 1] != 0.0:
                files_list[index].write(call_name)
                if call_name in sources_list:
                    files_list[index].write(' -> _SOURCE_\n')
                else:
                    files_list[index].write(' -> _SINK_\n')
                    # files_list[index].write(' ' + str(item[index+1]) + '\n')
    # close file
    for index in range(0, 11):
        files_list[index].close()
    conn.commit()
    cur.close()
    conn.close()

if __name__ == '__main__':
    gen_ss()