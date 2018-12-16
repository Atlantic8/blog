---
title: Maximum Entropy Model
date: 2017-08-27 12:11:22
tags: [machine learning]
categories: Algorithm
---

###### 定义
最大熵模型也是**判别模型**，其基本思想是最大熵思想，即**在给定关于概率分布不完全信息的情况下，仅有的无偏假设就是使得模型尽可能地均匀**，通俗点说就是**对一个随机事件的概率分布进行预测时，预测应当满足全部已知的约束，而对未知的情况不要做任何主观假设**。在这种思想下，合适的模型就是在满足给定限制情况下最大化模型的熵。对于条件模型$p(y|x)$，其条件熵的定义为
$$
\begin{aligned}
H(p)=-\sum_{(x,y)\in Z}p(x,y)\log p(y|x)
\end{aligned}
$$
其中，$Z$包含$x,y$的所有可能组合。

训练样本由输入、标签表征。这里引入特征函数的概念，特征函数和以前看到的特征不大一样，它是对输入和输出同时抽取特征，表示为$f(x,y)$。特征函数可以定义为二值函数，如果$x,y$满足一定的事实，那么$f(x,y)$为1，否则为0。

###### 约束

假设训练数据集$T$有$n$条数据，特征个数为$m$个，第$i$个特征对应的特征函数为$f_i(x,y)$。令由训练数据得到的经验联合分布为$\hat{p}(x,y)$，那么特征$f_i$关于经验分布的期望值为
$$
\begin{aligned}
\hat{E}(f_i)=\sum_{(x,y)\in T}\hat{p}(x,y)f_i(x,y)=\frac{1}{n}\sum_{(x,y)\in T}f_i(x,y)
\end{aligned}
$$
同样地，在模型分布上的特征函数均值可以表示为
$$
\begin{aligned}
E(f_i)&=\sum_{(x,y)\in Z}p(x,y)f_i(x,y)=\sum_{(x,y)\in Z}p(x)p(y|x)f_i(x,y) \\
&\approx\sum_{x,y}\hat{p}(x)p(y|x)f_i(x,y)=\frac{1}{n}\sum_{x\in T}\sum_{y\in Y}p(y|x)f_i(x,y)
\end{aligned}
$$
其中，$Z$是$x,y$所有可能组合。（这里因为$x,y$所有可能组合会很多，计算上不可行）。$x$仅考虑训练集中的$x$，而$y$则是所有可能的取值，但是在实际中，$y$的可能取值是有限的、比较少的，所以这里的计算也是高效的。

至此，得到第一种约束。如果模型可以从数据中获取足够多的信息，就可以认为**经验值约等于期望值**，即
$$
\begin{aligned}
\hat{E}(f_i)\approx E(f_i)
\end{aligned}
$$

---

第二种约束为概率本身的限制，即：
$$
\begin{aligned}
p(y|x) &\ge 0 \quad for\;all\;x,y \\
\sum_y p(y|x)&=1\quad for\;all\;x
\end{aligned}
$$

---

类似地，可以得到
$$
\begin{aligned}
H(p) = -\sum_{x,y}\hat{p}(x)p(y|x)\log p(y|x)
\end{aligned}
$$

###### 目标函数
按照最优化问题的优化习惯，将最大化问题改写成最小化问题
$$
\begin{aligned}
arg\min_{p(y|x)}&-H(p) \\
&s.t.\quad \hat{E}(f_i) = E(f_i) \quad for\;i\;in\,\lbrace 1,..,m \rbrace  \\
&\sum_y p(y|x)=1\quad for\;all\;x
\end{aligned}
$$

###### 模型训练
带约束的优化问题可以参考拉格朗日乘子法，引入参数$\lambda=(\lambda_1,...,\lambda_{m+1})$，令
$$
\begin{aligned}
\Gamma(p,\lambda) = -H(p)+\sum_{i=1}^m\lambda_i\left(E(f_i)-\hat{E}(f_i)\right)+\lambda_{m+1}\left(\sum_{y\in Y}p(y|x)-1\right)
\end{aligned}
$$
考虑上式与原始优化问题之间联系，对于约束问题，如果有一个不满足条件，那么将对应的$\lambda$分量扩展到$\infty$，那么整个公式的值就变成了$+\infty$。所以可以得到
$$
\begin{aligned}
\min_{p(y|x)}\Gamma(p,\lambda) = \min_{p(y|x)}\max_{\lambda}\Gamma(p,\lambda)
\end{aligned}
$$
因为函数$\Gamma(p,\lambda)$是$p(y|x)$的凸函数，所以根据拉格朗日对偶性有
$$
\begin{aligned}
 \min_{p(y|x)}\max_{\lambda}\Gamma(p,\lambda)=\max_{\lambda} \min_{p(y|x)}\Gamma(p,\lambda)
\end{aligned}
$$

---

首先看$\min_{p(y|x)}\Gamma(p,\lambda)$:
我们可以求$\Gamma(p,\lambda)$对$p(y|x)$的导数。逐项考虑，首先
$$
\begin{aligned}
\frac{\partial{H(y|x)}}{\partial p(y|x)} = -\hat{p}(x)\cdot[\log p(y|x)+1]
\end{aligned}
$$
第二项
$$
\begin{aligned}
&\frac{\partial{\sum_{i=1}^m\lambda_i\left(E(f_i)-\hat{E}(f_i)\right)}}{\partial p(y|x)} \\
&= \frac{\partial}{\partial p(y|x)}\sum_{i=1}^m\lambda_i \left( \sum_{(x,y)\in Z}\hat{p}(x)p(y|x)f_i(x,y) - \sum_{(x,y)\in T}\hat{p}(x,y)f_i(x,y) \right) \\
&= \sum_{i=1}^m\lambda_i \hat{p}(x) f_i(x,y) 
\end{aligned}
$$
第三项比较简单，就不单独列出来了，所以$\Gamma(p,\lambda)$对$p(y|x)$的导数可以表示为：
$$
\begin{aligned}
\frac{\partial \Gamma(p,\lambda)}{\partial p(y|x)} = -\hat{p}(x)\cdot[\log p(y|x)+1] + \sum_{i=1}^m\lambda_i \hat{p}(x) f_i(x,y) + \lambda_{m+1}
\end{aligned}
$$
令上式等于0可以得到：
$$
\begin{equation}
p(y|x) =\exp\left( \sum_{i=1}^m \lambda_if_i(x,y) \right)\cdot \exp\left( \frac{\lambda_{m+1}}{\hat{p}(x)}-1 \right)
\end{equation}
$$
为了使$p(y|x)$的表达式只与特征函数有关，我们最好消去$\hat{p}(x)$。注意到$\sum_y p(y|x)=1$，将上式两边对$y$求和，可以得到
$$
\begin{equation}
\exp\left( \frac{\lambda_{m+1}}{\hat{p}(x)}-1 \right)=\frac{1}{\sum_y \exp\left( \sum_{i=1}^m \lambda_if_i(x,y) \right)}
\end{equation}
$$
进一步可以得到
$$
\begin{equation}
p(y|x) = \exp\left( \sum_{i=1}^m \lambda_if_i(x,y) \right)\cdot \frac{1}{\sum_y \exp\left( \sum_{i=1}^m \lambda_if_i(x,y) \right)}
\end{equation}
$$
综上所述，最大熵模型也就是
$$
\begin{equation}
p_{\lambda}^{*}(y|x) = \exp\left( \sum_{i=1}^m \lambda_if_i(x,y) \right)\cdot \frac{1}{\sum_y \exp\left( \sum_{i=1}^m \lambda_if_i(x,y) \right)}
\end{equation}
$$

---

第二步，求解$\lambda^{\*}$:
令$\Psi_{p^{\*}}= \min_{p(y|x)}\Gamma(p,\lambda)$，下一步就是
$$
\begin{equation}
\lambda^{\*}=arg\max_{\lambda} \Psi_{p^{\*}}
\end{equation}
$$

---

可以证明，最大熵模型是适定的（well-defined），其解存在且唯一。

**参考文献**
[1]. Classical Probabilistic Models and Conditional Random Fields.pdf
[2]. 统计学习方法. 李航