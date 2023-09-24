import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from aliyun_api import AliyunAPI

aliyun = AliyunAPI(a, b, c)

text = "今天是周一，天气挺好的。"
speed = 1
print(aliyun.get_access_token())
