
## 背景
当复制PDF上面的文字，PDF的多行复制会产生冗余的换行。当复制的内容非常多，将耗费大量时间在手动删除冗余换行上，并且半角的英文字母和数字等符号在PDF上复制会变成全角符号，也需要手动重新编辑。

## 主要功能
1. PDF内容和网页上复制的文本，可自动过滤冗余换行符。
2. 自动识别中英文，纠正全角半角。
3. 自动识别中英文内容，过滤多余的空格。
4. 中间复制图片，文件等，也不会出现问题。

例如：
> 我   是a student,   and  人，此
> 刻我非常的    开心。  
> 哈哈哈
> 
处理后：
> 我是a student, and人，此刻我非常的开心。哈哈哈

## 使用介绍  
该程序有两个状态  
1. 打开状态：开启程序的功能     
2. 关闭状态：暂时关闭程序的功能

切换状态：按 F7 键（在任何界面下均可使用）

退出程序（提供两种方式）: 

1. Ctrl + F7; 
2. 直接关闭窗口；

## 使用方法
### 下载
1. 下载程序
> [点击下载程序](https://gitee.com/breath57/filter_pdf_copy/raw/master/dist/filter_pdf_copy-v1.1.exe)
1. 双击打开即可

### 自行打包
1. 拉取源码
```sh
git clone https://gitee.com/breath57/filter_pdf_copy
```
2. 进入项目
```sh
cd filter_pdf_copy
```
3. 打包
```sh
pyinstaller -F filter_pdf_copy.py
```
最终可在`dist`目录下看到`filter_pdf_copy.exe`程序
