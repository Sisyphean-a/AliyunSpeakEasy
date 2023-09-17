import tkinter as tk
from tkinter import ttk
import json


class SettingsWindow:
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title("设置")
        x = parent.winfo_x() + 90
        y = parent.winfo_y() + 200
        self.window.geometry(f"300x250+{x}+{y}")

        self.access_key_id_label = ttk.Label(self.window, text="AccessKey ID:")
        self.access_key_id_label.pack()
        self.access_key_id_entry = ttk.Entry(self.window)
        self.access_key_id_entry.pack()

        self.access_key_secret_label = ttk.Label(self.window, text="AccessKey Secret:")
        self.access_key_secret_label.pack()
        self.access_key_secret_entry = ttk.Entry(self.window)
        self.access_key_secret_entry.pack()

        self.appkey_label = ttk.Label(self.window, text="AppKey:")
        self.appkey_label.pack()
        self.appkey_entry = ttk.Entry(self.window)
        self.appkey_entry.pack()

        self.download_url_label = ttk.Label(self.window, text="文件下载地址:")
        self.download_url_label.pack()
        self.download_url_entry = ttk.Entry(self.window)
        self.download_url_entry.pack()

        self.save_button = ttk.Button(self.window, text="保存", command=self.save_settings)
        self.save_button.pack(pady=10)

        self.load_settings()

    def load_settings(self):
        try:
            with open("settings.json", "r") as file:
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
        with open("settings.json", "w") as file:
            json.dump(settings, file)

        self.window.destroy()
