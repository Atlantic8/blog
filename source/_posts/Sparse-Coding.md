---
title: Sparse Coding
date: 2016-12-20 10:26:20
tags: [machine learning]
categories: Algorithm
---
##### 字典学习
字典学习是与稀疏性相关的学习方法，它被用来寻找一组“超完备”基向量来更高效地表示样本数据。稀疏性会降低计算和存储的开销，并且会提高模型的可解释性。

	稀疏表示侧重于学习一个字典

给定数据集$\lbrace x_1,x_2,...,x_m \rbrace$，字典学习的简单形式如下
$$
\begin{aligned}
\min_{B,\alpha_i} \sum_{i=1}^m \Vert x_i-B\alpha_i \Vert_2^2 + \lambda \sum_{i=1}^m \Vert \alpha_i \Vert_1
\end{aligned}
$$
其中$B\in R^{d\times k}$为字典矩阵，$k$称为字典的词汇量，$\alpha_i \in R^k$是样本$x_i$的稀疏表示。实际中，根据应用场景的要求，第二项中的$\lambda \sum_{i=1}^m \Vert \alpha_i \Vert_1$也可以替换成别的代价函数。

###### 奇异值分解简述SVD
对任意矩阵奇异值分解$$M=U\Sigma V^T$$其中，$\Sigma$是对角矩阵，对角线上是矩阵的奇异值，$U$中的每一列是经过$M$转化后的标准正交基组成之一，而$V$表示了原始域的标准正交基，每一列是一个向量。
> 以后应该还有关于SVD的解释

###### 训练方法
上式的训练目标参数有$\alpha_i,B$，可以用<b>交替优化的方法</b>。

---

1 为每个样本$x_i$找到相应的$\alpha_i$，即
$$
\begin{aligned}
\min_{\alpha_i} \Vert x_i-B\alpha_i \Vert_2^2 + \lambda \Vert \alpha_i \Vert_1
\end{aligned}
$$
这一步可以使用lasso的优化方法。

---

2 以$\alpha_i$为初值来更新字典$B$，即
$$
\begin{aligned}
\min_{B} \Vert X-BA \Vert_F^2
\end{aligned}
$$
其中，$X=(x_1,x_2,...,x_m)\in R^{d\times m},A=(\alpha_1,\alpha_2,...,\alpha_m)\in R^{k\times m}$，矩阵的F范数是矩阵每个元素的平方和再开方。

上式的常用优化方法为<b>KSVD</b>，这是基于逐列更新的方法。令$b_i$表示字典$B$的第$i$列，$\alpha^i$表示稀疏矩阵$A$的第$i$行($\alpha_i$表示稀疏矩阵$A$的第$i$列)，$b_i\alpha^i$其实是个矩阵。则上式可以重写成
$$
\begin{aligned}
\min_{B} \Vert X-BA \Vert_F^2 &= \min_{b_i} \left\Vert X-\sum_{j=1}^k b_ja^j \right\Vert_F^2 \\
&= \min_{b_i} \left\Vert X-\sum_{j=1,j\not i}^k b_ja^j - b_i\alpha^i \right\Vert_F^2 \\
&= \min_{b_i} \Vert E_i-b_i\alpha^i \Vert_F^2
\end{aligned}
$$
更新字典第$i$列时，$E_i$是固定的，$E_i$表示没有$b_i$时表示的误差。所以最小化上式原则上就是对$E_i$进行奇异值分解(SVD)取得最大奇异值所对应的正交向量。对$E_i$进行奇异值分解$E_i=U\Sigma V^T$，那么$b_i$是$U$中最大奇异值对应的正交向量，但此时$\alpha^i$也需要更新，这就会破坏$\alpha^i$的稀疏性质。

为了避免这种情况，KSVD做如下处理。注意到要保持稀疏性，我们不能将$\alpha_i$原来为0的位置变成非零数。$b_i \alpha^i$是一个矩阵，它的第$j$列是$b_i\alpha_j^i$。如果原来$\alpha_j^i=0$，那么$b_i\alpha_j^i$就是全为0的列向量。这里，我们可以把$E_i$对应位置的列变成全0，这样奇异值分解后的结果就不会破坏$A$的稀疏性。然后，对$E_i$进行奇异值分解，更新$b_i$为$U$中最大奇异值对应的正交向量，更新$\alpha^i$为$V$中最大奇异值对应的正交向量(列向量)乘以最大奇异值。

---


##### 稀疏编码
稀疏编码是字典学习的下一步，在学习到了字典$B$后，给定一个新的样本$x_k$，只需要通过优化
$$
\begin{aligned}
\min_{\alpha_i}  \Vert x_k-B\alpha_k \Vert_2^2 + \lambda \Vert \alpha_k \Vert_1
\end{aligned}
$$
来找到$\alpha_k$，即求解出了基于字典$B$的关于$x_k$的稀疏表示。上式的优化方法即经典的Lasso优化问题，使用Proximal Gradient Descent方法。


比如说：
<center>![](http://img.my.csdn.net/uploads/201304/09/1365483491_9524.jpg)</center>