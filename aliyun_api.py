import io
import os
import json

import requests
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest


class AliyunAPI:
    def __init__(self):
        # 读取json配置文件内容，进行判断
        user_dir = os.path.expanduser("~")
        load_path = os.path.join(user_dir, "AliSpeak", "settings.json")
        with open(load_path) as f:
            config = json.load(f)
        self.API_KEY = config["access_key_id"]
        self.API_SECRET = config["access_key_secret"]
        self.APPKEY = config["appkey"]
        self.FILE_ADDRESS = config["download_url"]
        self.API_URL = "https://nls-gateway.aliyuncs.com/stream/v1/tts"
        # self.API_URL = "https://nls-gateway.aliyuncs.com/rest/v1/tts/async"
        self.client = AcsClient(self.API_KEY, self.API_SECRET, "cn-shanghai")

    def convert_text_to_speech(self, text, speed, voice):
        token = self.get_access_token()
        headers = {
            "Content-Type": "application/json",
        }
        data = {
            "text": text,
            "token": token,
            "appkey": self.APPKEY,
            "format": "mp3",
            "speech_rate": speed * 10,
            "voice": voice,
        }
        response = requests.post(self.API_URL, headers=headers, json=data)

        if response.status_code == 200:
            return response.content
        else:
            raise Exception(
                f"网络请求失败，状态码：{response.json()['status']}，错误信息：{response.json()['message']}"
            )

    def get_access_token(self):
        request = CommonRequest()
        request.set_accept_format("json")
        request.set_domain("nls-meta.cn-shanghai.aliyuncs.com")
        request.set_method("POST")
        request.set_protocol_type("https")
        request.set_version("2019-02-28")
        request.set_action_name("CreateToken")
        response = self.client.do_action_with_exception(request)
        response = json.loads(response)
        try:
            return response["Token"]["Id"]
        except Exception as e:
            return e
