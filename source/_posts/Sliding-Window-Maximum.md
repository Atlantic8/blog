---
title: Sliding Window Maximum
date: 2017-02-16 15:31:45
tags: [Sliding window]
categories: OJ
---

###### 题目描述
给定数组`nums`，和滑动窗口的长度`k`，输出滑动窗口一次一个元素地向前滑动时每一时刻滑动窗口内的最大值。要求在`O(n)`复杂度内完成。

	nums = [1,3,-1,-3,5,3,6,7],  k = 3
    Window position                Max
	---------------               -----
	[1  3  -1] -3  5  3  6  7       3
	 1 [3  -1  -3] 5  3  6  7       3
	 1  3 [-1  -3  5] 3  6  7       5
	 1  3  -1 [-3  5  3] 6  7       5
	 1  3  -1  -3 [5  3  6] 7       6
	 1  3  -1  -3  5 [3  6  7]      7
    ---------------               -----
	output [3,3,5,5,6,7]

###### 解题思路
滑动窗口内添加新元素简单，但是删除时比较麻烦，所以简单使用堆的思路不行。

双端队列对滑动窗口有比较好的模拟，其尾部、头部都可以添加和删除元素（也有受限的应用版本）。

本题使用的方法也称作**单调队列**，其定义如下：

	队列中元素之间的关系具有单调性，而且，队首和队尾都可以进行出队操作，只有队尾可以进行入队操作

以单调不减队列为例，队列内的元素$(e_1,e_2,...,e_n)$存在$(e_1\le e_2\le...\le e_n)$的关系，所以队首元素$e_1$一定是最小的元素。与优先队列不同的是，**当有一个新的元素$e$入队时，先要将队尾的所有大于$e$的元素弹出，以保证单调性，再让元素$e$入队尾**。

所以本题的方法描述如下：
- 队列元素如果超过了k的限制，那么从队头剔除
- 从队尾起，如果队尾的元素小于当前需要添加的元素，那么剔除队尾元素（它不可能成为最大值），直到队尾元素大于等于当前需要添加的元素。
- 此时，队列是非递减队列，所以队头元素就是最大值

```java
vector<int> maxSlidingWindow(vector<int>& nums, int k) {
	vector<int> ret;
	deque<int> window;
	if (nums.size()<1 || k<=0) return ret;
	for (int i=0; i<nums.size(); i++) {
		if (!window.empty() && window.front()<i-k+1)
			window.pop_front();
		while (!window.empty() && nums[window.back()]<nums[i])
			window.pop_back();
		window.push_back(i);
		if (i >= k-1) ret.push_back(nums[window.front()]);
	}
	return ret;
}
```
