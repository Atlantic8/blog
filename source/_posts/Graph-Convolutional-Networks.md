---
title: Graph Convolutional Networks
mathjax: true
date: 2020-09-01 22:55:41
tags: [Graph, deep learning]
categories: Algorithm
---

GCN是GNN中比较常用的一种网络结构，其主要思想是将卷积操作迁移到图结构上以提取图的结构特征。

研究GCN的原因如下：
- 图是一种定义拓扑关系的广义结构，可以表达丰富的结构特征
- CNN的方法不能对图做卷积，图中每个顶点的相邻顶点数目都可能不同，无法用一个同样尺寸的卷积核来进行卷积运算

### 网络结构
图上的卷积操作大体上有如下两种思路

#### spatial domain
这里是将卷积做了一个概念上的泛化。这里有两个概念
- aggregation：**用邻居的特征更新当前节点下一层的hidden state**
- readout
    - 单个节点的表征
    - 聚合所有节点的特征，得到**整个图的表征**

根据aggregation和readout的不同，就有不同的算法

###### NN4G（Neural Networks for Graph. 2009）
aggregation：节点$v$的第$k$隐层节点值为
$$
h_v^{(k)}=f\left(x_vW_{k}+\sum_{u\in N(v)}h_u^{(k-1)}W_{k,k-1}\right)
$$
其中，$x_v$为节点$v$的原始特征。

readout：**将每一层的hidden state求均值，然后加权求和作为整个图的表征**

###### DCNN（Diffusion-Convolution Neural Network. 2016）
DCNN将迭代看成是图上的扩散过程，每一层相当于在上一层的基础上再进行一跳。
aggregation：
$$
h_v^{(k)}=f\left( W_{k,v}\cdot MEAN(d(v,.)=k)\right)
$$
其中，$MEAN(d(v,.)=k)$表示与点$v$距离为$k$的节点的**原始特征**（**$x$**）的均值，这里注意不是用$k-1$层的hidden state，而是原始特征。

readout：将每一层的hidden state拼成矩阵，所有的矩阵就是图的表征；单个节点对应的所有hidden state拼一起就是单个节点的表征

###### DGC（Diffusion Graph Convolution）
整体上与DCNN类似，唯一不同的是在readout阶段，表征不再用各个hidden state拼接的结果，而是用**相加**的结果

###### MoNet（Mixture Model Network. 2017）
aggregation：
- 考虑了邻居的权重，不再使用邻居的简单相加，而是使用加权求和
- 节点$x,y$的边权重定义为：$u(x,y)=(\frac{1}{\sqrt{\deg(x)}},\frac{1}{\sqrt{\deg(y)}})^T$，其中$\deg()$表示节点的度函数

readout：-

###### GAT（Graph Attention Network. 2017）
MoNet将权重写死了，GAT通过attention机制计算出邻居节点的权重。这是较为常用的一种方法

###### GIN（Graph Isomorphism Network. How Powerful are Graph Neural Networks?. 2019）
主要思想如下
- aggregation的时候不要使用mean或者max pooling操作，而是使用sum。因为max、mean操作会丢失掉一些图的结构信息，比如3个2和4个2的均值、最大值都是2，但是和不一样
- aggregation按如下公示计算

$$
h_v^{(k)}=MLP^{(k)}\left( (1+\epsilon^{(k)})h_v^{(k-1)}+\sum_{u\in N_{v}}h_{u}^{(k-1)} \right)
$$

##### spectrum domain
结论：
> 信号在时域上的卷积等价于其在频域上的乘法

<img src="https://raw.githubusercontent.com/Atlantic8/picture/master/GCN-idea.jpeg" width = "550" height = "250" alt="" align=center />

所以，这种方法的思想是**将图信号上的卷积操作转换到频域上的乘法操作，最后再逆转回去**

###### 谱图理论(vertex domain -> spectral domain)
给定包含$N$个节点的图，定义$A,D$分别为图的邻接矩阵和度矩阵。
定义图上的拉普拉斯矩阵：$L=D-A$，对称，半正定。有如下特性
- 对称矩阵一定N个线性无关的特征向量
- 半正定矩阵的特征值一定非负
- 对阵矩阵的特征向量相互正交

对这个矩阵做SVD分解得到$L=U\Lambda U^T$（这里$U^T=U^{-1}$且$UU^T=E$），其中$\Lambda=diag(\lambda_0,...,\lambda_{N-1})$，$U=[u_0,...,u_{N-1}]$为包含正交向量（列向量）的特征矩阵。$\lambda_l$可以看成**频率**概念，而$u_l$则是对应的基（basis）。[这里频率概念的解释可以参考文献1中的视频解释]

**图傅立叶变换**：给定信号$x$，经过图傅立叶变换后得到(这里其实和PCA很像了)
$$
\hat{x}=U^Tx
$$
其中$U$是上述的特征矩阵。**图傅立叶逆变换**则如下：
$$
x=U\hat{x}
$$

有了经过图傅立叶变换的信号$\hat{x}$后，我们可以在频域上对信号做一个变换（滤波），简单的做法是做对应位相乘，引入参数$\theta$。为了表述统一，令$g_{\theta}(\Lambda)$为对角矩阵的对角$\theta$（参数写成$\Lambda$只是为了和频率对上）。所以有
$$
\hat{y}=g_{\theta}(\Lambda)\hat{x}=g_{\theta}(\Lambda)U^Tx
$$
再将频域信号转换到时域（或者说vertex domain），有
$$
y=U\hat{y}=Ug_{\theta}(\Lambda)U^Tx=g_{\theta}(U\Lambda U^T)x=g_{\theta}(L)x
$$
所以，要学$g_{\theta}()$函数。这个函数的选取需要考虑两个方面
- **参数规模**：上述推导的参数规模是$N$，不希望这么大
- **局部视野特性**：我们不希望当前节点能看到所有节点，所以函数不能分解成无限多项（因为矩阵$L$的$N$次方表示当前节点可以看到任何连通节点的信息）

**ChebNet**
$$
g_{\theta}(L)=\sum_{k=0}^K\theta_kL^k
$$
优点：
- 参数规模：O(K)
- 局部视野特性：K-localized
缺陷：
- 复杂度问题：矩阵乘法复杂度为O(N^2)，K次方下计算量大
 
根据Chebyshev多项式，满足
$$
T_0(\hat{\Lambda})=I, I\ is\ identity\ matrix \\ 
T_1(\hat{\Lambda})=\hat{\Lambda} \\
T_k(\hat{\Lambda})=2xT_{k-1}(\hat{\Lambda})-T_{k-2}(\hat{\Lambda})
$$
其中$\hat{\Lambda}=\frac{2\Lambda}{\lambda_{max}}-I, \hat{\lambda}\in[-1, 1]$。这个公式可以利用推倒结构，以
$$
y=\sum_{k=0}^K\theta'_kT_k(\hat{L})x \tag{1}
$$
代替原来的计算方式，降低计算复杂度。
每组$\theta$等价于一个filter，可以有多个filter，当作多个特征提取工具。

---


<img src="https://raw.githubusercontent.com/Atlantic8/picture/master/GCN-simplify.png" width = "550" height = "250" alt="" align="center" />

GCN是在公示1的基础上再做简化
- 令K=1，即只考虑两项
- $\hat{L}\approx L-I$，如果$L$是normalized laplacian，有$\lambda_{max} \approx2$，又$\hat{L}=\frac{2L}{\lambda_{max}}-I$
- 根据**Symmetric normalized Laplacian**定义有$L=I-D^{-\frac{1}{2}}AD^{-\frac{1}{2}}$
- 再次简化模型，令：$\theta=\theta'_0=-\theta'_1$
    - $y=\theta(I+D^{-\frac{1}{2}}AD^{-\frac{1}{2}})x$
- 再次trick，$I+D^{-\frac{1}{2}}AD^{-\frac{1}{2}} \to \hat{D}^{-\frac{1}{2}}\hat{A}\hat{D}^{-\frac{1}{2}}$
    - $\hat{A}=A+I$
    - $\hat{D}_{ii}=\sum_j\hat{A}_{ij}$，参考原paper
    - $H^{(l+1)}=\sigma(\hat{D}^{-\frac{1}{2}}\hat{A}\hat{D}^{-\frac{1}{2}}H^{(l)}W^{(l)})$，这里$W$对应$\theta$

上面重写一下(邻域要包含自己)：
$$
h_v=f\left( \frac{1}{|N(v)|}\sum_{u\in N(v)}Wx_u+b \right)
$$

---

[1]. https://www.bilibili.com/video/BV1G54y1971S?p=2

[2]. [SEMI-SUPERVISED CLASSIFICATION WITH GRAPH CONVOLUTIONAL NETWORKS](https://arxiv.org/pdf/1609.02907.pdf)

