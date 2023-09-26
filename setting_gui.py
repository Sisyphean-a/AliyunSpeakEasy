import json
import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog


# 单例设计模式，作用是让setting窗口只会存在一个
def singleton(cls):
    cls._instance = None

    def get_instance(*args, **kwargs):
        if cls._instance is None:
            cls._instance = cls(*args, **kwargs)
        return cls._instance

    return get_instance


@singleton
class SettingsWindow:
    def __init__(self, parent):
        # 窗口初始化大小
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title("设置")
        # 设置窗口最小尺寸
        self.window.minsize(300, 330)
        x = parent.winfo_x() + 90
        y = parent.winfo_y() + 200
        self.window.geometry(f"300x260+{x}+{y}")
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

        # AccessKey ID组件
        self.access_key_id_label = ttk.Label(self.window, text="AccessKey ID:")
        self.access_key_id_label.pack()
        self.access_key_id_entry = ttk.Entry(self.window)
        self.access_key_id_entry.pack()

        # AccessKey Secret组件
        self.access_key_secret_label = ttk.Label(self.window, text="AccessKey Secret:")
        self.access_key_secret_label.pack()
        self.access_key_secret_entry = ttk.Entry(self.window)
        self.access_key_secret_entry.pack()

        # AppKey组件
        self.appkey_label = ttk.Label(self.window, text="AppKey:")
        self.appkey_label.pack()
        self.appkey_entry = ttk.Entry(self.window)
        self.appkey_entry.pack(pady=(0, 10))

        # 分割线
        self.line = ttk.Separator(self.window, orient="horizontal").pack(
            fill="x", padx=70, pady=10
        )

        # 文件下载地址组件
        self.download_url_label = ttk.Label(self.window, text="文件下载地址:")
        self.download_url_label.pack()
        self.download_url_entry = ttk.Entry(self.window)
        self.download_url_entry.pack()
        self.select_folder_button = ttk.Button(
            self.window, text="选择文件夹", command=self.select_folder
        )
        self.select_folder_button.pack(pady=(0, 10))

        # 分割线
        self.line = ttk.Separator(self.window, orient="horizontal").pack(
            fill="x", padx=70, pady=10
        )

        # 保存按钮组件
        self.save_button = ttk.Button(
            self.window, text="保存", command=self.save_settings
        )
        self.save_button.pack()

        self.load_settings()

    def load_settings(self):
        try:
            # 获取用户目录
            user_dir = os.path.expanduser("~")
            # 如果用户目录不存在目标文件夹则创建一个
            if not os.path.exists(os.path.join(user_dir, "AliSpeak")):
                os.makedirs(os.path.join(user_dir, "AliSpeak"))
            # 获取目标文件夹路径
            self.load_path = os.path.join(user_dir, "AliSpeak", "settings.json")
            with open(self.load_path, "r", encoding="utf-8") as file:
                settings = json.load(file)
                if settings:
                    self.access_key_id_entry.insert(
                        0, settings.get("access_key_id", "")
                    )
                    self.access_key_secret_entry.insert(
                        0, settings.get("access_key_secret", "")
                    )
                    self.appkey_entry.insert(0, settings.get("appkey", ""))
                    self.download_url_entry.insert(0, settings.get("download_url", ""))
        except FileNotFoundError:
            pass

    def save_settings(self):
        settings = {
            "access_key_id": self.access_key_id_entry.get(),
            "access_key_secret": self.access_key_secret_entry.get(),
            "appkey": self.appkey_entry.get(),
            "download_url": self.download_url_entry.get(),
        }
        with open(self.load_path, "w", encoding="utf-8") as file:
            json.dump(settings, file)

        self.window.destroy()

    def select_folder(self):
        # 弹出文件夹选择窗口
        path = filedialog.askdirectory(parent=self.window, master=self.window)

        # 将文件夹路径设置到输入框
        text = self.download_url_entry.get()
        if not path == "":
            self.download_url_entry.delete(0, len(text))
        self.download_url_entry.insert(0, path)

        self.window.attributes("-topmost", True)

    def on_close(self):
        self.window.destroy()
        type(self)._instance = None
