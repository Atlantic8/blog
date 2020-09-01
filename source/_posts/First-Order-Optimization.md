---
title: First Order Optimization
mathjax: true
date: 2020-08-30 12:46:31
tags: Optimization
categories: Math
---

##### SGD：Stochastic Gradient Descent

mini-batch的更新方法

---

- 输入学习率$\epsilon$
- 停止条件未满足
    - 从样本集合中采样$m$个样本的batch
    - 计算梯度$g=\frac{1}{m}\bigtriangledown_{\theta} \sum_i L(f(x_i,\theta),y_i)$
    - 参数更新$\theta=\theta-\epsilon g$

---

学习率是SGD中的关键参数。在实践中，有必要随着时间推移减小学习率，一般的实践是将学习率线形衰减指导第$\tau$次迭代
math
\epsilon_k=(1-\alpha)\epsilon_0+\alpha \epsilon_{\tau}

其中$\alpha=\frac{k}{\tau}$。在$\tau$次迭代后，一般使$\epsilon$保持常数。$\tau_t$可以设置为$\tau_0$的1%。

##### Momentum

![image](https://raw.githubusercontent.com/Atlantic8/picture/master/momentum.jpg)

SGD在处理高曲率、小但一致的梯度，或者带噪声的梯度时，学习过程有时会很慢。动量算法引入了变量$v$充当速度角色。

---

- 输入初始速度$v$，学习率$\epsilon$
- 停止条件未满足
    - 从样本集合中采样$m$个样本的batch
    - 计算梯度$g=\frac{1}{m}\bigtriangledown_{\theta} \sum_i L(f(x_i,\theta),y_i)$
    - 计算更新速度$v=\alpha v-\epsilon g$
    - 参数更新$\theta=\theta+v$

---

$\alpha$叫做动量参数，一般取值为0.5、0.9、0.99。

##### Nesterov：Nesterov Accelerated Gradient（NAG）

此方法与动量方法的不同在于计算梯度步骤，**Nesterov**在每一步更新中，使用当前参数和速度得到临时更新，然后在临时更新后的参数的基础上计算梯度。**Nesterov方法可以解释为往标准动量方法中添加了一个校正因子**。

---

- 输入初始速度$v$，学习率$\epsilon$
- 停止条件未满足
    - 从样本集合中采样$m$个样本的batch
    - 计算临时更新$\hat{\theta}=\theta+\alpha v$
    - 计算梯度$g=\frac{1}{m}\bigtriangledown_{\hat{\theta}} \sum_i L(f(x_i,\hat{\theta}),y_i)$
    - 计算更新速度$v=\alpha v-\epsilon g$
    - 参数更新$\theta=\theta+v$

---

![image](https://raw.githubusercontent.com/Atlantic8/picture/master/nesterov.jpg)

##### AdaGrad
AdaGrad**记录参数在每个维度上的梯度累计量，然后缩放每个参数反比于其梯度累积量平方根**，减小梯度过大的方向更新过快、梯度过小的方向更新过满的缺陷。

---

- 输入小常数$\delta(10^{-7})$，学习率$\epsilon$
- 初始化梯度累计量$r=\bold{0}$
- 停止条件未满足
    - 从样本集合中采样$m$个样本的batch
    - 计算梯度$g=\frac{1}{m}\bigtriangledown_{\theta} \sum_i L(f(x_i,\theta),y_i)$
    - 累计平方梯度$r=r+g\odot g$
    - 计算更新$\Delta \theta\gets- \frac{\epsilon}{\delta+\sqrt{r}}\odot g$
    - 应用更新$\theta= \theta+\Delta \theta$

---

在凸优化背景下，AdaGrad有一些令人满意的性质。但经验上，对于训练深度模型，AdaGrad**从训练开始时累计梯度会导致有小学习率过早、过量的减小**。此算法在某些模型上效果不错，但不是全部。

##### RMSProp：Root Mean Square Prop

RMSProp是为了解决AdaGrad中**从训练开始时累计梯度会导致有小学习率过早、过量的减小**的缺陷，也有忘掉过去的功能，方法是引入参数$\rho$进行权重衰减。

---

- 输入小常数$\delta(10^{-6})$，学习率$\epsilon$，衰减速率$\rho$
- 初始化梯度累计量$r=\bold{0}$
- 停止条件未满足
    - 从样本集合中采样$m$个样本的batch
    - 计算梯度$g=\frac{1}{m}\bigtriangledown_{\theta} \sum_i L(f(x_i,\theta),y_i)$
    - 累计平方梯度$r=\rho r+(1-\rho)g\odot g$
    - 计算更新$\Delta \theta\gets- \frac{\epsilon}{\sqrt{\delta+r}}\odot g$
    - 应用更新$\theta= \theta+\Delta \theta$

---

RMSProp已被证明是一种有效且实用的深度神经网络优化算法，是实践者常采用的方法之一。

##### Adam：A Method for Stochastic Optimization

Adam是采用了梯度的一阶估计、二阶估计的算法，并且加入了偏差修正，可以看成是AdaGrad、RMSProp思想的结合。

---

- 输入矩估计的指数衰减速率$\rho_1,\rho_2$(默认建议为0.9、0.99)
- 输入小常数$\delta(10^{-6})$，步长$\epsilon$，衰减速率$\rho$
- 初始化一阶矩、二阶矩量$s=\bold{0},r=\bold{0}$
- 初始化时间步$t=0$
- 停止条件未满足
    - 从样本集合中采样$m$个样本的batch
    - 计算梯度$g=\frac{1}{m}\bigtriangledown_{\theta} \sum_i L(f(x_i,\theta),y_i)$
    - $t=t+1$
    - 更新有偏一阶矩估计$s=\rho_1 s+(1-\rho_1)g$
    - 更新有偏二阶矩估计$r=\rho_2 r+(1-\rho_2)g\odot g$
    - 修正一阶矩的偏差$\hat{s}=\frac{s}{1-\rho_1^t}$
    - 修正二阶矩的偏差$\hat{r}=\frac{r}{1-\rho_2^t}$
    - 计算更新$\Delta \theta=-\epsilon \frac{\hat{s}}{\sqrt{\hat{r}}+\delta}\odot g$
    - 应用更新$\theta= \theta+\Delta \theta$

这里的偏差修正可以这么看，刚开始一般会给定一个$s_0=0$，初期计算的几个结果会与真是的平均值有较大的差异，也就是有冷启动问题。用上面的修正公式进行修正，随着$t$增大，$\hat{s}$与$s$越来越接近，刚开始差距大一些，后期影响逐渐减小。

至于为什么第一步是$\frac{1}{1-\beta}$，是因为给定$\beta$，指数加权平均可以近似看成$\frac{1}{1-\beta}$个数据的移动平均值。见参考文献

---

Adam通常被认为对超参数的选择相当鲁棒。


---

[1]. [什么是指数加权平均、偏差修正?](http://www.bubuko.com/infodetail-2524026.html)




