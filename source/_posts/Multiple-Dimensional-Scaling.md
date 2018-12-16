---
title: Multiple Dimensional Scaling
date: 2016-12-18 10:22:41
tags: [machine learning]
categories: Algorithm
---

Multiple Dimensional Scaling (MDS、多维缩放)是经典的聚类算法。

---

假设原始$d$维样本空间中有$m$个样本$x_1,x_2,...,x_m$，其距离矩阵为$D \in R^{m\times m}$，$dist_{ij}$为$x_i$到$x_j$的距离。MDS的出发点是获得样本在$d^{'}$维空间内的表示$Z\in R^{d^{'} \times m}$，新空间内样本的距离等于原始空间的距离，即$$\Vert z_i-z_j \Vert = dist_{ij}$$令$B=Z^TZ \in R^{m\times m}$，其中$B$为降维后的样本内积矩阵，$b_{ij}=z_i^Tz_j$，有
$$
\begin{aligned}
dist_{ij}^2 &= \Vert z_i \Vert + \Vert z_j \Vert - 2z_i^Tz_j \\
&= b_{ii}+b_{jj}-2b_{ij}
\end{aligned}
$$
假设样本$Z$被中心化(normalization)，即$\sum_{i=1}^m z_i=0$。于是有$$\sum_{i=1}^mb_{ij}=\sum_{j=1}^mb_{ij}=0$$。继而有
$$
\begin{aligned}
\sum_{i=1}^m dist_{ij}^2 = tr(B)+mb_{jj} \\
\sum_{j=1}^m dist_{ij}^2 = tr(B)+mb_{ii} \\
\sum_{i=1}^m \sum_{j=1}^m dist_{ij}^2 = 2mtr(B)
\end{aligned}
$$
其中，$tr$表示矩阵的秩，$tr(B)=\sum_{i=1}^m \Vert z_i \Vert^2$，联立上式可得$$b_{ij}=-\frac{1}{2} \left( dist_{ij}^2 - \frac{1}{m}\sum_{i=1}^m dist_{ij}^2 -\frac{1}{m}\sum_{j=1}^m dist_{ij}^2 + \frac{1}{m^2}\sum_{i=1}^m \sum_{j=1}^m dist_{ij}^2 \right)$$由此即可通过降维前后保持不变的距离矩阵$D$求取内积矩阵$B$。

那么，下面就需要求$Z$了。方法是对$B$做特征值分解，得到
$$
\begin{aligned}
B=Z^TZ=V\Lambda V^T
\end{aligned}
$$
其中，$\Lambda=diag(\lambda_1,...,\lambda_{d})$为$d$个特征值构成的对角矩阵，$\lambda_1 \ge \lambda_2 \ge ... \ge \lambda_d$。令$\Lambda_{\*}=diag(\lambda_1,...,\lambda_{d^{\*}})$为对角矩阵，$\Lambda_{\*}$表示对应的特征向量矩阵，则$$Z=\Lambda_{\*}^{\frac{1}{2}}V_{\*}^T \in R^{d^{\*}\times m}$$现实中，仅需要降维后的距离与原始空间内的距离尽可能接近，不必严格相等。此时可取$d^{\*}$远小于$d$求解。

MDS算法描述如下：

---

输入：距离矩阵$D\in R^{m\times m}$，其元素$dist_{ij}$为样本$x_i$到$x_j$的距离；低维空间维度$d^{'}$

---

1 计算矩阵$B$
2 对$B$做特征值分解
3 取$\Lambda$为$d^{'}$个最大特征值所构成的对角矩阵，$V$为相应的特征向量矩阵

---

输出：$Z=\Lambda^{\frac{1}{2}}V^T$，其中$Z$的每列对应一个样本的低维坐标

---

