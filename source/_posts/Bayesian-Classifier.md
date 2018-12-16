---
title: Bayesian Classifier
date: 2017-02-26 14:49:57
tags: machine learning
categories: Algorithm
---

###### 朴素贝叶斯分类器
输入空间$\mathbb{R}$为$n$维向量的集合，输出空间为类标记集合$\mathcal{Y}=\lbrace c_1,c_2,...,c_K \rbrace$，给定训练数据集$$T=\lbrace (x_1,y_1),...,(x_N,y_N) \rbrace$$由联合概率分布$P(X,Y)$独立同分布产生。

朴素贝叶斯分类器旨在**最大化后验概率**，即
$$
\begin{aligned}
c&=\arg\max_{c_k} P(Y=c_k|X=x) \\
 &=\arg\max_{c_k} \frac{P(X=x|Y=c_k)P(Y=c_k)} {\sum_k P(X=x|Y=c_k)P(Y=c_k)}
\end{aligned}
$$
由于对于每一个不同的类别，上式中的分母都是一样的，所以上面的目标公式可以写成
$$
\begin{aligned}
c=\arg\max_{c_k} P(X=x|Y=c_k)P(Y=c_k)
\end{aligned}
$$
对于这个优化目标，可做如下统计
$$
\begin{aligned}
P(Y=c_k) &= \frac{ I\lbrace Y=c_k \rbrace }{N}
\end{aligned}
$$
朴素贝叶斯分类器对条件概率分布进行了**条件独立性**的假设 而$P(X=x|Y=c_k)$可以分解为
$$
\begin{aligned}
P(X=x|Y=c_k)=\prod_j^n P(X^{(j)}=x^{(j)}|Y=c_k)
\end{aligned}
$$
所以上式可以分开考虑，即在满足$Y=c_k$的集合中分别考虑，$P(X^{(1)}=x^{(1)}|Y=c_k)$就等于$Y=c_k$的集合中第一个属性为$x^{(1)}$样本所占的比例，所以上式可以写成
$$
\begin{aligned}
P(X=x|Y=c_k)=\prod_j^n \frac {I\lbrace X^{(j)}=x^{(j)}|Y=c_k \rbrace} {I\lbrace Y=c_k \rbrace}
\end{aligned}
$$
所以，经过统计，就可以使用后验概率最大准则进行分类。

当然，也可以使用极大似然估计对单个属性和属性进行建模，用$D_c$表示数据集中第$c$类样本的集合，参数$\theta_c$表示对第$c$类样本的建模，所以有
$$
\begin{aligned}
\mathcal{l} &= log \prod_{x\in D_c}P(x|\theta_c) \\
 &= \sum_{x\in D_c} logP(x|\theta_c)
\end{aligned}
$$
对$P(x|\theta_c)$进行适当建模，比如$P(x|\theta_c) \sim \mathcal{N}(\mu_c, \sigma^2_c)$，然后用经典的极大似然估计进行估值即可。


###### 贝叶斯估计
对于朴素贝叶斯分类器，做如下统计计算时
$$
\begin{aligned}
P(X=x|Y=c_k)=\prod_j^n \frac {I\lbrace X^{(j)}=x^{(j)}|Y=c_k \rbrace} {I\lbrace Y=c_k \rbrace}
\end{aligned}
$$
分子、分母可能为0，所以这里使用**拉普拉斯平滑**，所以统计方法如下
$$
\begin{aligned}
P(Y=c_k) &= \frac{ I\lbrace Y=c_k \rbrace+\lambda }{N+\lambda K} \\
P(X=x|Y=c_k)&=\prod_j^n \frac {I\lbrace X^{(j)}=x^{(j)}|Y=c_k \rbrace+\lambda} {I\lbrace Y=c_k \rbrace+\lambda K_j}
\end{aligned}
$$
其中，$K$是分类类别总数，而$K_j$表示第$j$个属性的可能取值数，$\lambda$是平滑参数，为1时则为Laplace平滑。

