import os
import json


class readSetting:
    def __init__(self,load_path):
        # 读取json配置文件内容，进行判断
        with open(load_path) as f:
            config = json.load(f)
        self.API_KEY = config["access_key_id"]
        self.API_SECRET = config["access_key_secret"]
        self.APPKEY = config["appkey"]
        self.FILE_ADDRESS = config["download_url"]

    def EmptyApi(self):
        if self.API_KEY == "" or self.API_SECRET == "" or self.APPKEY == "":
            return ""
        else:
            return self.API_KEY, self.API_SECRET, self.APPKEY

    def EmptyFile(self):
        if self.FILE_ADDRESS == "":
            return ""
        else:
            return self.FILE_ADDRESS
