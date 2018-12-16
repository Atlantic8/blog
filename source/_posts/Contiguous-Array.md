---
title: Contiguous Array
date: 2017-04-01 14:09:56
tags: [LeetCode]
categories: OJ
---

###### 题目描述
给定一个只包含0和1的整形数组，输出最长的连续子串的长度，要求子串中0和1的个数相同。

	Input: [0,1]
	Output: 2
	Explanation: [0, 1] is the longest contiguous subarray with equal number of 0 and 1.

	Input: [0,1,0]
	Output: 2
	Explanation: [0, 1] (or [1, 0]) is a longest contiguous subarray with equal number of 0 and 1.

数组长度不会超过50000.
###### 解题思路
$O(n^2)$的思路容易想到，但是数组长度太长，会超时。

方法如下：
- 先将数组中的`0`变成`-1`，这样连续子序列的和为`0`的时候满足条件
- 记录下`0-k`位置的和与`k`的对应关系，可以hash map的方法。和相同的只记录最左边的，毕竟长度要最长嘛
- 如果后面遇到了记录过的和，位置相减就能得到满足条件的子序列长度
- 时间复杂度为$O(n)$

代码如下：
```java
int findMaxLength(vector<int>& nums) {
	int n = nums.size(), ret=0, sum=0;
	unordered_map<int, int> map;
	map[0] = -1; // 没有数和也为0，防止只有[0,1]时输出0
	for (int i=0; i<n; i++) if (nums[i]==0) nums[i] = -1;
	for (int i=0; i<n; i++) {
		sum += nums[i];
		// 以前遇到过sum值，现在位置-以前位置可以得到一个满足要求的序列长度
		if (map.find(sum) != map.end()) {
			ret = max(ret, i-map[sum]);
		} else { // 第一次遇到sum值，记录就行
			map[sum] = i;
		}
	}
	return ret;
}

```
