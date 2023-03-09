

from enum import Enum


class TEnum(Enum):

    A = (0, "A")
    B = (1, "BA")
    C = (2, "C")

    def __init__(self, code, desc) -> None:
        self.code = code
        self.desc = desc

    @classmethod
    def codeOf(cls, code):
        for e in cls:
            if e.value[0] == code:
                return e

# print(TEnum.codeOf(0) == TEnum.A)
# print(TEnum.codeOf(1).desc)

import re
# e_signs = ':;,.!?'
# c_signs = '：；，。！？'　
# 　

e_signs = ':;,.!?[]()<>""\'\'`'
c_signs = '：；，。！？【】（）《》“”‘’·'
c2e_table = {c:e for e,c in zip(e_signs,c_signs)}
e2c_table = {e:c for e,c in zip(e_signs,c_signs)}

def escape_regex(str: str) -> str:
    """ 为了兼容正则，转义所有字符 """
    new_str = ""
    for c in str:
        new_str += f"\{c}"
    return new_str

def sign_E_trans_to_C(string: str) -> str:
    """ 将英文符号转换为中文符号；
    转换规则：(英文符号 + 空格) or (英文) -> 中文符号
    """
    if not string:
        return string
    pattern =  re.compile(rf"[{escape_regex(e_signs)}][ ]*")
    # 引号转换，“”‘’
    single_counter, double_counter = [0] * len(string), [0] * len(string)
    single_counter[0], double_counter[0] = string[0] == '\'', string[0] == '\"'
    # counter[i]，表示引号在[0:i]出现的次数
    for i in range(1, len(string)):
        c = string[i]
        if c == "\"":
            double_counter[i] = double_counter[i-1] + 1
            single_counter[i] = single_counter[i-1]
        elif c == "'":
            single_counter[i] = single_counter[i-1] + 1
            double_counter[i] = double_counter[i-1]
        else:
            single_counter[i] = single_counter[i-1]
            double_counter[i] = double_counter[i-1]

    def repl_func(match: re.Match):
        s = match.group().strip()[0]
        if s == '"':
            return "”" if double_counter[match.span()[0]] % 2 == 0 else "“"
        elif s == "'":
            return "’" if single_counter[match.span()[0]] % 2 == 0 else "‘"
        else:
            return e2c_table.get(s)
    return pattern.subn(repl_func, string)[0]

def sign_C_trans_to_E(string: str) -> str:
    """ 将英文符号转换为中文符号
    转换规则：中文符号 -> 英文符号 + 空格
    """
    pattern =  re.compile(rf"[{escape_regex(c_signs)}]")
    def repl_func(match: re.Match) -> str:
        s = match.group()
        if s in list("：；，。！？"):
            return c2e_table.get(s) + ' '
        return c2e_table.get(s)
    return pattern.subn(repl_func, string)[0]

# print(sign_C_trans_to_E("a，b，从。，。！？【】（）《》“”‘’·"))
# print(sign_E_trans_to_C("何志. 伟,  安徽，发, 可以的 :;,.!?[]()<>""\'\'`"))


print(sign_E_trans_to_C("\"\"\" \'\'\'"))