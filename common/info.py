#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/1/15 18:39
# @Author  : chuan.yang
# @File    : tips.py
# @Desc    : 提示信息常量


class ThCommonNoticeInfo:
    """
    software common notice information text
    """
    START_TEST = "开始测试"
    FINISH_TEST = "完成测试"
    TEST_SUCCESS = "测试成功"
    TEST_FAIL = "测试失败"
    DUT = "测试对象"
    UDP_SERVER_IS_RUNNING = "本地Udp Server已启动"
    WARN = "警告"
    ILLEGAL_IP_ADDRESS = "不合法IP地址"

class Constants:
    SIGNAL_TEST_RESULT = "signal_test_result"
    SIGNAL_INFORMATION = "signal_information"
    SIGNAL_NEXT = "next"
    SIGNAL_FINISH = "finish"
    SIGNAL_CASE_FINISH = "case_finish"
    SIGNAL_CLOSE = "close"
    RESULT_SUCCESS = "success"
    RESULT_FAIL = "fail"

class MainWindowConstants:
    QMESSAGEBOX_WARN = "警告"
    QMESSAGEBOX_WARN_CLOSE_CURRENT_MODULE = "请选择测试项目"
    QMESSAGEBOX_WARN_MODULE_NOT_EXISTED = "测试模块不存在"
    CONTENTS_TEST_CASE = "测试项目"