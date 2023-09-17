from aliyun_api import AliyunAPI

aliyun = AliyunAPI()

text = "今天是周一，天气挺好的。"
speed = 1
aliyun.convert_text_to_speech(text, speed)
