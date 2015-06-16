#! /usr/bin/evn python
# -*- coding:utf-8 -*-

__author__ = 'chen'

import os
import re
import MySQLdb

basedir = "/opt/results/classifications"

def insert(call_dict, apk_count):
    conn = MySQLdb.Connect(host="localhost", user="root", passwd="root", db="asec", port=3306, charset='utf8')
    cur = conn.cursor()
    for i in range(len(apk_count)):
        if apk_count[i] == 0:
            apk_count[i] = 1
    for call in call_dict:
        slist = call_dict[call]
        sqlString = "insert into asec_app_statistics values('%s',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"\
                    % (call,
                       slist[0] * 1.0 / apk_count[0],
                       slist[1] * 1.0 / apk_count[1],
                       slist[2] * 1.0 / apk_count[2],
                       slist[3] * 1.0 / apk_count[3],
                       slist[4] * 1.0 / apk_count[4],
                       slist[5] * 1.0 / apk_count[5],
                       slist[6] * 1.0 / apk_count[6],
                       slist[7] * 1.0 / apk_count[7],
                       slist[8] * 1.0 / apk_count[8],
                       slist[9] * 1.0 / apk_count[9],
                       slist[10] * 1.0 / apk_count[10])
        cur.execute(sqlString)
    conn.commit()
    cur.close()
    conn.close()

def list_dir():
    call_list = get_call_list()
    call_dict = {}
    apk_count = []
    for ele in call_list:
        slist = []
        for i in range(11):
            slist.append(0)
        call_dict[ele] = slist
    for i in range(11):
        apk_count.append(0)
    dirs = os.listdir(basedir)
    for dir in dirs:
        index = dir_map(dir)
        process_dir(basedir + '/' + dir, call_dict, apk_count, index - 1)
    insert(call_dict, apk_count)
    '''
    result_file = open("Statistics.txt", 'w')
    for call in call_dict:
        result_file.write(call)
        slist = call_dict[call]
        for s in slist:
            result_file.write(str(s) + ' ')
        result_file.write('\n')
    result_file.close()
    '''


def process_dir(dirpath, call_dict, apk_count, index):
    files = os.listdir(dirpath)
    for ele in files:
        if len(ele.split('.calls.txt')) == 2:
            apk_count[index] += 1
            process_file(dirpath + '/' + ele, call_dict, index)

def process_file(filepath, call_dict, index):
    callfile = open(filepath)
    for call in callfile:
        callstr = call.split('\n')[0]
        if callstr in call_dict:
            call_dict[callstr][index] += 1
    callfile.close()

def get_call_list():
    callfile = open("SourcesAndSinks.txt")
    call_list = []
    for line in callfile:
        if len(line.strip()) == 0 or line[0] == '%':
            continue
        if re.match("^.*<init>.*$", line) is not None:
            tmp = line.split(')>')[0].split('<')
            call_list.append(tmp[1] + '<' + tmp[2] + ')')
        else:
            call_list.append(line.split('>')[0].split('<')[1])
    callfile.close()
    return call_list

def dir_map(dir_name):
    if dir_name == "社交通信":
        return 1
    elif dir_name == "社交网络":
        return 2
    elif dir_name == "便捷生活":
        return 3
    elif dir_name == "影音视频":
        return 4
    elif dir_name == "拍摄优化":
        return 5
    elif dir_name == "主题壁纸":
        return 6
    elif dir_name == "理财购物":
        return 7
    elif dir_name == "系统工具":
        return 8
    elif dir_name == "资讯阅读":
        return 9
    elif dir_name == "旅游出行":
        return 10
    elif dir_name == "办公学习":
        return 11

if __name__ == "__main__":
    list_dir()