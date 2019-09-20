---
title: Increasing Triplet Subsequence
date: 2016-09-02 09:18:26
tags: LeetCode
categories: OJ
---
#### Problem
Given an unsorted array return whether an increasing subsequence of length 3 exists or not in the array.

Formally the function should:
Return true if there exists i, j, k
such that arr[i] < arr[j] < arr[k] given 0 ≤ i < j < k ≤ n-1 else return false.
Your algorithm should run in O(n) time complexity and O(1) space complexity.

Examples:
Given [1, 2, 3, 4, 5],
return true.

Given [5, 4, 3, 2, 1],
return false.

#### Solution
- 解题思路是维护两个变量，min和mid
- min表示当前遇到的最小的数
- mid表示在当前情况下，所有长度为2的递增序列第二个数的最小值（表示前面有一个比mid还小的数且没有一个小于mid的数能取代mid的位置）
- 当出现一个比min大的数时：
    1. 如果这个数比mid大，则返回true
    2. 如果这个数比mid小，则更新mid为当前值

代码如下：
```java
public boolean increasingTriplet(int[] nums) {
    int min = Integer.MAX_VALUE, secondMin = Integer.MAX_VALUE;
    for(int num : nums){
        if(num <= min) min = num;
        else if(num < secondMin) secondMin = num;
        else if(num > secondMin) return true;
    }
    return false;
}
```


