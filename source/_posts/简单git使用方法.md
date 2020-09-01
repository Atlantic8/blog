---
title: 简单git使用方法
date: 2016-06-08 09:34:40
tags: [git]
categories: Dev
---

##### 查看当前远程库
```git
$-> git remote
$-> git remote -v
BITDM   https://github.com/BITDM/bitdm.github.io.git (fetch)
BITDM   https://github.com/BITDM/bitdm.github.io.git (push)
bitdm   https://github.com/BITDM/bitdm.github.io (fetch)
bitdm   https://github.com/BITDM/bitdm.github.io (push)
origin  https://github.com/Atlantic8/bitdm.github.io.git (fetch)
origin  https://github.com/Atlantic8/bitdm.github.io.git (push)
```
##### 添加远程库
```git
$-> git remote add emacs git://github.com/lishuo/emacs
```
##### 从远程库抓取数据
```git
$->git fetch [remote-name]
```

##### 添加远程源，upstream可以是别的名字
```git
$-> git remote add upstream https://github.com/BITDM/bitdm.github.io.git
$-> git remote -v
BITDM   https://github.com/BITDM/bitdm.github.io.git (fetch)
BITDM   https://github.com/BITDM/bitdm.github.io.git (push)
origin  https://github.com/Atlantic8/bitdm.github.io.git (fetch)
origin  https://github.com/Atlantic8/bitdm.github.io.git (push)
upstream        https://github.com/BITDM/bitdm.github.io.git (fetch)
upstream        https://github.com/BITDM/bitdm.github.io.git (push)

```
##### 用远程源来更新自己的项目
```git
$-> git fetch upstream
$-> git merge upstream/master
```

##### 推送数据到远程仓库
```git
$-> git push [remote-name] [branch-name]
```

##### 远程仓库的删除和重命名
```git
$-> git remote rm [remote-name] 
$-> git remotw rename form-name to-name
```

##### 把本地文件夹放到github上作为repository
```git
首先在网页上创建github仓库
进入目标文件夹
git init   # initialize an empty repository
git remote add origin http://xxxxxx.git  # add remote repository address
git add --all   # 添加所有文件
git commit -m 'add'  # 提交/注释
git push origin master  # 提交
完成
```

##### 修改本地文件，同步到仓库
```git
# 先添加文件
git add test.txt
git commit -m "add test.txt"
# 删除文件，如果要在版本库中删除，使用git rm，并且commit
rm test.txt
git status   # 查看状态
git push origin master  # 推送到远程库

# 修改文件的话，先自行修改
git status  # 显示修改
git add 想要提交的文件名
git commit -m "注释的一些信息"
# 如果在这一步出错的话：git reset --hard HEAD 回滚到add之前的状态
git push # 完成
```