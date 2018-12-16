---
title: Count Primes
date: 2016-09-04 15:24:44
tags: [LeetCode, prime]
categories: OJ
---
#### Problem

Description:

Count the number of prime numbers less than a non-negative number, n.

#### Solution
###### 埃拉托斯特尼筛法

本题使用<b>埃拉托斯特尼筛法</b>解，此方法用于找出一定范围内的所有质数，也是最有效的方法之一
- 原理：从2开始，将每个质数的倍数标记成合数，倍数的实现可以借助于等差数列，不断剔除合数即可
- 方法：找出sqrt(n)以内的质数、并将相应的合数去掉即可。
- 说明：大于sqrt(n)的合数可以被消除，因为假设一个合数sqrt(n)小于z=a*b，那么，min(a,b)小于sqrt(n)，所以算法在遇到min(a,b)的时候就已经将z标记为合数了

埃拉托斯特尼筛法的伪代码如下
```java
Input: an integer n > 1
Let A be an array of Boolean values, indexed by integers 2 to n,
initially all set to true.

for i = 2, 3, 4, ..., not exceeding √n:
    if A[i] is true:
        for j = i2, i2+i, i2+2i, i2+3i, ..., not exceeding n :
            A[j] := false

Output: all i such that A[i] is true.
```
具体实现过程中，java使用BitSet类可以节约空间。

###### BitSet

- BitSet类实现了大小可动态改变, 取值为true或false的位集合(每位长度位1bit)。用于表示一组布尔标志，默认情况下，set 中所有位的初始值都是 false。
- 使用方法

```java
// 构造函数
public BitSet();
public BitSet(int nbits);
// 方法
public void set(int pos); //位置pos的字位设置为true
public void set(int bitIndex, boolean value); //将指定索引处的位设置为指定的值
public void clear(int pos); //位置pos的字位设置为false
public void clear(); //将此 BitSet 中的所有位设置为 false
public int cardinality(); //返回此 BitSet 中设置为 true 的位数
public boolean get(int pos); //返回位置是pos的字位值
public void and(BitSet other); //other同该字位集进行与操作，结果作为该字位集的新值
public void or(BitSet other); //other同该字位集进行或操作，结果作为该字位集的新值
public void xor(BitSet other); //other同该字位集进行异或操作，结果作为该字位集的新值
public void andNot(BitSet set); //清除此 BitSet 中所有的位,set-用来屏蔽此 BitSet 的 BitSet
public int size(); //返回此 BitSet 表示位值时实际使用空间的位数
public int length(); //返回此 BitSet 的“逻辑大小”：BitSet 中最高设置位的索引加 1
public int hashCode(); //返回该集合Hash 码， 这个码同集合中的字位值有关
public boolean equals(Object other); //如果other中的字位同集合中的字位相同，返回true
public Object clone(); //克隆此 BitSet，生成一个与之相等的新 BitSet
public String toString(); //返回此位 set 的字符串表示形式
```