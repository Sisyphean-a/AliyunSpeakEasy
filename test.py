import tkinter as tk


def remove_label():
    root.destroy()


root = tk.Tk()

label = tk.Label(root, text="这是一个消息")
label.pack()

root.after(2000, remove_label)  # 2000 毫秒后执行删除操作

root.mainloop()
