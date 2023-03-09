import re
# e_signs = ':;,.!?[]()<>""\'\'`'
 

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

# ------------

def strQ2B(content: str, is_transfer_chinese_signs: bool=True) -> str:
    """ 全角转半角
    transfer_chinese_signs: 中文符号是否需要转换

    设计原因：含有中文，一定是中文的内容，符号应该为中文的符号，符号使用中文。如果内容全为英文，那么需要将中文全角全转换为英文全角
    """
    new_content = ""
    for c in content: 
        if not is_transfer_chinese_signs and c in c_signs:
            new_content += c
            continue
        inside_code = ord(c)
        if inside_code == 12288:  # 全角空格直接转换
            inside_code = 32
        elif (inside_code >= 65281 and inside_code <= 65374):  # 全角字符（除空格）根据关系转化
            inside_code -= 65248
        new_content += chr(inside_code)
    return new_content


def is_chinese_char(char: str, ignore_sign=True) -> bool:
    assert len(char) == 1, "需传入长度为1的字符串"
    return '\u4e00' <= char <= '\u9fa5' or (not ignore_sign and char in c_signs)

def is_english_char(char: str) -> bool:
    return char.isascii()

def is_contains_chinese(content: str, ignore_sign=True) -> bool:
    for c in content:
        if is_chinese_char(c, ignore_sign):
            return True
    return False

def is_all_chinese(content: str) -> bool:
    for c in content:
        if not is_chinese_char(c):
            return False
    return True

def is_all_english(content: str) -> bool:
    for c in content:
        if not is_english_char(c):
            return False
    return True

def line_break_2_whitespace(content: str) -> str:
    """ 将换行符替换为空格 """
    return content.replace('\n', ' ').replace('\r', ' ')

def filter_blank(content: str):
    """ 删除空白字符 """
    import re
    return re.subn(r'\s', '', content)[0]

def filter_duplicate_blank(content: str) -> str:
    """ 去除多余的空白字符

    中文：后方向找到空格将其删除
    英文：后方跳过一个空格，将其后多余的删除；
    """
    j = 0
    str_list = list(content)
    while j < len(str_list):
        if is_chinese_char(str_list[j]):
            start = j + 1
            while start < len(str_list) and  str_list[start].isspace():
                str_list.pop(start)
        elif str_list[j].isascii():
            start = j + 1 # 英文字符后的第一个字符
            if start < len(str_list) and str_list[start].isspace():
                start += 1 # start 为英文后的 第二个空白符的位置
                while start < len(str_list) and str_list[start].isspace():
                    str_list.pop(start)
                # 如果为： 英文 + 空白 + 中文
                # 或者： 英文 + 空白 | 越界了，都将 空白剔除
                if start == len(str_list) or is_chinese_char(str_list[start]):
                    str_list.pop(start - 1)
        j += 1
    content =  "".join(str_list)
    # print(f'删除后：{content}')
    return content