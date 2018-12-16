---
title: Hidden Markov Model
date: 2016-12-31 09:41:54
tags: [machine learning]
categories: Algorithm
---

##### 概率图模型
概率图模型是一类用图来表达变量相关关系的概率模型，常见的是用一个节点表示一个或一组随机变量，节点之间的边表示变量之间的概率关系。概率模型可以大致分为两类：
- 第一类使用有向无环图表示变量之间的依赖关系，称之为有向图模型或者贝叶斯网
- 第二类使用无向无环图表示变量之间的依赖关系，称之为无向图模型或者马尔可夫网

本文要介绍的隐马尔可夫模型就是结构简单的动态贝叶斯网。

##### 隐马尔可夫模型
HMM的主要作用是时序数据建模，应用范围包括语音识别、自然语言处理等领域。
与马尔可夫过程不同，HMM中状态是无法直接观测的，取而代之，我们可以获取到与状态值息息相关的观测变量值，图中是经典的海藻与天气例子。

<center>![经典的海藻于天气示例](http://ww2.sinaimg.cn/large/9bcfe727jw1fb9wwz6vk7j20eq08cdg2.jpg)</center>

一个HMM模型中有两组变量，第一组是状态变量$Y=\lbrace y_1,y_2,...,y_n \rbrace$表示隐含的状态，下标表示时序。另一组是观测变量$X=\lbrace x_1,x_2,...,x_n \rbrace$，下标表示时序。系统可能会存在多个状态，这些状态的集合为$S=\lbrace s_1,s_2,...,s_N \rbrace$，如果$y_i = k$那么表示$i$时刻的状态为$s_k$。观测变量可以是离散的也可以是连续的，不妨假设其为离散值。同样地，定义观测值的集合$O = \lbrace o_1,o_2,...,o_M \rbrace$，如果$x_i = k$那么表示$i$时刻的状态为$o_k$。

HMM中有两个重要的性质：
- 观测变量的取值仅依赖于状态变量
- t时刻的状态仅依赖于t-1时刻的状态

基于上面两个性质，可以得到如下公式
$$
\begin{aligned}
p(x_1,y_1,...,x_n,y_n)=p(y_1)p(x_1|y_1)\prod_{i=2}^n p(y_i|y_{i-1})p(x_i|y_i)
\end{aligned}
$$
上式基本上描述了HMM的结构信息，在实际计算时还需要如下参数

---

状态转移概率$A=[a_{ij}]_{N\times N}$，其中$$a_{ij}=p(y_{t+1}=j|y_t=i)$$表示由状态$s_i$转移到状态$s_j$的概率。

输出观测概率$B=[b_{ij}]_{N\times M}$，其中$$b_{ij}=p(x_t=j|y_t=i)$$表示在状态$s_i$下观测值为$o_j$的概率。

初始状态概率$\pi=(\pi_1,...,\pi_N)$，其中$$\pi_i=p(y_1=i)$$表示初始状态为$s_i$的概率。

---

指定了状态空间$Y$，观测空间$X$和上述三组参数，一个HMM就确定了，所以一个HMM可以表示成一个五元组$(N,M,A,B,\pi)$，$N,M$分别表示状态值和观测值的可能取值范围。HMM也可以表示成$\lambda=(A,B,\pi)$。

下面考虑三个实际问题：

---

###### 模型于观测序列匹配度
给定模型$\lambda=(A,B,\pi)$，如何有效计算其产生观测序列$X=(x_1,x_2,...,x_T)$的概率$p(X|\lambda)$？

为解决这一问题，Baum提出了**前向算法**，具体如下：
**定义$\theta_t(j)$为在$t$时刻，整体观测序列为$x_1,...,x_t$，此时状态为$s_j$的概率**。其中我们有
$$
\begin{aligned}
\theta_1(i) = \pi_ib_{ix_1}
\end{aligned}
$$
表示第一个观测值的概率，其递推式也很容易写出
$$
\begin{aligned}
\theta_{t+1}(i)=\left[\sum_{j=1}^N\theta_t(j)a_{ji}\right]b_{ix_{t+1}}
\end{aligned}
$$
有两部分构成，第一部分是由枚举$t$时刻的状态并跳转到$t+1$时刻，第二部分是$t+1$时刻的状态产生观测值的概率。

当$n=1$时，输出序列为$x_1$，此时计算概率$p(x_1|\lambda)$也就是计算初始状态集合每个可能的状态产生观测值$x_1$的概率和，也就是
$$
\begin{aligned}
p(x_1|\lambda)=\sum_{i=1}^N \theta_1(i)
\end{aligned}
$$
当$n=2$时，输出序列为$x_1x_2$，所以有
$$
\begin{aligned}
p(x_1,x_2|\lambda) &=  \sum_{j=1}^N \theta_2(j)
\end{aligned}
$$


后面的依此类推，前向算法的描述如下：

---

1 初始化：$\theta_1(i)=\pi_ib_{i1}, 1\le i \le N$
2 $\theta_{t+1}(j)=\left[\sum_{i=1}^N \theta_t(i)a_{ij}\right]b_{jx_{t+1}}$
3 $p(x_1,...,x_T|\lambda)=\sum_{j=1}^N \theta_T(j)$

---

一共有$T$个时刻，每个时刻要考虑$N$个状态，每个状态又要考虑钱一个时刻的$N$个状态，所以时间复杂度为$O(N^2T)$。

###### 推断隐藏序列
由于有时候我们需要隐藏序列包含的信息，所以给出隐藏序列是有必要的（比如词性标注最终就需要给出词性序列）。问题的形式化表述即为
$$
\begin{aligned}
\arg\max_{y_1,...,y_T} p(y_1,...,y_T|x_1,...,x_T,\lambda)
\end{aligned}
$$
这个问题的解决方法是维特比（Viterbi）算法。

**定义维特比变量$\gamma_t(j)$：表示在时序$t$，观察序列为$x_1,...,x_t$，状态为$s_j$的最大概率**，即
$$
\begin{aligned}
\gamma_t(j)=\max p(y_1,...,y_t=j|x_1,...,x_t,\lambda)
\end{aligned}
$$
直观来说，在时序$t+1$状态为$s_j$的最大概率应该是时序$t$时所有状态转换到时序$t+1$、观测值为$x_{t+1}$并且状态为$s_j$的最大值，即
$$
\begin{aligned}
\gamma_{t+1}(j)=\max_k \gamma_{t}(k)a_{kj}b_{jx_{t+1}}
\end{aligned}
$$
并且，为了记忆路径，定义路径变量$\phi_t(j)$为该路径上的状态$s_j$的前一个状态，即从$t-1$时序到$t$的最优转移方式。

维特比算法的描述如下：

---

1 初始化：
2 $\quad \gamma_1(j)=\pi_i b_{ix_{1}},\;\phi_1(i)=0,1\le i \le N$
3 归纳计算：
4 $\quad \gamma_t(j)=\max_k \gamma_{t-1}(k)a_{kj}b_{jx_{t}}$
5 $\quad \phi_t(i)=\arg\max_j \gamma_{t-1}(j)a_{jk}b_{kx_{t}}$
6 确定路径：
7 $\quad y_T=\arg\max_{y_j} \gamma_{T}(j)$
8 $\quad for\;t=T-1,...,1$
9 $\quad \quad y_t=\phi_{t+1}(y_{t+1})$

---

###### 模型训练
HMM的学习就是给定观测序列$X=x_1,...,x_T$，试图找到最优的参数$\lambda$使得$p(X|\lambda)$最大。如果知道了状态序列，那么$\pi,A,B$就都可以统计出来。但是状态序列其实是隐变量，求解此问题的方法是前向后向算法，也叫做Baum-Welch算法。

定义
$$
\begin{aligned}
\beta_t(i)=p(x_{t+1},...,x_T|y_t=i,\lambda)
\end{aligned}
$$
表示**当前$t$时刻状态为$s_i$，部分观测序列为$x_{t+1},...,x_T$的概率**。与前向算法类似，$\beta_t(i)$也可以有效地计算，公式如下
$$
\begin{aligned}
\beta_t(i)&=\left[\sum_{j=1}^N \beta_{t+1}(j)a_{ij}\right]b_{jx_{t+1}},\; 1\le t \le T-1 \\
\beta_T(i)&=1
\end{aligned}
$$
进一步可以得到
$$
\begin{aligned}
p(X,y_t=i|\lambda)&=p(x_1,...,x_t,y_t=i|\lambda)p(x_{t+1},...,x_T,y_t=i|\lambda)=\theta_t(i)\beta_t(i) \\
p(X,y_t=i|\lambda)&=\sum_{i=1}^N \theta_t(i)\beta_t(i)
\end{aligned}
$$

<center>![](http://ww2.sinaimg.cn/large/9bcfe727jw1fbacpj6v5zj20cc064jrl.jpg)</center>

在前后向算法中，定义$$\xi_t(i,j)=p(y_t=i,y_{t+1}=j|X,\lambda)$$表示给定HMM和观测序列$X$，$t,t+1$时刻的状态分别是$s_i,s_j$的概率。如上图所示，对上式的推导为
$$
\begin{aligned}
\xi_t(i,j)&=\frac{p(y_t=i,y_{t+1}=j,X|\lambda)}{p(X|\lambda)} \\
&= \frac{\theta_t(i)a_{ij}\beta_{t+1}(j)b_{jx_{t+1}}} {\sum_{i=1}^N \sum_{j=1}^N \theta_t(i)a_{ij}\beta_{t+1}(j)b_{jx_{t+1}}}
\end{aligned}
$$
除此之外，再定义$$\eta_t(i)=p(y_t=i|X,\lambda)$$表示给定HMM和观测序列$X$，$t$时刻状态为$s_i$的概率，所以有
$$
\begin{aligned}
\eta_t(i) = \frac{p(y_t=i,X|\lambda)} {p(X|\lambda)} = \frac{\theta_t(i)\beta_t(i)}{\sum_{i=1}^N \theta_t(i)\beta_t(i)}
\end{aligned}
$$
考虑$\xi_t(i,j)$和$\eta_t(i)$的定义，就能够得到（想想就能得到）$$\eta_t(i)=\sum_{i=1}^N \xi_t(i,j)$$下面介绍前向后向算法的描述：

---

1  初始化：随机初始化参数$A,B,\lambda$
2  不满足停止条件时迭代计算：
3  $\quad \beta_T(i)=1,1\le i \le N$
4  $\quad \beta_t(i)=\left[\sum_{j=1}^N \beta_{t+1}(j)a_{ij}\right]b_{jx_{t+1}},\; t \in \lbrace T-1,...,1 \rbrace,1\le i \le N $
5  $\quad \theta_{t}(i)=\left[\sum_{j=1}^N \theta_{t-1}(j)a_{ji}\right]b_{ix_{t}}$
6  $\quad$计算$\xi_t(i,j),\eta_t(i), 1\le i,j \le N,1 \le t \le T$
7  $\quad $更新参数：
8  $\quad \pi=\eta_1(i),1\le i \le N$
9  $\quad a_{ij}=\frac{\sum_{t=1}^{T-1}\xi_t(i,j)}{\sum_{t=1}^{T-1}\eta_t(i)},1\le i,j \le N$
10 $\quad b_{jk}=\frac{\sum_{t=1,x_t=k}^T\quad \eta_t(j)} {\sum_{t=1}^{T}\eta_t(j)} ,1\le j \le N,1\le k \le M$
11 输出HMM：$\lambda=(A,B,\pi)$

$o_t=k$表示$t$时刻的观测值为第$k$种观测值。停止条件可以是：参数$\lambda=(A,B,\pi)$收敛。

---

