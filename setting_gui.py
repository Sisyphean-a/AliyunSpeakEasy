import tkinter as tk
import json


class SettingsWindow:
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title("设置")
        self.window.geometry("300x250")

        self.access_key_id_label = tk.Label(self.window, text="AccessKey ID:")
        self.access_key_id_label.pack()
        self.access_key_id_entry = tk.Entry(self.window)
        self.access_key_id_entry.pack()

        self.access_key_secret_label = tk.Label(self.window, text="AccessKey Secret:")
        self.access_key_secret_label.pack()
        self.access_key_secret_entry = tk.Entry(self.window)
        self.access_key_secret_entry.pack()

        self.appkey_label = tk.Label(self.window, text="AppKey:")
        self.appkey_label.pack()
        self.appkey_entry = tk.Entry(self.window)
        self.appkey_entry.pack()

        self.download_url_label = tk.Label(self.window, text="文件下载地址:")
        self.download_url_label.pack()
        self.download_url_entry = tk.Entry(self.window)
        self.download_url_entry.pack()

        self.save_button = tk.Button(self.window, text="保存", command=self.save_settings)
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
