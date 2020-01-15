#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/1/15 18:16
# @Author  : chuan.yang
# @File    : test_process.py
# @Desc    :
import subprocess

class ThComControlDeviceTestProcess:
    def __init__(self):
        pass

    def test_ip_connection(self, url):
        num = 1
        wait = 1000
        Ping = subprocess.Popen("ping -n {} -w {} {}".format(num, wait, url),
                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        exit_code = Ping.wait()
        if exit_code != 0:
            return False
        else:
            return True