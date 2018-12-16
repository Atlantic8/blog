---
title: GRU and LSTM
mathjax: true
date: 2018-12-16 21:27:29
tags: [Deep Learning, Machine Learning]
categories: Algorithm
---

GRU和LSTM都是RNNs中的特殊cell，目的是为了解决标准RNNs中的长期依赖的问题。这个问题是由于简单的RNNs求导公式中存在多个相同矩阵相乘的问题，容易造成梯度消散。使用Relu也只能说在一定程度解决了消散问题，但是会存在梯度爆炸的问题（见参考文献2）。

### 基本结构
相似点：都是通过引入门结构来解决长期依赖问题
不同点：门的数量，种类有差异
#### GRU
每个GRU单元的输入有$x^{(t)}$、$h^{(t-1)}$，分别表示当前步的输入和上一步的隐状态。**基本思想是先构建新的memory，然后再和上一隐含状态加权得到新的隐含状态**。

基本结构如下图所示

![image](http://ww1.sinaimg.cn/mw690/9bcfe727ly1fwkv73w0v5j20gy08y75m.jpg)

GRU包含几个门，分别是
- reset($r^{(t)}$)：从构建新new memory的角度出发，$r^{(t)}$决定$h^{(t-1)}$对new memory的贡献多大
- new memory($\hat{h}^{(t)}$)：由当前输入和上一步的隐含状态决定，当然，上一阶段隐含状态的重要性也受到reset gate的影响
- update($z^{(t)}$)：决定$h^{(t-1)}$对$h^{(t)}$的贡献多大
- hidden state($h^{(t)}$)：有上一步的隐含状态和new memory加权得到，权重有update gate决定

公式如下，懒得打了：

![image](http://ww1.sinaimg.cn/mw690/9bcfe727ly1fwkv5yp61gj20a30323yt.jpg)

#### LSTM
同样地，每个LSTM单元的输入有$x^{(t)}$、$h^{(t-1)}$，分别表示当前步的输入和上一步的隐状态。需要注意的是，**LSTM cell中的流动数据不仅包括隐含状态，还包括final memory** 。然后生成final memory，这个过程需要input gate和forget gate。最后**由output gate辅助生成当前的隐含状态(GRU没有这一步)**。结构图如下

![image](http://ww1.sinaimg.cn/mw690/9bcfe727ly1fwkw7pv9lvj20gy0c2mys.jpg)

- new memory：由当前输入和前一步的隐含状态决定，前一步的隐含状态贡献度由
- final memory：由上一步的final memory和当前的new memory生成。其中上一步final memory的贡献度由forget gate决定，当前new memory的贡献度由input gate决定
- input gate：作用在上面已经说明了，由上一步隐含状态和当前输入决定
- forget gate：同input gate
- output gate：决定final memory对当前隐层状态的贡献

贴一下公式

![image](http://ww1.sinaimg.cn/mw690/9bcfe727ly1fwkwdq6le8j20ay0473z1.jpg)

需要注意的是，上面公式倒数第二个写错了，forget gate决定的是$c^{(t-1)}$.


关于LSTM、GRU是如何避免梯度问题的，关键是将简单RNN的求导过程中的乘法变成了加法，之前的记忆不会受到乘法的影响，因此不会过分衰减。同时又通过其他的门结构保证灵活性。


---

**引用**

[1]. [LSTM 和GRU的区别](https://blog.csdn.net/u012223913/article/details/77724621)

[2]. [理解RNN梯度消失和弥散以及LSTM为什么能解决](https://blog.csdn.net/hx14301009/article/details/80401227)



---
