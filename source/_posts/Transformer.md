---
title: Transformer
mathjax: true
date: 2020-08-30 12:53:14
tags: [deep learning]
categories: Algorithm
---


### 介绍
Transformer放弃了将RNN/CNN作为encoder-decoder，仅仅用attention组件。不仅取得了更好的效果，并且其可并行的结构也可以降低训练时间

整体上看，Transformer是一个序列到序列的模型，基于encoder-decoder框架。编码器、解码器多个叠加在一起，大致如下所示：

![image](https://raw.githubusercontent.com/Atlantic8/picture/master/transformer-1.jpg)


### 编码器

![image](https://raw.githubusercontent.com/Atlantic8/picture/master/transformer-2.jpg)

每个编码器包括两个层，分别是多头注意力层和position-wise的前向网络，每个层都有一个残差连接+层normalization，

##### 多头注意力层

![image](https://raw.githubusercontent.com/Atlantic8/picture/master/transformer-3.jpg)

先看**单头注意力**，其核心是Scaled Dot-Product Attention（编码器中的Scaled Dot-Product Attention不需要mask，因为编码时**可以看到整个序列**）。基本是这样，每个头有3个线性映射矩阵$Q, K, V$，对于输入（向量序列构成矩阵），乘以3个矩阵映射到$Q',K',V'$，然后计算
$$
softmax(\frac{Q'\times K'^T}{\sqrt{d_k}})V'
$$
其实也就是计算$Q'$每个向量和$K'$每个向量的关系，归一化后当作$V'$的系数加权求和，其中$d_k$是$Q'$中单个向量的维度。

多头注意力，每个头有不同的$Q, K, V$（目的是学习到不同的表征），得到的多个**结果拼接起来**，最后做一个线性变换

encoder是并行的体现，**并行主要是可以同时计算多个head的输出**

##### 前向网络
$$
F(x)=\max(0, xW_1+b_1)W_2+b_2
$$
这一层的输入输出维度一直，并且，属于输入序列中的每个位置i，其对应的参数是一致的，所以叫position-wise

### 解码器

![image](https://raw.githubusercontent.com/Atlantic8/picture/master/transformer-4.jpg)

解码器有两种attention，第一种直接作用在输入上的self-attention，多了mask的概念（因为**解码按顺序进行的，不能获取未来的信息**）。第二种不是self-attention，其中的$K',V'$均来自编码器，$Q'$来自解码器

多个解码器叠加，每个解码器中的第二个attention中的$K',V'$均来自编码器。最后的输出经过线性变换+softmax得到输出

### 输入与位置编码
对输入序列的每一个word，先将其通过词嵌入算法转换为词向量，第一个编码器接受词向量序列，后面的编码器接受前面编码器的输出

但是问题是这种方法没有考虑加入位置信息，所以作者加入了位置向量，并且**将每个word的位置向量和词向量加起来作为这个词的特征向量**。每个word的位置向量和其词向量维度一样，假设其位置为$pos$，则其位置向量为
$$
PE_{(pos,2i)}=\sin(\frac{pos}{10000^{2i/d}}) \\
PE_{(pos,2i+1)}=\cos(\frac{pos}{10000^{2i/d}})
$$
其中$d$是词向量的维度。这个编码可以表示词之间的相对位置。


### 总结
self-attention处理特别长的序列时，计算复杂度会比较高，会做一些限制，比如当前位置只能看到其前后$r$个位置的词


self-attention之于CNN、RNN的优势
- 每层的计算复杂度
- 序列操作
- 最大路径长度（信号需要在网络中前向、后向传递的长度）
- 可解释性

前三项的比较如下图

![image](https://raw.githubusercontent.com/Atlantic8/picture/master/transformer-5.png)

其中，$n$序列长度，$d$是模型维度，$k$是卷积核大小，$r$是受限的self-attention对应的neighborhood大小

transformer的缺陷如下：
- 是不是对局部特征的捕捉能力降低了
- 位置编码用三角函数是不是不够


---

最后贴上经典的transformer动态图

![image](https://raw.githubusercontent.com/Atlantic8/picture/master/transform20fps.gif)

---

### Transformer XL
理论上，Transformer的encoder可以接受无限长的输入，但是限于计算资源问题，通常encoder处理的长度也是有限的。Transformer XL就是要**解决输入长度过长的情况**

###### 语言模型建模
以语言模型为例，语言模型就是要计算输入序列的概率
$$
P(t_{0:L})=p(t_0)\prod_{i=1}^Lp(t_i|t_{0:t-1})
$$
对于条件概率$p(t_i|t_{0:t-1})$，可以使用transformer对其建模。需要注意的一点是，上面的条件概率要求**只能看到当前左侧的token**，所以需要使用类似masked attention的方法

![image](https://raw.githubusercontent.com/Atlantic8/picture/master/transformer-xl.PNG)

###### vanilla model
实作上，一种简单粗暴的方法是**对输入进行截断**，在每个segment内分别处理，**忽略了段之间的上下文信息**。具体地
- 训练阶段：把文本切成segment，每个segment单独训练
- 预测阶段：按segment处理，移动步长为1

大致的训练方法见[ 深度Transformer构建字符语言模型 ](https://zhuanlan.zhihu.com/p/87576748)

###### recurrent model
主要思想是将上一个segment对应的hidden state保存起来，论文图中当前segment也只会用到上一segment中的信息，不用上上个segment的信息。可以形成segment的recurrent结构，不过只要增大cache，可以考虑使用前面更多的segment信息

---

[1]. Attention Is All You Need. 2017

[2]. [图解Transformer（完整版）](https://blog.csdn.net/longxinchen_ml/article/details/86533005)

[3]. [Transformer-XL: Attentive Language Models
Beyond a Fixed-Length Context]()https://arxiv.org/pdf/1901.02860.pdf

---
