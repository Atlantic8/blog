---
title: Expection Maximization
date: 2016-12-09 22:58:01
tags: [machine learning]
categories: Algorithm
---

##### EM算法
###### 极大似然估计
从极大似然法的角度引入EM算法，先考虑这样的一个问题。

给定训练数据，假设训练数据满足高斯分布$f(x|\mu,\sigma^2)$，求这个分布的参数.

这便是典型的极大似然估计问题，对数似然函数为$$l(\mu,\sigma^2|X)=\sum_iln(f(x_i|\mu,\sigma^2))$$上面的式子分别对$\mu$和$\sigma$求偏导，并设置其偏导数为0，那么$\mu$和$\sigma$的解可以直接计算。

###### 包含隐含变量的极大似然估计
假设还有一个条件：数据X有两个类别，$\lambda_1,\lambda_2$分别表示$f(x|\mu_1,\sigma_1^2)$和$f(x|\mu_2,\sigma_2^2)$在总体中的比率。因此总体分布就可以是$g(x|\lambda_1,\lambda_2,\mu_1,\mu_2,\sigma_1^2,\sigma_2^2)$，即两个分布的混合。所以有$$g(x|\lambda_1,\lambda_2,\mu_1,\mu_2,\sigma_1^2,\sigma_2^2)=\lambda_1f(x|\mu_1,\sigma_1^2)+\lambda_2f(x|\mu_2,\sigma_2^2) \quad s.t.: \quad \lambda_1+\lambda_2=1$$极大似然估计的求解方法如下，似然公式为$$l()=log(P(X|\lambda_1,\lambda_2,\mu_1,\mu_2,\sigma_1^2,\sigma_2^2))=log\left(\sum_ig(x_i|\lambda_1,\lambda_2,\mu_1,\mu_2,\sigma_1^2,\sigma_2^2) \right)$$上面式子是先求和在取对数，求偏导的方法就不行了！

###### Jensen不等式
如果一个函数满足：对于任意的$x$都有$f^{''}(x) \ge 0$，那么$f(x)$是凸函数(如果输入$x$是向量，那么对应于其hessian矩阵(半)正定)，如果等号可以去掉即可称之为**严格凸函数**。
Jensen不等式的表述如下：假设$f$是凸函数，X是一个随机变量，那么有：$$ E[f(X)] \ge f(E[X]) $$对立面的表述是，如果函数$f$是凹(concave)函数($f^{''}(x) \le 0$)，那么有$$E[f(X)] \le f(E[X])$$当不等式中的等号成立时，$f(X)$是常数函数。

###### 期望最大化
现在抽象化问题，已知模型为$p(x|\theta)$，$X=(x_1,x_2,...,x_n)$，求$\theta$。这里需要引入隐含变量$Z=(z_1,z_2,...,z_m)$，所以有：
$$
\begin{aligned}
P(X|\theta)=\sum_zP(x_i|z,\theta) \cdot P(z|\theta)
\end{aligned}
$$
定义似然函数为$$l(\theta)=log(P(X|\theta))=log\sum_z(P(x_i|z,\theta) \cdot P(z|\theta))$$ EM算法也是通过迭代方法求得$l(\theta)$的极值，假设第$n$轮迭代计算出的$\theta$为$\theta_n$，只要下一轮的$\theta$优于$\theta_n$即可，推导如下：
$$
\begin{aligned}
l(\theta)-l(\theta_n) &= log(P(X|\theta))-log(P(X|\theta_n)) \\
&= log(\sum_zP(x_i|z,\theta) \cdot P(z|\theta))-log(P(X|\theta_n)) \\
&= log(\sum_z P(z|X,\theta_n)\cdot \frac{P(x_i|z,\theta) \cdot P(z|\theta)}{P(z|X,\theta_n)})-log(P(X|\theta_n)) \\
&\ge \sum_z P(z|X,\theta_n) \cdot log\left( \frac{P(x_i|z,\theta) \cdot P(z|\theta)}{P(z|X,\theta_n)} \right) - \sum_z P(z|X,\theta_n) \cdot log(P(X|\theta_n)) \\
&= \sum_z P(z|X,\theta_n) \cdot log\left( \frac{P(x_i|z,\theta) \cdot P(z|\theta)}{P(z|X,\theta_n) \cdot P(X|\theta_n)} \right) \\
\end{aligned}
$$
进而有
$$
\begin{aligned}
l(\theta) &\ge l(\theta_n)+\sum_z P(z|X,\theta_n) \cdot log\left( \frac{P(x_i|z,\theta) \cdot P(z|\theta)}{P(z|X,\theta_n) \cdot P(X|\theta_n)} \right) \\
Set : l(\theta) &\ge M(\theta_n,\theta) \\
PS : l(\theta_n)&=M(\theta_n,\theta_n)
\end{aligned}
$$
所以，我们只要
$$
\begin{aligned}
\theta_{n+1} &= \mathop{arg\;max}_{\theta} M(\theta_n,\theta) \\
&= \mathop{arg\;max}_{\theta} \sum_z P(z|X,\theta_n) \cdot log(P(X|z,\theta) \cdot P(z|\theta)) \\
&= \mathop{arg\;max}_{\theta} \sum_z P(z|X,\theta_n) \cdot log(P(X,z|\theta)) \\
&= \mathop{arg\;max}_{\theta} E_{Z|X,\theta_n}[log(P(X,z|\theta)] \\
Set: F(\theta)&=E_{Z|X,\theta_n}[log(P(X,z|\theta)]
\end{aligned}
$$
所以，EM算法的步骤如下：

---

随机初始化$\theta_0$
迭代直到收敛：
E步：求条件期望$F(\theta,\theta_n)$
M步：求$F(\theta,\theta_n)$的极值$\theta_{n+1}$

---

##### 高斯混合模型
高斯混合模型是EM算法在高斯分布上的应用。多元高斯分布函数的定义如下：$$p(x|\mu,\Sigma)=\frac{1}{(2\pi)^{n/2}|\Sigma|^{1/2}} e^{-\frac{(x-\mu)^T \Sigma^{-1} (x-\mu) }{2}}$$ 其中，$\mu,\Sigma$分别是均值和协方差矩阵。混合高斯模型的定义为：
$$
\begin{aligned}
p_M(x)&=\sum_{i=1}^k \alpha_i \cdot p(x|\mu_i,\Sigma_i) \\
s.t.: \sum_{i=1}^k \alpha_i &= 1
\end{aligned}
$$
为了方便性，定义$j$个样本由第$i$个高斯分布产生的概率：
$$
\begin{aligned}
p_M(z_j=i|x_j)&=\gamma_{ji} \\
&= \frac{P(z_j=i) \cdot p_M(x_j|z_j=i)}{p_M(x_j)} \\
&= \frac{\alpha_i \cdot p(x_j|\mu_i,\Sigma_i)}{\sum_{l=1}^k \alpha_l \cdotp(x_j|\mu_l,\Sigma_l)}
\end{aligned}
$$
于是，给定样本集$D={x_1,...,x_m}$，用极大似然估计法，最大化似然对数：
$$
\begin{aligned}
l(D)=ln\left( \prod_{j=1}^m p_M(x_j) \right)=\sum_{j=1}^m ln\left( \sum_{i=1}^k \alpha_i \cdot p(x_j|\mu_i,\Sigma_i) \right)
\end{aligned}
$$
上式中，分别由$l(D)$对$\mu_i,\Sigma_i,\alpha_i$求偏导，由于$p_M(z_j=i|x_j)=\gamma_{ji}$，所以令偏导数=0的结果如下：
$$
\begin{aligned}
\mu_i &= \frac{\sum_{j=1}^m \gamma_{ji} \cdot x_j}{\sum_{j=1}^m \gamma_{ji}} \\
\Sigma_i &= \frac{\sum_{j=1}^m \gamma_{ji}(x_j-\mu_i)(x_j-\mu_i)^T}{\sum_{j=1}^m \gamma_{ji}} \\
\end{aligned}
$$
对于混合系数$\alpha_i$，除了考虑$l(D)$外，他还有一个限制$\sum_{i=1}^k \alpha_i=1$，所以这里可以使用拉格朗日乘子法：$$l(D)+\lambda \left( \sum_{i=1}^k \alpha_i-1 \right)$$上式对$\alpha_i$求导并设结果为0有(注意联系$\gamma_{ji}的定义式$)
$$
\begin{aligned}
\sum_{j=1}^m \frac{p(x_j|\mu_i,\Sigma_i)}{\sum_{l=1}^k \alpha_l \cdot p(x_j|\mu_l,\Sigma_l)} &= -\lambda \\
multiply\; \alpha_i,\; and\;get\; sum\; with\; respect\; to\; i \\
\sum_{i=1}^k \sum_{j=1}^m \frac{\alpha_i \cdot p(x_j|\mu_i,\Sigma_i)}{\sum_{l=1}^k \alpha_l \cdot p(x_j|\mu_l,\Sigma_l)} &= \sum_{i=1}^k -\lambda \cdot \alpha_i \\
hence: \lambda &= -m \\
\alpha_i &= \frac{1}{m} \sum_{j=1}^m \gamma_{ji}
\end{aligned}
$$
所以，混合高斯的EM方法就是：先根据当前参数计算每个样本属于每个高斯成分的后验概率$\gamma_{ji}$（E步）；然后根据上面的规则更新模型参数${(\mu_i,\Sigma_i,\alpha_i)|1\le i \le k}$.

最后给出<b>高斯混合聚类算法</b>表述：

---

输入：样本集$D={x_1,...,x_m}$，高斯混合成分个数$k$;

---

1  初始化高斯混合分布的模型参数${(\mu_i,\Sigma_i,\alpha_i)|1\le i \le k}$.
2  迭代，直到满足停止条件
3  $\quad  for\; j=1,...m \quad do$
4  $\quad \quad$计算$p_M(z_j=i|x_j)=\gamma_{ji},(1 \le i \le k)$
5  $\quad end\; for$
6  $\quad  for\; i=1,...k \quad do$
7  $\quad \quad$更新模型参数$(\mu_i,\Sigma_i,\alpha_i)$
8  $C_i=\emptyset,(1\le i \le k)$
9  $for\; j=1,...m \quad do$
10 $\quad$根据最大后验概率规则确定每个$x_j$的簇$\lambda_j$
11 $\quad C_{\lambda_j}=C_{\lambda_j}\cup \{x_j\}$
12 $end\; for$

---

输出：簇划分结果$C={C_1,..,C_k}$

---
