---
title: Graph Embedding
mathjax: true
date: 2020-09-01 22:49:52
tags: [deep learning]
categories: Algorithm
---

图嵌入，即用一个低维，稠密的向量去表示图中的点，该向量表示能反映图中的结构。但是在介绍图嵌入之前，可以大概描述一下词嵌入。

bert时代之前，word2vec是很有名的词嵌入技术，训练快，效果提升也比不用词向量明显。本质上就是由输入序列得到每个word的embedding，其目标函数为
$$
\sum_i\log p(w_i|w_{context(i)})
$$
即希望：给定上下文，当前词的概率更大。（skip-gram的意思也一致）

基本的图嵌入算法也借鉴了这个思想，问题就是图如何转化为序列

#### DeepWalk
> DeepWalk: Online Learning of Social Representations. 2014

DeepWalk通过**截断随机游走**(truncated random walk)学习网络的嵌入表示，就是等于对图进行采样，得到多个**节点序列**，跳转概率可以由节点之间的权重决定。然后对节点序列学习节点的embedding表示

**random walk实际上是一种可回头的DFS**

#### LINE
> Large scale information network embedding. 2015

![一阶二阶相似度](https://raw.githubusercontent.com/Atlantic8/picture/master/graph-embedding-1.PNG)

高维空间中相近的点在低维空间中也是相近的，相近的定义如下
###### 一阶相近
- 高维空间中：节点$i,j$之间的权重有经验分布：$\hat{p}_1(i,j)=\frac{w_{i,j}}{\sum_{(i,j)\in E}}$
- 低维空间中：则可以理解为embedding$\mu_i,\mu_j$的sigmoid函数（$p_1(i,j)=\frac{1}{1+\exp{(-u_i^Tu_j)}}$）
- 目标为最小化两个分布的距离，距离用KL散度，$O_1=-\sum_{(i,j)\in E}w_{i,j}\log p_1(i,j)$

###### 二阶相近，用于有向图
- 高维：node之间有多少公共一度节点(比如5和6之间有4个公共一度节点，也就是有多少相同的邻居)，经验分布为$\hat{p}_2(i,j)=\frac{w_{i,j}}{d_i}$，$d_i$是节点的出边的权值和
- 低维：条件概率$p_2(j|i)$可以表示为softmax形式
- 目标为最小化两个分布的距离，距离用KL散度，$O_2=-\sum_{(i,j)\in E}w_{i,j}\log p_2(j|i)$

每个顶点维护两个embedding向量，一个是该顶点本身的表示向量，一个是该点作为其他顶点的上下文顶点时的表示向量

#### Node2vec
> node2vec: Scalable Feature Learning for Networks. 2016

Node2vec基于二阶随机游走，通过参数$p,q$来控制游走策略，平衡BFS和DFS（**DFS倾向于获取结构相似性，BFS倾向于获取内容相似性，即局部相似性**）。通过改变采样结果来优化效果

![image](https://raw.githubusercontent.com/Atlantic8/picture/master/graph-embedding-2.PNG)

定义当前节点为$v$，上一节点为$t$，随机游走到下一个节点$x$的概率为
$$
\pi(x|v)=\frac{\alpha(t,x)}{\sum_{(y,v)\in E}\alpha(t,y)}
$$
其中，$\alpha$是控制函数，其定义为
$$
\alpha(t,x)=\left\{
\begin{aligned}
\frac{1}{p}, &  &  d_{tx}=0 \\
1, &  &  d_{tx}=1 \\
\frac{1}{q}, &  &  d_{tx}=2
\end{aligned}
\right.
$$
其中，$d_{tx}$是节点$t,x$之间的最短路径长度，因为最大就为2，所以有二阶的概念。$q$为**前进参数**（决定搜索远离$t$的节点的概率），$p$为**回溯参数**（决定了有多少概率下一个节点还是$t$）

如果图的边存在初始权重，则计算下一节点为$x$的概率时需要考虑权重，也就是归一化的时候乘上权重。

BTY：当$p=1,q=1$时，Node2vec等价于random walk


#### SDNE
> Structural Deep Network Embedding. 2016

SDNE使用深度学习模型学习网络嵌入，**使用自编码器的思想尝试对图的邻接矩阵进行嵌入表示，并且加入节点相似的考虑，属于半监督方法**。其损失函数与LINE类似，可以分为一阶相似损失和二阶相似损失，其中
- 一阶损失：**邻居节点之间的表示向量应该接近**
    - $\mathcal{L}_1=\sum_{i,j} s_{i,j}||u_i-u_j||_2^2$，其中$s_{i,j}$表示两个节点的权值，$u$是节点的embedding
    - 这一部分是**监督模式**
- 二阶损失：**具有相似邻居的节点之间的表示向量应该相似**
    - $\mathcal{L}_2=\sum_{i} ||(\hat{x}_i-x_i)\odot b_i||_2^2$
    - 这个便是自编码器的**重建误差**，$x_i$是原始的邻接向量，$\hat{x}_i$是重建的邻接向量
    - 这里的$b_i$主要用来**惩罚**$x_i=0$的情况，因为邻接向量一般比较**稀疏**，解码器输出全0向量也是不错的解；另外不邻接也不代表没关系
    - 这一部分是**无监督模式**

![image](https://raw.githubusercontent.com/Atlantic8/picture/master/graph-embedding-3.PNG)

整体的损失函数如下：
$$
\mathcal{L}=\alpha\mathcal{L}_1+\mathcal{L}_2+\mathcal{L}_{reg}
$$
最后一项是正则项，主要对网络中的参数进行惩罚

#### Struc2vec
> struc2vec:Learning Node  Representations from Structural  Identity. 2017

Struc2vec认为embedding不应该任何相邻性，而只考虑空间结构相似性。也就是要从：**相似的节点往往有比较相似的空间结构**

![image](https://raw.githubusercontent.com/Atlantic8/picture/master/graph-embedding-4.PNG)

论文表示空间结构相似的方法是：如果两个节点的所有邻接节点构成的序列相似，那么这两个节点相似.

定义$R_k(u)$为与节点$\mu$距离为$k$的节点集合，$s(K)$表示节点集合$K$的**有序度序列**，函数$g$可以表示两个序列的相似度函数(这里可以使用DTW算法)，令
$$
f_k(u,v)=f_{k-1}(u,v)+g\left(s\left(R_k(u)\right),s(R_k(v))\right)
$$
表示节点$u,v$之间的结构不相似性。我们按照不同的$k$分层，同层之间的节点权重为
$$
w_k(u,v)=e^{-f_k(u,v)}
$$
不同层的话，需要先层级转换，有上一层、下一层两种选择，对应权重为
$$
\left\{
\begin{aligned}
w(u_k,u_{k+1})&=\log{\Gamma_k(u)+e}, &  & \Gamma(u)=\sum_v1(w_k(u,v)>\overline{w_k})  \\
w(u_k,u_{k-1})&=1
\end{aligned}
\right.
$$
其中，$\overline{w_k}$是第$k$层的平均权值，$\Gamma_k(u)$表示第$k$层与$u$相连的边的边权大于平均边权的边的数量。是每一步会以一个概率$p$留在当前层，$1-p$跳出本层，如果留在本层，则下一个节点的概率是
$$
p_k(v|u)=\frac{w_k(u,v)}{Z_k(u)}
$$
如果跳出本层，则有
$$
\left\{
\begin{aligned}
p(u_{k+1}|u_k)&=\frac{w(u_k,u_{k+1})}{w(u_k,u_{k+1})+w(u_k,u_{k-1})} \\
p(u_{k-1}|u_k)&=1-p(u_{k+1}|u_k)
\end{aligned}
\right.
$$

---

综上所述，基本流程如下：
- 根据上面的权重公式计算：
    - 同一层中的节点权重($w_k(u,v)$)
    - 不同层次的同一顶点权重($w(u_k,u_{k\pm1})$)
- 获取顶点序列
    - 在当前层游走($p_k(u,v)$)
    - 切换到上下层的层游走($p(u_k,u_{k\pm 1})$)
- Skip-Gram来生成representation，然后训练embedding表示


Struc2vec有成功的工业应用案例，蚂蚁金服风控模型应用了Struc2vec后，较之前的node2vec有了质的提升


#### GraphSAGE
> Inductive representation learning on large graph. 2017

上面的方法都是**直推式**的学习方法，可以从graph中学习到一个矩阵表示，当**图结构变化时是需要重新学习**的。而GraphSAGE是一种归纳式学习方法，可以用邻居节点直接学习出新增节点的embedding

![GraphSAGE的算法流程](https://raw.githubusercontent.com/Atlantic8/picture/master/graph-embedding-5.PNG)

对每一层，主要有以下几个步骤
1. 采样当前节点的邻居顶点
2. 用聚合函数将上一层邻居的表示聚合起来
    - 聚合函数应该对输入顺序不敏感，且有较好的表达能力，候选有
    - mean aggregator
    - pooling aggregator
    - LSTM aggregator
3. 将上一层邻居的聚合表示和上一层当前节点的表示拼接起来，做一个线性映射

###### 参数学习
- 有监督：比如节点分类，可以根据任务目标直接设置
- 无监督：临近的顶点具有相似的向量表示，分离的顶点的表示尽可能区分


#### GraphGAN
> GraphGAN: Graph Representation Learning with Generative Adversarial Nets. 2018

![image](https://raw.githubusercontent.com/Atlantic8/picture/master/graph-embedding-6.PNG)

主要思想：
###### Discriminator$D(v,v_c;\theta_D)$
D判断一条边是否为原始图中的边，即给定节点，判断是否存在边$p(e_{i,j}|v_i,v_j)$

给定两个节点的表示，D判定两个节点有边的概率是
$$
p(e_{i,j}|v_i,v_j)=\sigma(d_i^Td_j)
$$
这里$d_i,d_j$是D中的节点embedding，**所有节点构成的embedding集合就可以看成是D的参数$\theta_D$**

###### Generator$G(v|v_c;\theta_G)$
G生成图中一条不存在的边，也就是要根据给定节点做一个连接，也就是要学习$p(v|v_c)$.（毕竟我们的主要目的就是学习到采样算法）。容易想到用softmax来表示，
$$
G(v|v_c)=\frac{\exp(g_v^Tg_{v_c})}{\sum_{v'\ne v_c}\exp(g_{v'}^Tg_{v_c})}
$$
这里$g_v,g_{v_c}$是G中的节点embedding，所有节点构成的embedding集合就可以看成是G的参数$\theta_G$。**G和D中不共用节点表达，所以最后的训练结果不能当作节点embedding**。但是存在两个问题
- 计算量大
- 没有考虑网络的拓扑结构

###### Graph Softmax
文章提出了Graph Softmax的概念，解决上述两个问题
- 以$v_c$为根，BFS构建树，树中$v_c$到任意节点可达且路径唯一，通过定义父子节点的关联概率（softmax，这里因为是父子节点，所以维度小很多了）和路径概率连乘，我们可以求得$v_c$到任意节点的概率


---

模型训练的时候就是训练D和G的参数，然后利用G进行路径采样，按照skip-gram的方式训练embedding，G的采样可以是：
- 根据Graph Softmax的结果直接进行采样
- 文章还提供了一种方法，不介绍了


效果：链接预测任务在效果上并没有提升太多，比DeepWalk好，跟node2vec差不多。但是也就是套上了GAN吧


---

**引用**

[1]. Graph Neural Network Review. 2018 

[2]. All the paper mentioned above.

