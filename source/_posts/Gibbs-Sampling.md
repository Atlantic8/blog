---
title: Gibbs Sampling
date: 2016-11-16 15:39:21
tags: random algorithm
categories: Algorithm
---
##### 蒙特卡洛数值积分
如果我们要求f(x)的积分$ \int_a^b f(x) \,dx $，而f(x)的形式比较复杂积分不好求，则可以通过数值解法来求近似的结果。常用的方法是蒙特卡洛积分:$$\int_a^b \frac{f(x)}{q(x)}q(x) \,dx$$这样把q(x)看做是x在区间内的概率分布，而把前面的分数部门看做一个函数，然后在q(x)下抽取n个样本，当n足够大时，可以用采用均值来近似:$$\frac{1}{n}\sum_{i}\frac{f(x_i)}{q(x_i)}$$因此只要q(x)比较容易采到数据样本就行了。随机模拟方法的核心就是如何对一个概率分布得到样本，即抽样（sampling）.

##### Box-Muller 变换
如果随机变量 $U_1,U_2$ 独立且$U_1,U_2 ∼ Uniform[0,1]$，如果有：$$Z_0=\sqrt{-2lnU_1}cos(2\pi U_2)$$ $$Z_1=\sqrt{-2lnU_1}sin(2\pi U_2)$$ 则 $Z_0,Z_1$ 独立且服从标准正态分布。

##### Monte Carlo principle
X 表示随机变量，服从概率分布 p(x), 那么要计算 f(x) 的期望，只需要我们不停从 p(x) 中抽样$x_i$，然后对这些$f(x_i)$取平均即可近似f(x)的期望:$$E(f)=\frac{1}{N}\sum_{i=1}^Nf(x^i)$$其中$E(f)$即为f的期望。
<center>![](http://ww4.sinaimg.cn/large/9bcfe727jw1f9u6nr4wtmj20cx08ht98.jpg)</center>

##### 接受-拒绝抽样（Acceptance-Rejection sampling)
有时候，p(x)是很难直接采样的的。
既然 p(x) 太复杂在程序中没法直接采样，那么我设定一个程序可抽样的分布 q(x) 比如高斯分布，然后按照一定的方法拒绝某些样本，达到接近 p(x) 分布的目的，其中q(x)叫做 proposal distribution。
具体操作如下，设定一个方便抽样的函数 q(x)，以及一个常量 k，使得 p(x) 总在 kq(x) 的下方。
- x 轴方向：从 q(x) 分布抽样得到 a。(如果是高斯，就用之前说过的 tricky and faster 的算法更快）
- y 轴方向：从均匀分布（0, kq(a)) 中抽样得到 u。
- 如果刚好落到灰色区域： u > p(a), 拒绝， 否则接受这次抽样
- 重复以上过程

在高维的情况下，Rejection Sampling 会出现两个问题，第一是合适的 q 分布比较难以找到，第二是很难确定一个合理的 k 值。这两个问题会导致拒绝率很高，无用计算增加。
<center>![](http://ww2.sinaimg.cn/large/9bcfe727jw1f9u6s3wo7hj20fa07vdgd.jpg)</center>


##### 马尔科夫稳态
马氏链即马尔可夫链。社会学家经常把人按其经济状况分成3类：下层(lower-class)、中层(middle-class)、上层(upper-class)，我们用1,2,3 分别代表这三个阶层。社会学家们发现决定一个人的收入阶层的最重要的因素就是其父母的收入阶层。如果一个人的收入属于下层类别，那么他的孩子属于下层收入的概率是 0.65, 属于中层收入的概率是 0.28, 属于上层收入的概率是 0.07。事实上，从父代到子代，收入阶层的变化的转移概率如下：
<center>![](http://ww3.sinaimg.cn/large/9bcfe727jw1f9u6zizzbaj20ch06hq2y.jpg)</center>

经过迭代，三种阶层的状态converge to

	[0.286, 0.489, 0.225]

<b>马氏链定理</b>
<center>![](http://ww1.sinaimg.cn/large/9bcfe727jw1f9u72rq6c8j20fa0btwfv.jpg)</center>

##### Markov Chain Monte Carlo (MCMC)

由于马氏链能收敛到平稳分布， 于是一个很的漂亮想法是：如果我们能构造一个转移矩阵为P的马氏链，使得该马氏链的平稳分布恰好是p(x), 那么我们从任何一个初始状态$x_0$出发沿着马氏链转移, 得到一个转移序列 $x_0,x_1,x_2,⋯x_n,x\_{n+1}⋯$,， 如果马氏链在第n步已经收敛了，于是我们就得到了 π(x) 的样本$x_n,x\_{n+1}⋯$。这是Metropolis算法的基本思想。MCMC 算法是 Metropolis 算法的一个改进变种，马氏链的收敛性质主要由转移矩阵P 决定, 所以基于马氏链做采样的关键问题是如何构造转移矩阵P,使得平稳分布恰好是我们要的分布p(x)。
<center>![](http://ww2.sinaimg.cn/large/9bcfe727jw1f9u7negt9mj20fa0f7tcc.jpg)</center>
假设我们已经有一个转移矩阵Q(对应元素为q(i,j)), 用于采样概率分布p(x)的算法如下：
<center>![](http://ww1.sinaimg.cn/large/9bcfe727jw1f9u7psj1wdj20fa06nmxc.jpg)</center>
<center>![](http://ww2.sinaimg.cn/large/9bcfe727jw1f9u7qj49bbj20fa0fk42d.jpg)</center>
<center>![](http://ww3.sinaimg.cn/large/9bcfe727jw1f9u7r9o55vj20fa07emxe.jpg)</center>


##### MCMC —— Gibbs Sampling算法
<center>![](http://ww1.sinaimg.cn/large/9bcfe727jw1f9u7s3xbp5j20fa0ddmzx.jpg)</center>
<center>![](http://ww1.sinaimg.cn/large/9bcfe727jw1f9u7sldz89j20ad08qgls.jpg)</center>
<center>![](http://ww4.sinaimg.cn/large/9bcfe727jw1f9u7tgi99tj20fa082q4m.jpg)</center>
<center>![](http://ww2.sinaimg.cn/large/9bcfe727jw1f9u7ueeigyj20fa0f1wj6.jpg)</center>
<center>![](http://ww3.sinaimg.cn/large/9bcfe727jw1f9u7uy86ffj20fa08oaa7.jpg)</center>

以上算法收敛后，得到的就是概率分布$p(x_1,x_2,⋯,x_n)$的样本。
