---
title: Factorization Machines
mathjax: true
date: 2021-01-02 15:49:44
tags: [machine learning, recommendation]
categories: Algorithm
---

### FM

> Factorization Machines. 2010

FM（Factorization Machine）是推荐系统常用典算法之一

LR（或者线性回归）是个简单的线性模型，可解释性好。LR假设所有的特征都是独立存在的，所以一个其明显的缺陷是不能的考虑组合特征。SVM的核函数（多项式函数$K(x_i,x_j)=(\gamma x_i^Tx_j+d)^n$可以考虑到特征组合的情况）,但是

LR也可以显示地加入组合特征，会导致要学习的参数数量增大。特征多的时候，总有部分特征是比较稀疏的，这时候组合特征就更稀疏了，在有限训练数据的条件下，组合特征的参数很可能学习得不充分。

FM解决了这个问题，下面介绍这个算法：

形式：
$$
y=\sum_i^n w_i x_i + \sum_i^n\sum_{j>i}^nv_i^Tv_jx_ix_j, \tag{1}
$$
这里，我们给每个特征一个隐向量（长度为$k<n$），交叉特征的权重由对应特征的隐向量内积表示，这样我们需要学习的参数就是$w,v$了，因为交叉特征的权重不再独立，参数学习也简单了许多，**泛化能力**也变强了（比如$x_i,x_k$的组合在训练数据这没出现过，依旧可以表示其系数$v_i^Tv_k$，如果赋予组合特征独立的参数，且就训练数据中不存在这样的的组合，那么其参数就学不到了）。

关于特征处理：
- 数值特征：对应一个隐向量
- 非数值特征：换成one-hot形式，对应多个隐向量

公式(1)的计算复杂度是比LR要高的，为平方复杂度，考虑隐向量的长度，复杂度为O(kn^2)，可以通过变换降低其复杂度：
$$
f(x)=\sum_i^n w_i x_i + \frac{1}{2}\sum_{f=1}^k\left[(\sum_i^n v_{i,f}x_i)^2-\sum_i^nv_{i,f}^2x_i^2\right]
$$
复杂度降为O(kn)。

训练就采用SGD即可，训练和预测都可以在线性时间完成。

FM中的隐向量可以看成是深度模型中的embedding，也就是每个特征的embedding，可以和NN结合构建深层网络。

### FFM

> Field-aware Factorization Machine. 2014

FFM（Field-aware Factorization Machine）是FM的进阶，通过引入field的概念，FFM把相同性质的特征归于同一个field。比如商品的末级品类编码生成了550个特征，这550个特征都是说明商品所属的品类，因此它们也可以放到同一个field中。

实现上，每一维特征$xi$，针对其它特征的每一种field$f_j$，都会学习一个隐向量$v_{i,fj}$，其中$f_j$是$j$个特征的field。因此，**隐向量不仅与特征相关，也与field相关**！算法形式如下：
$$
 f(x)=\sum_i w_ix_i + \sum_i\sum_{j>i}v_{i,f_j}^Tv_{j,f_i}x_ix_j
$$
从上式可以看出来，较FM而言FFM参数数量变大，训练也更加耗时。

**FFM将问题定义为分类问题，使用的是logistic loss**（label为1、-1），同时加入了正则项,训练优化目标为：
$$
\min_{\theta}\sum_i \log\left(1+\exp\{-y^if(x^i,\theta)\}\right)+\frac{\lambda}{2}||w||^2
$$

部分开源实现的FFM忽略了一次项，只保留了二次项。


---



