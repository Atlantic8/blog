---
title: word2vec
date: 2017-03-31 10:50:31
tags: [machine learning, NLP]
categories: Algorithm
---
##### 统计语言模型
自然语言处理中的一个基本问题是计算一段文本序列在某种语言下出现的概率，统计语言模型给出了这一类问题的一个基本解决框架。

对于一段文本序列$S=w_1,...,w_T$，它的概率是
$$
\begin{aligned}
P(S)=P(w_1,...,w_T)=\prod_{t=1}^Tp(w_t|w_1,...,w_{t-1})
\end{aligned}
$$
问题变成了如何去预测这些条件概率.

###### Ngram
上述模型的参数空间巨大，一个改进方法是Ngram，有
$$
\begin{aligned}
p(w_t|w_1,...,w_{t-1}) \approx p(w_t|w_{t-n+1},...,w_{t-1})
\end{aligned}
$$
Ngram本质上是将词当做一个个孤立的原子单元去处理的，用`ont-hot`的方式向量化word，向量维度等于词典大小。
Ngram及其他gram模型仍有局限性：
- 由于参数空间的爆炸式增长，它无法处理更长程的context
- 没有考虑词与词之间内在的联系性

##### Distributed Representation
用`ont-hot`的方式向量化单词面临着维度灾难问题，能否用一个连续的稠密向量去刻画一个word的特征呢？这样不仅可以直接刻画词与词之间的相似度，还可以建立一个从向量到概率的平滑函数模型，使得相似的词向量可以映射到相近的概率空间上。这个稠密连续向量也被称为word的`distributed representation`.

在信息检索领域里，这个概念被称为向量空间模型（`Vector Space Model`），VSM是基于一种`Statistical Semantics Hypothesis`，比较广为人知的两个版本是`Bag of Words Hypothesis`和`Distributional Hypothesis`，分别表示
- `Bag of Words Hypothesis`：一篇文档的词频（而不是词序）代表了文档的主题
- `Distributional Hypothesis`：上下文环境相似的两个词有着相近的语义

基于`Bag of Words Hypothesis`，我们可以构造一个`term-document`矩阵$A$，矩阵里的元素$A_{ij}$代表着word $w_i$在文档$D_j$中出现的次数（或频率）。可以提取行向量做为word的语义向量。

基于`Distributional Hypothesis`，我们可以构造一个`word-context`的矩阵$B$，矩阵里的元素$B_{ij}$代表着word $w_i$在context $C_j$中出现的次数（或频率）

这种co-occurrence矩阵仍然存在着数据稀疏性和维度灾难的问题，解决方法是基于SVD的稀疏矩阵分解方法。

##### word2vec原理
假设预料为$D=\lbrace w_1,...,w_V \rbrace$
###### CBoW模型（Continuous Bag-of-Words Model）
![Continuous Bag-of-Words Model](http://ww1.sinaimg.cn/large/9bcfe727ly1fe4l3rsmdtj20tm10gtee.jpg)

**CBoW的描述**(N对应图中的|V|)
- 利用位置$t$前后的$2m$个words，以它们的`one-hot`编码$x_k$作为输入。通过一个共享的$n\times N$投影矩阵$V$，将每个输入投影成$n$维词向量，$N$是词典大小。$v_{t+j}=Vx_{t+j},j\in \lbrace -m,...-1,1,...,m \rbrace$这里的$V$矩阵最终包含的就是我们要的结果。
- 在PROJECTION层上，将$2m$个投影结果汇总（平均值，舍弃了位置信息）.$\hat{v_t}=\frac{1}{2m}\sum_{j}v_{t+j},j\in \lbrace -m,...-1,1,...,m \rbrace$，通过矩阵$U_{Nn}(U^T=[u_1,...,u_N])$连接到输出层。
- 最后是softmax层，$N$个节点，每个节点表示中心词是$w_i$的概率。输出层的输入向量为$z$，$z_i=u_i^T\hat{v_t}$，输出结果为$y$，$\hat{y_i}=softmax(z_i)$

模型参数是两个词向量矩阵：$U,V$，对于中心词$w_t$，模型对它的损失函数为：
$$
\begin{aligned}
J_t&=-logP(w_t|w_{t-m},...,w_{t-1},w_{t+1},...,w_{t+m}) \\
 &=-log(softmax(z_t)) \\
 &=-log\frac{e^{u_t^T\hat{v_t}}}{\sum_{k=1}^V e^{u_k^T\hat{v_t}}} \\
 &=-z_t+log\sum_{k=1}^V e^{z_k}
\end{aligned}
$$
所以，整个模型的经验风险为
$$
\begin{aligned}
J&=\sum_{w_{t+m},w_{t-m}\in D} J_t
\end{aligned}
$$
风险$J$对$U,V$的导数为：
$$
\begin{aligned}
\frac{\partial J}{\partial u_i} &= (\hat{y_i}-y_i)\hat{v_t} \\
\frac{\partial J}{\partial U^T} &= \hat{v_t}(\hat{y_t}-y)^T \\
\frac{\partial J}{\partial v_{t+j}} &= \frac{1}{2m}U^T(\hat{y}-y)
\end{aligned}
$$
采取sgd更新方式，梯度下降。



###### Skip-gram
![Skip-gram](http://ww1.sinaimg.cn/mw690/9bcfe727ly1ffjr31ab9aj213q0tt1hg.jpg)

Skip-gram以当前词为中心，预测window内的词语，细节图中描述的很清楚了。为了描述方便，不妨假设图中的矩阵$W,W{\'}$分别为$U,V$。

由于输入向量$w_t$是`one-hot`向量(不妨假设第$k$行是1)，所以$Uw_t$就相当于$U$的第$k$列，在这里将其命名为$u_k$。经过$V$矩阵，得到$z=Vu_k,z_i=v_iu_k$，$v_i$是$V$的第$i$行。这里$V$也可以看成包含了所有单词对应向量的矩阵，$z$就表示了$u_k$和$V$中其他向量的相似度。最后对$z$做softmax归一化得到结果$y$(假设应该是$w_{t+1}$)，最大的对应输出。

假设真实的输出为$\hat{y}$（`one-hot`，$p$行为1），损失函数使用交叉熵，则对这单个样例的损失函数为
$$
\begin{aligned}
l(t,t+1)=-logy_p=-log\frac{e^{v_iu_k}}{\sum_ie^{v_iu_k}}
\end{aligned}
$$
所以一个句子的损失为
$$
\begin{aligned}
L=-\frac{1}{T}\sum_{t=1}^T\sum_{i=t-m}^{t+m}l(t,i)
\end{aligned}
$$
然后分别对$U,V$求导即可得到梯度。

###### Negative Sampling
继续`skip-gram`模型，在计算$l(t,i)$的时候，需要计算$w_t$对应的向量与每一个其他向量的相似程度$v_iu_k$，`softmax`对于特别大的词汇计算量很大。

负采样的思想就是把这里计算其他所有词的相似度改成只计算一部分的相似度，具体地，将这里的类`softmax`分类的方法变成`logistic regression`的方法，当前词的context的词为正样本，然后采样一部分其余的词作为负样本。

也就是将$log\frac{e^{v_iu_k}}{\sum_ie^{v_iu_k}}$变成
$$
\begin{aligned}
log\;\sigma(v_iu_k)+\sum_{j=1}^n E_{w_i\sim p_{neg}(w_t)}[log\;\sigma(-v_ju_k)]
\end{aligned}
$$
其中，$n$是超参数，表示负采样的数量，一般地，对小的训练集$n\in [20,50]$；对大的数据集，$n$可能只有$[2,5]$之间。$ p_{neg}(w_t)$表示对$w_t$负采样的分布。启发式的采样方法可以如下：

随机选取非正样本$w_i$，然后以一定的概率舍弃之，这个概率是
$$
\begin{aligned}
p(w_i)=1-\sqrt{\frac{c}{f(w_i))}}
\end{aligned}
$$
其中，$f(w_i)$是词$w_i$的词频，$c$是常数，一般在$10^{-5}$左右。这样选择，会过滤掉词频小于$c$的词，并且保证词频大的词语被选中的概率更大。

###### 层次Softmax
由于原始的CBoW和skip-gram最后都有softmax层，导致复杂度能达到O(nN)，**Hierarchical Softmax是一种对输出层进行优化的策略，输出层从原始模型的利用softmax计算概率值改为了利用`Huffman`树计算概率值**。

- 投影层的输出沿着`huffman`树不断进行logistic二分类，并修正各中间向量和词向量
- 词表中的**全部词作为叶子节点**，**词频作为节点的权**，叶子结点包含word本身
- 每一个非叶子结点都看作是一个logistic分类器，决定下一层的走向，它包含权值
- 从根节点出发，到达指定叶子节点的路径是唯一的
- 路过非叶子结点，修正logistic参数，并且**累计误差，误差最后用来修正投影矩阵$V$**
- `Hierarchical Softmax`正是利用这条唯一路径来计算指定词的概率

实现过程中，可以
- 不考虑投影矩阵，而是将每个词对应的向量（投影后的）设置为随机向量
- 通过huffman的每一个节点时都计算累加误差，利用累计误差更新当前节点的LR参数
- 累计误差将被用来调整词向量


##### word2vec的应用
###### 广告投放

    U1  a1,a2,a3……
    U2  a2,a3,a5,……
    U3  a1,a3,a6,……

公司A目前有很多用户的浏览数据，如用户u浏览了公司A的页面a1，a2，a3等。把每个用户的整体浏览记录当作一篇doc，每个记录就是一个word。利用word2vec算法，将每个记录转化为一个向量。向量化的页面就能够计算相似度，进而根据各种推荐规则进行推荐。
###### ctr预估模型
CTR（Click-Through-Rate）即点击通过率，是互联网广告常用的术语，指网络广告（图片广告/文字广告/关键词广告/排名广告/视频广告等）的点击到达率，即**该广告的实际点击次数（严格的来说，可以是到达目标页面的数量）除以广告的展现量（Show content）**。

广告ctr计算存在**冷启动**的问题，冷启动问题就是一个广告是新上线的，之前没有任何的历史投放数据，这样的广告由于数据不足，点击率模型经常不怎么凑效。

解决方法：**使用同类型广告点击率来缓解**，拿一个同行的广告的各种特征作为这个广告的特征，对这个新广告的点击率进行预估。
比如在媒体公司A上面有1000个广告主，它们的主页分别是a1、a2、……、a1000，运行word2vec得到每一个页面的向量，然后运行kmean或者其他聚类算法，把这1000个广告主聚成100个簇，然后每个簇里面的广告主看成是一个。

**引用**
[1] [word2vec前世今生](http://www.cnblogs.com/iloveai/p/word2vec.html)
[2] [深度学习word2vec笔记之应用篇](https://www.52ml.net/16951.html)
[3] [自己动手写word2vec](http://blog.csdn.net/u014595019/article/details/51884529)
[4] [word2vec的python实现](https://github.com/multiangle/pyword2vec)


