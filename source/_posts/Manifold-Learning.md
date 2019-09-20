---
title: Manifold Learning
date: 2016-12-18 11:50:16
tags: [machine learning]
categories: Algorithm
---

###### 流形

    流形学习是一类借鉴了拓扑流行概念的概念降维方法
    直观上来讲，一个流形好比是一个 d 维的空间
    在一个 m 维的空间中 (m > d) 被扭曲之后的结果

比如说一块布，可以把它看成一个二维平面，这是一个二维的欧氏空间，现在我们（在三维）中把它扭一扭，它就变成了一个流形（当然，不扭的时候，它也是一个流形，欧氏空间是流形的一种特殊情况），地球表面其实也只是一个二维流形。

    流形的一个特点是：流形是在局部与欧式空间 同胚 的空间
    即局部上具有欧式空间的特性，距离度量可以使用欧氏距离

所以，低维流形嵌入到高维空间中，数据样本在高维空间中的分布看上去会比较复杂，但在局部上具有欧式空间的特性。因此，可以容易地在局部建立降维映射关系，然后设法将局部关系映射到全局。<b>此种降维方法可被用于数据可视化</b>。

---

###### 等度量映射（Isometric Mapping）
Isomap的出发点是：低维嵌入流形上两点距离是“测地线距离”（地理上的概念，比如地球上两点的距离就不是欧氏距离）
但是利用流形的局部与欧式空间同胚特性，我们就能<b>在局部空间内找到每个点的近邻点，从而建立一个近邻连接图。
所以，“测地线距离”就是图中的最短距离</b>。最短路径算法可以使用Dijkstra算法或者Floyd算法。
有了距离度量表示，就可以降维了，降维方法可以使用MDS算法（当然也可以使用其他方法）

Isomap算法描述如下：

---

输入：样本集$D= \lbrace x_1,x_2,...,x_m \rbrace $; 近邻参数$k$; 低维空间维度$d^{'}$

---

1 $for\quad i=1,...,m \quad do$
2 $\quad$确定$x_i$的$k$近邻
3 $\quad x_i$与其$k$近邻的距离设置为其欧氏距离，与其他点的距离设置为无穷大
4 $end \quad for$
5 调用最短距离路径算法计算任意两点之间的距离$dist(x_i,x_j)$
6 将$dist(x_i,x_j)$作为MDS算法的输入，输出结果$Z$

---

输出：样本集$D$在低维空间的投影$Z$

---

###### 局部线性嵌入（Locally Linear Embedding）
Isomap 希望保持任意两点之间的测地线距离，保存的信息量大，但是计算量随着节点数量的增长爆炸增长（Dijkstra算法$O(n^2)$或者Floyd算法$O(n^3)$）。
LLE 希望保持局部线性关系，信息量较小，但是对数据量较大的情形则比较有效。

LLE假设$x_i$能够通过其邻域内的样本$x_j,x_k,x_l$线性表出，即$$x_i=\omega_{ij}x_j+\omega_{ik}x_k+\omega_{il}x_l$$所以，LLE需要先找出每个样本$x_i$的近邻下标集合$Q_i$，然后计算出基于$Q_i$中的样本对$x_i$进行线性重构的系数$\omega_i$：
$$
\begin{aligned}
\min_{\omega_1,\omega_2,...,\omega_m} \sum_{i=1}^m \left\Vert x_i-\sum_{j \in Q_i}\omega_{ij}x_j \right\Vert^2 \\
s.t. \quad \sum_{j \in Q_i}\omega_{ij}=1
\end{aligned}
$$
这里令$C_{jk}=(x_i-x_j)^T(x_i-x_k)$，$\omega_{ij}$有闭式解
$$
\begin{aligned}
\omega_{ij}=\frac{\sum_{k\in Q_i}C_{jk}^{-1}}{\sum_{l,s\in Q_i}C_{ls}^{-1}}
\end{aligned}
$$
因为LLE假设在低维空间中保持$\omega_i$保持不变，令$Z=(z_1,z_2,...,z_m)\in R^{d^{'}\times m},W_{ij}=\omega_{ij}$.所以$x_i$的低维坐标$z_i$可以通过
$$
\begin{aligned}
\min_{z_1,z_2,...,z_m} \sum_{i=1}^m \left\Vert z_i-\sum_{j\in Q_i}\omega_{ij}z_j \right\Vert^2 \\
\min_{z_1,z_2,...,z_m} \sum_{i=1}^m \left\Vert z_i-W_iZ \right\Vert^2
\end{aligned}
$$
求解，这里需要对$z_i$正规化以满足$\sum_i z_i=0,\frac{1}{m}\sum_i z_iz_i^T=I$。可以令$M=(I-W)^T(I-W)$，那么优化函数可以写成$$\min_Z tr(ZMZ^T) \quad s.t \; ZZ^T=I$$这里需要注意我们假设对$Z$正规化，才能满足$ZZ^T=I$。然后上面的优化函数可以通过特征值分解，取最小的$d^{'}$个非零特征值对应的特征向量即为$Z^T$。

LLE算法描述

---

输入：样本集$D={x_1,x_2,...,x_m}$; 近邻参数$k$; 低维空间维度$d^{'}$

---

1 $for\; i=1,...,m \quad do$
2 $\quad$确定$x_i$的$k$近邻
3 $\quad$求$\omega_{ij},\; j\in Q_i$, 不在$x_i$邻域内的系数为0
4 $end \; for$
5 求矩阵$M$
5 对$M$进行特征值分解
6 输出最小的$d^{'}$个非零特征值对应的特征向量

---

输出：样本集$D$在低维空间的投影$Z$

---

###### 拉普拉斯特征映射(Laplacian Eigenmaps)

> 待更......