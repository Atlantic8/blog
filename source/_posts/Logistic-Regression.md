---
title: Logistic Regression
date: 2016-12-13 13:52:06
tags: [machine learning]
categories: Algorithm
---

##### Logistic Regression
Logistic Regression的思想源于<b>广义线性模型</b>$$y=g(\omega^Tx+b)$$其中，函数$g()$称为联系函数。
逻辑回归中，联系函数其实<b>sigmoid函数</b>: $$y=\frac{1}{1+e^{-z}}$$其函数图如下：

<center>![](http://ww2.sinaimg.cn/large/9bcfe727jw1fap4kz80uzj208w05xt8q.jpg)</center>

令$z=\omega^T x $，所以$$y=\frac{1}{1+e^{-(\omega^T x)}}$$其中，（通过扩展训练数据将bias部分加入，就省去了bias部分）上式可以写成$$ln\frac{y}{1-y}=\omega^T x$$如果把$y$当作正样本的后验概率$p(y=1|x)$，那么$1-y$就是负样本的后验概率$p(y=0|x)$。所以有：
$$
\begin{aligned}
p(y=1|x) = \frac{e^{-(\omega^T x)}}{1+e^{-(\omega^T x)}} \\
p(y=0|x) = \frac{1}{1+e^{-(\omega^T x)}}
\end{aligned}
$$
我们通过极大似然法来估计$\omega$，给定数据集${(x_i,y_i)}_{i=1}^m$，对数似然函数可以写成：
$$
\begin{aligned}
l(\omega) &= ln\prod_{i=1}^m \left(\frac{e^{-\omega^T x_i}}{1+e^{-\omega^T x_i}}\right)^{y_i} \cdot \left(\frac{1}{1+e^{-\omega^T x_i}}\right)^{1-y_i} \\
&= \sum_{i=1}^m \left( y_i ln \frac{e^{-\omega^T x_i}}{1+e^{-\omega^T x_i}} + (1-y_i) ln \frac{1}{1+e^{-\omega^T x_i}} \right)
\end{aligned}
$$
这里使用经典的方法，$l(\omega)$对$\omega$求导，闭式解不好表示，所以可以使用梯度上升的方法表示，其中
$$
\begin{aligned}
\frac{dl(\omega)}{d\omega} &= \sum_{i=1}^m \left( y_ix_i-\frac{x_i e^{-\omega^T x_i}}{1+e^{-\omega^T x_i}} \right) \\
\omega &= \omega+\frac{dl(\omega)}{d\omega}
\end{aligned}
$$
将批量梯度下降转换成随机梯度下降有
$$
\begin{aligned}
& for\quad i\; \in \; \{1,2,...,m\} \\
& \quad\quad\omega = \omega+\alpha \cdot \left(y_i-\frac{e^{-\omega^T x_i}}{1+e^{-\omega^T x_i}} \right) \cdot x_i
\end{aligned}
$$

##### Generalized Linear Models
上面提到，广义线性模型的形式如下</b>$$y=g(\omega^Tx+b)$$联系线性回归、logistic回归。广义线性模型的训练，如果满足条件，其随机梯度下降的训练方法如下：
$$
\begin{aligned}
& for\quad i\; \in \; \{1,2,...,m\} \\
& \quad\quad\omega = \omega+\alpha \cdot \left(y_i-h_{\theta}(x_i) \right) \cdot x_i
\end{aligned}
$$
其中，$h_{\theta}(x) = g(\theta^Tx)$即是目标模型的形式.
