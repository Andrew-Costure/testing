#!/usr/bin/python3
# -*- coding:utf-8 -*-
import pymysql
import datetime
import os

cur_time=datetime.datetime.now().strftime('%Y%m%d%H%M%S')[2:]
default_Kernel_Version_Id="'6.1.54.REL.B%s'" %cur_time
default_Hardware_Platform_Id="'ICVHW204_6263_lab'"
default_Chip_Id="'BST_A1000'"
default_Sdk_Id="'BSTOS_2.3.04'"
default_Test_Tag="'Smoke'"
default_Scene_Type="'台架'"

dbConfig = {
    "host": "10.14.93.244",
    "port": 3306,
    "user": "jsptb",
    "password": "OS&jsp@23",
    "database": "Os_Testcase",
    "charset": "utf8",
    "cursorclass": pymysql.cursors.DictCursor
}

sshConfig = {
    "address": "20.7.0.62",
    "username": "root",
    "password": "bst2023",
    "default_port": "22"
}

excelConfig = {
   "workbook": "实车测试用例库_(自动化单测通过版).xlsx",
   #"workbook": "TestCasePass.xlsx",
   #"sheet": "实时性测试",
   "rtsheet": "实时性测试",
   "perfsheet": "性能测试",
   "driverfuncsheet": "驱动功能测试",
   "basicfuncsheet": "基础功能测试",
   "relisheet": "可靠性测试",
   "sheets": ["实时性测试","性能测试"],
}

clippyCmdList = [
    "cargo_clippy_%s" %datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
]

monoCmdList = [
    "apps/oscomp_%s" %datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
]

cargoCmdList = [
    "cargo_test_%s" %datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
]

tarpaulinCmdList = [
    "cargo_tarpaulin_%s" %datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
]

monoTcList = [
    # "monolithic_%s" %datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    "monolithic"
]

archTcList = [
    "riscv64",
    "x86_64",
    "aarch64"
]

uniCmdList = [
    "apps/helloworld",
    "apps/memtest",
    "apps/exception",
    "apps/display",
    "apps/task/yield",
    "apps/task/parallel",
    "apps/task/sleep",
    "apps/task/priority",
    "apps/task/tls",
    "apps/fs/shell",
    "apps/net/echoserver",
    "apps/net/httpclient",
    "apps/net/httpserver",
    "apps/net/udpserver",
    "apps/c/helloworld",
    "apps/c/memtest",
    "apps/c/sqlite3",
    "apps/c/httpclient",
    "apps/c/httpserver",
    "apps/c/udpserver",
    "apps/c/iperf",
    "apps/c/redis SMP=4"
]


lkCmdlist = [
     "rt_early_console",
     "rt_axlog2",
     "rt_axhal",
     "rt_user_stack",
     "rt_driver_block",
     "rt_driver_virtio",
     "rt_axmount",
     "rt_mutex",
     "rt_axalloc",
     "rt_page_table",
     "rt_bprm_loader",
     "rt_mm",
     "rt_fstree",
     #rt_task = "task"
     "rt_mmap",
     "rt_fileops",
     "rt_fork",
     "rt_exec",
     #rt_axtrap = "axtrap"
     "rt_macrokernel"
     #test_axmount = "axmount"
]


archTcList_test = [
    "riscv64",
    "x86_64",
]


commitConfig = {
    "仓库地址": "GIT_URL",
    "仓库名": "currentRepoName",
    "分支名": "GIT_BRANCH",
    "提交ID": "GIT_COMMIT"
}
