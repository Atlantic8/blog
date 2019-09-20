---
title: WordRank
date: 2017-07-30 14:35:42
tags: [machine learning, NLP]
categories: Algorithm
---

##### introduction
单词向量化在近些年一直是被广泛研究的课题，虽然state-of-the-art方法（word2vec）提供了通过低维矩阵嵌入方法有效地计算词之间相似性的方法，但是他们的motivation通常是不明确的。他们通用的模式是维护单词-上下文共现矩阵，初始化向量化的单词向量$u_w$、上下文单词向量$v_c$，然后使用一个可以近似表示$X_{w,c}$（$w,c$的共现次数）的函数$f(u_w,v_c)$，通过优化这个函数不断地更新$u_w,v_c$的值。（注意**上下文也是一个单词**，这个单词在当前单词的上下文环境中）

---

##### wordrank

wordrank把单词向量化定义成一个rank的问题，也就是：**给定一个单词$w$，我们想要输出一个上下文列表$\lbrace c_1,c_2,...\rbrace$单词列表，并且要求与单词$w$共现的上下文单词出现在列表的前面**。具体地，单词全集为$W$，上下文全集为$C$，$\Omega$是给定数据单词、上下文的共现矩阵，$\Omega_w$是与$w$共现的上下文集合，$\Omega_c$同理。

定义单词$w$的词向量为$u_w\in U$，上下文$c$的向量为$v_c\in V$，**词和上下文的相关性越大，他们的向量内积就越大**。给定单词$w$，上下文$c$的rank可以定义为其他上下文向量与单词向量乘积比当前上下文向量与但词向量乘积大的个数，也就是有多少个上下文不必当前的"差"，即：
$$
\begin{aligned}
rank(w,c)&=\sum_{c^{'}\in C-\lbrace c\rbrace} I(\langle u_w,v_c \rangle-\langle u_w,v_{c^{'}}\rangle) \\
&=\sum_{c^{'}\in C-\lbrace c\rbrace}I(\langle u_w, v_c-v_{c^{'}}\rangle)
\end{aligned}
$$
其中函数$I(x)$是0、1损失函数，当$x\leq 0$时输出为1，否则为0。由于函数$I(x)$是不连续的函数，我们将其近似为连续函数$l(x)$，要求$l$是$I(x)$的凸上界，可以使用的候选有$l(x)=max(0,1-x)$或者$l(x)=log_2(1+2^{-x})$，所以可以得到：
$$
\begin{equation}
rank(w,c)\leq \overline{rank}(w,c)=\sum_{c^{'}\in C-\lbrace c\rbrace}l(\langle u_w, v_c-v_{c^{'}}\rangle)
\end{equation}
$$
我们希望rank模型将与当前单词有关的context的rank值变小，所以模型的目标函数可以是：
$$
\begin{aligned}
J(U,V)=\sum_{w\in W}\sum_{c\in \Omega_w}r_{w,c} \cdot \rho\left( \frac{\overline{rank}(w,c)+\beta}{\alpha} \right)
\end{aligned}
$$
其中$r_{w,c}$是用以量化$w,c$之间关联的权重，定义为：
$$
\begin{aligned}
r_{w,c}= \begin{cases}
(X_{w,c}/x_{max})^{\epsilon} & X_{w,c}< x_{max} \\
1 & otherwize
\end{cases}
\end{aligned}
$$
其中，$x_{max},\epsilon$是超参数，可以看出共现次数越大，权重越大。$\rho(\cdot)$是一个**单调递增的凹rank损失函数**，量化rank的"好坏"，首先，递增是明显的，要求是凹函数是因为希望其一阶导数非递增，从而使得相关性低的context拥有较小的敏感度（增长得慢，attention减少，想想y=x-1和y=logx），使得模型的健壮性得到提高，是很关键的一步。可能的损失函数有：
$$
\begin{aligned}
\rho(x)&=log_2(1+x) \\
\rho(x)&=1-\frac{1}{log_2(2+x)} \\
\rho(x)&=\frac{x^{1-t}-1}{1-t},\quad t\neq 1
\end{aligned}
$$
$\alpha,\beta$是超参数，控制模型“放弃rank高的上下文、注重rank低的上下文”的程度，`the rate at which the algorithm gives up is determined by the hyperparameters a and b`。

---

##### optimization
目标函数可以等价定义为
$$
\begin{aligned}
J(U,C)=\sum_{(w,c)\in \Omega}r_{w,c}\cdot\rho\left( \frac{\sum_{c^{'}\in C-\lbrace c\rbrace} l(\langle u_w, v_c-v_{c^{'}}\rangle)+\beta }{\alpha} \right)
\end{aligned}
$$
这是一个包含对$\Omega$和$C$求和的公式，当语料库很大时，问题就会变得难以处理。随机梯度下降（SGD）可以解决$\Omega$这一层的问题，但是$C$这一层的却难以解决，**除非函数$\rho(\cdot)$是一个线性函数**。可惜的是，函数$\rho(\cdot)$的特性要求其不是线性函数。

解决方法是对函数$\rho(\cdot)$进行一阶泰勒分解，由于其凹函数的性质，可以有
$$
\begin{aligned}
\rho(x) \le \rho(\xi)+\rho'(\xi)\cdot(x-\xi)
\end{aligned}
$$
对于所有的$x$和$\xi$都成立，并且当$x=\xi$时等号成立。
令$\Xi=\lbrace \xi_{w,c} \rbrace_{(w,c)\in\Omega}$，于是我们可以得到一个$J(U,V)$的上界
$$
\begin{aligned}
\overline{J}(U,V,\Xi)&=\sum_{(w,c)\in\Omega}r_{w,c}\cdot \left\lbrace \rho(\xi_{w,c})+\rho'(\xi_{w,c})\cdot \left( \frac{\sum_{c^{'}\in C-\lbrace c\rbrace} l(\langle u_w, v_c-v_{c^{'}}\rangle)+\beta }{\alpha} - \xi_{w,c} \right) \right\rbrace \\
&=\sum_{w,c,c^{'}} r_{w,c}\cdot \left( \frac{\rho(\xi_{w,c})+\rho'(\xi_{w,c})\cdot (\frac{\beta}{\alpha}-\xi_{w,c})} {|C|-1} + \frac{1}{\alpha}\rho'(\xi_{w,c})\cdot l(\langle u_w, v_c-v_{c^{'}}\rangle) \right)
\end{aligned}
$$
其中$(w,c,c^{'}) \in \Omega\times (C-\lbrace c \rbrace)$，等号成立的条件是
$$
\begin{aligned}
\xi_{w,c} = \frac{\sum_{c^{'}\in C-\lbrace c\rbrace} l(\langle u_w, v_c-v_{c^{'}}\rangle)+\beta }{\alpha}
\end{aligned}
$$
最小化上面这个函数就等于最小化原目标函数的上界，也就是最小化目标函数了。并且$\overline{J}(U,V,\Xi)$很好地支持SGD（内层不需要求和）。

---

##### algorithm

---

- 学习率$\eta$
- 重复
    - **阶段 1**
    - 重复
        - 从$\Omega$中均匀采样$(w,c)$
        - 从$C-\lbrace c\rbrace$中均匀采样$(c^{'})$
        - // update
        - $u_w\gets u_w-\eta\cdot r_{w,c}\cdot \rho'(\xi_{w,c})\cdot l(\langle u_w, v_c-v_{c^{'}}\rangle) \cdot (v_c-v_{c^{'}})$
        - $v_c\gets v_c-\eta\cdot r_{w,c}\cdot \rho'(\xi_{w,c})\cdot l(\langle u_w, v_c-v_{c^{'}}\rangle) \cdot u_w$
        - $v_{c^{'}}\gets v_{c^{'}}-\eta\cdot r_{w,c}\cdot \rho'(\xi_{w,c})\cdot l(\langle u_w, v_c-v_{c^{'}}\rangle) \cdot u_w$
    - 直到$U$和$V$都收敛
    - **阶段2**
    - 对所有的$(w,c)\in \Omega$
        - $\xi_{w,c}=\left( \sum_{c^{'}\in C-\lbrace c\rbrace} l(\langle u_w, v_c-v_{c^{'}}\rangle)+\beta \right)/\alpha$
- 直到所有的$U,V,\Xi$都收敛

---

阶段1的时间复杂度为$O(|\Omega|)$，阶段2的时间复杂度为$O(|\Omega||C|)$，复杂度较高。考虑到阶段2其实包含矩阵乘法运算，可以考虑使用一些高效的矩阵乘法算法。训练完成后，$U,V$分别就是对应的词向量。

**引用**
[1]. WordRank: Learning Word Embeddings via Robust Ranking
