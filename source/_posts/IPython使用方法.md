---
title: IPython使用方法
date: 2016-05-11 21:05:36
tags: [IPython]
---
## IPython的部分功能整理
#### Tab自动完成
内容补全，与linux中的功能相似
#### 内省
显示对象通用信息
```python
b = [1, 2, 3, 4, 5]
b?
b??
np.*load*? #列出NumPy命名空间中所有包含load的函数
```
b也可以是函数对象，如果函数对象后面跟两个？，就可以显示函数代码。
#### %run
执行脚本文件
```python
#执行my_work.py中的python代码
%run my_work.py
```
绝对路径和相对路径都可以使用
#### 命令行中剪贴代码
```python
%paste
#粘贴代码，一次性粘贴完

%cpaste
#粘贴代码
#可以多次粘贴
#结束时输入--即可
#--
```
#### 代码性能分析
python主要的性能分析工具是cProfile模块
```python
#执行script.py并输出各函数的执行时间
python -m cProfile script.py
#按照cumulative time排序
python -m cProfile -s cumulative script.py
%run -p -s cumulative script.py

#IPython接口, %prun用于分析语句而不是模块
%prun -l 7 -s cumulative func()
```
对于逐行分析代码性能，可以使用line_profiler库，具体参见<利用python进行数据分析>74页。

#### 魔术命令
以%为前缀的命令叫做魔术命令

|    command    |        explaination        |
|:---------------:|:----------------------------------:|
| %quickref     |显示IPython快速参考|
| %magic     |显示所有魔术命令的详细文档|
| %debug     |从最新的异常跟踪底部进入交互式调试器|
| %hist     |打印命令的输入(也可是输出)历史|
| %pdb     |在异常发生后自动进入调试器|
| %paste     |执行剪贴板中的python代码|
| %cpaste     |打开特殊提示符以便手工粘贴待执行的python代码|
| %reset     |删除交互式命名空间中全部变量/名称|
| %page object     |通过分页器打印输出object|
| %run script.py     |执行script.py中的代码|
| %prun statement     |通过cProfile执行statement，并打印分析器结果|
| %time statement     |报告statement的执行时间|
| %timeit statement    |多次执行statement输出平均时间|
| %who %who_ls %whos     |显示交互式空间中定义的变量/信息级别/冗余度|
| %xdel variable     |删除变量varibale，并尝试清除其在IPython中对象上的一切引用|

与操作系统相关的魔术命令

|    command    |        explaination        |
|:---------------:|:----------------------------------:|
|!cmd|在系统shell中执行cmd |
|output=!cmd args|执行cmd，并将stdout存放在output中|
|%alias alias_name cmd|为系统shell命令定义别名|
|%bookmark|使用IPython的目录书签系统|
|%cd directory|将directory设置为当前目录|
|%pwd|返回系统当前工作目录|
|%pushd directory|将当前目录入栈，转向目标目录|
|%popd|弹出栈顶目录，并转向该目录|
|%dirs|返回一个含有当前目录栈的列表|
|%dhist|打印目录访问历史|
|%env|以dict形式返回系统环境变量|

