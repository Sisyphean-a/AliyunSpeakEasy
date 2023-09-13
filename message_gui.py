import tkinter as tk
import time
import threading
import asyncio

class MessageToplevel:

    def __init__(self, text, sleepTime):
        self.window = tk.Tk()
        self.window.title("消息提醒")
        self.text = text
        self.window.geometry("300x250")

        # 添加文本
        self.label = tk.Label(self.window, text = self.text)
        self.label.pack()

        # 绑定关闭事件
        # self.window.protocol("WM_DELETE_WINDOW", self.on_close)
        self.window.after(sleepTime, self.window.destroy())

        self.window.mainloop()



if __name__ == "__main__":
    message = MessageToplevel("请等待...",3000)
