#! /usr/bin/env python
# -*- coding:utf-8 -*-

import os

files = os.listdir(".");
for ele in files:
	if len(ele.split(".info.txt")) == 2:
		print ele
