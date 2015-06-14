#! /usr/bin/env python
# -*- coding:utf-8 -*-

import os

os.chdir('/home/chen.yayun/local/FlowDroid')

platforms = '/home/chen.yayun/local/sdk/platforms'

path1 = '/home/chen.yayun/local/apks/classifications/社交通信'
path2 = '/home/chen.yayun/local/results/classifications/社交通信'
files = os.listdir(path1)
for each in files:
	apkpath = path1 + '/' + each
	resultpath = path2 + '/' + each.split('.apk')[0] + '.txt'
	cmd = 'java -jar flowdroid-custom-sc.jar ' + apkpath + ' ' + platforms + ' ' + resultpath + ' ' + '--nocallbacks' 
	os.system(cmd)
