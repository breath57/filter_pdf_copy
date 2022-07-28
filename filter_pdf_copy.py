import os
from threading import Thread
import time
import keyboard
import pyperclip


def strQ2B(ustring):
    """全角转半角"""
    rstring = ""
    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code == 12288:  # 全角空格直接转换
            inside_code = 32
        elif (inside_code >= 65281 and inside_code <= 65374):  # 全角字符（除空格）根据关系转化
            inside_code -= 65248

        rstring += chr(inside_code)
    return rstring


class FormatClipboard(Thread):
    mode = True

    # 自定义处理函数
    def reFormat(self, content=""):
        # 全角转半角
        content = strQ2B(content)
        # 此处 去除换行
        content = content.replace('\n', '')
        content = content.replace('\r', '')
        # content = content.replace(' ', '')
        # 去除前后空格
        content = content.strip()
        print("new cnt: ", content)
        return content

    def __init__(self):
        Thread.__init__(self)

    def run(self):
        while True:
            # time.sleep(0.3)
            # 根据模式更改剪切板里的内容
            keyboard.add_hotkey('ctrl+c', self.dealWith)
            keyboard.add_hotkey('ctrl+x', self.dealWith)
            keyboard.wait()

    def dealWith(self):

        if self.mode is True:
            # 获取剪切板中的内容
            time.sleep(0.3)
            cpy_content = pyperclip.paste()
            if cpy_content == '':  # 修复BUG:复制内容为文件 导致 复制失效
                return
            # print("当前内容: ", cpy_content)
            new_content = cpy_content
            new_content = self.reFormat(cpy_content)
            pyperclip.copy(new_content)
            # 去除换行
            # print("最终内容: ", new_content)

    def switchMode(self):
        if self.mode is True:
            self.mode = False
        else:
            self.mode = True

    def showCurrentModeWindow(self):
        # 目前由bug
        print(f'当前为: {"打开状态" if self.mode else "关闭状态"}')
        return
        # messagebox.showinfo('FormatClipBoard',
        #                     f'当前为: {"打开状态" if self.mode else "关闭状态"}')


class KeyMonitor(Thread):
    """ 监听快捷键 """

    def __init__(self, t: FormatClipboard):
        Thread.__init__(self)
        self.t = t

    def switchEvent(self):
        self.t.switchMode()  # 切换模式
        self.t.showCurrentModeWindow()  # 显示窗口

    def run(self):
        while True:
            keyboard.add_hotkey('f7', self.switchEvent)
            keyboard.add_hotkey('ctrl+f7', self._exit)
            keyboard.wait()  # 监听并阻塞

    def _exit(self):
        os._exit(0)


print(
    """
=============Filter PDF Copy=============

欢迎加入QQ群：451316705

功能：对PDF内容，网页内容的复制，可自动过滤冗余换行符，并自动全角转半角

程序说明：该程序有两个状态
    1. 打开状态：开启程序的功能
    2. 关闭状态：暂时关闭程序的功能

切换状态：按 F7 键（在任何界面下均可使用）

如需退出程序，直接关闭窗口即可

当前状态为：打开状态
""")
# print('当前程序为，按 F7 键 可以暂时关闭该模式')
t = FormatClipboard()
km = KeyMonitor(t)
km.start()
t.start()
