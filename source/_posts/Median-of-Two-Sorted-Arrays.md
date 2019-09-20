---
title: Median of Two Sorted Arrays
date: 2016-09-01 11:01:10
tags: [LeetCode, Divide & Conquer]
categories: OJ
---
#### Problem
There are two sorted arrays nums1 and nums2 of size m and n respectively.

Find the median of the two sorted arrays. The overall run time complexity should be <b>O(log (m+n))</b>.

Example 1:
nums1 = [1, 3]
nums2 = [2]

The median is 2.0
Example 2:
nums1 = [1, 2]
nums2 = [3, 4]

The median is (2 + 3)/2 = 2.5

#### Solution
基本思路是分别将A、B分别切割，两个左边的部分合并，两个右侧的部分合并，如下所示：
```java
      left_part          |        right_part
A[0], A[1], ..., A[i-1]  |  A[i], A[i+1], ..., A[m-1]
B[0], B[1], ..., B[j-1]  |  B[j], B[j+1], ..., B[n-1]
```
如果
```java
len(left_part) == len(right_part)
max(left_part) <= min(right_part)
```
第一个条件可以通过设定j的值满足，设置j=(m+n+1)/2，使得左边部分的数量不小于右边数量，所以整体为奇数时，左边部分的最大值即为median。第二个条件需要验证，然后根据相应的情况移动A的切割选取范围。
那么
```java
median=[max(left_part) + min(right_part)]/2  m+n是偶数
median=[]

```
寻找A数组的分割位置可以使用binary search
整个算法的时间复杂度为O(log(min(m,n)))
代码如下：
```python
def median(A, B):
    m, n = len(A), len(B)
    if m > n:
        A, B, m, n = B, A, n, m
    if n == 0:
        raise ValueError
    # 设置half_len=(m + n + 1) / 2, 保证左边部分总是不小于右边
    imin, imax, half_len = 0, m, (m + n + 1) / 2
    while imin <= imax:
        i = (imin + imax) / 2
        j = half_len - i
        if j > 0 and i < m and B[j-1] > A[i]:
            # i 太小
            imin = i + 1
        elif i > 0 and j < n and A[i-1] > B[j]:
            # i 太大
            imax = i - 1
        else:
            # i 刚刚好
            if i == 0: max_of_left = B[j-1]
            elif j == 0: max_of_left = A[i-1]
            else: max_of_left = max(A[i-1], B[j-1])
            # 考虑整体是奇数的情况
            if (m + n) % 2 == 1:
                return max_of_left

            if i == m: min_of_right = B[j]
            elif j == n: min_of_right = A[i]
            else: min_of_right = min(A[i], B[j])
            # 考虑整体是偶数的情况
            return (max_of_left + min_of_right) / 2.0
```