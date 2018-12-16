---
title: Boosting
date: 2017-01-13 19:50:41
tags: [machine learning]
categories: Algorithm
---

Boosting是集成学习中的典型代表之一，与随机森林的不同在于：Boosting中的个体学习器之间有着强依赖、必须串行生成。Boosting族最典型的算法是AdaBoost。<b>AdaBoost每轮迭代尝试调整训练数据的分布以使得下一轮的基学习器能够修正现有学习器的一些错误</b>。Boosting算法从“偏差-方差”的角度看更加专注于降低偏差。

---

##### AdaBoost

---

###### 指数损失函数

AdaBoost可以理解成基学习器的叠加，即
$$
\begin{aligned}
H(x)=\sum_{t=1}^T \alpha_th_t(x)
\end{aligned}
$$
来最小化损失函数
$$
\begin{aligned}
l_{exp}(H|\mathcal{D})&=E_{x\sim D}[e^{-f(x)H(x)}] \\
&= E_{x\sim D}[e^{-H(x)}P(f(x)=1|x) + e^{H(x)}P(f(x)=-1|x)]
\end{aligned}
$$
其中$\mathcal{D}$表示数据集$D$的分布，也就是每个样本出现的概率。要选取最佳的$H(x)$使得损失函数$l$最小。这里假设原始数据集的标签$y_i\in \lbrace -1,+1 \rbrace$，$f(x)$是真实函数。自然地考虑$l_{exp}(H|\mathcal{D})$对$H(x)$求偏导数并且设置为0
$$
\begin{aligned}
\frac{\partial l_{exp}(H|\mathcal{D})}{\partial H(x)} &= -e^{-H(x)}P(f(x)=1|x) + e^{H(x)}P(f(x)=-1|x) = 0 \\
H(x) &= \frac{1}{2} ln \frac{P(f(x)=1|x)}{P(f(x)=-1|x)}
\end{aligned}
$$
其中，$H(x)$与真实函数输出一致，那么$-f(x)H(x)$为-1；反之$-f(x)H(x)=1$，所以最小化上述损失函数的意义就是希望$H(x)$与真实函数$f(x)$输出尽量一致。最后，考虑到问题本质，$sign \left( \frac{1}{2} ln \frac {P(f(x)=1|x)} {P(f(x)=-1|x)}\right) $还需要
$$
sign(H(x)) = sign \left( \frac{1}{2} ln \frac {P(f(x)=1|x)} {P(f(x)=-1|x)} \right) = \begin{cases}
 1 & {P(f(x)=1|x) \ge P(f(x)=-1|x)} \\
-1 & {P(f(x)=1|x) < P(f(x)=-1|x)}
\end{cases}
$$
表明$sign(H(x))$达到了贝叶斯最优错误率，也就是：若指数损失函数最小化，那么分类错误率最小化。

---

###### 权重更新

AdaBoost中，第一个分类器$h_1$通过直接将基学习算法用于初始数据分布$\mathcal{D}$而得，此后迭代地生成$h_t,\alpha_t$。当基分类器$h_t$基于分布$\mathcal{D}_t$产生后，$h_t$对应的权重$\alpha_t$应该使得$\alpha_th_t$最小化指数损失函数
$$
\begin{aligned}
l_{exp}(\alpha_th_t|\mathcal{D}_t) &= E_{x\sim \mathcal{D}_t} \left[ e^{-f(x)\alpha_th_t(x)} \right] \\
&= E_{x\sim \mathcal{D}_t} \left[ e^{-\alpha_t}I(f(x)=h_t(x)) + e^{\alpha_t}I(f(x)\neq h_t(x)) \right] \\
&= e^{-\alpha_t}P_{x\sim \mathcal{D}_t}(f(x)=h_t(x)) + e^{\alpha_t}P_{x\sim \mathcal{D}_t}(f(x)\neq h_t(x)) \\
&= e^{-\alpha_t}(1-\epsilon_t) + e^{\alpha_t}\epsilon_t
\end{aligned}
$$
其中，$\epsilon_t=P_{x\sim \mathcal{D}_t}(f(x)\neq h_t(x))$。上式对$\alpha_t$求导并使之为0可得
$$
\begin{aligned}
\alpha_t=\frac{1}{2} ln\left( \frac{1-\epsilon_t}{\epsilon_t} \right)
\end{aligned}
$$

---

###### 样本分布调整
获取$H_{t-1}$之后将样本分布进行调整，使下一轮的基学习器$h_t$能纠正$H_{t-1}$的错误，依旧采用最小化指数损失函数的思想，有
$$
\begin{aligned}
l_{exp}(H_{t-1}+h_t | \mathcal{D}) &= E_{x\sim \mathcal{D}} [e^{ -f(x) ( H_{t-1}(x)+h_t(x) ) }] \\
&= E_{x\sim \mathcal{D}} [ e^{-f(x)H_{t-1}} e^{-f(x)h_t(x)} ] \\
\end{aligned}
$$
对上式中的$e^{-f(x)h_t(x)}$做二阶泰勒展开，近似为
$$
\begin{aligned}
l_{exp}(H_{t-1}+h_t|\mathcal{D}) &\simeq E_{x\sim \mathcal{D}}\left[e^{-f(x)H_{t-1}(x)} \left( 1-f(x)h_t(x)+\frac{f(x)^2h_t(x)^2}{2} \right) \right] \\
&= E_{x\sim \mathcal{D}}\left[e^{-f(x)H_{t-1}(x)} \left( \frac{3}{2}-f(x)h_t(x) \right)\right] \\
\end{aligned}
$$
因为$\frac{3}{2}-f(x)h_t(x)>0$并且$f(x)H_{t-1}(x)$也是确定的值，所以最小化上式也就是等价于下式，也可以做一点变化变体
$$
\begin{aligned}
&\to \arg\max_{h} E_{x\sim \mathcal{D}}\left[e^{-f(x)H_{t-1}(x)} f(x)h(x)\right] \\
&\to \arg\max_{h} E_{x\sim \mathcal{D}}\left[\frac{e^{-f(x)H_{t-1}(x)}} {E_{x\sim \mathcal{D}} \left[ e^{-f(x)H_{t-1}(x) } \right] } f(x)h(x)\right]
\end{aligned}
$$
因为$E_{x\sim \mathcal{D}}e^{-f(x)H_{t-1}(x)}$是一个常数，令$\mathcal{D}_t$表示一个分布
$$
\begin{aligned}
D_t(x)=\mathcal{D}(x) \frac { e^{-f(x)H_{t-1}(x)} }  { E_{x\sim \mathcal{D}} \left[ e^{ -f(x)H_{t-1}(x) } \right] }
\end{aligned}
$$
根据数学期望的定义，这等价于令
$$
\begin{aligned}
h_t(x) &= \arg\max_{h} E_{x\sim \mathcal{D}}\left[\frac{e^{-f(x)H_{t-1}(x)}} {E_{x\sim \mathcal{D}} [e^{-f(x)H_{t-1}(x)}]} f(x)h(x)\right] \\
&= \arg\max_{h} E_{x\sim \mathcal{D}_t} [f(x)h(x)]
\end{aligned}
$$
由于$f(x),h(x)$都只能取$\lbrace -1,1 \rbrace$，所以上式中的优化问题也可以变成
$$
\begin{aligned}
h_t(x) = \arg\min_{h} E_{x\sim \mathcal{D}_t} [I(f(x) \neq h(x))]
\end{aligned}
$$
所以理想的$h_t$将在分布$\mathcal{D}_t$下最小化分类误差，因此弱分类器将基于$\mathcal{D}_t$来训练，且针对$\mathcal{D}_t$的分类误差应该不小于0.5（二分类至少要比猜的强）。根据上面的推导，分布之间的关系应该是
$$
\begin{aligned}
\mathcal{D}_{t+1}(x) &= \mathcal{D}(x) \frac{e^{-f(x)H_{t-1}(x)}} { E_{x\sim \mathcal{D}} [ e^{ -f(x) H_{t-1}(x) } ] } \\
&= \mathcal{D}(x) \frac{ e^{-f(x)H_{t-1}(x)}  e^{-f(x) \alpha_t h_t(x)} } {E_{x\sim \mathcal{D}} [ e^{ -f(x) H_{t-1}(x) } ] } \\
&= \mathcal{D}_{t}(x) e^{-f(x) \alpha_t h_t(x)} \frac{E_{x\sim \mathcal{D}} [ e^{-f(x)H_{t-1}(x)} ]} {E_{x\sim \mathcal{D}} [e^{-f(x)H_{t}(x)}]}
\end{aligned}
$$
至此，AdaBoost算法流程介绍完毕，下面是其算法描述

---

输入：训练集$D=\lbrace (x_1,y_1),...,(x_m,y_m) \rbrace$；基学习算法$\gamma$；训练轮数$T$

---

1. $\mathcal{D}_{1}(x)=\frac{1}{m}$. //初始为均匀分布
2. $for\;t=1,...,T$
3. $h_t=\gamma(D,\mathcal{D}_{t})$.
4. $\epsilon_t=P_{x\sim \mathcal{D}_{t} }(h_t(x)\neq f(x))$.
5. $if\;\epsilon_t>0.5\;then\;break\;$. // 错误率大于0.5的不要，至少比随机猜测好
6. $\alpha_t=\frac{1}{2}ln \frac {1-\epsilon_t}{\epsilon_t}$. //权重更新
7. $\mathcal{D}_{t+1}=\mathcal{D}_{t} \frac{exp(-\alpha_t f(x) h_t(x))} {Z_t}$. //分布调整

---

输出：$H(x)=sign\left( \sum_{t=1}^T \alpha_t h_t(x) \right)$

---

由算法描述的第三行可以看出，基学习算法需要能够对特定的数据分布进行学习，可以通过两种方法实现：
- 重赋权法：每一轮训练过程中，根据样本分布为每个样本重新赋予一个权重。也可以是在计算误差率的时候，为每个样本对应的项加上权重。
- 重采样法：每一轮训练过程中，根据样本分布进行重采样，用采样的样本集训练数据。（特别用于样本无法接受权值的基算法场景，此方法还可以在基学习器错误率大于0.5时不用退出，创新采样开始）


##### Boosting Tree
- 提升树被认为是统计学习中性能最好的方法之一
- 与RF类似，提升树也可以通过线性叠加基学习器的方法获得准确率的提升
- 基学习器为二叉树，分为分类、回归两种

###### 提升树
提升树的模型可以表示为$$f_M(x)=\sum_{m=1}^MT(x;\theta_m)$$其中，$M$为树的个数，$T(x;\theta_m)$表示决策树，$\theta_m$为决策树的参数。

步骤：首先确定初始提升树$f_0(x)=0$，第$m$步的模型是$$f_m(x)=f_{m-1}(x)+T(x;\theta_m)$$，通过经验风险最小化确定参数$\theta_m$为
$$
\begin{aligned}
\theta_m=\arg\min_{\theta_m^{\*}} \sum_{i=1}^N L \left (y_i,f_{m-1}(x_i)+T(x_i;\theta_m^{\*}) \right)
\end{aligned}
$$
即使**输入数据与输出数据之间的关系很复杂，树的线性组合也可以很好地拟合训练数据**。

在回归问题中，考虑使用平方误差损失函数，所以损失变为
$$
\begin{aligned}
&L \left(y,f_{m-1}(x)+T(x;\theta_m^{\*})\right) \\
&= \left(y-f_{m-1}(x)-T(x;\theta_m^{\*})\right)^2 \\
&=  \left(r-T(x;\theta_m^{\*})\right)^2
\end{aligned}
$$
其中$r=y-f_{m-1}(x)$是当前模型拟合数据的残差，所以算法就是**拟合当前模型的残差**，描述如下：

---

输入：训练数据集$D$

---

1. 初始化$f_0(x)=0$，迭代次数$M$
2. 对$m=1,...,M$
  - 计算每个样本的残差$r_{mi}=y_i-f_{m-1}(x_i)$
  - 拟合残差$r_m$得到一个回归树$T(x;\theta_m)$
  - 计算$f_m(x)=f_{m-1}(x)+T(x;\theta_m)$
3. 得到回归提升树$f_M(x)=\sum_{m=1}^MT(x;\theta_m)$

---

输出：$F_M(x)$

---

###### 梯度提升
- 损失函数是平方误差、指数损失函数时每一步优化比较明显；但一般损失函数就不那么容易了
- 使用最速下降的近似方法
- **利用损失函数的负梯度在当前模型的值残差的近似值**作为提升回归树的残差近似值

下面是梯度提升回归树算法

---

输入：数据集$D$，数量为$N$，迭代次数$M$

---

1. 初始化$f_0(x)=\arg\min_{c}\sum_{y=1}^NL(y_i,c)$
2. 对$m=1,...,M$
  - 计算$r_{mi}=-\left[ \frac{\partial{L(y_i,f_{m-1}(x_i))}}{\partial{f_{m-1}(x_i)}} \right]$
  - 对$r_m$拟合一个回归树，对于它的每一个叶节点$R_{mj}$，确定节点的值为$c_{mj}=\arg\min_c\sum_{x_i\in R_{mj}}L(y_i,f_{m-1}(x_i)+c)$
  - 更新$f_m(x)=f_{m-1}(x)+\sum_{j=1}^Jc_{mj}I(x\in R_{mj})$
3. 得到回归树$f_M(x)=\sum_{m=1}^M\sum_{j=1}^Jc_{mj}I(x\in R_{mj})$

---

输出：$f_M(x)$

---

`GBDT(Gradient Boosting Decision Tree)`几乎可用于所有的回归问题

