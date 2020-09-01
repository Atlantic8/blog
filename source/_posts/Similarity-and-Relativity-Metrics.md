---
title: Similarity and Relativity Metrics
mathjax: true
date: 2020-09-01 23:04:31
tags:
categories: Math
---

相似度度量出现在很多机器学习应用中，比如query-query相似度、排序等等，今天介绍一下常用的几个相似度衡量标准

### 闵可夫斯基距离
定义如下
$$
d(A,B)=\sqrt[p]{\sum_i|A_i-B_i|^p}
$$
根据p值的不同，可以是
- $p=1$: $d=\sum_i|A_i-B_i|$，曼哈顿距离
- $p=2$: $d=\sqrt{\sum_i|A_i-B_i|^2}$，欧几里得距离
- $p\to\infin$: $d=\max_i|A_i-B_i|$，切比雪夫距离

### 汉明距离
对比对象二进制表示的差异，**即二进制表示对应位不同的个数**。

### 编辑距离
允许增、删、改操作的序列距离，可用动态规划的方式求解，动态方程为
$$
d(i,j)=\left\{
\begin{aligned}
d(i-1,j-1), &  &  A[i]==B[j] \\
\min\left\{d(i-1,j-1), d(i-1,j), d(i,j-1)\right\}+1, &  &  else
\end{aligned}
\right.
$$

### 余弦相似度
$$
\cos(\theta)=\frac{A\cdot B}{|A||B|}
$$

### Jaccard系数
给定两个集合$A,B$，Jaccard系数定义为
$$
J(A,B)=\frac{|A\cap B|}{|A\cup B|}
$$
也就是集合的交集大小比上集合的并集大小。Jaccard系数的取值范围是[0, 1]，两个集合都是空集，Jaccard系数=1。

与Jaccard系数对应的是**Jaccard距离**，其计算方式是： Jaccard距离=1-Jaccard系数，距离越大，样本相似度越低


### pearson系数
两个连续变量$(X,Y)$的pearson相关性系数$(Px,y)$定义如下：
$$
P(x,y)=\frac{cov(X,Y)}{\sigma_X\cdot \sigma_Y}=\frac{E(XY)-E(X)E(Y)}{\sqrt{E(X^2)-E^2(X)}\sqrt{X(Y^2)-E^2(Y)}}=\frac{\sum_i(X_i-\mu_X)(Y_i-\mu_Y)}{\sqrt{\sum_i(X_i-\mu_X)^2}\sqrt{\sum_i(Y_i-\mu_Y)^2}} \tag{1}
$$
pearson系数取值总是在-1.0到1.0之间，越靠近0表示相关性越低，数值的正负表示正相关还是负相关.

注意公示1可以发现，pearson相关性系数也就是**把数据先正规化到均值为0、方差为1，然后求这两组数据的cosine夹角**


---

