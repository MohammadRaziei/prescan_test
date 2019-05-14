# -*- coding: utf-8 -*-
"""
Created on Mon May 13 22:22:34 2019

@author: MohammadRaziei
"""
import os
port = 9620
result = os.popen("netstat -ano | findstr :{} | findstr ESTABLISHED".format(port)).read().strip()
pid = result.split(" ")[-1]
os.popen("taskkill /PID {} /F".format(pid))