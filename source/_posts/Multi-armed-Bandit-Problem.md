---
title: Multi-armed Bandit Problem
date: 2017-01-06 10:22:34
tags: [Game Theory, machine learning]
categories: Algorithm
---

###### 背景描述
多臂老虎机问题来源于赌场，描述的是赌场中的一个赌徒，面对多个老虎机（多个摇臂），如何选择使用摇臂才能使自己的收益最大化的问题。想要最大化收益，赌徒需要知道每个摇臂对应的奖赏，然后选择下一次应该使用哪个摇臂。然而现实中，摇臂对应的奖赏往往不是一个确定的值，而是服从于某个分布的。这个问题属于强化学习研究的范畴。

对于每一次使用摇臂的机会，赌徒有两种选择:
1) 探索策略(exploration)：尝试新的摇臂以确定新的要比对应的奖赏
2) 利用策略(exploitation)：使用当前已知最好的摇臂
探索策略能很好估计每个摇臂的奖赏，却会失去很对选择好的摇臂的机会；而利用策略则相反，它只使用当前最好的选择，可能会错过最佳摇臂。这两个策略的出发点相同，但是操作上是相悖的，所以解决多臂老虎机问题可以从对这两个问题的折中上入手。

---

###### $\epsilon$-贪心
<b>$\epsilon$-贪心法的思想是：每次尝试时，以$\epsilon$的概率进行搜索（均匀搜索），以$1-\epsilon$的概率利用现有最佳。</b>

令$Q(k)$表示摇臂$k$的平均奖赏，摇臂$k$被使用了$n$次，收益分别是$v_1,v_2,...,v_n$，所以$Q(k)$可以表示成
$$
\begin{aligned}
Q(k)=\frac{1}{n} \sum_{i=1}^n v_i
\end{aligned}
$$
每次获得一个摇臂对应的奖赏，则更新其平均奖赏，这个只需要记录摇臂尝试次数和当前平均值即可进行下一次平均值的计算。算法描述如下：

---

输入：摇臂个数$K$，奖赏函数$R$，尝试次数$T$，搜索概率$\epsilon$

---

1 $r=0$.
2 $\forall i=1,...,K:set\;Q(i)=0,count(i)=0$.
3 $for\;t=1,...,T$
4 $\quad if\;rand()<\epsilon$
5 $\quad \quad k \xleftarrow{均匀选取} \lbrace 1,...,K \rbrace$.
6 $\quad else$
7 $\quad \quad k=\arg\max_i Q(i)$.
8 $\quad v=R(k)$.
9 $\quad r=r+v$.
10 $\quad Q(k)=\frac{Q(k)\times count(k)+v}{count(k)+1}$.
11 $\quad count(k)=count(k)+1$.

---

输出：累计奖励$r$

---

如果摇臂奖赏的不确定性较大，则需要更多的探索，对应的$\epsilon$也应该更大。反之，较小的$\epsilon$比较合适。当尝试次数非常大时，摇臂的奖赏可能都能很好地表示出来，而不再需要探索。为了防止问题退化，可让$\epsilon$随着尝试次数地增加而减少，比如$\epsilon=\frac{1}{\sqrt{t}}$。

---

###### Softmax
Softmax根据当前已知摇臂的平均奖赏对探索和利用进行折中，令$Q(k)$表示摇臂$k$的平均奖赏，摇臂概率的分布基于波尔兹曼分布
$$
\begin{equation}
P(k)=\frac{e^{\frac{Q(k)}{\tau}}} {\sum_{i=1}^K e^{\frac{Q(k)}{\tau}}}
\end{equation}
$$
其中，$\tau > 0$称为温度，$\tau$越小则平均奖赏高的摇臂被选取的概率越高。$\tau$趋近于0时，算法倾向于仅利用，$\tau$趋近于无穷大时，算法倾向于仅探索。Softmax算法描述如下：

---

输入：摇臂个数$K$，奖赏函数$R$，尝试次数$T$，温度参数$\tau$

---

1 $r=0$.
2 $\forall i=1,...,K:set\;Q(i)=0,count(i)=0$.
3 $for\;t=1,...,T$
4 $\quad$根据式$(1)$选取$k\gets \lbrace 1,...,K \rbrace$.
5 $\quad v=R(k)$.
6 $\quad r=r+k$.
7 $\quad Q(k)=\frac{Q(k)\times count(k)+v}{count(k)+1}$.
8 $\quad count(k)=count(k)+1$.

---

输出：累计奖励$r$

---

---

$\epsilon$-贪心和Softmax的优劣与应用相关，下图就是例子。

<center>![不同算法在不同尝试次数上的效果](http://wx1.sinaimg.cn/mw690/9bcfe727ly1fbgwaininnj213j0q0gv3.jpg)</center>

