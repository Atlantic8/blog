---
title: Softmax
date: 2017-05-10 10:40:25
tags: [machine learning]
categories: Algorithm
---

###### Softmax函数
Softmax函数的作用是归一化，对于向量$z=(z_1,...,z_n)$，Softmax函数的形式如下：
$$
\begin{aligned}
softmax(z)=(\frac{e^{z_1}}{\sum_je^{z_j}},...,\frac{e^{z_n}}{\sum_je^{z_j}})
\end{aligned}
$$


###### Softmax Regression形式
`Softmax regression`是`logistic regression`的多分类版本，也是线性分类器，假设一共有$K$个类别，样本特征空间维度为$n$。其基本形式如下
$$
\begin{aligned}
f(x)=softmax(\theta^T x)
\end{aligned}
$$
其中，$\theta$是系数矩阵，维度为$n\times K$，$x$是维度为$n$的样本，输出一个$K\times 1$的向量，选择最大值对应的类为结果。

###### 训练
为了方便描述，假设$z=\theta^Tx$，所以有$f(x)=softmax(z)$。
损失函数的定义与`logistic regression`类似，采用交叉熵形式。假设当前样本为$x_i$，输出为$y_i$，属于第$k$类，输出为$y_i$，对应的真实结果为$\hat{y_i}=[0 0 ... 1 ... 0]$，第$k$位为1，其余位为0。优化方法采用梯度下降。对所有的样本$x_1,...,x_m$，首先损失函数为：
$$
\begin{aligned}
L=-\sum_i^m\hat{y_i}logy_i
\end{aligned}
$$
首先，根据$y_i$的分量可知，对$y_i$求导的导数只有第$k$个分量的梯度不为0
$$
\begin{aligned}
\frac{\partial L}{\partial y_{i}}=\frac{\partial L}{\partial y_{ik}}=-\frac{1}{y_{ik}}
\end{aligned}
$$
然后再求$y_{ik}$对$z_i$的导数（其他的$y_{i}$分量梯度都是0，就不用考虑了）。具体来说，考虑$y_{ik}$对$z_{ij}$的导数。
如果$j==k$，那么
$$
\begin{aligned}
\frac{\partial y_{ik}}{\partial z_{ij}}&=\frac{\partial }{\partial z_{ik}} \frac{e^{z_{ik}}}{\sum_j e^{z_{ij}}} \\
&= \frac{e^{z_{ik}} \sum_j e^{z_{ij}}-e^{z_{ik}}e^{z_{ik}}}{\left( \sum_j e^{z_{ij}} \right)^2} \\
&= y_{ik}(1-y_{ik})
\end{aligned}
$$
所以有
$$
\begin{aligned}
\frac{\partial L}{\partial z_{ij}}=-\frac{1}{y_{ik}} y_{ik}(1-y_{ik})=y_{ik}-1
\end{aligned}
$$

如果$j!=k$，那么
$$
\begin{aligned}
\frac{\partial y_{ik}}{\partial z_{ij}}&=\frac{\partial }{\partial z_{ij}} \frac{e^{z_{ik}}}{\sum_j e^{z_{ij}}} \\
&= \frac{-e^{z_{ij}}e^{z_{ik}}}{\left( \sum_j e^{z_{ij}} \right)^2} \\
&= -y_{ij}y_{ik}
\end{aligned}
$$
所以有
$$
\begin{aligned}
\frac{\partial L}{\partial z_{ij}}=y_{ij}
\end{aligned}
$$
由于$\hat{y_i}$只有第$k$位为1，其余位都为0，所以综上所述
$$
\begin{aligned}
\frac{\partial L}{\partial z_{i}}=y_{i}-\hat{y_i}
\end{aligned}
$$

有了$z_i=\theta^Tx_i$的梯度，$\theta$（其中，$\theta_j$是$\theta$的第$j$列）的梯度就简单了
$$
\begin{aligned}
\frac{\partial L}{\partial \theta}&=\frac{\partial L}{\partial z_{i}} \frac{\partial z_i}{\partial \theta} \\
&=x_i(y_{i}-\hat{y_i})^T
\end{aligned}
$$
有了梯度就可以使用梯度下降方法更新权值了$\theta=\theta-\frac{\partial L}{\partial \theta}$。这是随机梯度下降的梯度表示，对完整梯度下降的表示为
$$
\begin{aligned}
\frac{\partial L}{\partial \theta}&=\sum_{i=1}^m\frac{\partial L}{\partial z_{i}} \frac{\partial z_i}{\partial \theta} \\
&=\sum_{i=1}^mx_i(y_{i}-\hat{y_i})^T
\end{aligned}
$$

---

但是，上面方法训练出来的模型还存在冗余问题，具体来说对于$\theta$的每一列$\theta_k$满足
$$
\begin{aligned}
\frac{e^{(\theta_k^T-\theta_0^T)x}}{\sum_je^{(\theta_j^T-\theta_0^T)x}}=\frac{e^{\theta_k^Tx}}{\sum_je^{\theta_j^Tx}}
\end{aligned}
$$
也就是说会有无穷多个能达到最优解的参数，解决方法是给损失函数加上一个权重衰减项
$$
\begin{aligned}
L=-\sum_i^m\hat{y_i}logy_i+\frac{\lambda}{2} \Vert \theta \Vert^2
\end{aligned}
$$
所以有
$$
\begin{aligned}
\frac{\partial L}{\partial \theta}&=\sum_{i=1}^mx_i(y_{i}-\hat{y_i})^T+\lambda\theta
\end{aligned}
$$

###### Softmax和logistic regression的关系
根据上文描述的`Softmax`存在的参数冗余性，构造一个二分类情况下的`softmax`分类器，形式如下
$$
\begin{aligned}
h_{\theta}(x)=\frac{1}{\sum_{i=1}^2e^{\theta_i^Tx}}
\begin{bmatrix}
     e^{\theta_1^Tx}  \\
     e^{\theta_2^Tx}
\end{bmatrix}
\end{aligned}
$$
把上式中的$\theta$因子全部减去$\theta_1^T$，则有
$$
\begin{aligned}
h_{\theta}(x)&=\frac{1}{\sum_{i=1}^2e^{\theta_i^Tx}}
\begin{bmatrix}
     e^{\theta_1^Tx}  \\
     e^{\theta_2^Tx}
\end{bmatrix} \\
&=\frac{1}{1+e^{(\theta_2-\theta_1)^Tx}}
\begin{bmatrix}
    1  \\
     e^{(\theta_2-\theta_1)^Tx}
\end{bmatrix}
\end{aligned}
$$
这样就又回到logistic regression的格式了！

**引用**
[1]. [UFLDL Softmax回归](http://ufldl.stanford.edu/wiki/index.php/Softmax%E5%9B%9E%E5%BD%92)
[2]. [手打例子一步一步带你看懂softmax函数以及相关求导过程](http://www.jianshu.com/p/ffa51250ba2e)