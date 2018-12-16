---
title: Prime Factor Index in Factorial
date: 2017-03-18 10:37:24
tags: [Math]
categories: Other
---

题目的中文翻译是：阶乘中质因数的指数。
比如说一道谷歌面试题，求`2014!`尾部0的个数.

求尾部0的个数，也就是求这个数中质因子5的个数，有定理

在$n!$ 中质因子$p(p<=n)$的指数为：$h=[\frac{n}{p}]+[\frac{n}{p^2}]+...$，其中`[]`表示取整符号。

所以`2014!`中5的指数是
$$
\begin{aligned}
&\left[\frac{2014}{5}\right]+\left[\frac{2014}{25}\right]+\left[\frac{2014}{125}\right]+\left[\frac{2014}{625}\right] \\
&= 402+80+16+3 \\
&= 501
\end{aligned}
$$
