import os
import json
import subprocess
import tkinter as tk
from datetime import datetime
from tkinter import ttk

from aliyun_api import AliyunAPI
from setting_gui import SettingsWindow
from read_setting import readSetting


class TextToSpeechApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("文字转语音应用")  # 设置窗口标题
        self.window.resizable(False, False)
        # 屏幕的宽度和高度
        start_x = (self.window.winfo_screenwidth() - 500) // 2
        self.window.geometry(f"+{start_x}+50")

        # 创建图形用户界面元素
        self.text_input = tk.Text(self.window, height=50, width=50)  # 文本输入框
        self.text_input.pack(side=tk.LEFT, padx=10, pady=10)

        # 右侧分成两个部分
        self.right_frame = ttk.Frame(self.window)  # 右侧框架
        self.right_frame.pack(
            side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True
        )

        # 调节面板
        self.settings_frame = ttk.Frame(self.right_frame)
        self.settings_frame.pack(padx=10, pady=10)

        # 设置发言人
        self.voice_label = ttk.Label(self.settings_frame, text="发音人选择:")
        self.voice_label.pack()

        self.voice = ttk.Combobox(
            self.settings_frame,
            value=("zhixiaobai", "xiaoyun", "qiaowei", "aiqi", "aimei", "sitong"),
            state="readonly",
            width=13,
        )
        self.voice.current(0)
        self.voice.pack(pady=(10, 20))

        # 语音速度标签
        self.speed_label = ttk.Label(self.settings_frame, text="语音速度:")
        self.speed_label.pack()

        # 语音速度调节滑块
        self.speed_scale = tk.Scale(
            self.settings_frame,
            from_=-50,
            to=50,
            resolution=5,
            orient=tk.HORIZONTAL,
            length=120,
        )
        self.speed_scale.set(1.0)
        self.speed_scale.pack()

        # 设置和保存按钮居中放置
        self.buttons_frame = ttk.Frame(self.right_frame)  # 按钮框架
        self.buttons_frame.pack(padx=10, pady=10)

        self.settings_button = ttk.Button(
            self.buttons_frame, text="设置", command=self.open_settings
        )
        # 设置按钮
        self.settings_button.pack(padx=5, pady=10)

        self.save_button = ttk.Button(
            self.buttons_frame, text="生成", command=self.save_audio
        )
        # 保存按钮
        self.save_button.pack(padx=5, pady=10)

        # 分割线
        self.line = ttk.Separator(self.right_frame, orient="horizontal").pack(fill="x")

        # 信息框架
        self.message_frame = ttk.Frame(self.right_frame)
        self.message_frame.pack(pady=10)

        self.message_one = ttk.Label(self.message_frame, text="输入文本以开始生成")
        self.message_one.grid(row=0, pady=10)
        self.message_button = ttk.Button(self.message_frame, text="合成后，点我播放")
        self.message_button.grid(row=3, pady=10)

        self.message_yes = ttk.Button(
            self.message_frame,
            text="Yes",
            command=lambda: self.handle_user_response("yes"),
        )
        self.message_no = ttk.Button(
            self.message_frame,
            text="No",
            command=lambda: self.handle_user_response("no"),
        )

    # 点击生成会调用这个函数
    def save_audio(self):
        self.yield_method = self.generate_speech_with_validation()
        try:
            next(self.yield_method)
        except StopIteration:
            return

    # 语音合成之前的预备代码，获取设定值并判断空值
    def generate_speech_with_validation(self):
        text = self.text_input.get("1.0", tk.END).strip()  # 获取输入的文字
        speed = self.speed_scale.get()  # 获取设定的语音速度
        voice = self.voice.get()  # 获取设定的发音人

        # ------------v 处理值为空的情况 v-------------
        if text == "":
            self.update_text(self.message_one, "文本不能为空！！")
            return

        # 读取json配置文件内容，进行判断
        user_dir = os.path.expanduser("~")
        load_path = os.path.join(user_dir, "AliSpeak", "settings.json")
        try:
            with open(load_path) as f:
                config = json.load(f)
        except FileNotFoundError:
            self.update_text(self.message_one, "未生成配置文件\n 先设置一下吧")
            return

        # 判断参数项存不存在
        read = readSetting(load_path)
        if read.EmptyApi() == "":
            self.update_text(self.message_one, "配置不全,先设置一下吧")
            return
        else:
            API_KEY, API_SECRET, APPKEY = read.EmptyApi()
            # 初始化阿里云API
            self.aliyun_api = AliyunAPI(API_KEY, API_SECRET, APPKEY)

        # 判断文件保存地址存不存在
        if read.EmptyFile() == "":
            self.update_text(self.message_one, "文本路径为空，依然要生成吗")
            self.message_yes.grid(row=1, pady=10)
            self.message_no.grid(row=2, pady=10)
            yield
        else:
            self.FILE_ADDRESS = read.EmptyFile()
        # ------------^ 处理值为空的情况 ^-------------

        self.generate_speech(text, speed, voice)

    # 语音合成代码
    def generate_speech(self, text, speed, voice):
        self.update_text(self.message_one, "开始生成，请耐心等待")

        # 获取当前日期
        now = datetime.now()
        self.date = now.strftime("%m%d-%H%M%S")
        self.music_path = os.path.join(self.FILE_ADDRESS, f"message-{self.date}.mp3")

        # 调用阿里云API将文字转换为语音
        audio_data = self.aliyun_api.convert_text_to_speech(text, speed, voice)
        # 将生成的语音保存为文件
        with open(self.music_path, "wb") as f:
            f.write(audio_data)

        self.update_text(self.message_one, "语音合成完成！")
        self.update_text(self.message_button, f"message-{self.date}.mp3")
        self.message_button.config(command=self.play_audio)

    # 选择是或者否之后会调用的函数
    def handle_user_response(self, event):
        if event == "yes":
            self.message_yes.grid_forget()
            self.message_no.grid_forget()
            try:
                next(self.yield_method)
            except StopIteration:
                return
        else:
            self.message_yes.grid_forget()
            self.message_no.grid_forget()
            self.open_settings()
            self.update_text(self.message_one, "重新点击合成吧")

    # 消息组件更新文本内容
    def update_text(self, object, new_text):
        object.config(text=new_text)
        self.window.update()

    # 点击播放之后执行的代码
    def play_audio(self):
        # 调用默认播放器播放音乐
        subprocess.run(["start", self.music_path], shell=True)

    def open_settings(self):
        settings_window = SettingsWindow(self.window)

    def open_floder(self):
        os.startfile(self.FILE_ADDRESS)

    def run(self):
        self.window.mainloop()  # 开始运行应用


if __name__ == "__main__":
    app = TextToSpeechApp()
    app.run()  # 运行应用
