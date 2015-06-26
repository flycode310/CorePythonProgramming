#! /usr/bin/env python
# -*- coding:utf-8 -*-

import os
import string
import re

os.chdir('/home/chen.yayun/local/FlowDroid/fanqiang')
platforms = '/home/chen.yayun/local/sdk/platforms'

apksbase = '/home/chen.yayun/local/apks/fanqiang'
resultsbase = '/home/chen.yayun/local/results/fanqiang'
logbase = '/home/chen.yayun/local/logs/fanqiang'

files = os.listdir(apksbase)
isFQ = {}
for each in files:
    apkpath = apksbase + '/' + each
    resultpath = resultsbase + '/' + each.split('.apk')[0] + '.txt'
    logpath = logbase + '/' + each.split('.apk')[0] + '.log.txt'
    # cmd = 'java -jar flowdroid-custom-fq.jar ' + apkpath + ' ' + platforms + ' ' + resultpath + ' ' + '--nocallbacks > ' + logpath + ' 2>&1'
    # os.system(cmd)
    print apkpath
    info_path = resultpath.split(".txt")[0] + '.info.txt'
    call_path = resultpath.split(".txt")[0] + '.calls.txt'

    # 判断权限列表中是否存在BIND_VPN_SERVICE
    # 首先在permission列表中查找
    info_file = open(info_path)
    for i in range(5):
        info_file.next()
    perm_count = string.atoi(info_file.next())
    vpnPermIsExisted = False
    for i in range(perm_count):
        if cmp(string.strip(info_file.next()), "android.permission.BIND_VPN_SERVICE") == 0:
            vpnPermIsExisted = True
            break
    # 如果没有需要在service中寻找
    if not vpnPermIsExisted:
        for line in info_file:
            if re.match("<service", line) is not None:
                if re.search("permission.BIND_VPN_SERVICE", line) is not None:
                    vpnPermIsExisted = True
                    break
    info_file.close()

    # 判断敏感调用列表中是否存在vpnservice敏感调用
    call_list = []
    if os.path.exists(call_path):
        netcall_file = open(call_path)
        for line in netcall_file:
            call_list.append(line)
        netcall_file.close()

    netApp = False
    if vpnPermIsExisted and len(call_list) > 0:
        netApp = True
    isFQ[each] = netApp

detectResult = resultsbase + '/detect.txt'
detect_file = open(detectResult, 'w')
for key in isFQ:
    tmp = "is not"
    if isFQ[key]:
        tmp = "is"
    detect_file.write(key + " " + tmp + " fanqiang app\n")
    print key
detect_file.close()