---
title: DeepFM
mathjax: true
date: 2021-01-31 17:35:23
tags: [deep learning, recommendation]
categories: Algorithm
---

### wide & deep

> Wide & Deep Learning for Recommender Systems. 2016

wide指的是形如LR的这种特征较为稀疏的比较“宽”的模型，这类模型的特点是计算简单、可解释性优秀（有比较好的**记忆能力**）；deep指的是各种NN类型的，将“宽”的输入转化为embedding，然后对embedding做处理，优点是不需要手工处理特征，且有较强的**泛化能力**。

wide&deep模型就是要将wide和deep联合起来，取各自的长处，其图示如下：

![wide&deep model](/images/wide&deep.png)

模型的输出为：
$$
f(x|\theta)=\sigma(W_{wide}^Tx+W_{deep}^Tx+b)
$$
实现中，wide部分可以考虑人工加入组合特征，以提升模型效果。

两部分模型需要联合在一起进行训练
- wide部分用FTRL进行优化，辅以L1正则项
- deep部分用了adagrad，当然也可以用adam这些方法


### DeepFM

> DeepFM: A Factorization-Machine based Neural Network for CTR Prediction. 2017

在推荐系统中，轻量模型一般用FM而不用LR，因为FM中考虑了特征交叉且对稀疏数据比较友好。DeepFM就从这个角度出发，将wide&deep模型中的LR换成了FM，其主要结构如下图

![deepfm model](/images/deepfm.png)

可以看到FM有两部分，加法是一阶特征的加权求和，乘法是利用隐向量内积计算出来的组合特征的部分；

deep网络部分则是使用特征的embedding作为输入，对于每个field，将其转化为一个dense embedding（这里搞个field的概念是防止映射矩阵太大，按field进行映射可以有效降低参数数量），然后将所有的embedding作为深度网络的输入。那么embedding怎么来的呢，**embedding是由原始特征通过以FM的隐向量为参数的映射得到**，如下图所示。

![deepfm embedding](/images/deepfm-embedding.png)

多说一句，数值类特征直接使用数值，非数值类特征转成one-hot。模型输出公示如下：
$$
y=\sigma(y_{NN}+y_{FM})
$$
最后输出的结果可以作为ctr预估的结果。

因为FM、DEEP两个部分共享参数，也就是特征的隐向量，所以这部分可以一起训练。

实际应用中，这种混合模型可能会出现问题，因为两边的训练速度不一致，所以收敛速度不一致。应用中可能需要调整两边的学习率。

---
