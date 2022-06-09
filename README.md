# linovelib
安装：`pip install linovelib`
本项目仅供学习交流，请勿用于商业用途，软件内产生的数据请关闭软件后立即删除！！！
# 使用

```
NAME
    linovelib

SYNOPSIS
    linovelib COMMAND

COMMANDS
    COMMAND is one of the following:

     download

     info

     pic

     rec

     search

     show
```

## download
下载功能，支持输入轻小说书名、id、网址、单篇网址

```
linovelib download <id>  <book_type> <起始章节> <结束章节> <保存位置> <wait_time> <split_char> <enable_pic_download>
```
+ id 可以为书名，调用search模块
+ book_type原生支持txt和markdown，其余格式如epub均由md转换而成（pandoc）
+ 起始章节等于结束章节时，默认全部下载
+ 保存位置默认为工作原目录
+ 等待时间默认0.5秒，如果小说较长，建议设置为1秒以上
+ 分割字符为每一段之间的分隔
+ enable_pic_download 意为是否下载图片，默认开启，如果关闭，则markdown中的插图会以链接形式出现。

```
NAME
    linovelib download

SYNOPSIS
    linovelib download ID <flags>

POSITIONAL ARGUMENTS
    ID

FLAGS
    --type_book=TYPE_BOOK
        Default: 'txt'
    --begin_chapter=BEGIN_CHAPTER
        Default: 0
    --end_chapter=END_CHAPTER
        Default: 0
    --path=PATH
        Default: os.getcwd()
    --wait_time=WAIT_TIME
        Default: 0.5
    --split_char=SPLIT_CHAR
        Default: '\n'
    --enable_pic_download=ENABLE_PIC_DOWNLOAD
        Default: True
```
## pic

```
linovelib pic <id> <起始章节> <结束章节> <保存位置> <wait_time>
```
+ 只下载小说插图
+ 插图分卷放置在文件夹中

```
NAME
    linovelib pic

SYNOPSIS
    linovelib pic ID <flags>

POSITIONAL ARGUMENTS
    ID

FLAGS
    --begin_chapter=BEGIN_CHAPTER
        Default: 0
    --end_chapter=END_CHAPTER
        Default: 0
    --wait_time=WAIT_TIME
        Default: 1
    --path=PATH
        Default: os.getcwd()
```
## show

```
linovelib show <id>
```
+ 显示目录，前面会有标号，按照其中标号可以进行章节下载
## search

```
linovelib search <keyword> <num>
```
+ 搜索功能
+ num默认5条
## rec

```
 linovelib rec <type> <page>
```
+ 从排行榜中随机推荐一部轻小说
+ type指什么排行榜，page指第几页
+ type如果为r、rand或random时，为随机排行榜
+ type可为：["monthvisit","allvisit","allvote","monthvote","allflower","monthflower","lastupdate","poastdate","signtime","words","goodnum","newhot"]
## info
```
linovelib info <id>
```
+ 显示小说详细信息。
# 参考
https://github.com/ShunJieZhang1995/linovelib_parser
