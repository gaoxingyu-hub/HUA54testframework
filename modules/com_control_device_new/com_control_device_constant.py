#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/20 10:52
# @Author  : chuan.yang
# @File    : com_control_device_constant.py
# @Desc    :
from common.info import SystemLanguage


class ModuleConstants:
    QMESSAGEBOX_WARN = "警告"
    QMESSAGEBOX_WARN_SELECTED_TEST = "请选择测试项目"
    QMESSAGEBOX_WARN_INPUT_PARAMETER_NOT_ENOUGH = "测试参数输入不完整"
    QMESSAGEBOX_WARN_IP_NOT_VALID = "输入IP地址有误"
    QMESSAGEBOX_CONTENTS_TEST_FINISH = "测试完成"
    WINDOW_TITLE_MAIN = "通信控制设备测试"
    PROCESS_CONTROL_NEXT = "next"
    PROCESS_CONTROL_FINISH = "finish"
    CONTENTS_NEXT = "下一步"
    CONTENTS_NOT = "不"
    CONTENTS_OVER = "测试结束"
    CONTENTS_YES = "是"
    CONTENTS_NO = "否"
    UDP_SEND_CONTENTS = "test"
    BUTTON_CONTENTS_NEXT = "下一步"
    BUTTON_CONTENTS_FINISH = "测试结束"

    if SystemLanguage.LANGUAGE == SystemLanguage.fr_FR:
        QMESSAGEBOX_WARN = "Alerte"
        QMESSAGEBOX_WARN_SELECTED_TEST = "Sélectionnez l’élement de test"
        QMESSAGEBOX_WARN_INPUT_PARAMETER_NOT_ENOUGH = "L’entrée des paramètres de test est imcomplète ou le format est incorrect"
        QMESSAGEBOX_WARN_IP_NOT_VALID = "Erreur d’entrée d’adresse IP"
        QMESSAGEBOX_CONTENTS_TEST_FINISH = "Achèvement de test"
        WINDOW_TITLE_MAIN = "Test de dispositif de contrôle de transmission"
        PROCESS_CONTROL_NEXT = "next"
        PROCESS_CONTROL_FINISH = "finish"
        CONTENTS_NEXT = "Étape suivante"
        CONTENTS_NOT = "a"
        CONTENTS_OVER = "Fin de test"
        CONTENTS_YES = "Oui"
        CONTENTS_NO = "Non"
        UDP_SEND_CONTENTS = "test"
        BUTTON_CONTENTS_NEXT = "Étape suivante"
        BUTTON_CONTENTS_FINISH = "Fin de test"
    else:
        QMESSAGEBOX_WARN = "警告"
        QMESSAGEBOX_WARN_SELECTED_TEST = "请选择测试项目"
        QMESSAGEBOX_WARN_INPUT_PARAMETER_NOT_ENOUGH = "测试参数输入不完整"
        QMESSAGEBOX_WARN_IP_NOT_VALID = "输入IP地址有误"
        QMESSAGEBOX_CONTENTS_TEST_FINISH = "测试完成"
        WINDOW_TITLE_MAIN = "通信控制设备测试"
        PROCESS_CONTROL_NEXT = "next"
        PROCESS_CONTROL_FINISH = "finish"
        CONTENTS_NEXT = "下一步"
        CONTENTS_NOT = "不"
        CONTENTS_OVER = "测试结束"
        CONTENTS_YES = "是"
        CONTENTS_NO = "否"
        UDP_SEND_CONTENTS = "test"
        BUTTON_CONTENTS_NEXT = "下一步"
        BUTTON_CONTENTS_FINISH = "测试结束"