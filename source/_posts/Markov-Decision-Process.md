---
title: Markov Decision Process
date: 2017-01-06 10:07:53
tags: [machine learning]
categories: Algorithm
---

马尔可夫决策过程MDP是经典的增强学习算法。MDP可以表示为一个元组$$MDP=(S,A,\lbrace P_{sa} \rbrace,\gamma,R)$$其中$S$是状态集合；$A$是动作集合，也就是可能的操作集合；$P_{sa}$为每一个状态$s$在每一个动作$a$上定义转移概率，转移到不同状态的概率不同；$\gamma \in [0,1]$为折扣因子；$R:S\times A \to \mathbb{R}$表示回报函数。

<center>![MDP模型](http://ww2.sinaimg.cn/large/9bcfe727jw1fbgomcnv49j20b408wwf9.jpg)</center>

---

##### 贝尔曼方程（Bellman equation）


贝尔曼方程是理查德贝尔曼提出的，它是典型的动态规划方程，也是动态规划最优性的必要条件。贝尔曼方程在最优控制理论中有着重要的作用。理查德贝尔曼证明了离散时间上的动态规划问题可以被表示成递归的、一步一步完成的后向推导形式，其中这过程需要写出价值函数的递推关系，其实贝尔曼方程的最基本思想就是<b>重叠子问题思想</b>。代价函数的递推关系被称为贝尔曼方程，其形式化表述如下。

假设时刻$t$时的状态为$s_t$，采取的动作是$a_t$，到达的新状态可以计算成$T(s_t,a_t)$，对应的收益为$F(s_t,a_t)$。联系折扣因子$\beta$，从$s_0$开始的无穷决策问题的收益是
$$
\begin{aligned}
V(s_0)=\max_{\lbrace a_t \rbrace_{t=0}^{\infty}} \sum_{t=0}^{\infty} \beta^tF(s_t,a_t) \\
s.t.:\; s_{t+1}=T(s_t,a_t)
\end{aligned}
$$
上是可以简化为
$$
\begin{aligned}
V(s_0)=\max_{a_0} \lbrace F(s_0,a_0)+\beta V(s_1) \rbrace,\;s.t.:\;s_1=T(s_0,a_0)
\end{aligned}
$$

---

##### MDP模型描述

---

###### MDP形式定义
MDP可表示成这样的过程
$$
\begin{aligned}
s_0 \xrightarrow{a_0} s_1 \xrightarrow{a_1} s_2 \xrightarrow{a_2} s_3 \xrightarrow{a_3} ...
\end{aligned}
$$
在上面的情况下，整体收益可以表示成
$$
\begin{aligned}
R(s_0,a_0)+\gamma R(s_1,a_1) + \gamma^2 R(s_2,a_2) + ...
\end{aligned}
$$
MDP的目标就是<b>选取一组动作以最大化收益均值</b>即
$$
\begin{aligned}
\arg \max_{a_0,a_1,...}E[R(s_0,a_0)+\gamma R(s_1,a_1) + \gamma^2 R(s_2,a_2) + ... ]
\end{aligned}
$$

一个策略（policy）是由状态到动作的任意映射$\pi : S \to A$。执行一个策略$\pi$也就是对于任意状态$s$，系统采取的动作是$a=\pi(s)$。定义一个策略$\pi$的<b>价值函数（value function）</b>为
$$
\begin{aligned}
V^{\pi}(s)&=E[R(s_0,a_0)+\gamma R(s_1,a_1) + \gamma^2 R(s_2,a_2) + ... |s_0=s,\pi] \\
V^{\pi}(s)&=R(s)+\gamma \sum_{s^{'}\in S}P_{s\pi(s)}(s^{'})V^{\pi}(s^{'})
\end{aligned}
$$
表示从状态$s$开始，根据策略$\pi$执行的累积收益和的均值。
定义最优价值函数为
$$
\begin{aligned}
V^{\*}(s)&=\max_{\pi} V^{\pi}(s) \\
V^{\*}(s)&=R(s)+\max_{a\in A}\gamma \sum_{s^{'}\in S}P_{sa}(s^{'})V^{\*}(s^{'})
\end{aligned}
$$
指的是任何可能的策略下的最优解.

接下来定义<b>最优策略</b>，一个最优策略$\pi^{\*}:S \to A$可以定义为
$$
\begin{equation}
\pi^{\*}(s)=\arg\max_{a\in A}\sum_{s^{'}\in S}P_{sa}(s^{'})V^{\*}(s^{'})
\end{equation}
$$
策略$\pi^{\*}$为每一个状态提供了最优策略，也就是说无论初始状态是什么，$\pi^{\*}$都是最优策略。事实上，对每一个状态$s$和每一个策略$\pi$，我们有
$$
\begin{aligned}
V^{\*}(s)=V^{\pi^{\*}}(s) \ge V^{\pi}(s)
\end{aligned}
$$

---

###### 价值迭代和策略迭代
为了描述简单，这里仅考虑有限状态空间、有限动作空间的MDP。在下面两个算法中，转移概率$\lbrace P_{sa} \rbrace$和回报函数$R$都是已知的。

---

价值迭代（value iteration）
1 初始化每个状态的价值$V(s)=0$
2 重复迭代直到收敛：
3 $\quad$对每个状态$s$，更新：$V(s)=R(s)+\max_{a\in A}\gamma \sum_{s^{'}}P_{sa}(s^{'})V(s{'})$

---

其中，更新方式有两种
同步更新：先计算所有状态的价值函数，然后再将其一起更新
异步更新：每计算出一个状态的价值函数，就将其更新
但无论是同步还是异步，$V$都会逐渐收敛至$V^{\*}$。有了$V^{\*}$，就可以根据公式$(1)$计算出对应的策略了。

---

策略迭代（policy iteration）
1 随机初始化$\pi$
2 重复迭代直到收敛：
3 $\quad (a):$使得$V=V^{\pi}$
4 $\quad (b):$对每个状态$s$，使得$\pi(s)=\arg\max_{a\in A}\sum_{s^{'}}P_{sa}(s^{'})V(s^{'})$

---

迭代过程中，先计算在当前策略$\pi$下每个状态的价值函数值，然后根据这些值找到每个状态对应的最佳动作（greedy）。这些动作的集合就构成了下一步的新策略。步骤$(a)$的计算还是先赋值再迭代计算直到收敛，只是要按照$\pi$策略跳转而已。

---

###### 学习一个MDP模型
上面的讨论中，转移概率$\lbrace P_{sa} \rbrace$和回报函数$R$都是已知的，但是实际中这两部分经常是未知的（通常$S,A,\gamma$是已知的），因此需要通过学习算法来学习。

数据可以是采集的，也可以是通过实验得出来的。对$P_{sa}$的估计方法可以是
$$
\begin{aligned}
P_{sa}(s^{'})=\frac{times\; s \xrightarrow{a} s^{'}}{times\; s \xrightarrow{a} any\; state}
\end{aligned}
$$
在样本不够大的情况下，可能出现$\frac{0}{0}$的情况，如果分母为0，则把对应的概率换成$\frac{1}{\vert S\vert}$.

$R$的更新思想类似。

---

##### 连续状态的MDP
现实中，MDP的离散状态假设是比较脆弱的。比如二维坐标中的位置就是连续的。那如何处理连续状态下的MDP呢

---

###### 离散化
离散化的思想很直观，比如二维空间就可以通过网格化来达到离散化的目的。但是离散化有两个缺陷：
<b>1 naive representation</b>
对于$V^{\*}$和$\pi^{\*}$的表示太过简单，因为离散化会主动放弃潜在信息因此对平滑函数的表示效果比较差。比如离散化后的线性回归可能会得到如下图中的结果

<center>![](http://ww3.sinaimg.cn/large/9bcfe727jw1fbfzpl9gu1j20cf09dq34.jpg)</center>

<b>2 维度诅咒</b>
假设状态空间是$n$维的，离散化会使得离散化后的状态个数指数增加。

---

###### 价值函数近似
一般地，在连续MDP问题中通常假设

在价值迭代中，连续状态的迭代公式应该是
$$
\begin{aligned}
V(s)&= R(s)+\gamma \max_{a} E_{s^{'}\sim P_{sa}}[V(s_{'}] \\
&= R(s)+\gamma \max_{a} \int_{s^{'}}P_{sa}(s^{'})V(s^{'})\,ds^{'}
\end{aligned}
$$
此式跟上面的区别是把原来的求和改成了积分。

在对应状态为$s^{(1)},s^{(2)},...,s^{(m)}$的有限个数样本情况下，<b>价值函数近似就是要将价值函数近似为状态的函数</b>，即
$$
\begin{aligned}
V(s)=\theta^T\phi(s)
\end{aligned}
$$
其中$\phi(s)$是状态$s$的合理映射。对于每一个样本$i$，算法先计算一个
$$
\begin{aligned}
y^{(i)} \gets R(s)+\gamma \max_{a} E_{s^{'}\sim P_{sa}}[V(s_{'}]
\end{aligned}
$$
上式的计算要使用采样逼近的原理，即采集多个样本求均值以逼近收集到每个样本的状态和对应的$y^{(i)}$，就可以使用监督学习算法训练出$V(s)$和$s$的模型。算法描述如下

---

1 随机采样$m$个状态，$s^{(1)},s^{(2)},...,s^{(m)} \in S$.
2 初始化$\theta=0$.
3 迭代：
4 $\quad for\;i=1,...,m$.
5 $\quad \quad for\;each\;a\in A$.
5 $\quad \quad \quad $采样$s_1^{'},...,s_k^{'} \sim P_{s^{(i)}a}$.
6 $\quad \quad \quad $设置$q(a)=\frac{1}{k} \sum_{j=1}^k R(s^{(i)})+\gamma V(s_j^{'})$.
7 $\quad \quad \quad $//因此$q(a)$就是$R(s^{(i)})+\gamma E_{s^{'}\sim P_{s^{(i)}a}}[V(s_{'}]$的估计.
8 $\quad \quad $令$y^{(i)}=\max_{a}q(a)$.
9 $\quad \quad $//因此$q(a)$就是$R(s^{(i)})+\gamma \max_{a} E_{s^{'}\sim P_{s^{(i)}a}}[V(s_{'}]$的估计.
10 $\quad$使得$\theta=\arg\min_{\theta}\frac{1}{2} \sum_{i=1}^m (\theta^T\phi(s^{(i)})-y^{(i)})^2$.

得到了近似于$V^{\*}$的$V$，最后选择action时还是根据
$$
\begin{aligned}
\arg\max_{a} E_{s^{'}\sim P_{sa}}[V(s^{'})]
\end{aligned}
$$

---

上述算法最后求$\theta$时使用的是线性回归方法，当然其他合适的方法也是可以的。
需要注意的是，价值函数近似方法并不能保证收敛，但是通常是收敛得。控制计算量的可用方法是调节算法第5步中的$k$值，有时候设置$k=1$也是可以的。
