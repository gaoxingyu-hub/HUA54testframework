# -*-coding:utf-8 -*-

# @Time    : 2020/2/5 13:46
# @File    : test_results_upload.py
# @User    : yangchuan
# @Desc    : 
from database.data_upload_task import TaskDataResultUpload
import json
import os

import frozen_dir

SETUP_DIR = frozen_dir.app_path()

if __name__ == '__main__':
    full_config_file = os.path.join(SETUP_DIR, "data", "example.json")
    with open(full_config_file, encoding='utf-8') as json_file:
        data = json.load(json_file)
        upload = TaskDataResultUpload("https://a326f99c-879d-4253-897e-29a7a1e7efd1.mock.pstmn.io/54/tptestre",data)
        upload.start()
        upload.wait(5000)
        print(upload.get_result())