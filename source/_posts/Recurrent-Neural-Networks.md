---
title: Recurrent Neural Networks
date: 2017-05-05 11:58:31
tags: [machine learning, deep learning]
categories: Algorithm
---

`RNN`中文名为递归神经网络，是深度学习理论的典型模型之一。`DNN`和`CNN`都假设输入是相互独立的，但在某些情况中，比如机器翻译，输入往往还应该包含上下文信息，所以`DNN`和`CNN`在处理时序或者顺序数据时会丢失上下文信息。`RNN`就是处理时序数据的典型代表，其延伸版本`LSTM`已经在诸多领域取得了辉煌的成绩。

##### vanilla RNNs
以`vanilla RNNs`为例，为了达到记忆效果，其`RNN`的基本结构及展开结构如下：

![RNN结构图](http://ww1.sinaimg.cn/large/9bcfe727gy1ffagf00esuj20m308vaaz.jpg)

展开后的结构通俗易懂，其中$x_i$时序列输入，比如单词中的字母序列，$o_i$表示输出序列，比如当前字母的下一个字母，$s_i$表示隐层的值，$U,V,W$是连接权值矩阵（共享），$s_i$经过$V$映射得到$y_i$，$y_i$经过`softmax`(这里的softmax只做归一化操作，不改变维度)得到结果$o_i$。

###### 前向传播
前向传播和`DNN`的前向传播类似，不同点在于`RNN`中隐层的输入不仅包含当前时刻的输入，还包含前一时刻的隐层输入。前向传播可由以下公式给出：
$$
\begin{aligned}
s_t &= f(Ws_{t-1}+Ux_t+b_1) \\
y_t &= Vs_t+b_2 \\
o_t &=softmax(y_t)
\end{aligned}
$$

###### Back Propagation Through Time
反向训练的过程与DNN的反响传导类似，不同点在于权值共享和隐层的处理，基本思路还是链式求导法则,误差函数可以是平方误差，也可以是交叉熵，这里选用交叉熵
$$
E_t=-o_tlog\hat{o_t}
$$
激活函数可以是`tanh`，也可以是`LeRU`。训练过程就是计算参数梯度累加值，最后更新参数。对一个序列$t=1,...,T$，训练过程如下：
$$
\begin{aligned}
&1. 初始化d_W,d_V,d_U, d_{b_1}, d_{b_2}, d_s,d_{s_{next}} \\
&2. For\ t\ from\ T\ to\ 1: \\
&3. \; \; \; \; \; \; \; \; d_y=\hat{o_t}-o_t \\
&4.  \; \; \; \; \; \; \; \;dV+=d_ys_t^T \\
&5. \; \; \; \; \; \; \; \; d_{b_2}+=d_y \\
&6.  \; \; \; \; \; \; \; \; d_s=V^Td_y+d_{s_{next}} \\
&7. \; \; \; \; \; \; \; \; d_{s_{raw}}=\frac{df(s_t)}{d_{s_t}}d_s \\
&8.  \; \; \; \; \; \; \; \; d_{b_1}+=d_{s_{raw}} \\
&9.  \; \; \; \; \; \; \; \; d_U+= d_{s_{raw}}x_t^T \\
&10. \; \; \; \; \; \; \; d_W+= d_{s_{raw}}s_{t-1}^T \\
&11. \; \; \; \; \; \; \;  d_{s_{next}}= W^Td_{s_{raw}}
\end{aligned}
$$
需要说明的是第3行$d_y=\frac{\partial E_t}{\partial y_t}$，其中推导比较麻烦，见文献[4]。由于在$t$时刻时就已经对$s_{t-1}$进行求导了，所以下一次需要加上这个导数，每一轮中对下一轮的$s$求导结果存储在$ d_{s_{raw}}$中，下一轮到的时候让$s_t$梯度加上$ d_{s_{raw}}$即可。此外式中的$d_{s_{raw}}$表示的是$Ws_{t-1}+Ux_t+b_1$的梯度，如果写成$s_{raw}=Ws_{t-1}+Ux_t+b_1,s_t=f(s_{raw})$可能会更好理解。训练完成得到各参数梯度和后，使用梯度下降思想更新参数即可。

###### RNN的用途

![RNN用途](http://ww1.sinaimg.cn/mw690/9bcfe727ly1ffaih8esrfj20rv094n0h.jpg)

`one to many` ：输入一个图片，输出一句描述图片的话。
`many to one` ：输入一句话，判断是正面还是负面情绪。
`many to many` ：有个延时的，譬如机器翻译。
`many to many` ：输入一个视频，判断每帧类别。

###### RNN的限制
**`vanilla RNN`无法解决长时依赖问题**(即当前的输出与前面很长的一段序列有关，一般超过十步就无能为力了)，`vanilla RNN`存在着梯度爆炸和梯度消散的问题（**因为梯度需要不断乘以矩阵$U,V,W$，如果矩阵最大特征值大于1，乘多次以后就会出现梯度爆炸；如果小于1，乘多次则会出现梯度消散**（联想一下多次乘以一个标量，大于1则爆炸，小于1则接近0））。

解决这个问题的方案：
- 梯度爆炸：梯度裁剪的方式避免，譬如梯度大于5就强制梯度等于5
- 梯度消散：LSTM（LSTM也可能出现梯度爆炸，所以需要梯度裁剪）

`vanilla RNN`简单，但是效果不好！
##### LSTM（Long Short Term Memory）
上一节描述了`vanilla RNN`以及其局限性，`vanilla RNN`结构简单，LSTM的结构就稍微复杂点，如下图所示：

![LSTM结构](http://ww1.sinaimg.cn/mw690/9bcfe727ly1ffakkmkg7pj20yg0cyn00.jpg)

在LSTM中引入了细胞结构的概念，并引入“门”结构来去除或者增加信息到细胞状态的能力，门是一种让信息选择式通过的方法，他们包含一个 `sigmoid` 神经网络层和一个 pointwise 乘法操作。这里箭头合并符号表示向量堆叠拼接，(比如$w_1x_1+w_2x_2+b$可以写成$[w_1\ w_2][x_1\ x_2]^T+b=WX^T+b$)，箭头合并表示拷贝复用。

LSTM 拥有三个门，分别是：
**忘记门**
![忘记门](http://ww1.sinaimg.cn/mw690/9bcfe727ly1ffaot7pdd6j20yg0an75d.jpg)

忘记门读取上一状态的隐层输出$h_{t-1}$和$x_t$，输出一个与$C_{t-1}$长度相同的向量，每个元素都是$[0,1]$之间的数字，表示$C_{t-1}$的通过率，1 表示完全保留，0 表示完全舍弃。

**输入门**
![输入门](http://ww1.sinaimg.cn/mw690/9bcfe727ly1ffaoypc44qj20yg0anabj.jpg)

这一步是要更新细胞状态，先将旧细胞状态$C_{t-1}$与$f_t$相乘，丢弃掉我们确定需要丢弃的信息。$\hat{C_t}$使用的激活函数是`tanh`，输出范围是$[-1,1]$，比`sigmoid`有更广的范围。$i_t$的功能与$f_t$类似，决定$\hat{C_t}$的通过情况。然后将$C_{t-1}$与$f_t$乘积加到$C_{t-1}$上更新细胞状态为$C_t$.

![更新细胞状态](http://ww1.sinaimg.cn/mw690/9bcfe727ly1ffautyg5vwj20yg0anjsl.jpg)

**输出门**
![输出门](http://ww1.sinaimg.cn/mw690/9bcfe727ly1ffap1r93v8j20yg0anwfz.jpg)

首先，运行一个`sigmoid`层来确定$[h_{t-1}, x_t]$的哪个部分将输出出去。接着，我们把细胞状态通过 tanh 进行处理（得到一个在 -1 到 1 之间的值）并将它和`sigmoid`门的输出相乘，最终我们仅仅会输出我们确定输出的那部分。

**引用**
[1]. 斯坦福大学深度学习资料 CS231n
[2]. [Standford CS231n 循环神经网络 简要笔记](http://blog.csdn.net/wyl1987527/article/details/56682347)
[3]. [简书：理解 LSTM 网络](http://www.jianshu.com/p/9dc9f41f0b29)
[4]. [softmax分类器+cross entropy损失函数的求导](http://www.cnblogs.com/wacc/p/5341676.html)
