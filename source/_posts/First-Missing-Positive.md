---
title: First Missing Positive
date: 2016-09-14 09:18:18
tags: [LeetCode]
categories: OJ
---

##### Problem
Given an unsorted integer array, find the first missing positive integer.

    For example,
    Given [1,2,0] return 3,
    and [3,4,-1,1] return 2.

Your algorithm should run in <b>O(n) time and uses constant space</b>.

##### Solution
解题思路
- 把每个数放在它应该的位置，比如找到4，就把4和num[3]兑换
- 小于1的数忽略，因为题目说是正数
- 大于数组长度的数也不可能是，因为它前面至少有n个数，至少有一个缺失
- 第一遍扫面把数放在正确的地方，第二遍，把num[i]!=i+1的最小序号输出

```java
class Solution
{
public:
    int firstMissingPositive(int A[], int n) {
        // 将数放在正确的地方
        for(int i = 0; i < n; ++ i)
            while(A[i] > 0 && A[i] <= n && A[A[i] - 1] != A[i]) swap(A[i], A[A[i] - 1]);
        // 找到缺失的数
        for(int i = 0; i < n; ++ i)
            if(A[i] != i + 1) return i + 1;

        return n + 1;
    }
};
```
