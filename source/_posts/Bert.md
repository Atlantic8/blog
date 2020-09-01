---
title: Bert
mathjax: true
date: 2020-08-30 12:58:01
tags: [deep learning, NLP]
categories: Algorithm
---

### 介绍
BERT=Bidirectional Encoder Representation from Transformers，就是用**双向transformer编码器**学习表征


基本结构如下

![image](https://raw.githubusercontent.com/Atlantic8/picture/master/bert-1.jpg)

模型是层级结构，每层一个transformer的encoder。与模型体量相关的变量是：
- 层数$L$：即transformer encoder的个数
- 隐层维度$H$：等于word embedding的维度
- 多头注意力的头数$A$：self-attention中multi-head的head数量

### 输入

![image](https://raw.githubusercontent.com/Atlantic8/picture/master/bert-2.jpg)

输入token表征是由三个加起来得到的，分别是token的embedding、位置编码、句子的embedding。bert中位置编码是当作参数学习出来的（transformer则是写死的）


### 预训练
##### Masked语言模型
训练过程中随机mask 15%的token，而不是把像cbow一样把每个词都预测一遍。最终的损失函数只计算被mask掉那个token。

**如果一直用标记[MASK]代替（在实际预测时是碰不到这个标记的）会影响模型**，所以随机mask的时候10%的单词会被替代成其他单词，10%的单词不替换，剩下80%才被替换为[MASK]

##### 下个句子预测
涉及到QA、推理方面的任务，所以训练加入了句子关系建模。训练的输入是句子A和B，模型预测B是不是A的下一句。

语料的选取很关键，要选用document-level的而不是sentence-level的，这样可以具备抽象连续长序列特征的能力。

### 微调与应用

![image](https://raw.githubusercontent.com/Atlantic8/picture/master/bert-3.jpg)

- 单个句子分类：结果在CLS对应的位置
- 句子对分类：结果在CLS对应的位置
- 问答任务：第二个句子是答案段落，

调参
- Batch size: 16, 32
- 学习率 (Adam): 5e-5, 3e-5, 2e-5
- Number of epochs: 3, 4

### 总结
优点
- 用的是Transformer，也就是相对rnn更加高效、能捕捉更长距离的依赖
- 效果很好

缺点：
- [MASK]标记在实际预测中不会出现，训练时用过多[MASK]影响模型表现
- 每个batch只有15%的token被预测，所以BERT收敛得比left-to-right模型要慢

---

### 相关工作

##### ELMO

![image](https://raw.githubusercontent.com/Atlantic8/picture/master/bert-4.jpg)

ELMO使用两层双向LSTM抽取特征，最后将双向的结果拼接起来
##### GPT

![image](https://raw.githubusercontent.com/Atlantic8/picture/master/bert-5.jpg)

GPT使用的是自左向右的transformer，即不能看到后面的数据，只能与前面的word计算attention

---

[1]. BERT: Pre-training of Deep Bidirectional Transformers for
Language Understanding.

[2]. [Google BERT详解](https://zhuanlan.zhihu.com/p/46652512)


---

