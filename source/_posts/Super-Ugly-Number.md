---
title: Super Ugly Number
date: 2016-09-04 10:09:59
tags: [LeetCode]
categories: OJ
---

#### Problem
Write a program to find the nth super ugly number.

Super ugly numbers are positive numbers whose all prime factors are in the given prime list primes of size k. For example, [1, 2, 4, 7, 8, 13, 14, 16, 19, 26, 28, 32] is the sequence of the first 12 super ugly numbers given primes = [2, 7, 13, 19] of size 4.

Note:
(1) 1 is a super ugly number for any given primes.
(2) The given numbers in primes are in ascending order.
(3) 0 < k ≤ 100, 0 < n ≤ 106, 0 < primes[i] < 1000.

#### Solution
- 维护一个长度为n的数组，存储ugly数
- 使用一个数组idx，长度与primes一致，用以记录每个primes元素已经和哪一位的ugly相乘过，相乘过就移动之
- 去重，需要扫描idx，对应primes[j]*un[idx[j]]<=un[i]的都要去掉

```java
public class Solution {
    public int nthSuperUglyNumber(int n, int[] primes) {
        int[] pos = new int[primes.length], un = new int[n];
        un[0] = 1;
        for (int i=1; i<n; i++) {
            un[i] = Integer.MAX_VALUE;
            // 找当下最小的数
            for (int j=0; j<primes.length; j++)
                un[i] = Math.min(primes[j]*un[pos[j]], un[i]);
            // 去重
            for (int j=0; j<primes.length; j++)
                while (primes[j]*un[pos[j]] <= un[i]) pos[j]++;
        }
        return un[n-1];
    }
}
```