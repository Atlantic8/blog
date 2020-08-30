---
title: Conditional Random Field
date: 2017-08-27 14:19:20
tags: [machine learning]
categories: Algorithm
mathjax: true
---

#### CRF
同朴素贝叶斯一样，HMM是生成式模型。它可以做线性序列预测分析，为了计算复杂度上的可行性，其**假设观测变量仅依赖于隐含变量**。然而，实际中**观测变量之间也存在不可忽略的依赖关系**，这导致HMM的假设会严重影响模型的精确性。


CRF现在是自然语言处理领域中多个任务的state-of-art方法，包括分词、词性标注，浅解析（shallow parsing）等。并且在命名实体识别、基因预测、图像标注、物体识别等领域有着重要的应用。

CRF是**判别**式模型。

---

##### 概率图模型
一般地，在概率图模型中，节点表示随机变量，边表示依赖关系。概率图模型的表示的前提是对图的划分，也就是因子分解，可以按有向图和无向图分别讨论。
###### 马尔可夫性
给定一个随机变量$y$及其联合概率分布$p(y)$和它的无向图表示$G$，下面给出关于马尔可夫性的三个等价定义。
- 成对马尔可夫性：设$u,v$是无向图中没有连接的两个点，$o$是其他节点，则有$p(u,v|o)=p(u|o)p(v|o)$
- 局部马尔可夫性：设$u$是无向图中任意一个节点，$w$是与$u$有连接的节点，$o$是其他节点，则有$p(v,o|w)=p(v|w)p(o|w)$
- 全局马尔可夫性：设$u,v$是被节点集$o$分隔开的任意节点集合，则有$p(u,v|o)=p(u|o)p(v|o)$

总结一下意思就是：**无连接的变量在以中继变量为条件的情况下相互独立**。

###### 有向图
定义在有向图上的条件概率模型的联合分布为**所有节点条件概率的乘积**，比如贝叶斯网络，马尔可夫链等。

---

###### 无向图
满足马尔可夫性的联合概率分布被称为概率无向图模型，也叫做**马尔可夫随机场**。定义在无向图上的条件概率模型的联合分布为**最大团上非负函数的乘积**（这也称为概率无向图模型的因子分解）。这里最大团（极大团）指的是不能再添加节点的团（团指的是两两相交的节点集）。形式化定义单个节点$v$的概率为$v$在所有最大团上的乘积，即
$$
\begin{aligned}
p(v)=\frac{1}{Z}\prod_{c\in C}\Psi_c(v_c)
\end{aligned}
$$
其中$\Psi_c(v_c) \ge 0$称为节点$v$在团$c$上的势函数。$Z$是归一化因子满足$Z=\sum_vp(v)$（其实最大熵模型也可以看成是势函数的乘积）。

---

#### CRF的表示
CRF是定义在无向图上的判别式模型，是给定随机变量$x$的条件下，随机变量$y$的马尔可夫随机场。按照无向图上的定义，可以有
$$
\begin{aligned}
p(y|x)&=\frac{p(x,y)}{p(x)}=\frac{p(x,y)}{\sum_{y'}p(x,y')} \\
&=\frac{\frac{1}{Z}\prod_{c\in C}\Psi_c(x_c,y_c)}{\frac{1}{Z}\sum_{y'}\prod_{c\in C}\Psi_c(x_c,y'_c)} \\
&=\frac{1}{Z(x)}\prod_{c\in C}\Psi_c(x_c,y_c)
\end{aligned}
$$
这就是CRF的基本形式。下面分别介绍线性链CRF和任意结构的CRF。

##### 线性链CRF
CRF的一种特殊形式，也是比较常用的形式-线性链式。在这种情况下，相邻点变成了最大团，即满足马尔可夫性
$$
\begin{aligned}
p(y_i|x,y_1,..,y_{i-1},y_{i+1},...,y_{n+1})=p(y_i|x,y_{i-1},y_{i+1})
\end{aligned}
$$
假设$x=(x_1,...x_{n+1})$，$y=(y_1,...y_{n+1})$（都是向量），链的长度为$n+1$，所以最大团的数量为$n$，上式就可以写成：
$$
\begin{aligned}
p(y|x)=\frac{1}{Z(x)}\prod_{j=1}^n\Psi_j(x,y)
\end{aligned}
$$
给定势函数$\Psi_j(x,y)$的形式为
$$
\begin{aligned}
\Psi_j(x,y)=\exp\left(\sum_{i=1}^m\lambda_if_i(x,y_{j-1},y_j,j)\right)
\end{aligned}
$$
其中，$j$表示序列位置（与$n$相关）。所以线性链的CRF可以表示为
$$
\begin{aligned}
p_{\lambda}(y|x)&=\frac{1}{Z_{\lambda}(x)}\cdot \exp\left( \sum_{j=1}^n \sum_{i=1}^m\lambda_if_i(x,y_{j-1},y_j,j) \right) \\
&=\frac{1}{Z_{\lambda}(x)}\prod_{j=1}^n \exp\left( \sum_{i=1}^m\lambda_if_i(x,y_{j-1},y_j,j) \right)
\end{aligned}
$$
其中，$Z_{\lambda}(x)$就是在$y$上对$p_{\lambda}(y|x)$求和的结果，这结构与最大熵的形式类似。

---

与HMM的模式类似，应用模型之前还需要解决一些问题，分别是
1. 给定序列集合$X$和对应的标注数据$Y$，如何训练CRF模型参数使得$p(Y|X,\mathcal{M})$最大
2. 给定模型$\mathcal{M}$和输入序列$X$，如何求输出序列$Y$

这里就不考虑求$p(X|\mathcal{M})$了，因为CRF是**判别式**模型。

---

###### 模型训练
目标是估计参数$\lambda$。给定数据集$T$，参数估计常用的方法就是MLE了，我们再取一个log，考虑regularization，推导如下：
$$
\begin{aligned}
\mathcal{L}(T)&=\sum_{(x,y)\in T}\log p(y|x) - \frac{1}{2\sigma^2}||\lambda||_2^2 \\
&=\sum_{(x,y)\in T} \log\left( \frac{\exp\left(\sum_{j=1}^n \sum_{i=1}^m\lambda_if_i(x,y_{j-1},y_j,j)\right)}{\sum_{y'}\exp\left(\sum_{j=1}^n \sum_{i=1}^m\lambda_if_i(x,y'_{j-1},y'_j,j)\right) } \right) - \frac{1}{2\sigma^2}\sum_{i=1}^m\lambda_i^2 \\
&=\sum_{(x,y)\in T}\sum_{j=1}^n \sum_{i=1}^m\lambda_if_i(x,y_{j-1},y_j,j) - \sum_{(x,y)\in T}\log Z_{\lambda}(x) - \frac{1}{2\sigma^2}\sum_{i=1}^m\lambda_i^2
\end{aligned}
$$
这里$\sigma^2$是控制regularization权重的超参数。上式可分为3部分，分别对$\lambda_k$求导
$$
\begin{aligned}
\frac{\partial}{\partial\lambda_k}\sum_{(x,y)\in T}\sum_{j=1}^n \sum_{i=1}^m\lambda_if_i(x,y_{j-1},y_j,j)&=\sum_{(x,y)\in T}\sum_{j=1}^n f_k(x,y_{j-1},y_j,j) \\
&=N\cdot\hat{E}(f_k)
\end{aligned}
$$
其结果刚好是训练数据集上特征$f_i$的期望值的$N$（训练集数据个数*(n+1)）倍。

---

$$
\begin{aligned}
&\frac{\partial}{\partial\lambda_k}\sum_{(x,y)\in T}\log Z_{\lambda}(x)=\sum_{(x,y)\in T}\frac{1}{Z_{\lambda}(x)}\frac{\partial Z_{\lambda}(x)}{\partial\lambda_k} \\
&=\sum_{(x,y)\in T}\frac{1}{Z_{\lambda}(x)} \frac{\partial}{\partial\lambda_k}\sum_{y'}\exp\left(\sum_{j=1}^n \sum_{i=1}^m\lambda_if_i(x,y'_{j-1},y'_j,j)\right) \\
&=\sum_{(x,y)\in T}\frac{1}{Z_{\lambda}(x)} \sum_{y'}\left[\exp\left(\sum_{j=1}^n \sum_{i=1}^m\lambda_if_i(x,y'_{j-1},y'_j,j)\right)\cdot \sum_{j=1}^n f_k(x,y'_{j-1},y'_j,j)\right] \\
&=\sum_{(x,y)\in T}\sum_{y'}p_{\lambda}(y'|x)\sum_{j=1}^n f_k(x,y'_{j-1},y'_j,j) \\
&=N\cdot E(f_k)
\end{aligned}
$$
上面倒数第二行第一个求和符号的范围可以退化成$x\in X$，其结果刚好是模型分布上特征$f_i$的期望值的$N$（训练集数据个数*(n+1)）倍。

---

$$
\begin{aligned}
\frac{\partial}{\partial\lambda_k}\frac{1}{2\sigma^2}\sum_{i=1}^m\lambda_i^2=\frac{\lambda_k}{\sigma^2}
\end{aligned}
$$

---

综上，我们可以得到
$$
\begin{aligned}
\frac{\partial \mathcal{L}(T)}{\partial \lambda_k}=N\cdot(\hat{E}(f_k)-E(f_k))-\frac{\lambda_k}{\sigma^2}
\end{aligned}
$$
继而，令上式等于0，就可以求出$\lambda_k$的值。这里，$\hat{E}(f_k)$可以通过简单的统计特征$f_k$在数据集中的出现的次数实现。而想要直接计算$E(f_k)$就不容易了，因为CRF这里处理的是序列数据，序列组合导致可能性指数上升。

---

解决方法是利用HMM也用到的**前后向算法**的修改版。
定义函数$T_j(s)$为状态$s$在输入位置$j$时，位置$j+1$的可能状态集合。定义函数$T_j^{-1}(s)$为$T_j(s)$的反函数，即输出状态$s$的前置集合。定义序列初始状态为$\vdash$，终止状态为$\dashv$。在此基础上定义**前向、后向函数**：
- 前向函数：$\alpha_j(s|x)=\sum_{s'\in T_j^{-1}(s)}\alpha_{j-1}(s'|x)\cdot \Psi_j(s',s,x)$，初始化$\alpha_0(\vdash|x)=1$
- 后向函数：$\beta_j(s|x)=\sum_{s'\in T_j(s)}\beta_{j+1}(s'|x)\cdot \Psi_j(s,s',x)$，初始化$\beta_{|x|+1}(\dashv|x)=1$

其中，与上文的势函数对应，$\Psi_j(s',s,x)=\exp(\sum_{i=1}^m\lambda_if_j(y_{i-1}=s',y_i=s,x,j))$。根据前向、后向函数的定义，可以有
$$
\begin{aligned}
p(y_j=s|x)= \frac{\alpha_j(s|x)\beta_j(s|x)}{Z_{\lambda}(x)}
\end{aligned}
$$
因此，$E(f_k)$的计算就变得可行了
$$
\begin{aligned}
E(f_k)&=\sum_{(x,y)\in T}\frac{1}{Z_{\lambda}(x)}\sum_{j=1}^n\sum_{s\in S}\sum_{s'\in T_j(s)} f_j(s,s',x,j)\alpha_j(s|x)\Psi_j(s,s',x)\beta_{j+1}(s'|x) \\
Z_{\lambda}(x)&=\beta_0(\vdash|x)=\alpha_{|x|+1}(\dashv|x)
\end{aligned}
$$
其中$S$是状态集合。这相当于计算了所有可能状态序列的可能，$\alpha, \beta$的值只需要计算一次，存储起来就好。前后向算法的时间复杂度为$O(|S|^2n)$。

至此，$\lambda$的更新变得可行，模型训练ok。

---

###### 序列标注
序列标注即要在给定模型参数情况下找到输入序列对应的概率最大的标注序列，可以采用维特比算法的思想。定义: **$\delta_j(s|x)$表示序列到位置$j$时，状态为$s$的最大概率**，即
$$
\begin{aligned}
\delta_j(s|x)=\max_{y_1,..,y_{j-1}}p(y_1,...,y_{j-1},y_j=s|x)=\max_{s'\in S}\delta_{j-1}(s')\cdot \Psi_j(s',s,x)
\end{aligned}
$$
还需要**数组$\phi_j(s)$记录下$j$位置状态为$s$时$j-1$位置的状态是什么**。
算法的步骤如下：

---

1. 从开始状态初始$\vdash$化，对所有的状态$s\in S$，令
    $\delta_1(s|x)=\Psi_1(\vdash,s,x)$.
    $\phi_1(s)=\vdash$
2. 递归计算，对每一个$s\in S, 1\le j\le n$
    $\delta_j(s|x)=\max_{s'\in S}\delta_{j-1}(s')\cdot \Psi_j(s',s,x)$
    $\phi_j(s)=arg\max_{s'\in S}\delta_{j-1}(s')\cdot \Psi_j(s',s,x)$
3. 结束迭代
    $p_{max}=\max_{s'\in S}\delta_{n}(s')$
    $y_n=arg\max_{s'\in S}\delta_n(s'|x)$
4. 回溯
    根据$\phi$数组和$y_n$求出整个$y$序列。

---

##### 任意结构CRF
> TODO







**参考文献**
[1]. Classical Probabilistic Models and Conditional Random Fields.pdf
