---
title: Latent Dirichlet Allocation
date: 2017-03-31 10:16:10
tags: [machine learning, NLP]
categories: Algorithm
---

##### TF-IDF
问题的起源是文档排名，就像使用搜索引擎那样，给定关键字，返回排好序的文档列表。既然提到排序，就肯定有衡量标准，给定关键词，一个文档的重要性或者说相关性如何度量呢？

###### TF
首先，直观地，如果一篇文档中出现要查询的词的次数越多，相关性应该越大。于是很容易想到**`词频(TF)`**这个标准

	词频TF(t)就是关键词t在文档中出现的次数

###### IDF
但是仅仅考虑词频必然会出现问题，因为不同的词应该有不同的重要性，举个例子：在计算机科学类的paper中，出现算法和文学类paper中出现算法的重要性是不一样的，又或者“的”这个字在汉语中出现的次数相当大，一篇文档中没有“的”字的概率是很小的，此时仅仅按照关键词中的“的”判断文档排名显然是不准确的。于是，我们希望加大稀缺词的权重，所以定义了**`逆文档频率(IDF)`**，`IDF`的定义如下$$IDF(t) = log\frac{N} {DF(t)} $$其中，$N$为文档总数，$DF(t)$为所有文档中出现了关键词$t$的文档个数。所以，越是普遍的单词（“的”，“因此”等）`IDF`越小，而稀缺的单词（如文学paper中的“算法”）就对应着比较大的`IDF`。

将TF和IDF结合到一起，得到TF-IDF的计算方法：$$TF-IDF(t,d) = TF(t,d) * IDF(t)$$所以，**一篇文档和一条Query的相关度为Query中所有单词在这篇文档中的TF-IDF值之和**。而**两个文档间的相关度是文档向量的余弦值**，余弦值越接近1，就表明夹角越接近0度，也就是两个向量越相似，这就叫"余弦相似性"。

###### TF-IDF的缺陷
- 单纯地认为文本频数小的单词就越重要，文本频数大的单词就越无用，并不是完全正确的
- 不能有效地反映单词的重要程度和特征词的分布情况，TF-IDF的精度并不是很高
- 没有体现出单词的位置信息，这也是空间向量模型的不足

#### 主题模型
TF-IDF模型中没有考虑文字背后的语义关联，即语义层面上的关联，可能在两个文档共同出现的单词很少甚至没有，但两个文档是相似的。判断文档相关性的时候需要考虑到文档的语义，而语义挖掘的利器是主题模型，LDA就是其中一种比较有效的模型。

主题模型的思想源于生成模型，其思想如下：**一篇文章的每个词都是通过：以一定概率选择了某个主题，并从这个主题中以一定概率选择某个词语**，形式化表述为$$p(word|doc)=\sum_{topic}p(word|topic)\times p(topic|doc)$$，具体内容在下文中描述。

能够发现文档-词语之间所蕴含的潜在语义关系（即主题）——将文档看成一组主题的混合分布，而主题又是词语的概率分布——从而**将高维度的“文档-词语”向量空间映射到低维度的“文档-主题”和“主题-词语”空间**，有效提高了文本信息处理的性能。

##### 基础知识
###### 二项分布（Binomial distribution）
$n$次重复伯努利试验，一次概率为$p$，$k$次试验概率函数为$$P(K=k)=C_n^kp^k(1-p)^{n-k}$$，二项分布计为$X\sim b(n,p)$。

###### 多项式分布
每次试验可能有$k$种结果，每种结果的可能性是$p_i$，则$n$次试验各种结果出现次数分别为$x_1,...,x_k$的概率是
$$
\begin{aligned}
P(x_1,...,x_k;n,p_1,...,p_k)=\frac{n!}{x_1!...x_k!}p_1^{x_1}...p_k^{x_k}
\end{aligned}
$$
是二项分布的扩展。

###### gamma函数
gamma函数形如$$\Gamma(x)=\int_0^{\infty}t^{x-1}e^{-t}dt$$这个函数有如下性质$\Gamma(x+1)=x\Gamma(x)$，因此gamma函数可以看作是阶乘在实数集上的延拓$$\Gamma(n)=(n-1)!$$此外，gamma函数还有如下性质
- 对$x\in (0,1)$，$\Gamma(1-x)\Gamma(x)=\frac{\pi}{sin(\pi x)}$
- $\Gamma(\frac{1}{2})=\sqrt{\pi}$

###### 共轭先验分布
**定义**
设$\theta$是总体分布中的参数，$p(\theta)$是$\theta$的先验密度函数，假如**由抽样信息$x$算得的后验密度函数$p(\theta|x)$与$p(\theta)$有相同的函数形式(同一个分布簇)，则称$p(\theta)$是$p(\theta|x)$的(自然)共轭先验分布**，称$p(\theta)$和$p(\theta|x)$为共轭分布。

###### Beta分布-二项分布的共轭先验分布
给定参数$\alpha>0,\beta>0$，取值范围为$[0,1]$的随机变量$x$的概率密度函数为
$$
\begin{aligned}
f(x;\alpha,\beta)&=\frac{\Gamma(\alpha+\beta)}{\Gamma(\alpha)\Gamma(\beta)}x^{\alpha-1}(1-x)^{\beta-1} \\
&=\frac{1}{B(\alpha,\beta)} x^{\alpha-1}(1-x)^{\beta-1}
\end{aligned}
$$
则称$x$满足Beta分布，Beta分布的均值为$\frac{\alpha}{\alpha+\beta}$，方差为$\frac{\alpha\beta}{(\alpha+\beta)^2(\alpha+\beta+1)}$。参数$\alpha,\beta$共同控制Beta分布的函数的形状，见下图。

![](http://ww1.sinaimg.cn/large/9bcfe727ly1fe1c0iuzclj20pb0ko788.jpg)

假定先验分布$p(\theta)$和似然概率$p(x|\theta)$满足
$$
\begin{aligned}
p(\theta)&=\frac{\Gamma(\alpha+\beta)}{\Gamma(\alpha)\Gamma(\beta)}\theta^{\alpha-1}(1-\theta)^{\beta-1}\\&=\frac{1}{B(\alpha,\beta)}\theta^{\alpha-1}(1-\theta)^{\beta-1} \\
p(x|\theta)&=C_n^k\theta^k(1-\theta)^{n-k}
\end{aligned}
$$
那么，考虑到$p(x)$为常数项，可知后验概率
$$
\begin{aligned}
p(\theta|x)&=\frac{p(x|\theta)p(\theta)}{p(x)} \\
&= \frac{1}{Z}  \theta^{\alpha+k-1}(1-\theta)^{\beta+n-k-1}.
\end{aligned}
$$
所以，根据定义，$p(\theta)$和$p(\theta|x)$是共轭分布。

###### Dirichlet分布
维度$k \ge 2$的狄利克雷分布在参数$\alpha_1, ..., \alpha_k > 0$上，其概率密度函数为
$$
\begin{aligned}
f(\theta_1,..,\theta_k;\alpha_1,...,\alpha_k)&=\frac{1}{B(\alpha)} \prod_{i=1}^k\theta_i^{\alpha_i-1} \\
B(\alpha) &= \frac{\prod_{i=1}^k\Gamma(\alpha_i)}{\Gamma(\sum_{i=1}^k\alpha_i)}
\end{aligned}
$$
同上，假设$\theta=(\theta_1,...,\theta_k)$有先验分布和似然函数,可以有
$$
\begin{aligned}
p(\theta)&= \frac{1}{B(\alpha)} \prod_{i=1}^k\theta_i^{\alpha_i-1} \\
p(x|\theta)&= \frac{n!}{n_1!...n_k!}\theta_1^{n_1}...\theta_k^{n_k} \\
p(\theta|x)&= \frac{1}{Z} \prod_{i=1}^k\theta_i^{\alpha_i+n_i-1}
\end{aligned}
$$
和Dirichlet分布形式一致。
Dirichlet分布的均值向量为$\left( \frac{\alpha_1}{\sum_i^k \alpha_i},...,\frac{\alpha_k}{\sum_i^k \alpha_i} \right)$。

##### 铺垫模型
定义：
- $w$表示词，$V$表示所有单词的个数（固定值）
- $z$表示主题，$k$是主题的个数（预先给定，固定值）
- $D=(d_1,...,d_M)$表示语料库，其中$M$是语料库中的文档数（固定值）
- $d=(w_1,...,w_N)$表示一个文档，其中$N$表示一个文档中的词数（随机变量）

###### Unigram model
对于文档$d=(w_1,...,w_N)$，用$p(w_n)$表示$w_n$的先验概率，生成文档$d$的概率为$$p(d)=\prod_{n-1}^Np(w_n)$$unigram model假设文本中的词服从Multinomial分布，而Multinomial分布的先验分布为Dirichlet分布。

![Unigram model](http://ww1.sinaimg.cn/large/9bcfe727ly1fe1cpt0cu9j20j40iudgr.jpg)

上图中，$w_n$是在文本中观察到的第$n$个词，$p$和$α$是隐含未知变量,其中
- $p$是词服从的Multinomial分布的参数
- $\alpha$是Dirichlet分布（即Multinomial分布的先验分布）的参数

一般$\alpha$由经验事先给定，$p$由观察到的文本中出现的词学习得到，表示文本中出现每个词的概率。

###### Mixture of unigrams model
Mixture of unigrams model生成过程是：给某个文档先选择**一个主题**，再根据该主题生成文档，该文档中的所有词都来自一个主题。假设主题有$z_1,...,z_k$，生成文档$d$的概率为
$$
\begin{aligned}
p(d)=\sum_zp(z) \prod_{n=1}^N p(w_n|z)
\end{aligned}
$$

![Mixture of unigrams model](http://ww1.sinaimg.cn/large/9bcfe727ly1fe1cx1ll6gj205a02rwec.jpg)

如上图所示。

###### PLSA模型
Mixture of unigrams model中假定一篇文档只由一个主题生成，可实际中，一篇文章往往有多个主题，只是这多个主题各自在文档中出现的概率大小不一样。PLSA是一种词袋模型，不关注词和词之间的出现顺序。

假设一组共现(co-occurrence)词项关联着一个隐含的主题类别$z_k\in \lbrace z_1,...,z_K \rbrace$。同时定义
- $p(d_i)$表示海量文档中某篇文档被选中的概率
- $p(w_j|d_i)$表示词$w_j$在给定文档$d_i$中出现的概率
- $p(z_k|d_i)$表示具体某个主题$z_k$在给定文档$d_i$下出现的概率
- $p(w_j|z_k)$表示具体某个词$w_j$在给定主题$z_k$下出现的概率，与主题关系越密切的词，其条件概率越大

---

**文档到词项的生成方法**
1. 按照概率$p(d_i)$选择一篇文档$d_i$
2. 选定文档$d_i$后，从主题分布中按照概率$p(z_k|d_i)$选择一个隐含的主题类别$z_k$
3. 选定$z_k$后，从词分布中按照概率$p(w_j|z_k)$选择一个词$w_j$

整个过程便是：选定文档->生成主题->确定主题生成词。

---

**发现文档集中的主题（分布）**

![PLSA](http://ww1.sinaimg.cn/large/9bcfe727ly1fe1del7l22j207c02qt8m.jpg)

如上图所示，文档$d$和单词$w$是可被观察到的（样本），但主题$z$却是隐藏的。因为$p(w_j|d_i)$是已知的(统计文档词频)，根据大量已知的文档-词项信息可以训练出$p(z_k|d_i),p(w_j|z_k)$。文档中每个词的生成概率为
$$
\begin{aligned}
p(w_j,d_i) &= p(d_i)p(w_j|d_i) \\
&= p(d_i)\sum_{k=1}^Kp(w_j|z_k)p(z_k|d_i)
\end{aligned}
$$
其中$p(d_i)$可事先计算求出，$p(z_k|d_i),p(w_j|z_k)$未知。

考虑词和词($N$)之间、文档($M$)和文档之间的独立性，则整个语料库中词的分布为
$$
\begin{aligned}
p(w,D)=\prod_{i=1}^M\prod_{j=1}^Np(w_j,d_i)^{n(w_j,d_i)}
\end{aligned}
$$
其中$n(w_j,d_i)$表示词项$w_j$在文档$d_i$中出现的次数，$n(d_i)$表示文档$d_i$中词的总数，并且令$p(w_j|z_k)=\phi_{kj},p(z_k|d_i)=\theta_{ik}$将未知量矩阵化成$\Phi,\Theta$。所以得到对数似然函数
$$
\begin{aligned}
l(\Phi,\Theta)&= \sum_{i=1}^M\sum_{j=1}^Nn(w_j,d_i)\log p(w_j,d_i) \\
&= \sum_{i=1}^M\sum_{j=1}^Nn(w_j,d_i)\left(\log p(d_i)+\log\sum_{k=1}^Kp(w_j|z_k)p(z_k|d_i)\right) \\
&= \sum_{i=1}^Mn(d_i)\left( \log p(d_i)+ \sum_{j=1}^N \frac{n(w_j,d_i)}{n(d_i)} \log\sum_{k=1}^K \phi_{kj}\theta_{ik} \right) \\
&\propto \sum_{i=1}^M \sum_{j=1}^N n(w_j,d_i) \log\sum_{k=1}^K \phi_{kj}\theta_{ik} \\
& \ge \sum_{i=1}^M \sum_{j=1}^N n(w_j,d_i) \sum_{k=1}^K p(z_k|d_i,w_j) \log(\phi_{kj}\theta_{ik})
\end{aligned}
$$
含有隐含变量的优化可以使用EM算法求解，很复杂，不具体写了
**E步**
$$
\begin{aligned}
p(z_k|d_i,w_j)&=\frac{p(z_k,d_i,w_j)}{\sum_{l=1}^Kp(z_l,d_i,w_j)}=\frac{\phi_{kj}\theta_{ik}}{\sum_{l=1}^M\phi_{lj}\theta_{il}}
\end{aligned}
$$
**M步**
经过E步，还需考虑约束条件，即
$$
\begin{aligned}
\sum_{j=1}^N\phi_{kj}&=1 \\
\sum_{k=1}^K\theta_{ik}&=1
\end{aligned}
$$
用拉格朗日乘子法解得
$$
\begin{aligned}
\phi_{kj} &= \frac{\sum_{i=1}^M n(d_i,w_j)p(z_k|d_i,w_j)} {\sum_{i=1}^M\sum_{j=1}^N n(d_i,w_j)p(z_k|d_i,w_j)} \\
\theta_{ik} &= \frac{\sum_{j=1}^N n(d_i,w_j)p(z_k|d_i,w_j) }{n(d_i)}
\end{aligned}
$$
这样就求解出了$\Phi,\Theta$。PLSA的模型示意如下图所示:

![PLSA](http://ww1.sinaimg.cn/large/9bcfe727ly1fe1sf8anmrj20dm09ojsc.jpg)


##### LDA(Latent Dirichlet Allocation)
**LDA在pLSA的基础上加层贝叶斯框架**，在贝叶斯框架下的LDA中，我们不再认为**主题分布（各个主题在文档中出现的概率分布）和词分布（各个词语在某个主题下出现的概率分布）是唯一确定的（而是随机变量）**。这体现了贝叶斯派的核心思想，**把未知参数当作是随机变量，不再认为是某一个确定的值**。即选主题和选词依然都是两个随机的过程。

LDA需要两个Dirichlet先验参数，这个Dirichlet先验为某篇文档随机抽取出某个主题分布和词分布。

###### LDA模型中文档生成方式

![](http://ww1.sinaimg.cn/large/9bcfe727ly1fe2a4qu9g3j20dq06sq2y.jpg)

$\alpha$是主题分布的先验分布，$\beta$是词分布的先验分布。

1. 按照先验概率$p(d_i)$选择一篇文档$d_i$
2. 从Dirichlet分布$\alpha$中取样生成文档$d_i$的主题分布$\theta_i$，换言之，主题分布$\theta_i$由超参数为$\alpha$的Dirichlet分布生成
3. 从主题的多项式分布$\theta_i$中取样生成文档$d_i$第$j$个词的主题$z_{ij}$
4. 从Dirichlet分布$\beta$中取样生成主题$z_{ij}$对应的词语分布$\phi_{z_{ij}}$，换言之，词语分布$\phi_{z_{ij}}$由参数为$\beta$的Dirichlet分布生成
5. 从词语的多项式分布$\phi_{z_{ij}}$中采样最终生成词语$w_{ij}$

示意图如下:

![LDA](http://ww1.sinaimg.cn/large/9bcfe727ly1fe1sknkxg2j20dm09oq46.jpg)

LDA在pLSA的基础上给这两参数$p(z_k|d_i),p(w_j|z_k)$加了两个先验分布的参数（贝叶斯化）：一个主题分布的先验分布Dirichlet分布$\alpha$，和一个词语分布的先验分布Dirichlet分布$\beta$。这里$\alpha,\beta$都是参数向量。

LDA生成文档的过程中，先从dirichlet先验中“随机”抽取出主题分布，然后从主题分布中“随机”抽取出主题，最后从确定后的主题对应的词分布中“随机”抽取出词。虽说是随机取值，但是不同的参数$\alpha,\beta$导致可选值的分布是不一样的，如下图所示

![不同参数的dirichlet分布](http://ww1.sinaimg.cn/large/9bcfe727ly1fe2a310d1rj20ic07tt9k.jpg)

###### LDA发现文档集中的主题
文档生成后，LDA把这两参数$p(z_k|d_i),p(w_j|z_k)$变成随机变量，且加入dirichlet先验。

在pLSA中，我们使用EM算法去估计“主题-词项”矩阵和“文档-主题”矩阵：$\Phi,\Theta$，这两参数都是个固定的值。在LDA中，估计$\Phi,\Theta$这两未知参数可以用变分(Variational inference)-EM算法，也可以用gibbs采样，前者的思想是最大后验估计MAP（MAP与MLE类似，都把未知参数当作固定的值），后者的思想是贝叶斯估计。

**Gibbs采样**
Gibbs抽样是马尔可夫链蒙特卡尔理论（MCMC）中用来获取一系列近似等于指定多维概率分布（比如2个或者多个随机变量的联合概率分布）观察样本的算法。

给定一个文档集合，$w$是可以观察到的已知变量，$\alpha,\beta$和是根据经验给定的先验参数，其他的变量$z，\Theta和\Phi$都是未知变量。

求解$\Theta,\Phi$的过程很复杂，最终求解的Dirichlet分布期望为：
$$
\begin{aligned}
\phi_{kt}&=\frac{n_k^{t}+\beta_t} {\sum_{t=1}^V(n_k^{t}+\beta_t)} \\
\theta_{mk}&=\frac{n_m^{k}+\alpha_k}{\sum_{k=1}^K(n_m^{k}+\alpha_k)}
\end{aligned}
$$
其中，$\phi_{kt}=p(w_t|z_k),\theta_{mk}=p(z_k|d_m)$，$n_t^k$是词$w_t$在主题$z_k$中出现的次数，$n_m^k$是主题$z_k$在文章$d_m$中出现的次数。





**引用**
[1] [LDA-math-神奇的Gamma函数](https://cos.name/2013/01/lda-math-gamma-function/)
[2] [共轭先验分布](http://blog.csdn.net/u010945683/article/details/49149815)
[3] [通俗理解LDA主题模型](http://blog.csdn.net/yhao2014/article/details/51098037)
[4] [关于Beta分布、二项分布与Dirichlet分布、多项分布的关系](http://blog.163.com/zzz216@yeah/blog/static/162554684201381382117133/)