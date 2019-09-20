---
title: Happy Number
date: 2016-12-01 09:04:43
tags: [LeetCode]
categories: OJ
---

###### 问题描述
Write an algorithm to determine if a number is "happy".

A happy number is a number defined by the following process: Starting with any positive integer, <b>replace the number by the sum of the squares of its digits, and repeat the process until the number equals 1 </b>(where it will stay), or it loops endlessly in a cycle which does not include 1. Those numbers for which this process ends in 1 are happy numbers.

    Example: 19 is a happy number

    12 + 92 = 82
    82 + 22 = 68
    62 + 82 = 100
    12 + 02 + 02 = 1

###### 解题思路
可以使用hashset记录出现过的值，然后判断重复的是否是1
本质上，这题可以使用[Floyd Cycle Detection](http://atlantic8.github.io/2016/12/01/Floyd-Cycle-Detection/)来解。其中
- 由一个数跳转到另一个数可以当作是链表寻找下一个节点
- 设置两个指针，每次分别前进1、2位
- 如果最后相交于1，那么输出true；否则输出no

```java
int digitSquareSum(int n) {
    int sum = 0, tmp;
    while (n) {
        tmp = n % 10;
        sum += tmp * tmp;
        n /= 10;
    }
    return sum;
}

bool isHappy(int n) {
    int slow, fast;
    slow = fast = n;
    do {
        slow = digitSquareSum(slow);
        fast = digitSquareSum(fast);
        fast = digitSquareSum(fast);
    } while(slow != fast);
    if (slow == 1) return 1;
    else return 0;
}
```