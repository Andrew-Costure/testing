#!/usr/bin/python3
# -*- coding:utf-8 -*-
import pytest
import json
import allure
import os
import sys
import logging

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
logging.info(BASE_DIR)
sys.path.append(BASE_DIR)

from lib import cmd
from lib import ssh
from lib import excel
from lib import db
from lib import validator

from config import *


@allure.step("测试前置步骤一：初始化cmd库")
@pytest.fixture(scope='module', name='cmdRun', autouse=True)
def step_setup_lkmodel():  # 步骤函数命名不能以test_开头，否则将被识别为自动化用例
    logging.info("测试前置步骤一：初始化cmd库")
    logging.info("Setup for class with cmd")
    cmdRun = cmd.cmd()
    yield cmdRunii
    logging.info("测试后置步骤：打印日志")


@allure.step("测试步骤一：执行 lktool 测试")
def step_01_lk(cmdRun, archac, cmdac, repo_name):
    _cmd = 'cd $pywork && cd .. && lktool config %s && lktool chroot %s && lktool prepare && lktool run' %(archac, cmdac)
    logging.info("test_type=test")
    logging.info("test_cmd=" + _cmd)
    retcode, res = cmdRun.run_cmd(_cmd)
    logging.info("res=" + res)
    flag, msg = validator.validator().check(retcode, res)
    allure.dynamic.description("码仓提交信息===>%s\n" %json.dumps(commitConfig, indent=0, ensure_ascii=False)
                             + "用例结果信息===>%s\n" %msg)
    allure.dynamic.title("测试 仓库" + repo_name + " lktool 基本功能")
    logging.info("用例结果信息--->" + msg)
    assert flag, msg



@allure.feature("特性（对应敏捷开发中的feature）")
@allure.issue(url="",name="用例对应issuer的链接，若没有可删除此行")
@allure.link(url="",name="用例对应需求的链接，若没有，可删除此行")
@allure.story("故事（对应敏捷开发中的story)")
@allure.severity('用例的级别，一般常用的级别为：blocker（阻塞缺陷），critical（严重缺陷），normal（一般缺陷），minor次要缺陷，trivial（轻微缺陷）')
@allure.title("测试 微内核 基本功能")
@allure.description("测试用例简要描述")
@pytest.mark.mainrepo
@pytest.mark.parametrize("archTcList_test", archTcList_test)
@pytest.mark.parametrize("lkCmdlist", lkCmdlist)
def test_lkmodel_lk(cmdRun, archTcList_test, lkCmdlist):
    """测试子仓"""
    kpi = step_01_lk(cmdRun, archTcList_test, lkCmdlist, lkCmdlist)



if __name__ == '__main__':
    pytest.main(['-sv', '--alluredir', 'report/result', 'testcase/test_lkmodel.py', '--clean-alluredir'])
