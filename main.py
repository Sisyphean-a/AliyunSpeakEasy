import tkinter as tk
from tkinter import ttk
from aliyun_api import AliyunAPI
from setting_gui import SettingsWindow
from pydub import AudioSegment
import io
import subprocess
from datetime import datetime
import os


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

        self.voice = ttk.Combobox(self.settings_frame,value=("xiaoyun","zhixiaobai", "qiaowei", "aiqi","aimei","sitong"),state="readonly",width=13)
        self.voice.current(0)
        self.voice.pack(pady=(10,20))

        # 语音速度标签
        self.speed_label = ttk.Label(self.settings_frame, text="语音速度:")
        self.speed_label.pack()

        # 语音速度调节滑块
        self.speed_scale = tk.Scale(
            self.settings_frame, from_=-50, to=50, resolution=5, orient=tk.HORIZONTAL,length=120
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
        self.line = ttk.Separator(self.right_frame, orient='horizontal').pack(fill='x')

        # 信息框架
        self.message_frame = ttk.Frame(self.right_frame)
        self.message_frame.pack(pady=10)

        self.message_one = ttk.Label(self.message_frame, text="输入文本以开始生成")
        self.message_one.grid(row=0, pady=10)
        self.message_two = ttk.Button(self.message_frame, text="合成后，点我播放")
        self.message_two.grid(row=3, pady=10)

        self.message_yes = ttk.Button(
            self.message_frame, text="Yes", command=lambda: self.handle_user_response("yes")
        )
        self.message_no = ttk.Button(
            self.message_frame, text="No", command=lambda: self.handle_user_response("no")
        )

        # 初始化阿里云API
        self.aliyun_api = AliyunAPI()

    def save_audio(self):
        self.yield_method = self.generate_speech_with_validation()
        next(self.yield_method)

    def generate_speech_with_validation(self):
        text = self.text_input.get("1.0", tk.END).strip()  # 获取输入的文字

        # ------------v 处理值为空的情况 v-------------
        if text == "":
            self.update_text(self.message_one, "文本不能为空！！")
            return

        API_KEY = self.aliyun_api.API_KEY
        API_SECRET = self.aliyun_api.API_SECRET
        APPKEY = self.aliyun_api.APPKEY
        if API_KEY == "" or API_SECRET == "" or APPKEY == "":
            self.update_text(self.message_one, "要先设置了才能使用")
            return

        FILE_ADDRESS = self.aliyun_api.FILE_ADDRESS
        if FILE_ADDRESS == "":
            self.update_text(self.message_one, "文本路径为空，依然要生成吗")
            self.message_yes.grid(row=1, pady=10)
            self.message_no.grid(row=2, pady=10)
            yield
        # ------------^ 处理值为空的情况 ^-------------

        self.generate_speech(text)

    def generate_speech(self,text):
        self.update_text(self.message_one, "开始生成，请耐心等待")
        now = datetime.now()
        self.date = f"{now.year}-{now.month}-{now.day}-今日特价.mp3"

        # 获取设定的语音速度
        speed = self.speed_scale.get()
        # 获取设定的发音人
        voice = self.voice.get()

        # 调用阿里云API将文字转换为语音
        audio_data = self.aliyun_api.convert_text_to_speech(text, speed,voice)
        # 将生成的语音保存为文件
        audio = AudioSegment.from_file(io.BytesIO(audio_data), format="mp3")
        audio.export(self.date, format="mp3")  # 导出为MP3格式的文件

        self.update_text(self.message_one, "语音合成完成！")
        self.update_text(self.message_two, "<" + self.date + ">")
        self.message_two.config(command=self.play_audio)

    def handle_user_response(self, event):
        if event == "yes":
            self.message_yes.grid_forget()
            self.message_no.grid_forget()
            next(self.yield_method)
        else:
            self.message_yes.grid_forget()
            self.message_no.grid_forget()
            self.open_settings()
            self.update_text(self.message_one, "重新点击合成吧")

    def update_text(self, object, new_text):
        object.config(text=new_text)
        self.window.update()

    def play_audio(self):
        file_name = self.date
        file_abs = os.getcwd()
        file_path = os.path.join(file_abs, file_name)
        subprocess.run(["start", file_path], shell=True)

    def open_settings(self):
        SettingsWindow(self.window)

    def run(self):
        self.window.mainloop()  # 开始运行应用


if __name__ == "__main__":
    app = TextToSpeechApp()
    app.run()  # 运行应用
