from enum import Enum
import os
from threading import Thread
import time
import keyboard
import pyperclip
from utils import *

class SignModeEnum(Enum): 
        AUTO = (0, "自动识别处理（包含中文，统一转换为中文符号，否则转换为英文符号）")
        ENGLISH = (1, "英文符号（自动修正所有符号为英文符号）")
        CHINESE = (2, "中文符号（自动修正所有符号为中文符号）")

        def __init__(self, code:int, desc: str) -> None:
            self._code = code; self._desc = desc

        @property
        def code(self):
            return self._code
        
        @property
        def desc(self):
            return self._desc

        @classmethod
        def codeOf(cls, code:int):
            for e in cls:
                if e.value[0] == code:
                    return e
        
        @classmethod
        def counts(cls):
            return len(cls.__members__)


class FormatClipboard(Thread):
    """ 监听并处理剪切板内容 """

    def __init__(self):
        self.open_status = True # True 程序开启状态，False 程序关闭状态
        self.sign_mode: SignModeEnum = SignModeEnum.AUTO # 符号模式
        # 剪切板旧的内容
        self.old_content = pyperclip.paste()
        Thread.__init__(self)

    # 自定义处理函数
    def re_format(self, content: str="") -> str:
        """ 核心处理函数
        @param content: 剪切板的内容
        @return: 处理后的文本
        """
        # 全角转半角
        content = strQ2B(
                content=content, 
                is_transfer_chinese_signs=is_all_english(content=content)
            )
        # 换行替换为空格
        content = line_break_2_whitespace(content)
        
        # 去掉都去的空白字符
        content = filter_duplicate_blank(content)

        # 符号规则统一
        content = self.unify_sign(content)
        
        # 去除前后空格
        content = content.strip()
        # print("New Content: ", content)
        return content

    def unify_sign(self, content: str):
        """ 根据符号模式统计符号"""
        if self.sign_mode is SignModeEnum.CHINESE:
            content = sign_E_trans_to_C(content)
        elif self.sign_mode is SignModeEnum.ENGLISH:
            content = sign_C_trans_to_E(content)
        else:
            if is_contains_chinese(content, ignore_sign=True):
                content = sign_E_trans_to_C(content)
            else:
                content = sign_C_trans_to_E(content)
        return content

    def run(self):
        while True:
            # time.sleep(0.2)
            # 根据模式更改剪切板里的内容
            # keyboard.add_hotkey('ctrl+c', self.dealWith)
            # keyboard.add_hotkey('ctrl+x', self.dealWith)
            # keyboard.wait()
            time.sleep(0.5) # 检测周期
            self.deal_with() # 开始处理

    def deal_with(self):

        if self.open_status is True:
            # 获取剪切板中的内容
            cpy_content = pyperclip.paste()
            # 判断是否是旧内容
            if cpy_content == self.old_content:
                return
            if cpy_content == '':  # 修复BUG:复制内容为文件 导致 复制失效
                return
            # print("当前内容: ", cpy_content)
            new_content = cpy_content
            new_content = self.re_format(cpy_content) # 核心逻辑
            pyperclip.copy(new_content)

            # 更新旧的内容
            self.old_content = new_content
            # 去除换行
            print("处理后: ", new_content)

    def switchProcessStatus(self):
        """ 切换程序的运行状态 """
        self.open_status = not self.open_status
        print(f'当前为: {"打开状态" if self.open_status else "关闭状态"}')

    def switchSignMode(self):
        """ 符号模式轮转切换 """
        self.sign_mode = SignModeEnum.codeOf(
                (self.sign_mode.code + 1) % SignModeEnum.counts()
            )
        self.old_content = None
        print(f"当前符号模式：{self.sign_mode.desc}")

    def showCurrentModeWindow(self):
        # 目前由bug
        print(f'当前为: {"打开状态" if self.open_status else "关闭状态"}')
        if self.open_status:
            print(f"当前符号模式：{self.sign_mode.desc}")
        # messagebox.showinfo('FormatClipBoard',
        #                     f'当前为: {"打开状态" if self.mode else "关闭状态"}')
class KeyMonitor(Thread):
    """ 监听快捷键 """

    def __init__(self, fc: FormatClipboard):
        Thread.__init__(self)
        self.fc:FormatClipboard = fc
        self.fc.showCurrentModeWindow()  # 显示窗口

    def switchProcessStatus(self):
        self.fc.switchProcessStatus()  # 切换模式
    
    def switchSignMode(self):
        self.fc.switchSignMode()

    def run(self):
        while True:
            keyboard.add_hotkey('f7', self.switchProcessStatus)
            keyboard.add_hotkey('ctrl+f7', self._exit)
            keyboard.add_hotkey('f8', self.switchSignMode)
            keyboard.wait()  # 监听并阻塞

    def _exit(self):
        os._exit(0)


print(
    """
=============Filter PDF Copy=============

欢迎加入QQ群：451316705

主要功能：
1. PDF内容和网页上复制的文本，可自动过滤冗余换行符。
2. 自动识别中英文，纠正全角半角。
3. 自动识别中英文内容，过滤多余的空格。
4. 复制文字 -> 复制图片 -> 复制文字，也不会出现问题。

使用说明：

程序有两个状态:
    1. 打开状态：开启程序的功能
    2. 关闭状态：暂时关闭程序的功能

程序有3种符号模式:
    1. (默认模式)自动识别处理（包含中文，统一转换为中文符号，否则转换为英文符号）
    2. 英文符号（自动修正所有符号为英文符号）
    3. 中文符号（自动修正所有符号为中文符号）
    
相关操作说明：
    切换状态：按 F7 键（在任何界面下均可使用）
    切换符号模式：按 F8 键（在任何界面下均可使用）
    退出程序: 1. Ctrl + F7; 或者 2.直接关闭窗口即可
""")
if __name__ == "__main__":
    fc = FormatClipboard()
    km = KeyMonitor(fc)
    km.start()
    fc.start()
