---
title: mean shift
date: 2016-05-11 21:07:55
tags: [machine learning]
categories: Algorithm
mathjax: true
---

#### 基本Mean Shift
![示意图](http://pic002.cnblogs.com/images/2012/358029/2012051215035738.jpg)
给定d维空间$R^d$的n个样本点 ,i=1,…,n,在空间中任选一点x，那么Mean Shift向量的基本形式定义为:
<center>![](http://pic002.cnblogs.com/images/2012/358029/2012051213564761.jpg)</center>

其中，$S_k$是在一个半径为h的高维球区域中的点集合。

#### 基于核函数的Mean Shift
<center>![](http://pic002.cnblogs.com/images/2012/358029/2012051215383189.jpg)</center>
解释一下K()核函数，h为半径，$\frac{C\_{k,d}}{nh^d}$  为单位密度，要使得上式f得到最大，最容易想到的就是对上式进行求导，的确meanshift就是对上式进行求导.。

#### Mean Shift Clustering伪代码
```python
// e is a predefined threshold value.
for data in dataset:
    x = data;
    do :
        calculate mean shift of x: ms;
        error = f(ms-x);
    while (error < e);
    dict{data} = x;
dict{x}=dict{y} -> x,y in same cluster
```
