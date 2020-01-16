#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/1/15 18:16
# @Author  : chuan.yang
# @File    : test_process.py
# @Desc    :
import subprocess
import socket
import threading
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtCore

class ThComControlDeviceTestProcess:

    def __init__(self):
        self.udp_remote_client = None
        self.udp_local_server = None
        self.com_contents = "test"
        self.udp_test_result = False
        self.local_udp_server_alive = True

    def test_ip_connection(self, url):
        num = 1
        wait = 1000
        ping = subprocess.Popen("ping -n {} -w {} {}".format(num, wait, url),
                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        exit_code = ping.wait()
        if exit_code != 0:
            return False
        else:
            return True

    def udp_send(self,host,port):
        socket.setdefaulttimeout(0.01)
        serverAddressPort = (host, port)
        self.udp_remote_client = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        result = self.udp_remote_client.sendto(self.com_contents.encode("utf-8"), serverAddressPort)
        if result > 0:
            return True
        else:
            return False



class UdpServerThread(QtCore.QThread):
    _signalInfo = pyqtSignal(str)

    def __init__(self,host,port,verify_contents):
        super(UdpServerThread, self).__init__()
        self.local_host = host
        self.local_port = port
        self.verify_contents = verify_contents
        self.local_udp_server_alive = True
        self._signalInfo.emit("thread start")

    def __del__(self):
        self.wait()


    def run(self):
        try:
            udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            udp_socket.bind((self.local_host, self.local_port))
            while self.local_udp_server_alive:
                recv_msg = udp_socket.recvfrom(1024)
                recv_msg = recv_msg[0].decode("utf-8")
                if self.verify_contents == recv_msg:
                    self._signalInfo.emit("test success")
        except BaseException as e:
            print(str(e))
            self._signalInfo.emit(str(e))

    def callback(self, msg):
        pass
if __name__ == '__main__':
    temp = ThComControlDeviceTestProcess()
    # temp.udp_server_contents_verify("127.0.0.1",11001)
    temp.udp_send("127.0.0.1",11001)
