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
    # close file
    for index in range(0, 11):
        files_list[index].close()
    cur.close()
    conn.commit()
    conn.close()


def gen_power():
    detail_list = []
    # get the source list
    sources_file = open("sources.txt")
    for line in sources_file:
        if line != '\n' and line[0] != '%':
            details = line.split(';')
            detail_list.append(details)
    sources_file.close()
    # get the sink list
    sinks_file = open("sinks.txt")
    for line in sinks_file:
        if line != '\n' and line[0] != '%':
            details = line.split(';')
            detail_list.append(details)
    sinks_file.close()
    detail_dict = {}
    for detail in detail_list:
        detail_dict[detail[0]] = detail[1:3]


    # get power form mysql
    # query the mysql
    conn = MySQLdb.Connect(host="localhost", user="root", passwd="root", db="asec", port=3306, charset='utf8')
    cur = conn.cursor()
    sql_string = "select * from asec.asec_app_statistics"
    cur.execute(sql_string)
    # get power_dict for every call without parameters
    power_dict = {}
    for item in cur.fetchall():
        call_no_para = '<' + item[0].split('(')[0] + '()>'
        power_list = []
        for i in range(1, 12):
            power_list.append(item[i])
        if call_no_para not in power_dict:
            power_dict[call_no_para] = power_list
        else:
            tmp_list = power_dict[call_no_para]
            for i in range(0, 11):
                tmp_list[i] += power_list[i]
    cur.close()
    conn.commit()
    conn.close()

    # write detail to powerconfig
    files_dir = "powerconfig/"
    files_list = []
    # open file
    for index in range(0, 11):
        files_list.append(open(files_dir + str(index + 1) + '.txt', 'w+'))
    # write file
    for call in power_dict:
        power_list = power_dict[call]
        detail_list = detail_dict[call]
        for index in range(0, 11):
            if power_list[index] != 0.0:
                line_str = call + ';' + \
                           detail_list[0].decode('utf-8') + ';' + \
                           detail_list[1].decode('utf-8') + ';' + \
                           str(power_list[index]).decode('utf-8') + '\n'

                files_list[index].write(line_str.encode('utf-8'))
    # close file
    for index in range(0, 11):
        files_list[index].close()


if __name__ == '__main__':
    # gen_ss()
    gen_power()