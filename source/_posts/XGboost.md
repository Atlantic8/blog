---
title: XGboost
mathjax: true
date: 2020-08-30 13:00:24
tags: [machine learning]
categories: Algorithm
---

XGBoost是提升树的一种，是一种非常常用且效果很好的算法。


#### 目标函数
提升树的基本思想就是将$K$个弱学习器以相加的方式集成到一起
$$
\hat{y_i}=\sum_{k=1}^K f_k(x_i)
$$

假设有数据集$D=\{(x_1,y_1),...,(x_n,y_n)\}$
对于树型弱学习器，结构化损失函数的形式如下：
$$
L=\sum_il(y_i,\hat{y_i})+\sum_k\Omega(f_k) \\
\Omega(f)=\gamma T+\frac{1}{2}\lambda \Vert w\Vert^2
$$
其中，正则项有两个部分，$T$表示叶子节点的数量，$w$是叶子节点的权值。

为了推导，我们假设第$t$次迭代的损失函数为
$$
L^{(t)}=\sum_i^nl(y_i,\hat{y_i}^{(t-1)}+f_k(x_i))+\Omega(f_t)
$$
做一次泰勒二次展开
$$
L^{(t)}\gets\sum_i^n[l(y_i,\hat{y_i}^{(t-1)})+g_if_t(x)+\frac{1}{2}h_if_t^2(x_i)] + \Omega(f_t)
$$
其中，$g_i=\partial_{\hat{y_i}^{(t-1)}}l(y_i,\hat{y_i}^{(t-1)})$是$l$对$\hat{y_i}^{(t-1)}$的一阶导数，$h_i=\partial^2_{\hat{y_i}^{(t-1)}}l(y_i,\hat{y_i}^{(t-1)})$是二阶导数。将常数项放在一起，我们有
$$
\widetilde{L}^{(t)}=\sum_i^n[g_if_t(x)+\frac{1}{2}h_if_t^2(x_i)]+\gamma T+\frac{1}{2}\lambda \sum_j\Vert w_j\Vert^2+C
$$
做一次转换，将上式中的**样本求和转换到以叶子节点求和**。**令$q(x_i)$表示$x_i$属于的叶子节点（也就是表示了整课树了）**，$I_j=\{i|q(x_i)=j\}$表示属于第$j$个叶子节点的样本序号集合。对于$\sum_i^ng_if_t(x)$，将其分散到各个叶子节点上，第$j$个叶子节点上的样本序号为$I_j$，整体有
$$
\widetilde{L}^{(t)}=\sum_{j=1}^T[(\sum_{i\in I_j}g_i)w_j+\frac{1}{2}(\sum_{i\in I_j}h_i+\gamma)w_j^2]+\gamma T+C
$$
对于$w$而言，上式是一个二次函数。最优值可以通过对$w_j$求导，有
$$
w_j^*=-\frac{\sum_{i\in I_j}g_i}{\sum_{i\in I_j}h_i+\gamma}
$$
带回损失函数有
$$
\widetilde{L}^{(t)}_{optimal}=-\frac{1}{2}\sum_{j=1}^T\frac{(\sum_{i\in I_j}g_i)^2}{\sum_{i\in I_j}h_i+\gamma}+\gamma T
$$
上式可以看成对树结构$q$函数的度量。有了上式，我们可以衡量分裂节点前后目标函数的变化。未分裂时，当前节点就是叶子节点，分裂后**一个叶子节点($I$)变成了两个($I_L$和$L_R$)，树的其他部分不变化**，所以我们只考虑在当前位置的目标函数变化
$$
L_{split}=\frac{1}{2}[\frac{(\sum_{i\in I_L}g_i)^2}{\sum_{i\in I_L}h_i+\gamma}+\frac{(\sum_{i\in I_R}g_i)^2}{\sum_{i\in I_R}h_i+\gamma}-\frac{(\sum_{i\in I}g_i)^2}{\sum_{i\in I}h_i+\gamma}]-\gamma
$$
分裂树节点可以使用贪婪的方法进行，从单个结点开始.



#### 收缩（shrinkage）与列采样
除了上一节损失函数中加入正则项，XGBoost还有收缩（shrinkage）与列采样这两种减少过拟合的方法
- shrinkage在每迭代一棵树后为其加上一个收缩权值，减少当前树的作用，为后续的树留下空间
- 列采样的思想在随机森林中出现，就是在建树过程中选择一部分属性值作为可能分裂属性，而不是所有；除了减少过拟合，还可以降低计算复杂度

#### 节点分裂
###### 贪婪算法
- 对于离散特征，枚举所有的分裂方法（所有特征、所有取值），根据目标函数选择分割方法
- 对于连续特征：一般会先排序，但是枚举带来的计算复杂度太高

###### 近似算法
主要思想是根据特征的分位数给出候选分割点，根据分割点将连续特征转换到bucket中，计算bucket中的聚合统计量。候选分割点可以在算法初始阶段计算（全局），也可以在每次split之后重新计算（局部），一般地，全局策略需要更多的候选分裂点，可以重复使用；而局部策略在每次split之后计算，在层数较深的树中会比较好。

###### 稀疏性
现实中，输入很可能是稀疏的：
- 缺失值
- 未见过的值
- 类似ont-hot的人工特征

算法对于缺失值的处理如下：
- 遇到缺失值，算法将其划分到**默认的分支**
- 默认分支选取是通过非缺失样本算出来的最优解

下图是计算划分以及默认分支的算法

![image](https://raw.githubusercontent.com/Atlantic8/picture/master/xgboost-1.jpg)


#### 系统设计
- Column Block：支持列采样；使得列的划分点查找可以并行化
- Cache-aware Access：预取技术、block大小
- 外存（Out-of-core）计算：主存有限，需要外存，如何解决外存
    - block压缩
    - block分片，即使用多个外存

---

[1]. Tianqi Chen, Carlos Guestrin. XGBoost: A Scalable Tree Boosting System. 2016

