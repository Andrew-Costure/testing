#!/usr/bin/python3
# -*- coding:utf-8 -*-
import pytest
import allure
import os
import sys

sys.path.append((os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))))


@pytest.fixture(scope="session", autouse=True)
def prepare_before_all_case():
    print("初始化步骤：在所有的自动化脚本之前自动执行一次")
    pass

# 添加命令行参数
def pytest_addoption(parser):
    parser.addoption(
        "--cmdrepo",
        action="store",
        # default: 默认值，命令行没有指定时，默认用该参数值
        default="ComponentStarry",
        help="test case project commit repo name"
    )

# autouse=True自动执行该前置操作
@pytest.fixture(scope="session", autouse=True)
def repo(request):
    '''获取命令行参数'''
    # 获取命令行参数给到环境变量
    os.environ["repo"] = request.config.getoption("--cmdrepo")
    print("当前用例关联的代码提交仓库:%s"%os.environ["repo"])
