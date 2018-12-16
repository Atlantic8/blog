---
title: Split Array Largest Sum
date: 2016-10-02 20:26:17
tags: [LeetCode, Binary Search]
categories: OJ
---

##### Problem
Given an array which consists of non-negative integers and an integer m, you can split the array into m non-empty continuous subarrays. Write an algorithm to minimize the largest sum among these m subarrays.

Note:
Given m satisfies the following constraint: 1 ≤ m ≤ length(nums) ≤ 14,000.

	Examples:

	Input:
	nums = [1,2,3,4,5]
	m = 2

	Output:
	9

Explanation:
There are four ways to split nums into two subarrays.
The best way is to split it into [1,2,3] and [4,5],
where the largest sum among the two subarrays is only 9.


##### Solution
普通的递归方法会超时！！！

首先确定任意合法的m值，对应结果的范围[left ~ right]
其中left = max(nums[]), right = sum(nums[]).

这里考虑使用二分查找法，如果left = right，那么返回left就好
给定一个可能的结果mid = left+(right-left)/2.，验证<b>是否合法</b>

	判断一个x是否合法的方法如下：
    顺序扫描nums[]，计算块和不大于（尽可能接近）mid的个数c
    如果c > m，那么mid应该变大，相应的c变小；反之，c <= m，说明mid应该变小，相应c变大

如果合法：mid应该变小，即 right = mid；
否则，mid应该变大，即 left = mid + 1；

```java
class Solution {
public:
	// check if nums can be divided into m subsets s.t each subset's summation <= sum
    bool canSplit(vector<int>& nums, int m, long sum) {
        int c = 1;
        long s = 0;
        for (auto& num : nums) {
            s += num;
            if (s > sum) {
                s = num; // first element
                ++c;  // a new subset
            }
        }
        // c<=m indicates nums can be divided into m subsets s.t each subset's summation <= sum
        return c <= m;
    }

    int splitArray(vector<int>& nums, int m) {
        long left = 0, right = 0;
        for (auto& num : nums) {
            left = max(left, (long)num);
            right += num;
        }
        while (left < right) {
            if (left == right) return left; // answer found
            long mid = left + (right-left)/2;
            if (canSplit(nums, m, mid)) right = mid; // be smaller.
            else left = mid+1; // be bigger
        }
        return left;
    }
};
```
