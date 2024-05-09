#!/usr/bin/python3
# -*- coding:utf-8 -*-

import os
import sys
import re
from unittest import case

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)
sys.path.append(BASE_DIR)


class validator:
    def __init__(self):
        pass

    def check(self, retCode, caseRes):
        if retCode != 0:
            return False, "测试失败，命令执行失败，错误信息：\n%s" %caseRes

        m1 = re.findall('( fault | error |^fail |^fail!|Segmentation fault)', caseRes, re.IGNORECASE|re.MULTILINE)
        m2 = re.findall('(pass|success)', caseRes, re.IGNORECASE|re.MULTILINE)
        m3 = re.findall('(.*not found|.*unknown operand)', caseRes, re.IGNORECASE|re.MULTILINE)
        print(m3)
        if m1:
            succCaseNum = len(m2) if m2 else 0
            return False, "测试失败，失败用例条数：%s，成功用例条数：%s，错误信息：\n%s" %(len(m1), succCaseNum, '\n'.join(m3))
        if m2:
            failCaseNum = len(m1) if m1 else 0
            return True, "测试成功，成功用例条数：%s，失败用例条数：%s，错误信息：\n%s" %(len(m2), failCaseNum, '\n'.join(m3))

        return True, "测试成功"