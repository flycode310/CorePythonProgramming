#! /usr/bin/env python
# -*- coding:utf-8 -*-

import os
import string

os.chdir('/home/chen.yayun/local/FlowDroid/net')
platforms = '/home/chen.yayun/local/sdk/platforms'

apksbase = '/home/chen.yayun/local/apks/net'
resultsbase = '/home/chen.yayun/local/results/net'

files = os.listdir(apksbase)
isNet = {}
for each in files:
    apkpath = apksbase + '/' + each
    resultpath = resultsbase + '/' + each.split('.apk')[0] + '.txt'
    cmd = 'java -jar flowdroid-custom-net.jar ' + apkpath + ' ' + platforms + ' ' + resultpath + ' ' + '--nocallbacks'
    os.system(cmd)

    info_path = resultpath.split(".txt")[0] + '.info.txt'
    netcall_path = resultpath.split(".txt")[0] + '.calls.txt'

    # 判断权限列表中是否存在网络权限
    info_file = open(info_path)
    for i in range(5):
        info_file.next()
    perm_count = string.atoi(info_file.next())
    netPermIsExisted = False
    for i in range(perm_count):
        if cmp(string.strip(info_file.next()), "android.permission.INTERNET") == 0:
            netPermIsExisted = True
            break
    info_file.close()

    # 判断敏感调用列表中是否存在网络敏感调用
    call_list = []
    if os.path.exists(netcall_path):
        netcall_file = open(netcall_path)
        for line in netcall_file:
            call_list.append(line)
        netcall_file.close()

    netApp = False
    if netPermIsExisted and len(call_list) > 0:
        netApp = True
    isNet[each] = netApp

detectResult = resultsbase + '/detect.txt'
detect_file = open(detectResult, 'w')
for key in isNet:
    tmp = "is not"
    if isNet[key]:
        tmp = "is"
    detect_file.write(key + " " + tmp + " net app\n")
detect_file.close()