---
title: NLP Pre-train Models after Bert
mathjax: true
date: 2020-08-30 13:16:49
tags: [deep learning, NLP]
categories: Algorithm
---

BERT开启了NLP领域预训练模型的时代，BERT之后大量的改型出现，以下会介绍一些。

### ALBERT
ALBERT的设计目标是解决BERT参数量大的问题

其主要做了如下的修改
- embedding分解
    - intuition是：transformer的输入词的embedding维度和隐层输出维度一样大，但是**隐层除了词本身信息还包含了上下文信息**，所以词的embedding维度可以小一点
    - 降低维度的方法是**对输入的onehot矩阵进行分解，映射到低维度空间E，然后再映射到H维**，输入到Transformer中。将参数量由O(VH)降到O(VE+EH)，当E远小于H时，参数量会下降很多。（假设V为词的总数）
- 参数贡献
    - 共享encoder内的所有参数，包含多头注意力和前向网络
- Sentence-Order Prediction
    - BERT的next sentence prediction是个二分类任务，负样本是通过采用两个不同的文档的句子，后续的研究发现该任务效果并不好。NSP其实**包含主题预测与句子关系一致性预测两个子任务**，但是主题预测相比于关系一致性预测简单太多了，模型学习NSP任务的时候可能**只学到了主题预测**，而没学到句子关系一致性
    - SOP则在样本选取上去除了主题不同的因素，将**正样本反过来当作负样本**

ALBERT论文表示在训练了100w步之后，模型依旧没有过拟合，于是乎作者移除了dropout，没想到对下游任务的效果竟然有一定的提升。这也是业界**第一次发现dropout对大规模的预训练模型会造成负面影响**

### ERNIE
ERNIE是大百度的中文预训练模型，有两个版本

##### 1.0
ERNIE1.0在BERT的基础上做了如下事情
- 在mask语言模型上，不再局限于mask单个token，而是考虑mask短语和实体
- **直接对先验语义知识单元进行建模，增强了模型语义表示能力**
- 海量中文数据，Dialogue Language Model

##### 2.0
ERNIE2.0的要点如下：
- 多任务学习的引入，**输入层加入了task embedding**
- 构建了词法级别，语法级别，语义级别的预训练任务
    - 词法
        - **mask短语和实体**，同1.0
        - **大写字母预测**：大写的词一般会有特殊含义
        - **Token-Document关系预测**：预测一个词在文中的A 段落出现，是否会在文中的B 段落出现
    - 语法
        - **句子顺序预测**：文本分段，所有shuffle的组合后模型预测正确顺序
        - **句子距离预测**：三分类任务（0表示两个句子是同一个文章中相邻的句子，1表示两个句子是在同一个文章，但是不相邻，2表示两个句子是不同的文章）
    - 语义
        - 判断句子对之间的**语义关系**，比如修辞
        - 搜索下**query和title的相关性**
- 大量的百度生态语料
    - 搜索日志
    - 贴吧对话
    - 百科数据
    - 新闻内容

### XLNET
> XLNet: Generalized Autoregressive Pretraining
for Language Understanding

Elmo、GPT这种单向语言模型属于**自回归语言模型(
autoregressive)**，模型在当前位置只能看到之前看到过的数据。Bert这类双向语言模型，属于自编码语言模型（autoencoder），可以**对上下文进行完整建模**，在BERT与GPT的对比数据中也可以看出来其优点。但是这种模型也存在问题：
- bert训练时用到了mask语言模型，引入了[MASK]标识，但是fine-tuning阶段没有，导致**预训练阶段和fine-tuning阶段存在不一致的问题**
- 模型在预测一个被mask掉的单词，**无法利用其他被mask掉的单词信息**

xlnet就是想鱼和熊掌兼得，那么怎么能够在单词Ti的上文中Contenxt_before中揉入下文Context_after的内容呢?

##### Permutation Language Model
最naive的思想就是：在预测$x_k$时，固定$x_k$，将$x_{!= k}$打乱，这样当前单词就能看见原来在其之后的单词了。在随机排列组合后的各种可能里，再选择一部分作为模型预训练的输入。

但是这样会有问题，假设出现一个长度为n的序列，原序列为$x$，两个排列$z^{(1)},z^{(2)}$，第t个位置不一样(对应于之前的$x_i,x_j$)，之前的位置都一样，所以由自回归语言模型定义可知
$$
p_{\theta}(z^{(1)}_t(x)=x_i)=p_{\theta}(z^{(2)}_t(x)=x_j)
$$
即，**对$x_i,x_j$的预测满足同一分布**，这显然是不合理的

并且，**fine-tuning时不可能也去排列组合原始输入**

#### 双流自注意力机制
双流注意力机制就是为了解决上述问题的，分为**query流**和**内容流**，其实就是在两个层面表示当前输入（内容层面和位置层面），其中
- 内容流self-attention
    - 内容编码信息$h_t$，计算方式和标准的self-attention一致
    - 能看到自己
    - 内容流输入是token的Embedding向量
- query流self-attention
    - 位置编码信息$g_t$，后一层的query向量不包含当前位置的查询向量
    - 不能看到自己
    - 在模型输入端对每个token都是统一的，是可学习的参数

![xlnet-1](https://raw.githubusercontent.com/Atlantic8/picture/master/xlnet-1.PNG)

上图中，预测下一层的内容向量时，用到当前层能看到的所有内容向量（**包括自己**）[a]；预测下一层的query向量时，用到当前层能看到的所有内容向量（**不包括自己**）[b]。

整体上来看，以序列$x=[x_1,x_2,x_3,x_4]$为例，通过**attention mask矩阵**来完成mask操作，决定排列顺序后即可得到mask矩阵。假如排列之后得到$[x_3,x_2,x_4,x_1]$，mask矩阵也有两个分为内容流（能看见自己）、query流（不能看见自己）两个，上图中，红色表示可见，白色表示不可见，第$k$行表示第$k$个位置能看到哪些位置的信息

##### Transformer XL
借助transformer xl，**增强对长文本的友好程度**，其主要思想就是分段然后引入recurrent连接结构

##### pretrain & finetune
- pretrain阶段
    - 在输出端**对query流向量**预测相应的token
    - 只预测有足够长的依赖上下文的token，降低训练难度
    - **放弃了Next Sentence Prediction任务**
    - 与BERT相比，加大增加了预训练阶段使用的数据规模
- finetune阶段
    - **只需要内容流向量**，不再需要query流向量
    - 使用的时候，**只需要内容流向量**

### RoBerta
> RoBERTa: A Robustly Optimized BERT Pretraining Approach

较于BERT，其升级点如下
- 训练模型时间更长，Batch Size更大，数据更多
- 放弃Next Sentence Prediction训练任务
- 对较长序列的训练
- 动态mask应用于训练数据的mask模式
    - BERT静态mask：随机mask和替换在开始时只执行一次，后续保存
    - 作者将训练数据重复10次，以便在40个epoch中以10种不同的方式对每个序列进行mask，**避免在每个epoch中对每个训练实例使用相同的mask**
- 新建数据集（CC-NEWS）
- 使用Sennrich[2]等人提出的Byte-Pair Encoding (BPE)字符编码
    - 避免出现较多的未登录词

### T5

### ELECTRA
> Efficiently Learning an Encoder that Classifies Token Replacements Accurately

ELECTRA的特色如下
- 放弃BERT随机选取token预测的方法，而是通过MLM过滤非常容易学到的token，加大学习难度
- 预测目标不是预测目标究竟是哪个token，而是预测这个句子中哪些词被替换过，也就是说**模型需要看输入的每一个token，而不仅仅是被mask选取的那些，加速了学习过程**
- 解决BERT中MASK标志在train和finetune阶段的不一致问题

##### GAN视角

![GAN视角](https://raw.githubusercontent.com/Atlantic8/picture/master/electra-1.PNG)

模型整体可以看成有两部分，一部分是Generator，一部分是Discriminator。模型依然需要随机地mask一部分token，但是用途不一样

流程
- 对于输入文本序列，随机mask一部分token（15%）
- 带MASK标志的输入序列，G会**预测每个被MASK掉的token具体是什么**，这里其实就是MLM做的事情
- D**判别这个序列中哪些token是G生成的**
    - 二分类，

需要注意的是，G的训练方式与传统的GAN不一样，**G的训练目标不是去糊弄Discriminator，而是通过极大似然估计训练**。因为**D的梯度不能直接流到G**，原因是G输出的token在表示上是离散的
$$
\mathcal{L}_{MLM}(x,\theta_G)=\mathbb{E}\left(\sum_{i}-\log p_G(x_i|x^{masked})\right)
$$
其中，$i$是被选中mask的token序号。作者也尝试了用强化学习的训练思路做，但是效果没有直接使用MLE效果好

而Discriminator因为是要对每个token判断是否是原始token，所以可以看成一个二分类问题（序列上看也可以看成序列标注，只是tag之间没有直接关系），其损失函数为交叉熵形式
$$
\mathcal{L}_{D}(x,\theta_G)=\mathbb{E}\left(-\sum_{t=1}^n\mathbf{I}(x_t^{G}=x_t)\log D(x^G,t) + \mathbf{I}(x_t^{G}\ne x_t)\log (1-D(x^G,t)) )\right)
$$
这里可以看成是使用MLM的**负采样**方法，颇有word2vec的CBOW意味。类似地，把多分类换成二分类也可以有效降低参数数量。此外，D的目标也刚好消除了BERT中MASK标识导致的mismatch问题

所以，整体的目标就是
$$
\min_{\theta_G,\theta_D}\sum_{x\in X}\mathcal{L}_{MLM}+\lambda\mathcal{L}_{D}(x,\theta_G)
$$
其中，$X$是整体的数据集，$\lambda$是平衡系数，作者设为50，原因是D的任务较G简单，损失也小。

##### 其他点
- G和D共享token的embedding
    - G会对embedding进行调整，但是D不会，所以需要参数共享
- 建议G要小一点
    - G太猛了，D学起来会比较费劲。D可能会将注意力更多放在对G的建模上而不是实际的数据分布
    - 建议G的规模为D的1/4-1/2


---

[1]. [一文揭开ALBERT的神秘面纱](https://blog.csdn.net/u012526436/article/details/101924049)

[2]. [一文读懂最强中文NLP预训练模型ERNIE](https://blog.csdn.net/PaddlePaddle/article/details/102713947)

[3]. [XLNet:运行机制及和Bert的异同比较](https://zhuanlan.zhihu.com/p/70257427)

[4]. [自然语言处理之XLNet](https://zhuanlan.zhihu.com/p/86845458)

[5]. [XLNet: Generalized Autoregressive Pretraining
for Language Understanding](https://arxiv.org/pdf/1906.08237.pdf)

[6]. [RoBERTa: A Robustly Optimized BERT Pretraining Approach](https://arxiv.org/pdf/1907.11692.pdf)

[7]. [如何评价RoBERTa?](https://www.zhihu.com/question/337776337)

[8]. [Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer](https://arxiv.org/pdf/1910.10683.pdf)

[10]. [ELECTRA: PRE-TRAINING TEXT ENCODERS AS DISCRIMINATORS RATHER THAN GENERATORS](https://openreview.net/pdf?id=r1xMH1BtvB)

[11]. [如何评价NLP算法ELECTRA的表现？](https://www.zhihu.com/question/354070608/answer/885907890)
