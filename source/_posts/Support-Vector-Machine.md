---
title: Support Vector Machine
date: 2016-12-27 10:59:50
tags: [machine learning]
categories: Algorithm
---

##### 支持向量机（SVM）

---

支持向量机是一种非常优秀的线性分类器。
给定数据集$D=\lbrace (x_1,y_1),(x_2,y_2),...,(x_m,y_m) \rbrace ,y_i\in \lbrace -1,1 \rbrace$，当$y_i=1$时，称$x_i$为正类；否则为负类。基本思想是在样本及空间内找到一个超平面将不同类别的样本分开。设超平面为
$$
\begin{aligned}
\omega^Tx+b=0
\end{aligned}
$$
将特征空间划分两个部分，一部分是正类，一部分是负类，法向量指向的一侧为正类，反之为负类。相应的分类决策函数为$f(x)=sign(\omega^Tx+b)$。

---

###### 函数间隔
定义超平面$(\omega,b)$关于样本点$(x_i,y_i)$的函数间隔为
$$
\begin{aligned}
\hat{\gamma_i}=y_i(\omega^Tx_i+b)
\end{aligned}
$$
函数间隔的正负可以表示分类结果是否准确，其大小可以**相对地**表示样本点到超平面的远近，越远置信度越高。
定义超平面$(\omega,b)$关于数据集$D$的函数间隔为$(\omega,b)$关于$D$中样本点$(x_i,y_i)$的函数间隔的最小值，即
$$
\begin{aligned}
\hat{\gamma}=\min_{i=1,...,m}\hat{\gamma_i}
\end{aligned}
$$
函数间隔可以表示分类的准确度和置信度。但是，函数间隔还存在一个明显问题，比如将$\omega$和$b$都扩大2倍，超平面不变，但是函数间隔却扩大了2倍，解决方案是对函数间隔添加规范化约束。

###### 几何间隔
定义超平面$(\omega,b)$关于分类正确的样本点$(x_i,y_i)$的几何间隔为
$$
\begin{aligned}
\gamma_i=\frac{y_i( \omega^Tx_i+b )}{\Vert \omega \Vert}
\end{aligned}
$$
定义超平面$(\omega,b)$关于数据集$D$的几何间隔为$(\omega,b)$关于$D$中样本点$(x_i,y_i)$的几何间隔的最小值，即
$$
\begin{aligned}
\gamma=\min_{i=1,...,m}\gamma_i
\end{aligned}
$$

###### 间隔最大化
**SVM学习的基本思想是求解能够正确划分训练数据集并且几何间隔最大的分离超平面**，意味着以充分大的确信度对训练数据进行分类，以获得更好的泛化能力。所以问题就变成了
$$
\begin{aligned}
& \max_{\omega,b}\quad\gamma \\
& s.t. \quad \frac{y_i( \omega^Tx_i+b )}{\Vert \omega \Vert} \ge \gamma,\; i=1,2,...,m
\end{aligned}
$$
考虑到$\gamma=\frac{\hat{\gamma} }{\Vert \omega \Vert}$，所以上式可以写成
$$
\begin{aligned}
& \max_{\omega,b}\quad\frac{\hat{\gamma} }{\Vert \omega \Vert} \\
& s.t. \quad y_i( \omega^Tx_i+b ) \ge \hat{\gamma},\; i=1,2,...,m
\end{aligned}
$$
前面提到将$(\omega,b)$按比例缩放不会影响最终结果，所以可以取$\hat{\gamma}=1$，所以原问题可以转化为如下问题
$$
\begin{aligned}
& \max_{\omega,b}\quad\frac{1 }{\Vert \omega \Vert} \\
& s.t. \quad y_i( \omega^Tx_i+b ) \ge 1,\; i=1,2,...,m
\end{aligned}
$$
即
$$
\begin{aligned}
&\min_{\omega,b} \frac{1}{2}\Vert \omega \Vert^2 \\
& s.t. \quad y_i( \omega^Tx_i+b ) \ge 1,\; i=1,2,...,m
\end{aligned}
$$
这就是SVM的基础形态，是一个凸二次规划问题。

---

###### 拉格朗日对偶性
考虑如下的优化问题
$$
\begin{aligned}
\min_{\omega} f(\omega) \\
\quad \quad s.t. \quad g_i(\omega) &\le 0  \\
h_i(\omega) &= 0
\end{aligned}
$$
对应的拉格朗日函数如下，$\alpha,\beta$是拉格朗日乘子
$$
\begin{aligned}
L(\omega,\alpha,\beta)=f(\omega)+\sum_{i=1}^k\alpha_ig_i(\omega) + \sum_{i=1}^l\beta_ih_i(\omega).
\end{aligned}
$$
考虑下面的优化问题
$$
\begin{aligned}
\theta_P(\omega)=\max_{\alpha,\beta:\alpha_i\ge 0} L(\omega,\alpha,\beta)
\end{aligned}
$$
下标$P$是$primal$的意思，优化目标针对变量$\alpha,\beta$。给定$\omega$，如果$\omega$的任何一个分量违背了限制条件(比如$g_i(\omega)>0$或者$h_i(\omega) \neq 0$)，那么$\theta_P(\omega)$就是无穷大！反之，如果限制条件没有被打破，那么$\theta_P(\omega)=f(\omega)$，所以
$$
\theta_P(\omega)=\begin{cases}
f(\omega)   &    如果 \omega满足限制条件 \\
\infty      &    其他
\end{cases}
$$
下式成立
$$
\begin{aligned}
\min_{\omega} \theta_P(\omega) = \min_{\omega} \max_{\alpha,\beta:\alpha_i\ge 0} L(\omega,\alpha,\beta) = p^{\*}
\end{aligned}
$$

---

下面考虑对偶问题，定义
$$
\begin{aligned}
\theta_D(\alpha,\beta) = \min_{\omega} L(\omega,\alpha,\beta)
\end{aligned}
$$
这里下标$D$表示$dual$，优化目标针对变量$\omega$。所以有
$$
\begin{aligned}
\max_{\alpha,\beta:\alpha_i\ge 0} \theta_D(\alpha,\beta) = \max_{\alpha,\beta:\alpha_i\ge 0} \min_{\omega} L(\omega,\alpha,\beta) = d^{\*}
\end{aligned}
$$

---

对于上面的$p^{\*}$和$d^{\*}$，有如下的规律
$$
\begin{aligned}
d^{\*}=\max_{\alpha,\beta:\alpha_i\ge 0} \min_{\omega} L(\omega,\alpha,\beta) \le \min_{\omega} \max_{\alpha,\beta:\alpha_i\ge 0} L(\omega,\alpha,\beta) = p^{\*}
\end{aligned}
$$
上式中等号成立的条件是：函数$f$和$g_i$都是凸函数，$h_1,h_2,...,h_l$函数是同族函数。并且每个$g_i$函数都是严格合理的，即对每一个$i$，都存在一些$\omega$满足$g_i(\omega)小于0$。此外，存在$(\alpha,\beta,\omega)$满足**KKT条件**，即
$$
\begin{aligned}
\frac{dL(\alpha,\beta,\omega)}{d\omega_i} &= 0,\quad i=1,...,m \\
h_i(\omega)&= 0,\quad i=1,...,l \\
\alpha_i g_i(\omega) &= 0, \quad i=1,...,k \\
g_i(\omega) &\le 0, \quad i=1,...,k \\
\alpha_i &\ge 0 , \quad i=1,...,k
\end{aligned}
$$

---

###### 对偶问题
由最大化间隔得出的优化问题是一个凸二次规划问题，可以使用现成的工具完成。使用拉格朗日乘子法可得到其对偶问题，为其每项约束添加一个拉格朗日乘子$\alpha_i \ge 0$，拉格朗日目标函数为
$$
\begin{aligned}
L(\omega,b,\alpha) = \frac{1}{2}\Vert \omega \Vert^2 + \sum_{i=1}^m \alpha_i(1-y_i(\omega^Tx_i+b))
\end{aligned}
$$
其中，$\alpha=(\alpha_1;\alpha_2;...;\alpha_m)$。上式分别对$\omega,b$求偏导并令其为0可得
$$
\begin{aligned}
\omega = \sum_{i=1}^m \alpha_iy_ix_i \\
0 = \sum_{i=1}^m \alpha_iy_i
\end{aligned}
$$
将上式代入$L(\omega,b,\alpha)$中，消去$\omega,b$，则上式变成
$$
\begin{aligned}
L(\omega,b,\alpha) = \sum_{i=1}^m \alpha_i - \frac{1}{2} \sum_{i=1}^m \sum_{j=1}^m \alpha_i \alpha_j y_i y_j x_i^T x_j
\end{aligned}
$$
由于满足KKT条件，所以原问题$f(\omega)$的优化问题可以写成
$$
\begin{aligned}
\min_{\omega,b} f(\omega) &\to \min_{\omega,b} \max_{\alpha} L(\omega,b,\alpha) \\
&\to \max_{\alpha} \min_{\omega,b} L(\omega,b,\alpha)
\end{aligned}
$$
这里$ \max_{\alpha} L(\omega,b,\alpha)$的意义在于选择参数$\alpha$使得$ L(\omega,b,\alpha)$最大，根据$ L(\omega,b,\alpha)$的公式，由于$1\le y_i(\omega^Tx_i+b)$，所以一旦出现$1 < y_i(\omega^Tx_i+b)$的情况，就应该有$\alpha_i=0$，否则这一项就是负值，整体也就不是最小值了。所以，优化问题最终转化为
$$
\begin{aligned}
\max_{\alpha} \sum_{i=1}^m \alpha_i - \frac{1}{2} \sum_{i=1}^m \sum_{j=1}^m \alpha_i \alpha_j y_i y_j x_i^T x_j \\
s.t. \; \sum_{i=1}^m\alpha_iy_i=0,\alpha_i \ge 0,\; i=1,...,m
\end{aligned}
$$

---

###### Sequential Minimal Optimization
对偶问题依旧是二次规划问题，但问题的规模正比于训练样本数。SMO是高效算法之一，其思想是每次选取两个变量$\alpha_i,\alpha_j$并固定其他的$\alpha_k$，不断执行迭代步骤。这种方法也称为坐标上升方法（coordinate ascent）。

令$$\alpha_iy_i+\alpha_jy_j=-\sum_{k\neq i,j}\alpha_ky_k=c$$用这个式子消去优化目标函数中的$\alpha_j$可以得到一个以$\alpha_i$为单变量的二次规划问题，该问题有闭式解且简单易懂。解出之后，$\alpha_i,\alpha_j$就得到了更新。SMO选取$\alpha_i,\alpha_j$时，启发式地选择对应样本间隔最大的变量进行更新。

然后根据$\omega = \sum_{i=1}^m \alpha_iy_ix_i$求出$\omega$，对于$b$，可以使用任意一个支持向量的性质$y_s \left(\omega^Tx_s+b \right)=1$来计算。当然更鲁棒的方法是使用所有的支持向量并对求出的$b$取均值。

---


##### 软间隔支持向量机（Soft Margin SVM）
基础型的SVM的假设所有样本在样本空间是线性可分的(硬间隔)，但是现实中的情况通常不满足这种特性。对应的软间隔允许某些样本不满足
$$
\begin{aligned}
y_i(\omega^Tx_i+b)\ge 1
\end{aligned}
$$
为了解决这个问题，可以对每个样本点引入一个松弛变量$\xi_i\ge 0$满足
$$
\begin{aligned}
y_i(\omega^Tx_i+b)+\xi_i\ge 1
\end{aligned}
$$
同时，对每个松弛变量支付一个代价$\xi_i$。训练时应该要保持不满足约束的样本尽量少，所以优化函数可以表示成
$$
\begin{aligned}
&\min_{\omega,b,\xi_i} \frac{1}{2}\Vert \omega \Vert^2 + C\sum_{i=1}^m \xi_i \\
&s.t. \; y_i(\omega^Tx_i+b) \ge 1-\xi_i \\
&\quad \xi_i \ge 0,\;i=1,...,m
\end{aligned}
$$
其中，$C>0$是一个惩罚参数，调节损失函数两项的权重。
这就是常用的软间隔支持向量机，通过拉格朗日乘子法，得到如下拉格朗日函数
$$
\begin{aligned}
L(\omega,b,\alpha,\xi,\mu) = \frac{1}{2}\Vert \omega \Vert^2 + C\sum_{i=1}^m \xi_i + \sum_{i=1}^m \alpha_i(1-\xi_i-y_i(\omega^Tx_i+b)) - \sum_{i=1}^m \mu_i\xi_i
\end{aligned}
$$
其中，$\alpha_i,\mu_i$就是拉格朗日乘子。令$L(\omega,b,\alpha,\xi,\mu)$对$\omega,b,\xi$的偏导数为0得到
$$
\begin{aligned}
\omega &= \sum_{i=1}^m \alpha_iy_ix_i \\
0 &= \sum_{i=1}^m \alpha_iy_i \\
C &= \alpha_i + \mu_i
\end{aligned}
$$
由上式可知$0 \le \alpha_i \le C$。将上式代入$L(\omega,b,\alpha,\xi,\mu)$中，并求解优化函数的对偶形式
$$
\begin{aligned}
&\max_{\alpha} \sum_{i=1}^m \alpha_i - \frac{1}{2} \sum_{i=1}^m \sum_{j=1}^m \alpha_i \alpha_j y_i y_j x_i^T x_j \\
&s.t. \sum_{i=1}^m\alpha_iy_i=0 \\
&0 \le \alpha_i \le C,\; i=1,...,m
\end{aligned}
$$
对于软间隔支持向量机，其KKT条件是
$$
\begin{aligned}
\alpha_i y_i(\omega^x_i+b)-1+\xi_i &= 0, \quad i=1,...,m \\
y_i(\omega^x_i+b)-1+\xi_i &\le 0, \quad i=1,...,m \\
\alpha \ge 0,\mu_i &\ge 0, \quad i=1,...,m \\
\xi_i \ge 0, \mu_i \xi_i &= 0, \quad i=1,...,m
\end{aligned}
$$
对于非支持向量，$\alpha_i=0$。对支持向量，有$0 < \alpha_i \le C$，即有$y_i(\omega^x_i+b)=1-\xi_i$，样本点$x_i$到间隔边界的距离为$\frac{\xi_i}{\Vert \omega \Vert}$，软间隔的支持向量有以下几种情况
- 或者在间隔边界上（$\alpha_i < C,\xi_i=0$）
- 或者在间隔边界与分离超平面之间（$\alpha_i=C,0 < \xi_i < 1$，此时分类也是正确的）
- 或者在分离超平面误分那一侧（$\alpha_i=C,\xi_i>1$，分类错误，该样本是异常点）


上述优化问题依旧可以使用SMO算法，求出$\omega$之后，$b$的求法如下。注意到满足$0<\alpha_i < C$的样本是支持向量，即满足$y_i(\omega^Tx_i+b)=1$，所以$b$就可解了。

##### 非线性核支持向量机（Kernal SVM）
###### 核函数判定定理
设$X$是输入空间，$k(\cdot,\cdot)$是定义在$X\times X$的对称函数，则$k$是核函数当且仅当对于任意数据集$D=\lbrace x_1,x_2,...,x_m \rbrace$，核矩阵$K$总是半正定的，其中半正定是指对于每个非零的复向量$z$，$z^{\*}Kz > 0$，其中$z^{\*}$是$z$的共轭转置。

常用的核函数有
$$
\begin{aligned}
Linear\; kernal &: \quad k(x_i,x_j)= x_i^Tx_j \\
Multinomial\; kernal &: \quad k(x_i,x_j)= (x_i^Tx_j)^d \\
Gaussian\; kernal &: \quad k(x_i,x_j)= e^{-\frac{\Vert x_i-x_j \Vert^2}{2\sigma^2}} \\
Laplace\; kernal &: \quad k(x_i,x_j)= e^{-\frac{\Vert x_i-x_j \Vert}{\sigma}} \\
Sigmoid\; kernal &: \quad k(x_i,x_j)= tanh(\beta x_i^Tx_j+\theta),\beta>0,0>\theta
\end{aligned}
$$
另外核函数的线性组合、乘积也是核函数。并且对于任意函数$g(\cdot)$，$k(x,z)=g(x)k_1(x,z)g(z)$也是核函数。

---

###### KSVM
基础型的SVM的假设样本在样本空间是线性可分的，但是现实中的情况通常不满足这种特性。对于这种问题，一种可能的方法是将样本从原始空间映射到更高维的特征空间，使得其在线性可分。令$\phi (x)$表示将$x$映射后的特征向量，于是特征空间中的超平面可以表示为$$f(x)=\omega^T \phi (x)+b$$优化的对偶问题变成
$$
\begin{aligned}
\max_{\alpha} \sum_{i=1}^m \alpha_i - \frac{1}{2} \sum_{i=1}^m \sum_{j=1}^m \alpha_i \alpha_j y_i y_j \phi (x_i)^T \phi (x_j) \\
s.t. \; \sum_{i=1}^m\alpha_iy_i=0,\alpha_i \ge 0,\; i=1,...,m
\end{aligned}
$$
由于可能存在维度诅咒，计算$\phi (x_i)^T \phi (x_j)$将非常困难。这里引入**核函数**的概念
$$
\begin{aligned}
k(x_i,x_j) = \langle \phi (x_i),\phi (x_j) \rangle = \phi (x_i)^T \phi (x_j)
\end{aligned}
$$
满足$x_i,x_j$在特征空间的内积等于它们在原始样本空间中通过函数$k(\cdot)$计算的结果，核函数是避免维度诅咒的一种方法。


引用
[1]. 统计学习方法. 李航著. 清华大学出版社
[2]. 机器学习. 周志华.