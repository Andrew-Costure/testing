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
def step_setup01():  # 步骤函数命名不能以test_开头，否则将被识别为自动化用例
    logging.info("测试前置步骤一：初始化cmd库")
    logging.info("Setup for class with cmd")
    cmdRun = cmd.cmd()
    yield cmdRun
    logging.info("测试后置步骤：打印日志")


@allure.step("测试步骤一：执行 代码扫描测试")
def step_01_clip(cmdRun, cmdApp):
    _cmd = 'cd $pywork && cd .. && cargo clippy'
    logging.info("test_type=clippy")
    logging.info("test_cmd=" + _cmd)
    retcode, res = cmdRun.run_cmd(_cmd)
    logging.info("res=" + res)
    flag, msg = validator.validator().check(retcode, res)
    allure.dynamic.description("码仓提交信息===>%s\n" %json.dumps(commitConfig, indent=0, ensure_ascii=False)
                             + "用例结果信息===>%s\n" %msg)
    allure.dynamic.title("测试 仓库" + os.environ["repo"] + " 代码扫描 基本功能")
    logging.info("用例结果信息--->" + msg)
    assert flag, msg


@allure.step("测试步骤一：执行 单元测试")
def step_01_cargo(cmdRun, cmdApp):
    _cmd = 'cd $pywork && cd .. && cargo test '
    logging.info("test_type=cargo_test")
    logging.info("test_cmd=" + _cmd)
    retcode, res = cmdRun.run_cmd(_cmd)
    logging.info("res=" + res)
    flag, msg = validator.validator().check(retcode, res)
    allure.dynamic.description("码仓提交信息===>%s\n" %json.dumps(commitConfig, indent=0, ensure_ascii=False)
                             + "用例结果信息===>%s\n" %msg)
    allure.dynamic.title("测试 仓库" + os.environ["repo"] + " 单元测试 基本功能")
    logging.info("用例结果信息--->" + msg)
    assert flag, msg


@allure.step("测试步骤一：执行 代码覆盖率测试")
def step_01_tarpaulin(cmdRun, cmdApp):
    _cmd = 'cd $pywork && cd .. && cargo tarpaulin --ignore-tests'
    logging.info("test_type=tarpaulin")
    logging.info("test_cmd=" + _cmd)
    retcode, res = cmdRun.run_cmd(_cmd)
    logging.info("res=" + res)
    flag, msg = validator.validator().check(retcode, res)
    allure.dynamic.description("码仓提交信息===>%s\n" %json.dumps(commitConfig, indent=0, ensure_ascii=False)
                            + "用例结果信息===>%s\n" %msg)
    allure.dynamic.title("测试 仓库" + os.environ["repo"] + " 代码覆盖率 基本功能")
    logging.info("用例结果信息--->" + msg)
    assert flag, msg


@allure.step("测试步骤一：执行 微内核 测试")
def step_01_uni(cmdRun, cmdTc, archTc):
    _cmd = 'cd $pywork && make A=%s ARCH=%s' %(cmdTc, archTc)
    logging.info("test_type=unikernel")
    logging.info("test_cmd=" + _cmd)
    retcode, res = cmdRun.run_cmd(_cmd)
    logging.info("res=" + res)
    flag, msg = validator.validator().check(retcode, res)
    allure.dynamic.description("码仓提交信息===>%s\n" %json.dumps(commitConfig, indent=0, ensure_ascii=False)
                             + "用例结果信息===>%s\n" %msg)
    allure.dynamic.title("测试 仓库" + os.environ["repo"] + " 微内核 基本功能")
    logging.info("用例结果信息--->" + msg)
    assert flag, msg


@allure.step("测试步骤一：执行 宏内核测试")
def step_01_mono(cmdRun, cmdTc, archTc):
    _cmd = 'cd $pywork && make disk_img && make test_monolithic ARCH=%s' %archTc
    logging.info("test_type=monokernel")
    logging.info("test_cmd=" + _cmd)
    retcode, res = cmdRun.run_cmd(_cmd)
    logging.info("res=" + res)
    flag, msg = validator.validator().check(retcode, res)
    allure.dynamic.description("码仓提交信息===>%s\n" %json.dumps(commitConfig, indent=0, ensure_ascii=False)
                             + "用例结果信息===>%s\n" %msg)
    allure.dynamic.title("测试 仓库" + os.environ["repo"] + " 宏内核 基本功能")
    logging.info("用例结果信息--->" + msg)
    assert flag, msg


@allure.feature("特性（对应敏捷开发中的feature）")
@allure.issue(url="",name="用例对应issuer的链接，若没有可删除此行")
@allure.link(url="",name="用例对应需求的链接，若没有，可删除此行")
@allure.story("故事（对应敏捷开发中的story)")
@allure.severity('用例的级别，一般常用的级别为：blocker（阻塞缺陷），critical（严重缺陷），normal（一般缺陷），minor次要缺陷，trivial（轻微缺陷）')
@allure.title("测试 宏内核 基本功能")
@allure.description("测试用例简要描述: %s" %json.dumps(commitConfig, indent=0, ensure_ascii=False))
@pytest.mark.mainrepo
@pytest.mark.parametrize("monoTcList", monoTcList)
@pytest.mark.parametrize("archTcList", archTcList)
def test_arceos_monokernel(cmdRun, monoTcList, archTcList):
    """测试内核实时性指标"""
    kpi = step_01_mono(cmdRun, monoTcList, archTcList)


@allure.feature("特性（对应敏捷开发中的feature）")
@allure.issue(url="",name="用例对应issuer的链接，若没有可删除此行")
@allure.link(url="",name="用例对应需求的链接，若没有，可删除此行")
@allure.story("故事（对应敏捷开发中的story)")
@allure.severity('用例的级别，一般常用的级别为：blocker（阻塞缺陷），critical（严重缺陷），normal（一般缺陷），minor次要缺陷，trivial（轻微缺陷）')
@allure.title("测试 微内核 基本功能")
@allure.description("测试用例简要描述")
@pytest.mark.mainrepo
@pytest.mark.parametrize("uniCmdList", uniCmdList)
@pytest.mark.parametrize("archTcList", archTcList)
def test_arceos_unikernel(cmdRun, uniCmdList, archTcList):
    """测试内核实时性指标"""
    kpi = step_01_uni(cmdRun, uniCmdList, archTcList)


@allure.feature("特性（对应敏捷开发中的feature）")
@allure.issue(url="",name="用例对应issuer的链接，若没有可删除此行")
@allure.link(url="",name="用例对应需求的链接，若没有，可删除此行")
@allure.story("故事（对应敏捷开发中的story)")
@allure.severity('用例的级别，一般常用的级别为：blocker（阻塞缺陷），critical（严重缺陷），normal（一般缺陷），minor次要缺陷，trivial（轻微缺陷）')
@allure.title("测试 代码扫描 基本功能")
@allure.description("测试用例简要描述")
@pytest.mark.mainrepo
@pytest.mark.childrepo
@pytest.mark.parametrize("clippyCmdList", clippyCmdList)
def test_arceos_clippy(cmdRun, clippyCmdList):
    """测试内核实时性指标"""
    kpi = step_01_clip(cmdRun, clippyCmdList)


@allure.feature("特性（对应敏捷开发中的feature）")
@allure.issue(url="",name="用例对应issuer的链接，若没有可删除此行")
@allure.link(url="",name="用例对应需求的链接，若没有，可删除此行")
@allure.story("故事（对应敏捷开发中的story)")
@allure.severity('用例的级别，一般常用的级别为：blocker（阻塞缺陷），critical（严重缺陷），normal（一般缺陷），minor次要缺陷，trivial（轻微缺陷）')
@allure.title("测试 单元测试 基本功能")
@allure.description("测试用例简要描述")
@pytest.mark.mainrepo
@pytest.mark.childrepo
@pytest.mark.parametrize("cargoCmdList", cargoCmdList)
def test_arceos_cargo(cmdRun, cargoCmdList):
    """测试内核实时性指标"""
    kpi = step_01_cargo(cmdRun, cargoCmdList)


@allure.feature("特性（对应敏捷开发中的feature）")
@allure.issue(url="",name="用例对应issuer的链接，若没有可删除此行")
@allure.link(url="",name="用例对应需求的链接，若没有，可删除此行")
@allure.story("故事（对应敏捷开发中的story)")
@allure.severity('用例的级别，一般常用的级别为：blocker（阻塞缺陷），critical（严重缺陷），normal（一般缺陷），minor次要缺陷，trivial（轻微缺陷）')
@allure.title("测试 代码覆盖率 基本功能")
@allure.description("测试用例简要描述: %s" %json.dumps(commitConfig, indent=0, ensure_ascii=False))
@pytest.mark.mainrepo
@pytest.mark.childrepo
@pytest.mark.parametrize("tarpaulinCmdList", tarpaulinCmdList)
def test_arceos_tarpaulin(cmdRun, tarpaulinCmdList):
    """测试内核实时性指标"""
    kpi = step_01_tarpaulin(cmdRun, tarpaulinCmdList)


if __name__ == '__main__':
    pytest.main(['-sv', '--alluredir', 'report/result', 'testcase/test_arceos.py', '--clean-alluredir'])
