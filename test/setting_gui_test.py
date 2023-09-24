import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from setting_gui import SettingsWindow
import tkinter as tk


class Test:
    def __init__(self):
        self.window = tk.Tk()
        self.window.withdraw()
        self.setting()

    def setting(self):
        self.settings_window = SettingsWindow(self.window)
        self.settings_window.window.protocol(
            "WM_DELETE_WINDOW", self.on_settings_closing
        )

    def on_settings_closing(self):
        self.window.destroy()

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = Test()
    app.run()  # 运行应用
