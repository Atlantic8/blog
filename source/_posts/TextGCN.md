---
title: TextGCN
mathjax: true
date: 2020-09-01 22:58:00
tags: [Graph, deep learning, NLP]
categories: Algorithm
---

GNN在NLP上的应用

#### Text GCN
> Graph Convolutional Networks for Text Classification. AAAI. 2019 

给定文章若干，目标是基于GCN搞一个分类器。

图的构建方法，邻接矩阵为
$$
A_{i,j}=\left\{
\begin{aligned}
PMI(i,j), &  &  both\ words \\
TF-IDF_{i,j}, &  & word\ \&\ doc  \\
1, &  &  i=j \\
0, & & otherwise
\end{aligned}
\right.
$$
其中PMI是point-wise mutual information，计算方式如下
$$
PMI(i,j)=\log\frac{p(i,j)}{p(i)p(j)}
$$
概率的计算可以使用滑动窗口统计出现次数，分母是corpus中所有的滑动窗口数量。PMI反应了节点之间的关系，负数表示相关度低，所以**只把PMI>0的节点添加边**。这里，doc和doc之间没有边相连，但是在图上通过一跳就可以达到，所以网络层数应该大于1，论文的实验也说明了这点，layer=2明显好于1.

<img height="320" width="700" src="https://raw.githubusercontent.com/Atlantic8/picture/master/TextGCN.jpeg">

以这个图为基础，构建一个2层的GCN，最后的结果经过softmax做分类
$$
Z=\rm{softmax}\left( \tilde{A}\ \mathcal{ReLU}(\tilde{A}XW_0)W_1 \right) 

\tilde{A}=D^{-\frac{1}{2}}AD^{-\frac{1}{2}}
$$
损失函数就用交叉熵即可。

试验结果显示，TextGCN表现优秀，但是在短文本和情感分析等这种**对word-order比较敏感或者可建模的边数量较少的任务上不够好**。

本方法还有一个固然的缺陷：**无法处理未见过的文档**，因为不在图里

