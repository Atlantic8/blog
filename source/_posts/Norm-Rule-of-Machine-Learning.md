---
title: Norm Rule of Machine Learning
date: 2016-11-17 11:05:32
tags: [machine learning]
categories: Algorithm
---

	L0范数是指向量中非0的元素的个数。
    L1范数是指向量中各个元素绝对值之和，也称为“稀疏规则算子”（Lasso regularization）
    L2范数是指向量各元素的平方和然后求平方根
    核范数是指矩阵奇异值的和

###### L0和L1范数
L0和L1范数都有使得参数变得稀疏的作用，因为L0范数的求解困难（NP难），所以一般使用L1范数来逼近L0范数。
稀疏的重要性在于：
1. 特征选择
2. 可解释性（减小多种特征带来的复杂性）

###### L2范数
L2范数也是使用颇为广泛的范数，再回归里使用L2范数的叫做<b>“岭回归”</b>
<b>condition number<b>

	condition number是一个矩阵（或者它所描述的线性系统）的稳定性或者敏感度的度量
    如果一个矩阵的condition number在1附近，那么它就是well-conditioned的
    如果远大于1，那么它就是ill-conditioned的，如果一个系统是ill-conditioned的
    比如：AX=b方程，稍微改动矩阵A的值，b就有很大变化，那么这个方程是ill-conditioned的

非奇异方阵的condition number定义为：$$k(A)=\Vert A \Vert \times \Vert A^{-1} \Vert$$.

L2范数的重要性在于
1. 改善过拟合现象
2. 处理 condition number不好的情况下矩阵求逆很困难的问题

关于2的解释
因为目标函数如果是二次的，对于线性回归来说，那实际上是有解析解的，求导并令导数等于零即可得到最优解为: $$w=(X^TX)^{-1}X^Ty$$
当样本X的数目比每个样本的维度还要小的时候，矩阵$X^TX$将会不是满秩的，也就是不可逆，所以$w$就没办法直接计算出来了，也可以说是有无穷多个解。这就是发生了<b>过拟合</b>。

但是如果加入了L2范数约束，就有：$$w=(X^TX+\lambda I)^{-1}X^Ty$$ 这样求逆就简单些了。

###### L1范数容易产生稀疏解的原因
<center>![](http://ww3.sinaimg.cn/large/9bcfe727jw1f9yxypfys9j20hb0a7q60.jpg)</center>

###### 核范数
低秩矩阵：如果矩阵的秩远小于它的行数和列数，那么它就是低秩矩阵。
核范数是指<b>矩阵奇异值的和</b>，可以用来<b>近似低秩矩阵的秩</b>。
低秩的应用：
1. 矩阵填充，矩阵各行(列)之间的线性相关求出丢失的元素
2. 鲁棒PCA
3. 背景建模
4. 低秩纹理映射算法

###### 近似梯度下降(Proximal Gradient Descent)
近似梯度下降是解决L1优化问题的算法，优化问题的定义形式如下：$$\min_x f(x)+\lambda \Vert x \Vert_1$$其中$f(x)$是凸函数并且可微，而$\lambda \Vert x \Vert_1$是凸函数但是不可微(non-differentiable)，所以不能按照岭回归那样求解。若$f(x)$可导，且$\nabla f$满足L-Lipschitz条件，即存在常数$L>0$使得$$\Vert \nabla f(x_1)-\nabla f(x) \Vert_2^2 \le L \Vert x_1-x \Vert,\; (\forall x,x_1)$$在$x_k$附近将$f(x)$通过二阶泰勒展开式可以写成：
$$
\begin{aligned}
f(x) &\simeq f(x_k)+\nabla f(x_k)(x-x_k)+\frac{ \frac{\nabla f(x)-\nabla f(x_k)}{x-x_k} }{2} \Vert x-x_k \Vert^2 \\
&= f(x_k)+\nabla f(x_k)(x-x_k)+\frac{L}{2} \Vert x-x_k \Vert^2 \\
&= \frac{L}{2} \left\Vert x-\left( x_k-\frac{1}{L}\nabla f(x_k) \right) \right\Vert_2^2 + \varphi (x_k)
\end{aligned}
$$
其中，最后一步将关于$x$的项集中到一起，以及一个$\varphi (x_k)$只包含$x_k$不包含$x$。$\varphi (x_k)$可通过将最后一个式子拆开并和倒数第二个式子比较得到。这样，上式的最小值即为$$x_{k+1}=x_k-\frac{1}{L}\nabla f(x_k)$$这就是梯度下降的思想，梯度下降的每次迭代其实是在最小化原目标的一个二次近似函数。

将这种转化$f(x)$的思想应用到L1优化的目标函数上，可得每一步迭代其实是$$x_{k+1}=arg\min_x \frac{L}{2} \left\Vert x-\left( x_k-\frac{1}{L}\nabla f(x_k) \right) \right\Vert_2^2 + \lambda \Vert x \Vert_1$$即在每一步对$f(x)$进行梯度下降的时候同时考虑优化L1范数。
此时，可以先计算$z=x_k-\frac{1}{L}\nabla f(x_k)$，然后求解
$$
\begin{aligned}
x_{k+1} = arg\min_x \frac{L}{2} \Vert x-z \Vert_2^2 + \lambda \Vert x \Vert_1
\end{aligned}
$$
这里考虑整个$x$就不合适了，考虑$x$的每个分量不会相互影响，即没有$x^ix^j$项。对于第$i$个分量$x^i$所以有$$x_{k+1}^i = arg\min_x \frac{L}{2} (x^i-z_i)^2+\lambda \vert x^i \vert$$所以每个分量的更新方法为（高中知识，二次函数、分类讨论）
$$
x_{k+1}^i=\begin{cases}
z^i-\frac{\lambda}{L}    & { \frac{\lambda}{L}<z^i } \\
0                        & { \vert z^i \vert \le \frac{\lambda}{L}} \\
z^i+\frac{\lambda}{L}    & {\frac{\lambda}{L}+z^i < 0}
\end{cases}
$$
上面就是PGD方法的详细说明，通过PGD就可以求解L1优化问题。

