

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


@allure.step("测试步骤一：执行 代码扫描 测试")
def step_01_clip(cmdRun, cmdApp):
    _cmd = 'export PATH=$PATH:/home/runner/.cargo/bin:%s/riscv64-linux-musl-cross/bin:%s/x86_64-linux-musl-cross/bin:%s/aarch64-linux-musl-cross/bin && \
            cd %s && make A=apps/monolithic_userboot ARCH=%s %s' %(commitConfig.get("工作目录"), \
                                                 commitConfig.get("工作目录"), \
                                                 commitConfig.get("工作目录"), \
                                                 commitConfig.get("工作目录"), \
                                                 commitConfig.get("测试架构"),\
                                                 cmdApp
                                                    )
    logging.info("test_type=clippy")
    logging.info("test_cmd=" + _cmd)
    retcode, res = cmdRun.run_cmd(_cmd)
    logging.info("res=" + res)
    flag, msg = validator.validator().check(retcode, res)
    allure.dynamic.description("码仓提交信息===>%s\n" %json.dumps(commitConfig, indent=0, ensure_ascii=False)
                             + "用例结果信息===>%s\n" %msg)
    logging.info("用例结果信息--->" + msg)
    assert flag, msg


# @allure.step("测试步骤一：执行 微内核 测试")
# def step_01_uni(cmdRun, cmdApp):
#     _cmd = 'cd %s && make A=%s ARCH=%s run' %(commitConfig.get("工作目录"), \
#                                               cmdApp, \
#                                               commitConfig.get("测试架构"))
#     logging.info("test_type=unikernel")
#     logging.info("test_cmd=" + _cmd)
#     retcode, res = cmdRun.run_cmd(_cmd)
#     logging.info("res=" + res)
#     flag, msg = validator.validator().check(retcode, res)
#     allure.dynamic.description("码仓提交信息===>%s\n" %json.dumps(commitConfig, indent=0, ensure_ascii=False)
#                              + "用例结果信息===>%s\n" %msg)
#     logging.info("用例结果信息--->" + msg)
#     assert flag, msg


@allure.step("测试步骤一：执行 宏内核 测试")
def step_01_mono(cmdRun, cmdTc):
    _cmd = 'export PATH=$PATH:/home/xh/qemu-7.0.0/build:/home/runner/.cargo/bin:%s/riscv64-linux-musl-cross/bin:%s/aarch64-linux-musl-cross/bin:%s/x86_64-linux-musl-cross/bin && \
             cd %s && ./build_img.sh %s %s && sudo fuser -k 5555/tcp 5555/udp; make A=apps/monolithic_userboot ARCH=%s TC=%s APP_FEATURES=batch run' %(commitConfig.get("工作目录"), \
                                                                                      commitConfig.get("工作目录"), \
                                                                                      commitConfig.get("工作目录"), \
                                                                                      commitConfig.get("工作目录"), \
                                                                                      commitConfig.get("测试架构"), \
                                                                                      commitConfig.get("文件系统"), \
                                                                                      commitConfig.get("测试架构"), \
                                                                                      cmdTc)
    logging.info("test_type=monokernel")
    logging.info("test_cmd=" + _cmd)
    retcode, res = cmdRun.run_cmd(_cmd)
    logging.info("res=" + res)
    flag, msg = validator.validator().check(retcode, res)
    allure.dynamic.description("码仓提交信息===>%s\n" %json.dumps(commitConfig, indent=0, ensure_ascii=False)
                             + "用例结果信息===>%s\n" %msg)
    logging.info("用例结果信息--->" + msg)
    assert flag, msg


@allure.feature("特性（对应敏捷开发中的feature）")
@allure.issue(url="",name="用例对应issuer的链接，若没有可删除此行")
@allure.link(url="",name="用例对应需求的链接，若没有，可删除此行")
@allure.story("故事（对应敏捷开发中的story)")
@allure.severity('用例的级别，一般常用的级别为：blocker（阻塞缺陷），critical（严重缺陷），normal（一般缺陷），minor次要缺陷，trivial（轻微缺陷）')
@allure.title("测试ArceOS 代码扫描 基本功能")
@allure.description("测试用例简要描述")
@pytest.mark.parametrize("clippyCmdList", clippyCmdList)
@pytest.mark.repeat(1)
def test_arceos_clippy(cmdRun, clippyCmdList):
    """测试内核实时性指标"""
    kpi = step_01_clip(cmdRun, clippyCmdList)


# @pytest.mark.skip('暂不测试微内核')
# @allure.feature("特性（对应敏捷开发中的feature）")
# @allure.issue(url="",name="用例对应issuer的链接，若没有可删除此行")
# @allure.link(url="",name="用例对应需求的链接，若没有，可删除此行")
# @allure.story("故事（对应敏捷开发中的story)")
# @allure.severity('用例的级别，一般常用的级别为：blocker（阻塞缺陷），critical（严重缺陷），normal（一般缺陷），minor次要缺陷，trivial（轻微缺陷）')
# @allure.title("测试ArceOS 微内核 基本功能")
# @allure.description("测试用例简要描述")
# @pytest.mark.parametrize("uniCmdList", uniCmdList)
# @pytest.mark.repeat(1)
# def test_arceos_unikernel(cmdRun, uniCmdList):
#     """测试内核实时性指标"""
#     kpi = step_01_uni(cmdRun, uniCmdList)


@allure.feature("特性（对应敏捷开发中的feature）")
@allure.issue(url="",name="用例对应issuer的链接，若没有可删除此行")
@allure.link(url="",name="用例对应需求的链接，若没有，可删除此行")
@allure.story("故事（对应敏捷开发中的story)")
@allure.severity('用例的级别，一般常用的级别为：blocker（阻塞缺陷），critical（严重缺陷），normal（一般缺陷），minor次要缺陷，trivial（轻微缺陷）')
@allure.title("测试ArceOS 宏内核 基本功能")
@allure.description("测试用例简要描述: %s" %json.dumps(commitConfig, indent=0, ensure_ascii=False))
@pytest.mark.parametrize("monoTcList", monoTcList)
@pytest.mark.repeat(1)
def test_arceos_monokernel(cmdRun, monoTcList):
    """测试内核实时性指标"""
    kpi = step_01_mono(cmdRun, monoTcList)

if __name__ == '__main__':
    pytest.main(['-sv', '--alluredir', 'report/result', 'testcase/test_arceos.py', '--clean-alluredir'])
