
## 背景
当复制PDF上面的文字，PDF的多行复制会产生冗余的换行。当复制的内容非常多，将耗费大量时间在手动删除冗余换行上，并且半角的英文字母和数字等符号在PDF上复制会变成全角符号，也需要手动重新编辑。

## 主要功能
PDF内容和网页上复制的文本，可自动过滤冗余换行符，并自动全角转半角。

## 使用介绍  
该程序有两个状态  
1. 打开状态：开启程序的功能     
2. 关闭状态：暂时关闭程序的功能

切换状态：按 F7 键（在任何界面下均可使用）

如需退出程序，直接关闭窗口即可

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
